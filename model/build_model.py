# -*- coding: utf-8 -*-
"""FTAI Aviation financial model builder (Point72 Academy pitch).
Reproducible: python -I build_model.py   (needs openpyxl; `formulas` only for --verify)
Builds model/FTAI_Model.xlsx from a blank Workbook(). Historicals are typed inputs (blue) with sources;
every projection is a live formula that traces back to the Drivers tab.
"""
import csv, os, re, sys, json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as CL
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule
from openpyxl.chart import BarChart, Reference

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DATA = os.path.join(BASE, "research", "FTAI", "phase2", "data")
OUT = os.path.join(HERE, "FTAI_Model.xlsx")
SNAP_JSON = os.path.join(HERE, "scenario_snapshot.json")
TEAM = "[TEAM NAME]"
SCEN = ["Bear", "Base", "Bull", "Mgmt Guide"]

# ---------------------------------------------------------------- styles
BLUE, GREEN, BLACK, RED = "0000FF", "00803C", "000000", "C00000"
YEL = PatternFill("solid", fgColor="FFF2A8")
HDR = PatternFill("solid", fgColor="1F3864")
SEC = PatternFill("solid", fgColor="D9E1F2")
GREY = PatternFill("solid", fgColor="F2F2F2")
F_NUM = '#,##0.0;(#,##0.0);"-"'
F_NUM0 = '#,##0;(#,##0);"-"'
F_PCT = '0.0%;(0.0%);"-"'
F_USD = '$#,##0.00;($#,##0.00)'
F_X = '0.0"x"'
F_3 = '0.000'
LINK_RE = re.compile(r"^=\s*'?[A-Za-z_ ]+'?!\$?[A-Z]{1,3}\$?\d+$")


def W(ws, addr, v, fmt=None, bold=False, comment=None, fill=None, color=None, italic=False, align=None, wrap=False):
    c = ws[addr]
    c.value = v
    if color is None:
        if isinstance(v, str) and v.startswith("="):
            color = GREEN if LINK_RE.match(v) else BLACK
        elif isinstance(v, (int, float)):
            color = BLUE
        else:
            color = BLACK
    c.font = Font(name="Calibri", size=10, bold=bold, italic=italic, color=color)
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = fill
    if comment:
        c.comment = Comment(comment, "Model")
        c.comment.width, c.comment.height = 320, 120
    if align or wrap:
        c.alignment = Alignment(horizontal=align, wrap_text=wrap, vertical="top" if wrap else None)
    return c


def label(ws, row, text, bold=False, indent=0, key=False, col="A"):
    c = ws[f"{col}{row}"]
    c.value = text
    c.font = Font(name="Calibri", size=10, bold=bold or key, color=RED if key else BLACK)
    c.alignment = Alignment(indent=indent)


def title(ws, text, sub=None, width=14):
    ws["A1"].value = text
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color="1F3864")
    if sub:
        ws["A2"].value = sub
        ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="595959")


def header_row(ws, row, labels, start_col=1, fill=HDR):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=start_col + i, value=t)
        c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        c.fill = fill
        c.alignment = Alignment(horizontal="center" if i else "left", wrap_text=True, vertical="center")


def section(ws, row, text, ncols):
    for i in range(1, ncols + 1):
        ws.cell(row=row, column=i).fill = SEC
    c = ws.cell(row=row, column=1, value=text)
    c.font = Font(name="Calibri", size=10, bold=True, color="1F3864")


def setup_print(ws, last_row, last_col, freeze=None, landscape=True):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.oddHeader.center.text = f"{TEAM} | FTAI Aviation (NASDAQ: FTAI) | SHORT | 12-mo PT ~$145"
    ws.oddFooter.left.text = "Page &P of &N"
    ws.oddFooter.right.text = "&A"
    ws.print_area = f"A1:{CL(last_col)}{last_row}"
    ws.sheet_view.showGridLines = False
    if freeze:
        ws.freeze_panes = freeze


def setw(ws, widths):
    for k, v in widths.items():
        ws.column_dimensions[k].width = v


# ---------------------------------------------------------------- data loading
def fnum(s):
    try:
        return float(s)
    except Exception:
        return None


def load_csv(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


IS = {}
for r in load_csv("is_quarterly.csv"):
    v = fnum(r["value_usd_m_(EPS_in_$)"])
    if v is not None:
        IS[(r["segment"], r["line_item"], r["period"])] = v
CF = {(r["item"], r["period"]): fnum(r["value_usd_m"]) for r in load_csv("cash_flow.csv")}
BS = {(r["item"], r["quarter_end"]): fnum(r["value_usd_m_(pref_in_M_shares)"]) for r in load_csv("balance_sheet.csv")}
SEGE = {}
for r in load_csv("segment_ebitda.csv"):
    SEGE[(r["segment"], r["metric"], r["period"])] = fnum(r["value_usd_m"])
RP = {}
for r in load_csv("related_party.csv"):
    k = list(r.values())
    RP[(k[1], k[0])] = fnum(k[2])

YEARS = ["2023", "2024", "2025"]
QTRS = ["Q1-2024", "Q2-2024", "Q3-2024", "Q4-2024", "Q1-2025", "Q2-2025", "Q3-2025", "Q4-2025", "Q1-2026", "Q2-2026"]
HPER = ["FY2023", "FY2024", "FY2025"] + QTRS


def qsum(f, yr):
    vals = [f(f"Q{q}-{yr}") for q in (1, 2, 3, 4)]
    if any(v is None for v in vals):
        return None
    return round(sum(vals), 6)


def is_get(seg, variants, fy="csv", sign=1):
    def g(p):
        if p.startswith("FY") and fy == "sum":
            yr = p[2:]
            return qsum(g, yr)
        for l in variants:
            v = IS.get((seg, l, p))
            if v is not None:
                return v * sign
        return None
    return g


def cf_get(item, sign=1):
    def g(p):
        if p.startswith("FY"):
            return qsum(g, p[2:])
        v = CF.get((item, p))
        return None if v is None else v * sign
    return g


def bs_get(item):
    def g(p):
        if p.startswith("FY"):
            p = "Q4-" + p[2:]
        return BS.get((item, p))
    return g


def seg_get(seg, metric="Adjusted EBITDA"):
    def g(p):
        if seg.startswith("Elim"):
            for k, v in SEGE.items():
                if k[0].startswith("Elim") and k[2] == p:
                    return v
            return None
        if seg.startswith("Total"):
            for k, v in SEGE.items():
                if k[0].startswith("Total Adjusted") and k[2] == p:
                    return v
            return None
        return SEGE.get((seg, metric, p))
    return g


def rp_get(item_prefix, fy_from_q4=True):
    def g(p):
        pp = p
        if p.startswith("FY"):
            return None
        for (it, per), v in RP.items():
            if it.startswith(item_prefix) and per == pp:
                return v
        return None
    return g


# ---------------------------------------------------------------- workbook skeleton
SHEETS = ["Summary", "Drivers", "Historical", "Quarterly", "Annual", "FCF_Quality", "Valuation", "Bridge",
          "Sensitivity", "Checks", "Sources"]


def new_book():
    wb = Workbook()
    wb.active.title = SHEETS[0]
    for s in SHEETS[1:]:
        wb.create_sheet(s)
    return wb


def wrap_col(ws, col, width, first=5, last=None, size=8):
    """wrap long text in a notes column and grow row height to fit (openpyxl does not auto-fit)"""
    import math
    last = last or ws.max_row
    for r in range(first, last + 1):
        c = ws[f"{col}{r}"]
        if isinstance(c.value, str) and not c.value.startswith("="):
            lines = max(1, math.ceil(len(c.value) / (width * 1.15)))
            c.alignment = Alignment(wrap_text=True, vertical="top")
            if lines > 1:
                cur = ws.row_dimensions[r].height or 12.75
                ws.row_dimensions[r].height = max(cur, 10.5 * lines + 2)


# ================================================================= HISTORICAL
SRC_IS = ("SEC EDGAR 10-Q/10-K segment note, latest filing containing each period (Q2-26 10-Q acc 0001628280-26-051412; "
          "FY25 10-K; Q4 = FY less 9M, derived). Via phase2/data/is_quarterly.csv")
SRC_SEG = ("Q2-26 8-K Ex99.1 2026-07-29 acc 0001628280-26-050622 and 10-Q MD&A/segment notes (phase2/data/segment_ebitda.csv). "
           "Eliminations = Total less 3 segments")
SRC_CF = "Statement of cash flows; Q2-Q4 derived as YTD less prior YTD (DERIVED). phase2/data/cash_flow.csv"
SRC_BS = "10-Q/10-K balance sheet & debt note (phase2/data/balance_sheet.csv); FY = Q4 balance"


def _blank_if(skip, fn):
    return lambda p: None if p in skip else fn(p)


def hist_spec():
    s = []
    A = s.append
    A(("sec", "Income statement (USD m, EPS in $)"))
    A(dict(key="aeprod", label="Aerospace products revenue (ex-MRE)", get=is_get("Total", ["Aerospace products revenue"]), src=SRC_IS))
    A(dict(key="mre", label="MRE Contract revenue (to 2025 Partnership)", get=is_get("Total", ["MRE Contract revenue"]), src=SRC_IS + ". Starts Q1-25"))
    A(dict(key="lease", label="Lease income", get=is_get("Total", ["Lease income"]), src=SRC_IS + ". FY24 differs from quarterly sum by 0.08 (recast between lease income and other revenue; total unaffected)"))
    A(dict(key="maint", label="Maintenance revenue", get=is_get("Total", ["Maintenance revenue"]), src=SRC_IS))
    A(dict(key="asale", label="Asset sales revenue", get=is_get("Total", ["Asset sales revenue"]), src=SRC_IS))
    A(dict(key="orev", label="Other revenue", get=is_get("Total", ["Other revenue"]), src=SRC_IS))
    A(dict(key="totrev", label="Total revenues (reported)", get=is_get("Total", ["Total revenues"]), src=SRC_IS, bold=True))
    A(dict(key="revchk", label="  check: components less total (should be ~0)", f=lambda c, R: f"=SUM({c}{R['aeprod']}:{c}{R['orev']})-{c}{R['totrev']}", fmt=F_NUM, src="Formula check (small FY24 differences are source recasts)"))
    A(dict(key="aerorev", label="Aerospace segment revenue (products + MRE)", get=is_get("Aerospace Products", ["Total revenues"]), src=SRC_IS))
    A(dict(key="leaserev", label="Aviation Leasing segment revenue", get=is_get("Aviation Leasing", ["Total revenues"]), src=SRC_IS))
    A(dict(key="cogs", label="Cost of sales (total)", get=is_get("Total", ["Cost of sales"]), src=SRC_IS))
    A(dict(key="aerocogs", label="Cost of sales - Aerospace segment", get=is_get("Aerospace Products", ["Cost of sales"]), src=SRC_IS))
    A(dict(key="opex", label="Operating expenses", get=is_get("Total", ["Operating expenses"]), src=SRC_IS))
    A(dict(key="ga", label="General and administrative", get=is_get("Total", ["General and administrative"]), src=SRC_IS))
    A(dict(key="acq", label="Acquisition and transaction expenses", get=is_get("Total", ["Acquisition and transaction expenses"]), src=SRC_IS))
    A(dict(key="da", label="Depreciation and amortization", get=is_get("Total", ["Depreciation and amortization"]), src=SRC_IS))
    A(dict(key="int", label="Interest expense (positive = expense)", get=is_get("Total", ["Interest expense"]), src=SRC_IS + ". Sign normalised to positive in source CSV"))
    A(dict(key="gainp", label="Gain on sale to the 2025 Partnership", get=is_get("Total", ["Gain on sale to the 2025 Partnership"]), src=SRC_IS + ". Booked in Aviation Leasing"))
    A(dict(key="equity", label="Equity in earnings (losses) of unconsolidated entities", get=is_get("Total", [
        "Equity in (losses) earnings of unconsolidated entities", "Equity in earnings (losses) of unconsolidated entities",
        "Equity in losses of unconsolidated entities"], fy="sum"),
        src=SRC_IS + ". FY = sum of quarters (the CSV FY25 value of -6.8 is the Q4 figure only). FY23 not complete"))
    SK = ("FY2023", "FY2024", "Q4-2024")
    A(dict(key="pretax", label="Income (loss) before income taxes", get=_blank_if(SK, is_get("Total", ["Income (loss) before income taxes"])),
           src=SRC_IS + ". FY23/FY24 and Q4-24 not cleanly parsed in source (continuing/discontinued label variants), left blank"))
    A(dict(key="tax", label="Provision for income taxes", get=_blank_if(SK, is_get("Total", ["Provision for (benefit from) income taxes"])), src=SRC_IS + ". As above"))
    A(dict(key="ni", label="Net income (loss)", get=_blank_if(SK, is_get("Total", ["Net income (loss)"])), src=SRC_IS + ". As above"))
    A(dict(key="niattr", label="Net income attributable to shareholders", get=is_get("Total", ["Net income attributable to shareholders"]), src=SRC_IS, bold=True))
    A(dict(key="prefnci", label="Preferred dividends + non-controlling interest (NI less attributable)",
           f=lambda c, R: f'=IF(OR({c}{R["ni"]}="",{c}{R["niattr"]}=""),"",{c}{R["ni"]}-{c}{R["niattr"]})', fmt=F_NUM, src="Formula"))
    A(dict(key="eps", label="Diluted EPS ($)", get=is_get("Total", ["Diluted EPS ($)"]), fmt=F_USD, src=SRC_IS))
    A(dict(key="shares", label="Diluted weighted shares (M)", get=is_get("Total", ["Diluted weighted shares (M)"]), fmt=F_3, src=SRC_IS))
    A(("sec", "Segment Adjusted EBITDA (USD m)"))
    A(dict(key="e_aero", label="Aerospace Products", get=seg_get("Aerospace Products"), src=SRC_SEG))
    A(dict(key="e_leas", label="Aviation Leasing", get=seg_get("Aviation Leasing"), src=SRC_SEG))
    A(dict(key="e_corp", label="Corporate and Other", get=seg_get("Corporate and Other"), src=SRC_SEG))
    A(dict(key="e_elim", label="Eliminations (profit elimination on sales to 2025 Partnership)", get=seg_get("Elim"), src=SRC_SEG))
    A(dict(key="e_tot", label="Total Adjusted EBITDA (company basis)", get=seg_get("Total"), src=SRC_SEG, bold=True))
    A(dict(key="e_chk", label="  check: segments less total (should be 0)", f=lambda c, R: f"={c}{R['e_aero']}+{c}{R['e_leas']}+{c}{R['e_corp']}+{c}{R['e_elim']}-{c}{R['e_tot']}", fmt=F_NUM, src="Formula check"))
    A(dict(key="e_seg", label="Segment-basis EBITDA (Aerospace + Leasing; excl. Corporate and Elims)", f=lambda c, R: f"={c}{R['e_aero']}+{c}{R['e_leas']}", fmt=F_NUM,
           src="Formula. Basis used by management guidance (2026: 1,525 = 1,050 + 475)"))
    A(dict(key="modules", label="Aerospace modules produced (units)", get=lambda p: {"Q1-2025": 138, "Q2-2025": 184, "Q4-2025": 228, "Q2-2026": 296}.get(p), fmt=F_NUM0,
           src="Q2-25 release (184); Q4-25 call (228); Q2-26 call (296); Q1-25 (~138) back-solved from '+33%'. Q3-25 and Q1-26 not found. Call figures are secondary"))
    A(dict(key="modules_est", label="Aerospace modules incl. Q1-26 estimate (Q1-26 = EBITDA / Q2-26 EBITDA per module)", est=True, fmt=F_NUM0,
           src="ASSUMPTION (derived): Q1-26 modules not disclosed in sources; estimated at Q2-26 derived EBITDA/module of 0.84"))
    A(("sec", "Gains embedded in Adjusted EBITDA (cash-flow-statement add-backs, positive = gain)"))
    A(dict(key="g_asset", label="Gain on sale of assets", get=cf_get("Gain_on_sale_of_assets_(CFO_addback,neg)", -1), src=SRC_CF))
    A(dict(key="g_part", label="Gain on sale to the 2025 Partnership (seed assets)", get=cf_get("Gain_on_sale_to_2025_Partnership_(CFO_addback,neg)", -1), src=SRC_CF))
    A(dict(key="g_ins", label="Gain on insurance recoveries (Russia)", get=cf_get("Gain_on_insurance_recoveries_(CFO_addback,neg)", -1), src=SRC_CF))
    A(dict(key="g_tot", label="Total gains (segment attribution not disclosed)", f=lambda c, R: f"=SUM({c}{R['g_asset']}:{c}{R['g_ins']})", fmt=F_NUM, src="Formula"))
    A(("sec", "Cash flow (USD m)"))
    A(dict(key="cfo", label="Cash flow from operations (CFO)", get=cf_get("CFO"), src=SRC_CF, bold=True))
    A(dict(key="cfi", label="Cash flow from investing (CFI)", get=cf_get("CFI"), src=SRC_CF, bold=True))
    A(dict(key="cfocfi", label="CFO + CFI", f=lambda c, R: f"={c}{R['cfo']}+{c}{R['cfi']}", fmt=F_NUM, src="Formula", bold=True))
    A(dict(key="proc", label="CFI: proceeds from sale of assets", get=cf_get("Proceeds_sale_of_assets_(CFI)"), src=SRC_CF))
    A(dict(key="seed", label="CFI: proceeds from sale of seed assets to 2025 Partnership", get=cf_get("Proceeds_sale_to_2025_Partnership_(CFI)"), src=SRC_CF))
    A(dict(key="insproc", label="CFI: insurance settlement proceeds (Russia)", get=cf_get("Proceeds_insurance_settlement_(CFI)"), src=SRC_CF + ". Proceeds (not the CFO gain add-back)"))
    A(dict(key="acqeq", label="CFI: acquisition of leasing equipment", get=cf_get("Acquisition_of_leasing_equipment_(CFI)"), src=SRC_CF))
    A(dict(key="invunc", label="CFI: investment in unconsolidated entities (SCI)", get=cf_get("Investment_in_unconsolidated_entities_(CFI)"), src=SRC_CF + ". Not reported 2024"))
    A(dict(key="ppe", label="CFI: acquisition of PP&E", get=cf_get("Acquisition_of_PP&E_(CFI)"), src=SRC_CF))
    A(dict(key="roc", label="CFI: return of capital from unconsolidated entities (SCI distributions)", get=cf_get("Return_of_capital_from_unconsolidated_CFI"),
           src="Carried from prior research (phase2/data/cash_flow.csv), not re-parsed from filings. Reported from Q1-25"))
    A(dict(key="invchg", label="CFO: change in inventory (negative = outflow)", get=cf_get("Inventory_change_in_CFO_(negative=outflow)"), src=SRC_CF))
    A(dict(key="invproc", label="Memo: inventory-sourced sale proceeds booked in CFI", get=cf_get("Inventory_sourced_sale_proceeds_in_CFI"),
           src="Prior research carry-over (inventory-sourced items), labelled in cash_flow.csv. Reported from Q1-25"))
    A(dict(key="adjfcf", label="Company-reported Adjusted FCF", get=lambda p: {"FY2025": 724.0, "Q2-2025": 423.5, "Q1-2026": 158.0, "Q2-2026": 97.0}.get(p), fmt=F_NUM,
           src="Q2-25 release (EDGAR); FY25 724 and Q1-26 158 from calls (secondary). Q2-26 = 1H26 255 less Q1 158 (derived)"))
    A(("sec", "Balance sheet (period end, USD m)"))
    A(dict(key="cash", label="Cash and cash equivalents", get=bs_get("Cash and cash equivalents"), src=SRC_BS))
    A(dict(key="inv", label="Inventory, net", get=bs_get("Inventory, net"), src=SRC_BS))
    A(dict(key="leq", label="Leasing equipment, net", get=bs_get("Leasing equipment, net"), src=SRC_BS))
    A(dict(key="invest", label="Investments in unconsolidated entities (incl. 2025 Partnership)",
           get=bs_get("Investments (unconsolidated entities incl. 2025 Partnership equity-method)"), src=SRC_BS))
    A(dict(key="sci", label="  of which: 2025 Partnership (SCI I) equity-method carrying value", get=lambda p: {"FY2025": 281.74, "Q4-2025": 281.74, "Q2-2026": 365.485}.get(p),
           src="related_party.csv: 12/31/25 281.74; 6/30/26 365.485 (19% interest)"))
    A(dict(key="ta", label="Total assets", get=bs_get("Total assets"), src=SRC_BS))
    A(dict(key="debt", label="Total debt (carrying, before issuance costs)", get=bs_get("Debt - total carrying value before issuance costs"), src=SRC_BS))
    A(dict(key="iss", label="Unamortized issuance costs", get=bs_get("Debt - less unamortized issuance costs"), src=SRC_BS))
    A(dict(key="tl", label="Total liabilities", get=bs_get("Total liabilities"), src=SRC_BS))
    A(dict(key="eq", label="Shareholders' equity", get=bs_get("Shareholders' equity"), src=SRC_BS))
    A(dict(key="prefsh", label="Preferred shares outstanding (M; $25 liquidation preference)",
           get=bs_get("Preferred shares outstanding (millions of shares; $25 liquidation pref each; book value is par only)"), fmt=F_NUM, src=SRC_BS))
    A(("sec", "Related party (2025 Partnership / SCI)"))
    A(dict(key="sfee", label="Servicing / management fees from Partnership", get=rp_get("Servicing / management fees"), src="related_party.csv (10-Q segment note)"))
    A(dict(key="recv", label="Accounts receivable from Partnership", get=rp_get("Accounts receivable from Partnership"), src="related_party.csv"))
    A(("sec", "KPIs (computed)"))
    A(dict(key="days", label="Days in period", get=lambda p: 365 if p.startswith("FY") else 91.25, fmt=F_NUM, src="Input: 365 for FY, 365/4 for quarters"))
    A(dict(key="k_gain", label="Gains as % of Adjusted EBITDA", f=lambda c, R: f'=IF({c}{R["e_tot"]}=0,"",{c}{R["g_tot"]}/{c}{R["e_tot"]})', fmt=F_PCT, src="Formula (gains from CFS add-backs)"))
    A(dict(key="k_mre", label="MRE share of Aerospace segment revenue", f=lambda c, R: f'=IF(OR({c}{R["mre"]}="",{c}{R["aerorev"]}=0),"",{c}{R["mre"]}/{c}{R["aerorev"]})', fmt=F_PCT, src="Formula"))
    A(dict(key="k_marg", label="Aerospace Adj. EBITDA margin", f=lambda c, R: f'=IF({c}{R["aerorev"]}=0,"",{c}{R["e_aero"]}/{c}{R["aerorev"]})', fmt=F_PCT, src="Formula"))
    A(dict(key="k_invd", label="Inventory days (on total cost of sales)", f=lambda c, R: f'=IF({c}{R["cogs"]}=0,"",{c}{R["inv"]}/{c}{R["cogs"]}*{c}{R["days"]})', fmt=F_NUM,
           src="Formula: period-end inventory / period cost of sales x days. Q2-26 ~222"))
    A(dict(key="k_invda", label="Inventory days (on Aerospace cost of sales)", f=lambda c, R: f'=IF({c}{R["aerocogs"]}=0,"",{c}{R["inv"]}/{c}{R["aerocogs"]}*{c}{R["days"]})', fmt=F_NUM, src="Formula"))
    A(dict(key="k_cfo", label="CFO / Adjusted EBITDA", f=lambda c, R: f'=IF({c}{R["e_tot"]}=0,"",{c}{R["cfo"]}/{c}{R["e_tot"]})', fmt=F_PCT, src="Formula"))
    A(dict(key="k_cfocfi", label="(CFO + CFI) / Adjusted EBITDA", f=lambda c, R: f'=IF({c}{R["e_tot"]}=0,"",{c}{R["cfocfi"]}/{c}{R["e_tot"]})', fmt=F_PCT, src="Formula"))
    A(dict(key="k_seed", label="Seed-sale proceeds + insurance proceeds (one-off CFI items)", f=lambda c, R: f"=N({c}{R['seed']})+N({c}{R['insproc']})", fmt=F_NUM, src="Formula"))
    A(dict(key="k_clean", label="Clean CFO + CFI (excl. seed-sale and insurance proceeds)", f=lambda c, R: f"={c}{R['cfocfi']}-{c}{R['k_seed']}", fmt=F_NUM, src="Formula", bold=True))
    return s


H_ROW, H_COL = {}, {}


def hc(key, period, absolute=True):
    """Absolute reference into the Historical sheet."""
    c, r = H_COL[period], H_ROW[key]
    return f"Historical!${c}${r}" if absolute else f"Historical!{c}{r}"


def build_historical(wb):
    ws = wb["Historical"]
    title(ws, "Historical financials (typed inputs, blue; each row cites its source)",
          "USD millions except per-share. Fiscal year = calendar year. Q4 figures are derived as FY less 9M, so 'quarters sum to FY' for IS rows holds by construction (not independent verification).")
    heads = ["USD m", "FY2023A", "FY2024A", "FY2025A", "Q1'24A", "Q2'24A", "Q3'24A", "Q4'24A", "Q1'25A", "Q2'25A", "Q3'25A", "Q4'25A", "Q1'26A", "Q2'26A", "Source / rationale"]
    header_row(ws, 4, heads)
    for i, p in enumerate(HPER):
        H_COL[p] = CL(2 + i)
    spec = hist_spec()
    r = 5
    plan = []
    for it in spec:
        plan.append((r, it))
        if isinstance(it, dict):
            H_ROW[it["key"]] = r
        r += 1
    for r, it in plan:
        if isinstance(it, tuple):
            section(ws, r, it[1], 15)
            continue
        label(ws, r, it["label"], bold=it.get("bold", False))
        fmt = it.get("fmt", F_NUM)
        for p in HPER:
            c = H_COL[p]
            if "get" in it:
                v = it["get"](p)
                if v is not None:
                    W(ws, f"{c}{r}", v, fmt=fmt, bold=it.get("bold", False))
            elif it.get("est"):
                if p == "Q1-2026":
                    W(ws, f"{c}{r}", f"=ROUND({c}{H_ROW['e_aero']}/({H_COL['Q2-2026']}{H_ROW['e_aero']}/{H_COL['Q2-2026']}{H_ROW['modules']}),0)", fmt=fmt,
                      color=BLUE, italic=True,
                      comment="ASSUMPTION: Q1-26 module count not found in sources. Estimated as Q1-26 Aerospace EBITDA divided by Q2-26 derived EBITDA per module (249.7/296 = 0.84).")
                elif p == "Q2-2026":
                    W(ws, f"{c}{r}", f"={c}{H_ROW['modules']}", fmt=fmt)
            else:
                W(ws, f"{c}{r}", it["f"](c, H_ROW), fmt=fmt, bold=it.get("bold", False))
        ws[f"O{r}"].value = it["src"]
        ws[f"O{r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    last = r
    setw(ws, {"A": 62, "O": 90, **{CL(i): 10.5 for i in range(2, 15)}})
    wrap_col(ws, "O", 90, 5, last)
    setup_print(ws, last, 15, freeze="B5")
    return ws


# ================================================================= DRIVERS
DRV = {}          # key -> dict(rows=[...], live=row, scen=bool)
QC = ["D", "E", "F", "G", "H", "I"]            # Q3'26 .. Q4'27 (Drivers and Quarterly share these letters)
AC = ["J", "K", "L"]                            # FY28..FY30 on Drivers
QLAB = ["Q3'26E", "Q4'26E", "Q1'27E", "Q2'27E", "Q3'27E", "Q4'27E"]
ENG = {}          # engine registry


def dq(key, col):
    """live (selected-scenario) driver cell, absolute row"""
    return f"Drivers!{col}${DRV[key]['live']}"


def dsc(key, i, col):
    return f"Drivers!{col}${DRV[key]['rows'][i]}"


def dsc_loc(key, i, col):
    return f"{col}{DRV[key]['rows'][i]}"


class DrvBuilder:
    def __init__(self, ws):
        self.ws = ws
        self.r = 16

    def head(self, text, sub=None):
        ws = self.ws
        r = self.r
        section(ws, r, text, 13)
        header_row(ws, r + 1, ["Driver", "Unit", "Q2'26A"] + QLAB + ["FY2028E", "FY2029E", "FY2030E", "Source / rationale"], fill=PatternFill("solid", fgColor="44546A"))
        self.r = r + 2

    def ts(self, key, text, unit, data, fmt=F_NUM, src="", scen=True, cols="DEFGHI", flag=None, comment=None, live_fmt=None):
        ws = self.ws
        r = self.r
        label(ws, r, text, bold=True, key=bool(flag))
        ws[f"B{r}"].value = unit
        ws[f"B{r}"].font = Font(name="Calibri", size=9, color="595959")
        ws[f"M{r}"].value = src
        ws[f"M{r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
        ws[f"M{r}"].alignment = Alignment(wrap_text=False)
        fill = YEL if flag else None
        if scen:
            rows = []
            for i, s in enumerate(SCEN):
                rr = r + 1 + i
                rows.append(rr)
                label(ws, rr, s, indent=2)
                for col, v in zip(cols, data[s]):
                    if v is None:
                        continue
                    W(ws, f"{col}{rr}", v, fmt=fmt, fill=fill)
            live = r + 5
            label(ws, live, "Selected scenario (live)", bold=True, indent=2)
            for j, col in enumerate(cols):
                if data["Base"][j] is None:
                    continue
                W(ws, f"{col}{live}", f"=INDEX({col}{rows[0]}:{col}{rows[3]},$E$4)", fmt=live_fmt or fmt, bold=True)
            if comment:
                ws[f"A{r}"].comment = Comment(comment, "Model")
                ws[f"A{r}"].comment.width, ws[f"A{r}"].comment.height = 360, 160
            self.r = r + 7
        else:
            rows = [r]
            live = r
            for col, v in zip(cols, data):
                if v is None:
                    continue
                W(ws, f"{col}{r}", v, fmt=fmt, fill=fill)
            if comment:
                ws[f"A{r}"].comment = Comment(comment, "Model")
            self.r = r + 2
        DRV[key] = dict(rows=rows, live=live, scen=scen)
        return live

    def scalar(self, key, text, unit, v, fmt=F_NUM, src="", comment=None, col="D", flag=None):
        ws = self.ws
        r = self.r
        label(ws, r, text, key=bool(flag))
        ws[f"B{r}"].value = unit
        ws[f"B{r}"].font = Font(name="Calibri", size=9, color="595959")
        W(ws, f"{col}{r}", v, fmt=fmt, comment=comment, fill=YEL if flag else None)
        ws[f"M{r}"].value = src
        ws[f"M{r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
        DRV[key] = dict(rows=[r], live=r, scen=False, col=col)
        self.r = r + 1
        return r


def S(key):  # scalar absolute ref
    d = DRV[key]
    return f"Drivers!${d.get('col', 'D')}${d['live']}"


def build_drivers(wb, scenario="Base"):
    ws = wb["Drivers"]
    title(ws, "Drivers: every projection traces to this tab",
          "Blue = typed input; black = formula; green = link. Yellow fill + red bold label = KEY ASSUMPTION. Scenario selector below drives all 'Selected' rows. USD m unless stated.")
    label(ws, 4, "SCENARIO SELECTOR (dropdown)", bold=True)
    W(ws, "C4", scenario, bold=True, fill=YEL, color=BLUE, comment="Choose Bear / Base / Bull / Mgmt Guide. Named range 'Scenario'. All 'Selected' driver rows use INDEX on this choice.")
    label(ws, 5, "Scenario index (formula)")
    W(ws, "E4", "=MATCH(C4,G4:J4,0)", fmt="0")
    for i, s in enumerate(SCEN):
        W(ws, f"{CL(7 + i)}4", s, color=BLACK, bold=True)
    ws["F4"].value = "list:"
    wb.defined_names["Scenario"] = DefinedName("Scenario", attr_text="Drivers!$C$4")
    dv = DataValidation(type="list", formula1='"Bear,Base,Bull,Mgmt Guide"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add("C4")
    B = DrvBuilder(ws)

    # ---------------- general
    B.head("0. General constants")
    B.scalar("qpy", "Quarters per year", "#", 4, fmt="0", src="Calendar constant")
    B.scalar("dpq", "Days per quarter", "days", 91.25, src="365/4")
    B.scalar("dpy", "Days per year", "days", 365, fmt="0", src="Calendar constant")
    B.scalar("mpy", "Months per year", "months", 12, fmt="0", src="Calendar constant")
    B.scalar("nq", "Quarters of actuals in 1H26", "#", 2, fmt="0", src="Q1-26 and Q2-26 actuals")
    B.scalar("prefpar", "Preferred liquidation preference per share", "$", 25, fmt=F_USD, src="$25 per preferred share (balance_sheet.csv label)")

    # ---------------- aerospace
    B.head("1. Aerospace (SCI / MRE modules + products)")
    B.ts("mod", "Modules produced and sold per quarter", "units",
         {"Bear": [285, 295, 315, 330, 350, 355], "Base": [305, 320, 355, 370, 385, 390], "Bull": [315, 345, 400, 420, 435, 445], "Mgmt Guide": [310, 330, 400, 420, 435, 445]},
         fmt=F_NUM0, flag="KEY1",
         comment="KEY ASSUMPTION #1 (volume leg): 2027 Aerospace EBITDA = modules x EBITDA per module. Mgmt guide needs 1,700 modules (+42% vs 2026 pace of ~1,200); Base 1,500.",
         src="KEY #1. 2027 totals Bear 1,350 / Base 1,500 / Bull 1,700 / Mgmt 1,700 per A_2027_guide_segment_build.csv. 2026 Mgmt total 1,200 (Q2-26 call). 2H26 splits are analyst assumptions (Q2-26 actual 296)")
    B.ts("modg", "Module growth y/y (FY28-FY30)", "%", {"Bear": [.03, .03, .03], "Base": [.08, .06, .05], "Bull": [.12, .10, .08], "Mgmt Guide": [.12, .10, .08]},
         fmt=F_PCT, cols="JKL", src="ASSUMPTION: guidance ends 2027. Mgmt Guide FY28+ set equal to Bull. Rationale: 3,000-module physical capacity, GE shop-visit demand ~2,400/yr")
    B.ts("revpm", "Aerospace revenue per module (products + MRE)", "$M", [2.96] * 6 + [None] * 3, fmt='0.000', scen=False, cols="DEFGHIJKL",
         src="Q2-26 actual: 875.0 segment revenue / 296 modules = 2.956 (A_2027_guide.md uses ~2.96)")
    B.ts("revpmg", "Revenue per module growth y/y (FY28-FY30)", "%", [0.0, 0.0, 0.0], fmt=F_PCT, scen=False, cols="JKL", src="ASSUMPTION: flat pricing/mix")
    B.ts("epm", "Aerospace EBITDA per module", "$M",
         {"Bear": [.80, .80, .7778, .7778, .7778, .7778], "Base": [.84, .84, .82, .82, .82, .82], "Bull": [.86, .88, .8412, .8412, .8412, .8412],
          "Mgmt Guide": [.9027, .9027, .8235, .8235, .8235, .8235]}, fmt='0.0000', flag="KEY1",
         comment="KEY ASSUMPTION #1 (margin leg): EBITDA per module. Q2-26 actual 0.84 (28.5% margin). Mgmt guide implies 0.8235 in 2027; 2H26 guide implies ~0.90 (a +16% step-up on Q2 EBITDA).",
         src="2027: Bear 0.78 / Base 0.82 / Bull 0.84 per A segment build (rounded to land 1,050 / 1,230 / 1,430); Mgmt 0.8235 = 1,400/1,700. Mgmt 2H26 0.9027 solves to 1,050 FY26 guide. Q2-26 actual 0.84")
    B.ts("mre", "MRE share of Aerospace revenue", "%", [0.22] * 6 + [0.20] * 3, fmt=F_PCT, scen=False, cols="DEFGHIJKL",
         src="Q2-26 actual 20.9%; 1H26 25.0%; FY25 17.3%. ASSUMPTION: 22% 2H26-2027, 20% after")
    B.ts("acap", "Aerospace margin cap (economies of scale limit)", "%", {"Bear": [.28], "Base": [.31], "Bull": [.33], "Mgmt Guide": [.31]}, fmt=F_PCT, cols="D",
         src="ASSUMPTION: margin cannot exceed cap. Mgmt now guides ~30% near term (walked back from 40% target)")
    B.scalar("aelast", "Scale elasticity: margin points gained per 1 point of volume growth", "pp/pp", 0.10, fmt="0.00",
             src="ASSUMPTION: +10% module volume adds +1.0pp margin, up to the cap (competition tip on economies of scale)")

    # ---------------- power
    B.head("2. Power (J&F JV, equity-accounted; Adj. EBITDA includes pro-rata share)")
    B.ts("units", "Power units delivered per quarter (FY28-30: per year)", "units",
         {"Bear": [0, 0, 0, 4, 8, 8, 40, 50, 50], "Base": [0, 0, 4, 10, 14, 16, 70, 80, 90], "Bull": [0, 0, 10, 18, 24, 28, 100, 100, 100], "Mgmt Guide": [0, 0, 6, 14, 19, 21, 80, 100, 100]},
         fmt=F_NUM0, cols="DEFGHIJKL", flag="KEY3",
         comment="KEY ASSUMPTION #3: the Power ramp. First deliveries start 2027 (mgmt: 'prudent to expect'). 2027 units Bear 20 / Base 44 (~75% of the 59-unit PO) / Bull 80 / Mgmt 60 ($450M / $7.5M). FY28+ are analyst assumptions.",
         src="KEY #3. A_2027_guide_segment_build.csv: Bear 20, Base 44, Bull 59 + ~20 add-on, Mgmt 450/7.5 = 60. 2026 = 0 (first delivery 'prudent to expect' 2027). Quarterly phasing is an assumption (batches run through Nov-2027)")
    B.ts("epu", "Power EBITDA per unit (pro-rata)", "$M", {s: [7.5] * 9 for s in SCEN}, fmt="0.00", cols="DEFGHIJKL", flag="KEY3",
         comment="KEY ASSUMPTION #3 (cont.): EBITDA per unit of $7.5M is from secondary reports and is UNVERIFIED. Q4-25 call: Power margin 'as good or better than Aerospace' (30-35% on ~$25M = $7.5-8.75M).",
         src="UNVERIFIED secondary source ($7-8M per unit; $1M/MW x 25MW). Held at 7.5 in all scenarios so the units drive the spread (per A segment build)")
    B.scalar("pprice", "Power revenue per unit to FTAI (turbine sale to JV)", "$M", 25.0, src="UNVERIFIED: ~$1M per MW x 25 MW (secondary). Used for revenue memo only")
    B.scalar("pcost", "Power turbine cost per unit (working-capital investment)", "$M", 17.5, src="ASSUMPTION = price less EBITDA per unit (25 - 7.5). Funded one quarter ahead of delivery")
    B.scalar("pcash", "Power: share of EBITDA that is cash in CFO", "%", 0.75, fmt=F_PCT, src="ASSUMPTION (invented): pro-rata JV earnings are non-cash until distributed; 25% haircut")
    B.scalar("ppre", "Power: share of EBITDA that reaches pre-tax income", "%", 0.75, fmt=F_PCT, src="ASSUMPTION (invented): JV-level D&A/interest/tax absorb 25% of pro-rata EBITDA. Moves Bull EPS materially")

    # ---------------- leasing
    B.head("3. Leasing (book run-off, SCI fees and co-investment returns)")
    B.ts("sold", "Leasing book value sold (per quarter; FY28-30 per year)", "$M",
         {"Bear": [100, 80, 70, 60, 50, 40, 150, 100, 75], "Base": [150, 130, 110, 100, 90, 80, 250, 150, 100], "Bull": [170, 150, 130, 120, 110, 100, 200, 100, 50],
          "Mgmt Guide": [170, 150, 130, 120, 110, 100, 200, 100, 50]}, fmt=F_NUM, cols="DEFGHIJKL",
         src="ASSUMPTION calibrated so segment Leasing EBITDA lands on A's 2027 targets (270/360/450/450) and the 2026 guide (475). Book was 1,146 at 6/30/26 (22 aircraft, 176 engines); balance-sheet check on Checks tab")
    B.scalar("gain", "Gain on sale as % of book value sold", "%", 0.15, fmt=F_PCT, src="ASSUMPTION: Q2-26 'balance-sheet leasing and gains' $48M less ~$26M rent implies ~15% gains on ~$140M sold. 1H26 CFS gains $178M + $18M")
    B.scalar("yield", "Lease EBITDA yield on beginning book (annualised)", "%", 0.085, fmt=F_PCT, src="ASSUMPTION: ~$25M quarterly rent EBITDA on ~$1.2B book (lease income 27.8 + maintenance 25.8 less costs)")
    B.ts("aum", "SCI total AUM (end of period; FY28-30 year-end)", "$M",
         {"Bear": [6000, 6150, 6300, 6450, 6600, 6750, 6900, 7500, 8100, 8700], "Base": [6000, 6300, 6600, 6900, 7200, 7500, 7800, 9000, 10200, 11400],
          "Bull": [6000, 6450, 6900, 7350, 7800, 8250, 8700, 10500, 12000, 13500], "Mgmt Guide": [6000, 6450, 6900, 7350, 7800, 8250, 8700, 10500, 12000, 13500]},
         fmt=F_NUM0, cols="CDEFGHIJKL",
         src="Q2'26A ~6,000: SCI I total capital ~$6.0B (thesis.md). SCI II targets $6B, deploys $2-3B in 2026-27 (bull). Growth path is an ASSUMPTION; servicing fee grows with AUM")
    B.scalar("sci_call", "SCI fees and co-invest returns per Q2-26 call (quarter)", "$M", 35.0, src="Q2-26 call (secondary): $5M insurance / $48M balance-sheet leasing and gains / $35M SCI fees and co-invest returns")
    r_fee = B.scalar("feerate", "SCI servicing fee rate (annualised % of AUM)", "%", f"={hc('sfee', 'Q2-2026')}*{S('qpy')}/$C${DRV['aum']['rows'][1]}", fmt='0.000%',
                     src="Formula: Q2-26 servicing fees 6.988 x 4 / AUM 6,000")
    B.ts("prorata", "Pro-rata SCI EBITDA and co-invest returns (included in Adj. EBITDA; non-cash until distributed)", "$M",
         {"Bear": [28.3, 28.3, 30.9, 32.9, 34.9, 37.0], "Base": [33.2, 33.3, 50.0, 52.0, 54.0, 56.2], "Bull": [53.9, 53.8, 70.3, 72.3, 74.3, 76.5],
          "Mgmt Guide": [63.3, 63.3, 70.3, 72.3, 74.3, 76.5]}, fmt=F_NUM,
         src="Calibrated to A's SCI component (Bear 190 / Base 240 / Bull 300 for 2027, 2027 = fees + this line). Q2-26 run-rate ~28 (35 less 7.0 fees). NOTE: Mgmt 2H26 of 63/qtr is what the 475 guide requires, roughly double the Q2 run-rate")
    B.ts("insur", "Insurance recoveries included in Leasing EBITDA", "$M", [0.0] * 6, scen=False, src="ASSUMPTION: none (Q1-26 44.6 gain, Q2-26 5.0 were one-offs)")
    B.ts("lgrow", "Leasing EBITDA growth y/y (FY28-30)", "%", {"Bear": [-.05, 0, 0], "Base": [.05, .05, .05], "Bull": [.10, .08, .06], "Mgmt Guide": [.10, .08, .06]}, fmt=F_PCT, cols="JKL",
         src="ASSUMPTION: SCI fees grow with AUM while book run-off continues")
    B.ts("acq", "Leasing equipment acquisitions (cash; FY28-30 per year)", "$M", [25] * 6 + [100] * 3, scen=False, cols="DEFGHIJKL", fmt=F_NUM,
         src="ASSUMPTION: asset-light. 1H26 actual 163 (87.8 + 75.3), falling; added to book value")
    B.scalar("dist", "SCI cash distributions as % of pro-rata EBITDA", "%", 0.65, fmt=F_PCT, src="Q2-26 return of capital 19.2 vs ~28 pro-rata (69%); FY25 27.1 total. ASSUMPTION 65%")
    B.scalar("coinv", "SCI co-investment as % of AUM growth (cash)", "%", 0.15, fmt=F_PCT, src="FTAI commits ~15% of SCI II (Q2-26 call, secondary); 19% of SCI I")
    B.scalar("seedsh", "Share of book sold that is a seed sale to SCI (cash proceeds stripped from 'clean' FCF)", "%", 0.30, fmt=F_PCT,
             src="ASSUMPTION. 1H26 seed proceeds 175.7 are 'non-recurring' per 10-Q; seed sales shrinking (15 aircraft 1H26 vs 37 1H25)")
    B.scalar("leasrev", "Leasing revenue as % of Leasing EBITDA", "%", f"={hc('leaserev', 'Q2-2026')}/{hc('e_leas', 'Q2-2026')}", fmt=F_PCT, src="Formula: Q2-26 segment revenue 78.1 / EBITDA 88.2")

    # ---------------- corporate
    B.head("4. Corporate, D&A, interest, tax, shares")
    B.ts("corp", "Corporate and Other EBITDA (quarter; FY28-30 growth in cost)", "$M", [-40.0] * 6 + [0.03] * 3, scen=False, cols="DEFGHIJKL", fmt=F_NUM,
         src="Q1-26 -40.0, Q2-26 -39.9. FY28-30 columns = annual cost growth % (ASSUMPTION 3%). Excluded from management segment guidance")
    B.scalar("elimp", "Profit elimination as % of MRE revenue", "%", f"=-({hc('e_elim', 'Q1-2026')}+{hc('e_elim', 'Q2-2026')})/({hc('mre', 'Q1-2026')}+{hc('mre', 'Q2-2026')})", fmt=F_PCT,
             src="Formula: 1H26 eliminations 16.6 / MRE revenue 404.0 (4.1%)")
    B.scalar("odna", "Other (non-leasing) D&A in Q2-26", "$M", 2.5, src="ASSUMPTION: Aerospace PP&E / other depreciation; remainder of Q2-26 D&A is allocated to the leasing book")
    B.scalar("deprate", "Leasing D&A rate (% of beginning leasing book, per quarter)", "%",
             f"=({hc('da', 'Q2-2026')}-D{B.r - 1})/{hc('leq', 'Q1-2026')}", fmt='0.00%', src="Formula: (Q2-26 D&A 47.0 less other 2.5) / beginning book 1,248.8")
    B.scalar("life", "Useful life of Aerospace capex base", "years", 10, fmt="0", src="ASSUMPTION: new capex depreciates straight-line over 10 years (links D&A to the Aerospace capex base)")
    B.ts("capex", "PP&E capex (quarter; FY28-30 per year)", "$M", [15] * 6 + [60] * 3, scen=False, cols="DEFGHIJKL", fmt=F_NUM, src="Q1-26 6.6, Q2-26 17.4. ASSUMPTION 15/quarter")
    B.scalar("tax", "Effective tax rate", "%", 0.18, fmt=F_PCT, src="1H26 effective rate 17.8% (57.1/320.1); FY25 17.4%")
    B.scalar("pnci", "Preferred dividends + NCI per quarter", "$M", f"={hc('prefnci', 'Q2-2026')}", src="Formula: Q2-26 net income less attributable (7.5). Preferred shares fell to 2.6M (65M liquidation)")
    B.scalar("shs", "Diluted shares (quarterly, before buyback)", "M", f"={hc('shares', 'Q2-2026')}", fmt=F_3, src="Q2-26 diluted weighted 104.04M")
    B.scalar("bbtog", "Buyback toggle (1 = on, 0 = off)", "0/1", 0, fmt="0", src="$500M program reported but UNVERIFIED -> default OFF", comment="Reported, not verified. Default OFF.")
    B.scalar("bbamt", "Buyback program size", "$M", 500, src="UNVERIFIED press report")
    B.scalar("bbq", "Buyback executed evenly over (quarters)", "#", 6, fmt="0", src="ASSUMPTION: spread over Q3'26-Q4'27")
    B.scalar("dps", "Common dividend per share per quarter", "$", 0.30, fmt=F_USD, src="ASSUMPTION - NOT IN PROVIDED DATA: recollection of FTAI's quarterly dividend; UNVERIFIED. Funds via cash/revolver only")
    B.scalar("mincash", "Minimum cash balance (revolver sweep)", "$M", 300, src="ASSUMPTION; Q2-26 cash 337")
    B.scalar("revrate", "Revolver interest rate", "%", 0.06, fmt=F_PCT, src="ASSUMPTION: SOFR + 1.25-2.00% (Note 6); undrawn at 6/30/26")
    B.scalar("refi", "Refinancing coupon on 2028 notes (from May 2028)", "%", 0.07, fmt=F_PCT, src="ASSUMPTION: 7.0% (recent issues 7.0%-7.875%)")
    B.scalar("n28m", "Months of 2028 notes at old coupon in FY2028", "months", 4, fmt="0", src="Maturity 2028-05-01 (debt_schedule.csv)")
    # notes table
    ws[f"A{B.r}"].value = "Senior notes (face USD m at 6/30/26 | coupon | maturity)"
    ws[f"A{B.r}"].font = Font(name="Calibri", size=10, bold=True)
    B.r += 1
    notes = [("2028 notes", 1000.0, 0.055, "2028-05-01"), ("2030 notes", 500.0, 0.07875, "2030-12-01"), ("2031 notes", 700.0, 0.07, "2031-05-01"),
             ("2032 notes", 800.0, 0.07, "2032-06-15"), ("2033 notes", 500.0, 0.05875, "2033-04-15")]
    DRV["notes"] = dict(first=B.r, last=B.r + len(notes) - 1)
    for nm, face, cpn, mat in notes:
        label(ws, B.r, nm, indent=2)
        W(ws, f"D{B.r}", face, fmt=F_NUM)
        W(ws, f"E{B.r}", cpn, fmt='0.000%')
        W(ws, f"F{B.r}", mat, color=BLUE)
        ws[f"M{B.r}"].value = "debt_schedule.csv; 10-Q Q2-26 Note 6 (acc 0001628280-26-051412)"
        ws[f"M{B.r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
        B.r += 1
    n1, n2 = DRV["notes"]["first"], DRV["notes"]["last"]
    B.scalar("cpnint", "Annual coupon interest at current face", "$M", f"=SUMPRODUCT(D{n1}:D{n2},E{n1}:E{n2})", src="Formula: sum(face x coupon) = 228.8 (ties to 10-K 12-month interest due)")
    B.scalar("othint", "Other interest, fees and amortisation per quarter", "$M", f"={hc('int', 'Q2-2026')}-{S('cpnint')}/{S('qpy')}",
             src="Formula: Q2-26 interest expense 64.1 less coupon interest 57.2 (issuance cost amortisation, commitment fees, other)")
    B.scalar("pgap", "Pro-rata SCI EBITDA, Q1-26 and Q2-26 (assumed equal)", "$M/qtr", f"={S('sci_call')}-{hc('sfee', 'Q2-2026')}",
             src="Formula: call 35 less servicing fees 7.0 = 28.0. ASSUMPTION: Q1-26 assumed equal (components not disclosed). Back-test below")
    B.scalar("eqconv", "Equity earnings as % of pro-rata SCI EBITDA", "%", f"=({hc('equity', 'Q1-2026')}+{hc('equity', 'Q2-2026')})/({S('nq')}*{S('pgap')})", fmt=F_PCT,
             src="Formula: 1H26 equity earnings (-2.4 + 10.0) / pro-rata EBITDA (2 x 28.0)")
    B.scalar("othadj", "Other EBITDA-to-pretax adjustments per quarter (SBC, acquisition costs, other)", "$M",
             f"=(({hc('e_tot', 'Q1-2026')}+{hc('e_tot', 'Q2-2026')})-({hc('da', 'Q1-2026')}+{hc('da', 'Q2-2026')})-({hc('int', 'Q1-2026')}+{hc('int', 'Q2-2026')})-({hc('pretax', 'Q1-2026')}+{hc('pretax', 'Q2-2026')})-({S('nq')}*{S('pgap')}-({hc('equity', 'Q1-2026')}+{hc('equity', 'Q2-2026')})))/{S('nq')}",
             src="Formula: 1H26 gap between Adj. EBITDA less D&A less interest and reported pre-tax income (72.1), less the SCI pro-rata adjustment, per quarter. Back-test on Checks tab reproduces Q1/Q2 EPS")

    # ---------------- working capital
    B.head("5. Working capital (KEY #2: inventory conversion = the 2H26 FCF ramp)")
    B.scalar("d0", "Inventory days at Q2-26 (inventory / Aerospace cost of sales proxy)", "days",
             f"={hc('inv', 'Q2-2026')}/({hc('aerorev', 'Q2-2026')}-{hc('e_aero', 'Q2-2026')})*{S('dpq')}", fmt=F_NUM,
             src="Formula: inventory 1,544.6 / (Aerospace revenue less Aerospace EBITDA as cost-of-sales proxy) x 91.25. Thesis metric on total COGS is ~222")
    B.scalar("tdays", "Normalised inventory days (target if 100% converted)", "days", 150, fmt=F_NUM, src="ASSUMPTION: FY23 run-rate ~100-150 days on quarterly COGS; FY25 Q4 ~290")
    B.ts("phase", "Conversion phasing (share of conversion achieved by quarter)", "x", [0.5, 1.0, 1.0, 1.0, 1.0, 1.0], scen=False, fmt="0.00",
         src="ASSUMPTION: half by Q3'26, complete by Q4'26, held flat through 2027")
    B.ts("conv", "Inventory conversion % (share of excess days above target converted to cash by Q4'26)", "%",
         {"Bear": [0.0], "Base": [0.10], "Bull": [0.25], "Mgmt Guide": [MGMT_CONV]}, fmt=F_PCT, cols="D", flag="KEY2",
         comment="KEY ASSUMPTION #2: 2H26 FCF ramp. FY26 Adj. FCF guide $878M requires ~$623M in 2H26 vs $255M in 1H26. The Mgmt Guide value is BACK-SOLVED (not a judgment) so FY26 Adjusted FCF = 878. Bear/Base/Bull are judgment inputs. Q3 on 10/28 is the first test.",
         src="KEY #2. Mgmt Guide value back-solved in build_model.py so FY26 company-defined Adj. FCF = $878M (guide, 7/30/26). Others are analyst judgment")
    B.ts("days", "Resulting inventory days (on Aerospace cost-of-sales proxy)", "days",
         {s: [f"=$D${DRV['d0']['live']}-$D${DRV['conv']['rows'][i]}*($D${DRV['d0']['live']}-$D${DRV['tdays']['live']})*{c}${DRV['phase']['live']}" for c in QC]
          for i, s in enumerate(SCEN)}, fmt=F_NUM, src="Formula: D0 - conversion x (D0 - target) x phase")
    B.ts("daych", "Change in annual inventory days (FY28-30, days on annual Aerospace COGS)", "days", [-5, -5, -5], scen=False, cols="JKL", fmt=F_NUM,
         src="ASSUMPTION: gradual normalisation after 2027")
    B.scalar("hotp", "Hot-section parts investment added back in company Adjusted FCF (per quarter)", "$M", 12.5,
             src="Q4-25 call: $50M of hot-section parts in FY25 (12.5/qtr). Used only for the company Adjusted FCF definition")

    # ---------------- valuation inputs
    B.head("6. Valuation inputs")
    B.scalar("price", "Share price (10/6/26 close)", "$", 179.44, fmt=F_USD, src="stockanalysis.com /forecast (consensus.csv)")
    B.scalar("vsh", "Shares outstanding for per-share value", "M", 102.71, fmt=F_3, src="stockanalysis /statistics (102.71M; 102.625M at 6/30/26)")
    B.scalar("mcap", "Market cap (stockanalysis)", "$M", 18430, fmt=F_NUM0, src="stockanalysis /statistics")
    B.scalar("evsa", "Enterprise value (stockanalysis)", "$M", 21590, fmt=F_NUM0, src="stockanalysis /statistics (approx. mkt cap + 3,500 debt - 337 cash; excludes 65 preferred)")
    B.scalar("ndsa", "Net debt implied by stockanalysis (EV - market cap)", "$M", f"={S('evsa')}-{S('mcap')}", fmt=F_NUM, src="Formula = ~3,160")
    B.scalar("ndbs", "Net debt, balance sheet 6/30/26 (debt carrying less cash)", "$M", f"={hc('debt', 'Q2-2026')}-{hc('cash', 'Q2-2026')}", fmt=F_NUM,
             src="Formula: 3,496.4 - 337.2 = 3,159.2 (reconciles to stockanalysis 3,160 within 1)")
    B.scalar("prefliq", "Preferred at liquidation value (2.6M x $25)", "$M", f"={hc('prefsh', 'Q2-2026')}*{S('prefpar')}", fmt=F_NUM, src="Formula: 65.0 (balance_sheet.csv pref shares x $25)")
    B.scalar("prefon", "Deduct preferred in equity bridge (1 = yes)", "0/1", 1, fmt="0", src="ASSUMPTION: included for rigour; stockanalysis EV excludes it (worth ~$0.63/share)")
    B.scalar("book", "Leasing book (equipment net + SCI I stake) at 6/30/26", "$M", f"={hc('leq', 'Q2-2026')}+{hc('sci', 'Q2-2026')}", fmt=F_NUM, src="Formula: 1,146.4 + 365.5 = 1,511.9 (thesis: ~$1.5B)")
    B.ts("mult_a", "Aerospace EV/EBITDA multiple (x 2027E)", "x", {"Bear": [11.7], "Base": [13.0], "Bull": [16.0], "Mgmt Guide": [13.0]}, fmt=F_X, cols="D",
         src="thesis.md section 2: StandardAero 11.7x / mid / AAR-AerSale-HEICO blend. Mgmt Guide uses Base multiple (bridge isolates EBITDA)")
    B.ts("mult_p", "Power EV/EBITDA multiple", "x", {"Bear": [8.0], "Base": [10.0], "Bull": [12.0], "Mgmt Guide": [10.0]}, fmt=F_X, cols="D", src="thesis.md: 8x / 10x / 12x")
    B.ts("mult_l", "Leasing multiple of book value", "x", {"Bear": [1.0], "Base": [1.0], "Bull": [1.2], "Mgmt Guide": [1.0]}, fmt='0.00"x"', cols="D", src="thesis.md: book x 1.0 / 1.0 / 1.2")
    B.scalar("corpcap", "Include corporate costs in SOTP (1 = on), capitalised at each scenario's blended Aero+Power multiple", "flag", 1, fmt="0",
             src="Orchestrator review: corporate costs (~$160M/yr) are real and must be valued. v1 excluded them (spec error)")
    B.scalar("pelo", "Forward P/E, low (MRO peers AAR / StandardAero / AerSale)", "x", 16, fmt=F_X, src="thesis.md: 16-18x (peer forward P/E 15.9-18.1x)")
    B.scalar("pehi", "Forward P/E, high", "x", 18, fmt=F_X, src="thesis.md")
    B.scalar("fwdpe", "FTAI forward P/E per stockanalysis", "x", 20.2, fmt=F_X, src="stockanalysis 10/6/26. Data notes flag it as inconsistent with its own FY26 EPS (30.8x)")
    B.scalar("consfy27", "Consensus FY27 EPS implied (price / forward P/E)", "$", f"={S('price')}/{S('fwdpe')}", fmt=F_USD, src="Formula = ~$8.87 (implied; FY27 consensus is paywalled)")
    B.scalar("streetpt", "Street mean price target (7 dated post-June PTs)", "$", 330, fmt=F_USD, src="consensus.csv: mean of 290/300/310/350/360/375/325 (median 325)")
    B.scalar("wacc", "DCF WACC", "%", 0.10, fmt=F_PCT, src="ASSUMPTION fixed before viewing output: equity-heavy cyclical aero with 7%+ cost of debt")
    B.scalar("tg", "DCF terminal growth", "%", 0.03, fmt=F_PCT, src="ASSUMPTION fixed before viewing output")
    B.scalar("w_sotp", "Blend weight: SOTP", "%", 0.40, fmt=F_PCT, src="ASSUMPTION")
    B.scalar("w_pe", "Blend weight: P/E", "%", 0.30, fmt=F_PCT, src="ASSUMPTION")
    B.scalar("w_dcf", "Blend weight: DCF", "%", 0.30, fmt=F_PCT, src="ASSUMPTION")
    B.ts("prob", "Scenario probability weight", "%", {"Bear": [.25], "Base": [.50], "Bull": [.25], "Mgmt Guide": [0.0]}, fmt=F_PCT, cols="D", src="thesis.md: 25/50/25 (30/50/20 alt). Mgmt Guide 0% (it is the bridge anchor)")
    B.scalar("thr", "Recommendation threshold (+/- upside)", "%", 0.10, fmt=F_PCT, src="ASSUMPTION: Long if value/price-1 > +10%, Short if < -10%, else Neutral / marginal")
    B.scalar("marg", "Marginal-call buffer around the threshold", "%", 0.05, fmt=F_PCT, src="ASSUMPTION: flag the call as MARGINAL when |upside| is within 5 points of the threshold")

    # ---------------- engine
    build_engine(ws, B)
    # key assumption panel (rows 7-13)
    build_key_panel(ws)
    setw(ws, {"A": 66, "B": 8, "C": 9, "M": 85, **{CL(i): 10.5 for i in range(4, 13)}})
    wrap_col(ws, "M", 85, 7, B.r)
    setup_print(ws, B.r, 13, freeze="D6")
    return B.r


def build_engine(ws, B):
    """Parallel segment-EBITDA engine for all four scenarios (feeds per-scenario SOTP, bridge, key panel)."""
    B.head("7. Scenario engine: segment EBITDA for ALL scenarios in parallel (feeds Valuation SOTP, Bridge, tie-outs)")
    ws[f"M{B.r - 1}"].value = "Live check on Checks tab: engine for the selected scenario equals the Quarterly tab"
    for i, s in enumerate(SCEN):
        label(ws, B.r, f"Scenario: {s}", bold=True)
        B.r += 1
        e = {}
        names = [("aero", "Aerospace EBITDA"), ("pow", "Power EBITDA"), ("book", "Leasing book, end of period"), ("leas", "Leasing EBITDA"), ("tot", "Segment-basis EBITDA")]
        for k, nm in names:
            e[k] = B.r
            label(ws, B.r, nm, indent=2)
            B.r += 1
        ENG[s] = e
        for j, c in enumerate(QC):
            p = "C" if j == 0 else QC[j - 1]
            W(ws, f"{c}{e['aero']}", f"={c}{DRV['mod']['rows'][i]}*{c}{DRV['epm']['rows'][i]}", fmt=F_NUM)
            W(ws, f"{c}{e['pow']}", f"={c}{DRV['units']['rows'][i]}*{c}{DRV['epu']['rows'][i]}", fmt=F_NUM)
            prevbook = hc("leq", "Q2-2026") if j == 0 else f"{p}{e['book']}"
            W(ws, f"{c}{e['book']}", f"={prevbook}-{c}{DRV['sold']['rows'][i]}-{S('deprate')}*{prevbook}+{c}{DRV['acq']['live']}", fmt=F_NUM)
            W(ws, f"{c}{e['leas']}",
              f"={S('yield')}/{S('qpy')}*{prevbook}+{S('gain')}*{c}{DRV['sold']['rows'][i]}+{S('feerate')}/{S('qpy')}*{p}{DRV['aum']['rows'][i]}+{c}{DRV['prorata']['rows'][i]}+{c}{DRV['insur']['live']}",
              fmt=F_NUM)
            W(ws, f"{c}{e['tot']}", f"={c}{e['aero']}+{c}{e['pow']}+{c}{e['leas']}", fmt=F_NUM, bold=True)
    # summary table
    r = B.r + 1
    section(ws, r, "Scenario summary: segment-basis Adjusted EBITDA (guide basis: excludes Corporate and Eliminations)", 13)
    header_row(ws, r + 1, ["USD m", "", ""] + SCEN + ["", "", "", "", "Target / source"], fill=PatternFill("solid", fgColor="44546A"))
    rows = [("a26", "FY2026E Aerospace"), ("p26", "FY2026E Power"), ("l26", "FY2026E Leasing"), ("t26", "FY2026E Segment total"),
            ("a27", "FY2027E Aerospace"), ("p27", "FY2027E Power"), ("l27", "FY2027E Leasing"), ("t27", "FY2027E Segment total")]
    SUMR = {}
    rr = r + 2
    for k, nm in rows:
        SUMR[k] = rr
        label(ws, rr, nm, bold=k.startswith("t"))
        rr += 1
    for i, s in enumerate(SCEN):
        c = CL(4 + i)
        e = ENG[s]
        W(ws, f"{c}{SUMR['a26']}", f"={hc('e_aero', 'Q1-2026')}+{hc('e_aero', 'Q2-2026')}+SUM(D{e['aero']}:E{e['aero']})", fmt=F_NUM)
        W(ws, f"{c}{SUMR['p26']}", f"=SUM(D{e['pow']}:E{e['pow']})", fmt=F_NUM)
        W(ws, f"{c}{SUMR['l26']}", f"={hc('e_leas', 'Q1-2026')}+{hc('e_leas', 'Q2-2026')}+SUM(D{e['leas']}:E{e['leas']})", fmt=F_NUM)
        W(ws, f"{c}{SUMR['t26']}", f"=SUM({c}{SUMR['a26']}:{c}{SUMR['l26']})", fmt=F_NUM, bold=True)
        W(ws, f"{c}{SUMR['a27']}", f"=SUM(F{e['aero']}:I{e['aero']})", fmt=F_NUM)
        W(ws, f"{c}{SUMR['p27']}", f"=SUM(F{e['pow']}:I{e['pow']})", fmt=F_NUM)
        W(ws, f"{c}{SUMR['l27']}", f"=SUM(F{e['leas']}:I{e['leas']})", fmt=F_NUM)
        W(ws, f"{c}{SUMR['t27']}", f"=SUM({c}{SUMR['a27']}:{c}{SUMR['l27']})", fmt=F_NUM, bold=True)
    notes = {"t26": "Mgmt guide 2026: 1,525 (Aero 1,050 + Leasing 475; 7/29/26 8-K)", "a26": "Guide 1,050", "l26": "Guide 475",
             "t27": "Targets: Bear 1,470 / Base 1,920 / Bull 2,480 / Mgmt 2,300 (A_2027_guide_segment_build.csv)", "a27": "Bear 1,050 / Base 1,230 / Bull 1,430 / Mgmt 1,400",
             "p27": "Bear 150 / Base 330 / Bull 600 / Mgmt 450", "l27": "Bear 270 / Base 360 / Bull 450 / Mgmt 450"}
    for k, t in notes.items():
        ws[f"M{SUMR[k]}"].value = t
        ws[f"M{SUMR[k]}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    # selected column
    label(ws, r + 1, "", bold=True)
    ws[f"H{r + 1}"].value = "Selected"
    ws[f"H{r + 1}"].font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    ws[f"H{r + 1}"].fill = PatternFill("solid", fgColor="44546A")
    for k in SUMR:
        W(ws, f"H{SUMR[k]}", f"=INDEX(D{SUMR[k]}:G{SUMR[k]},$E$4)", fmt=F_NUM, bold=True)
    ENG["SUMR"] = SUMR
    B.r = rr + 2


def sumcell(key, scen_i):
    return f"Drivers!${CL(4 + scen_i)}${ENG['SUMR'][key]}"


def build_key_panel(ws):
    section(ws, 7, "KEY ASSUMPTIONS (3): values by scenario", 13)
    header_row(ws, 8, ["Key assumption", "Unit", ""] + SCEN + ["Selected"], fill=PatternFill("solid", fgColor="44546A"))
    items = [
        ("KEY #1: 2027 Aerospace EBITDA (modules x EBITDA per module)", "$M", [f"={sumcell('a27', i)}" for i in range(4)], F_NUM,
         "KEY ASSUMPTION #1: 2027 Aerospace EBITDA = modules x EBITDA/module. Mgmt guide 1,400 (1,700 modules); Base 1,230 (1,500 modules at 0.82). The guide is a volume call (+42% modules vs 2026), not a margin call."),
        ("KEY #2: Inventory conversion % (drives the 2H26 FCF ramp)", "%", [f"=$D${DRV['conv']['rows'][i]}" for i in range(4)], F_PCT,
         "KEY ASSUMPTION #2: share of excess inventory days converted to cash by Q4'26. Needed for the $878M FY26 Adj. FCF guide ($623M in 2H26 vs $255M in 1H26). Mgmt value is back-solved."),
        ("KEY #3: 2027 Power EBITDA (units x EBITDA per unit)", "$M", [f"={sumcell('p27', i)}" for i in range(4)], F_NUM,
         "KEY ASSUMPTION #3: Power units x EBITDA per unit (7.5, unverified). 2027 units Bear 20 / Base 44 / Bull 80 / Mgmt 60."),
    ]
    for j, (t, u, f, fm, cm) in enumerate(items):
        r = 9 + j
        label(ws, r, t, key=True)
        ws[f"A{r}"].comment = Comment(cm, "Model")
        ws[f"A{r}"].comment.width, ws[f"A{r}"].comment.height = 360, 140
        ws[f"B{r}"].value = u
        for i in range(4):
            W(ws, f"{CL(4 + i)}{r}", f[i], fmt=fm, fill=YEL, bold=True)
        W(ws, f"H{r}", f"=INDEX(D{r}:G{r},$E$4)", fmt=fm, fill=YEL, bold=True)
    label(ws, 12, "Memo: 2027 segment EBITDA total")
    for i in range(4):
        W(ws, f"{CL(4 + i)}12", f"={sumcell('t27', i)}", fmt=F_NUM)
    W(ws, "H12", "=INDEX(D12:G12,$E$4)", fmt=F_NUM, bold=True)


# ================================================================= QUARTERLY + ANNUAL
LAYOUT = [
    ("sec", "AEROSPACE"),
    ("mod", "Modules produced / sold (units)", F_NUM0, False),
    ("revpm", "Revenue per module ($M)", "0.000", False),
    ("aerorev", "Aerospace segment revenue", F_NUM, False),
    ("mrep", "  MRE share of Aerospace revenue", F_PCT, False),
    ("mre", "  MRE Contract revenue (to 2025 Partnership)", F_NUM, False),
    ("epm", "EBITDA per module ($M)", "0.0000", False),
    ("aero", "Aerospace Adj. EBITDA  [KEY #1 = modules x EBITDA per module]", F_NUM, True),
    ("amarg", "  Aerospace EBITDA margin", F_PCT, False),
    ("acogs", "  Aerospace cost of sales (actual; forecast proxy = revenue less EBITDA)", F_NUM, False),
    ("sec", "POWER (J&F JV; pro-rata Adj. EBITDA)"),
    ("units", "Power units delivered", F_NUM0, False),
    ("epu", "EBITDA per unit ($M)", "0.00", False),
    ("power", "Power Adj. EBITDA  [KEY #3 = units x EBITDA per unit]", F_NUM, True),
    ("powrev", "  Power revenue to FTAI (memo, unverified price)", F_NUM, False),
    ("sec", "LEASING"),
    ("bbeg", "Leasing book, beginning", F_NUM, False),
    ("sold", "  less: book value sold (run-off)", F_NUM, False),
    ("dep", "  less: depreciation on book", F_NUM, False),
    ("acq", "  plus: leasing equipment acquisitions", F_NUM, False),
    ("bend", "Leasing book, end", F_NUM, False),
    ("rent", "  Lease EBITDA on beginning book (yield)", F_NUM, False),
    ("gains", "  Gains on sale (% of book sold)", F_NUM, False),
    ("aum", "  SCI AUM, end ($M)", F_NUM0, False),
    ("fee", "  SCI servicing fees (grow with AUM)", F_NUM, False),
    ("prorata", "  Pro-rata SCI EBITDA and co-invest returns (non-cash)", F_NUM, False),
    ("insur", "  Insurance recoveries", F_NUM, False),
    ("leas", "Leasing Adj. EBITDA", F_NUM, True),
    ("leasrev", "  Leasing segment revenue", F_NUM, False),
    ("sec", "CORPORATE AND TOTALS"),
    ("corp", "Corporate and Other EBITDA", F_NUM, False),
    ("elim", "Eliminations (profit on sales to 2025 Partnership)", F_NUM, False),
    ("tot", "Total Adjusted EBITDA (company basis)", F_NUM, True),
    ("seg", "Segment-basis EBITDA (Aero + Power + Leasing; guide basis)", F_NUM, True),
    ("totrev", "Total revenues", F_NUM, False),
    ("tmarg", "  Adj. EBITDA margin on revenue", F_PCT, False),
    ("sec", "EPS BRIDGE"),
    ("b_ebitda", "Total Adjusted EBITDA", F_NUM, False),
    ("da", "less: D&A (leasing book + Aerospace capex base)", F_NUM, False),
    ("oda", "  memo: other (non-leasing) D&A", F_NUM, False),
    ("capex", "  memo: PP&E capex", F_NUM, False),
    ("int", "less: interest expense (debt schedule)", F_NUM, False),
    ("adj", "less: EBITDA-to-pretax adjustments (SCI/Power pro-rata not in pretax, SBC, other)", F_NUM, False),
    ("pretax", "Pre-tax income", F_NUM, True),
    ("taxes", "Income taxes", F_NUM, False),
    ("ni", "Net income", F_NUM, False),
    ("pnci", "less: preferred dividends and NCI", F_NUM, False),
    ("niattr", "Net income attributable to common", F_NUM, True),
    ("shares", "Diluted shares (M)", F_3, False),
    ("eps", "Diluted EPS ($)", F_USD, True),
    ("sec", "CASH FLOW BUILD (CFO + CFI, GAAP classification combined)"),
    ("c_ebitda", "Total Adjusted EBITDA", F_NUM, False),
    ("c_gain", "less: gains in EBITDA (proceeds sit in CFI)", F_NUM, False),
    ("c_pro", "less: pro-rata SCI EBITDA (non-cash)", F_NUM, False),
    ("c_dist", "plus: SCI cash distributions (return of capital)", F_NUM, False),
    ("c_pow", "less: Power EBITDA not converted to cash", F_NUM, False),
    ("c_int", "less: cash interest", F_NUM, False),
    ("c_tax", "less: cash taxes (= book taxes)", F_NUM, False),
    ("c_inv", "less: increase in Aerospace inventory  [KEY #2]", F_NUM, False),
    ("c_powinv", "less: Power turbine working-capital investment (next quarter's units)", F_NUM, False),
    ("c_powrel", "plus: Power working-capital release on delivery", F_NUM, False),
    ("c_sold", "plus: leasing book sold (at book value; gain already in EBITDA)", F_NUM, False),
    ("c_acq", "less: leasing equipment acquisitions", F_NUM, False),
    ("c_coinv", "less: SCI co-investment", F_NUM, False),
    ("c_capex", "less: PP&E capex", F_NUM, False),
    ("c_insp", "plus: insurance proceeds", F_NUM, False),
    ("total", "CFO + CFI (GAAP basis, model)", F_NUM, True),
    ("seed", "  memo: seed-sale proceeds to SCI (one-off)", F_NUM, False),
    ("insm", "  memo: insurance proceeds (one-off)", F_NUM, False),
    ("clean", "Clean CFO + CFI (excl. seed-sale and insurance proceeds)", F_NUM, True),
    ("adjfcf", "Company-defined Adjusted FCF (adds back SCI co-invest, NET Power turbine investment, hot-section parts)", F_NUM, True),
    ("sec", "FINANCING AND BALANCE SHEET ITEMS"),
    ("div", "Common dividends", F_NUM, False),
    ("pncic", "Preferred dividends and NCI (cash)", F_NUM, False),
    ("bb", "Share buybacks (toggle)", F_NUM, False),
    ("precash", "Cash before revolver", F_NUM, False),
    ("revchg", "Revolver draw / (repayment)", F_NUM, False),
    ("cash", "Cash, end", F_NUM, True),
    ("rev", "Revolver balance, end", F_NUM, False),
    ("notes", "Senior notes (carrying, before issuance costs)", F_NUM, False),
    ("netdebt", "Net debt", F_NUM, True),
    ("inv", "Inventory, end", F_NUM, False),
    ("invd", "Inventory days (Aerospace cost-of-sales basis)", F_NUM, False),
]
LROW = {}
_r = 5
for _it in LAYOUT:
    if _it[0] != "sec":
        LROW[_it[0]] = _r
    _r += 1
LAST_ROW = _r


def x(key, col):
    return f"{col}{LROW[key]}"


Q_ALL = ["B", "C", "D", "E", "F", "G", "H", "I"]
Q_HIST = {"B": "Q1-2026", "C": "Q2-2026"}
Q_NEXT = {c: Q_ALL[i + 1] if i + 1 < len(Q_ALL) else None for i, c in enumerate(Q_ALL)}
BB_TERM = lambda: f"{S('bbtog')}*{S('bbamt')}/{S('bbq')}/{S('price')}"

# keys whose FY value = sum / last / computed
FY_SUM = {"mod", "aerorev", "mre", "aero", "acogs", "units", "power", "powrev", "sold", "dep", "acq", "rent", "gains", "fee", "prorata", "insur", "leas", "leasrev",
          "corp", "elim", "tot", "seg", "totrev", "b_ebitda", "da", "capex", "int", "adj", "pretax", "taxes", "ni", "pnci", "niattr", "c_ebitda", "c_gain", "c_pro", "c_dist",
          "c_pow", "c_int", "c_tax", "c_inv", "c_powinv", "c_powrel", "c_sold", "c_acq", "c_coinv", "c_capex", "c_insp", "total", "seed", "insm", "clean", "adjfcf",
          "div", "pncic", "bb", "revchg", "oda"}
FY_LAST = {"bend", "aum", "cash", "rev", "notes", "netdebt", "inv", "precash"}


def ratio_formula(key, c, days="dpy"):
    """computed rows (same formula on both sheets)"""
    if key == "revpm":
        return f"=IF({x('mod', c)}=0,\"\",{x('aerorev', c)}/{x('mod', c)})"
    if key == "mrep":
        return f"=IF({x('aerorev', c)}=0,\"\",{x('mre', c)}/{x('aerorev', c)})"
    if key == "epm":
        return f"=IF({x('mod', c)}=0,\"\",{x('aero', c)}/{x('mod', c)})"
    if key == "amarg":
        return f"=IF({x('aerorev', c)}=0,\"\",{x('aero', c)}/{x('aerorev', c)})"
    if key == "tmarg":
        return f"=IF({x('totrev', c)}=0,\"\",{x('tot', c)}/{x('totrev', c)})"
    if key == "eps":
        return f"={x('niattr', c)}/{x('shares', c)}"
    return None


def quarterly_formula(key, c):
    """returns formula for Quarterly column c (B..I)"""
    i = Q_ALL.index(c)
    p = Q_ALL[i - 1] if i > 0 else None
    n = Q_NEXT[c]
    act = c in Q_HIST
    hp = Q_HIST.get(c)
    X = lambda k, col=c: x(k, col)
    if act:
        m = {
            "mod": f"={hc('modules_est', hp)}", "aerorev": f"={hc('aerorev', hp)}", "mre": f"={hc('mre', hp)}", "aero": f"={hc('e_aero', hp)}", "acogs": f"={hc('aerocogs', hp)}",
            "units": 0, "power": 0, "powrev": 0,
            "bbeg": f"={hc('leq', 'Q4-2025')}" if c == "B" else f"={X('bend', 'B')}", "acq": f"=-{hc('acqeq', hp)}",
            "bend": f"={hc('leq', hp)}", "fee": f"={hc('sfee', hp)}", "prorata": f"={S('pgap')}", "leas": f"={hc('e_leas', hp)}", "leasrev": f"={hc('leaserev', hp)}",
            "corp": f"={hc('e_corp', hp)}", "elim": f"={hc('e_elim', hp)}", "tot": f"={X('aero')}+{X('power')}+{X('leas')}+{X('corp')}+{X('elim')}",
            "seg": f"={X('aero')}+{X('power')}+{X('leas')}", "totrev": f"={hc('totrev', hp)}",
            "b_ebitda": f"={X('tot')}", "da": f"={hc('da', hp)}", "capex": f"=-{hc('ppe', hp)}", "int": f"={hc('int', hp)}",
            "adj": f"={X('pretax')}-({X('tot')}-{X('da')}-{X('int')})", "pretax": f"={hc('pretax', hp)}", "taxes": f"={hc('tax', hp)}", "ni": f"={hc('ni', hp)}",
            "pnci": f"={hc('prefnci', hp)}", "niattr": f"={hc('niattr', hp)}", "shares": f"={hc('shares', hp)}", "eps": f"={hc('eps', hp)}",
            "total": f"={hc('cfocfi', hp)}", "seed": f"={hc('seed', hp)}", "insm": f"={hc('insproc', hp)}", "clean": f"={X('total')}-{X('seed')}-{X('insm')}",
            "adjfcf": f"={hc('adjfcf', hp)}", "cash": f"={hc('cash', hp)}", "rev": 0, "notes": f"={hc('debt', hp)}", "netdebt": f"={X('notes')}+{X('rev')}-{X('cash')}",
            "inv": f"={hc('inv', hp)}",
        }
        if c == "C":
            m["aum"] = f"={dq('aum', 'C')}"
            m["oda"] = f"={S('odna')}"
        if key in m:
            return m[key]
        return ratio_formula(key, c) if key in ("revpm", "mrep", "epm", "amarg", "tmarg") else (
            f"=IF({X('acogs')}=0,\"\",{X('inv')}/{X('acogs')}*{S('dpq')})" if key == "invd" else None)
    # ------------- forecast
    un = f"{n}{LROW['units']}" if n else f"{dq('units', 'J')}/{S('qpy')}"
    m = {
        "mod": f"={dq('mod', c)}", "revpm": f"={dq('revpm', c)}", "aerorev": f"={X('mod')}*{X('revpm')}", "mrep": f"={dq('mre', c)}", "mre": f"={X('aerorev')}*{X('mrep')}",
        "epm": f"={dq('epm', c)}", "aero": f"={X('mod')}*{X('epm')}", "amarg": f"={X('aero')}/{X('aerorev')}", "acogs": f"={X('aerorev')}-{X('aero')}",
        "units": f"={dq('units', c)}", "epu": f"={dq('epu', c)}", "power": f"={X('units')}*{X('epu')}", "powrev": f"={X('units')}*{S('pprice')}",
        "bbeg": f"={x('bend', p)}", "sold": f"={dq('sold', c)}", "dep": f"={S('deprate')}*{X('bbeg')}", "acq": f"={dq('acq', c)}",
        "bend": f"={X('bbeg')}-{X('sold')}-{X('dep')}+{X('acq')}",
        "rent": f"={S('yield')}/{S('qpy')}*{X('bbeg')}", "gains": f"={S('gain')}*{X('sold')}", "aum": f"={dq('aum', c)}",
        "fee": f"={S('feerate')}/{S('qpy')}*{x('aum', p)}", "prorata": f"={dq('prorata', c)}", "insur": f"={dq('insur', c)}",
        "leas": f"={X('rent')}+{X('gains')}+{X('fee')}+{X('prorata')}+{X('insur')}", "leasrev": f"={X('leas')}*{S('leasrev')}",
        "corp": f"={dq('corp', c)}", "elim": f"=-{S('elimp')}*{X('mre')}",
        "tot": f"={X('aero')}+{X('power')}+{X('leas')}+{X('corp')}+{X('elim')}", "seg": f"={X('aero')}+{X('power')}+{X('leas')}",
        "totrev": f"={X('aerorev')}+{X('powrev')}+{X('leasrev')}", "tmarg": f"={X('tot')}/{X('totrev')}",
        "b_ebitda": f"={X('tot')}", "da": f"={X('dep')}+{X('oda')}", "oda": f"={x('oda', p)}+{X('capex')}/({S('life')}*{S('qpy')})", "capex": f"={dq('capex', c)}",
        "int": f"={S('cpnint')}/{S('qpy')}+{S('othint')}+{x('rev', p)}*{S('revrate')}/{S('qpy')}",
        "adj": f"=-({X('prorata')}*(1-{S('eqconv')})+{S('othadj')}+(1-{S('ppre')})*{X('power')})",
        "pretax": f"={X('tot')}-{X('da')}-{X('int')}+{X('adj')}", "taxes": f"={X('pretax')}*{S('tax')}", "ni": f"={X('pretax')}-{X('taxes')}", "pnci": f"={S('pnci')}",
        "niattr": f"={X('ni')}-{X('pnci')}",
        "shares": (f"={S('shs')}-{BB_TERM()}" if c == "D" else f"={x('shares', p)}-{BB_TERM()}"), "eps": f"={X('niattr')}/{X('shares')}",
        "c_ebitda": f"={X('tot')}", "c_gain": f"=-({X('gains')}+{X('insur')})", "c_pro": f"=-{X('prorata')}", "c_dist": f"={S('dist')}*{X('prorata')}",
        "c_pow": f"=-(1-{S('pcash')})*{X('power')}", "c_int": f"=-{X('int')}", "c_tax": f"=-{X('taxes')}", "c_inv": f"=-({X('inv')}-{x('inv', p)})",
        "c_powinv": f"=-{S('pcost')}*{un}", "c_powrel": f"={S('pcost')}*{X('units')}", "c_sold": f"={X('sold')}", "c_acq": f"=-{X('acq')}",
        "c_coinv": f"=-{S('coinv')}*({X('aum')}-{x('aum', p)})", "c_capex": f"=-{X('capex')}", "c_insp": f"={X('insur')}",
        "total": f"=SUM({X('c_ebitda')}:{X('c_insp')})", "seed": f"={S('seedsh')}*{X('sold')}*(1+{S('gain')})", "insm": f"={X('insur')}",
        "clean": f"={X('total')}-{X('seed')}-{X('insm')}", "adjfcf": f"={X('total')}-{X('c_coinv')}+MAX(0,-({X('c_powinv')}+{X('c_powrel')}))+{S('hotp')}",
        "div": f"=-{S('dps')}*{X('shares')}", "pncic": f"=-{X('pnci')}", "bb": f"=-{S('bbtog')}*{S('bbamt')}/{S('bbq')}",
        "precash": f"={x('cash', p)}+{X('total')}+{X('div')}+{X('pncic')}+{X('bb')}", "revchg": f"=MAX(-{x('rev', p)},{S('mincash')}-{X('precash')})",
        "cash": f"={X('precash')}+{X('revchg')}", "rev": f"={x('rev', p)}+{X('revchg')}", "notes": f"={x('notes', p)}", "netdebt": f"={X('notes')}+{X('rev')}-{X('cash')}",
        "inv": f"={dq('days', c)}*{X('acogs')}/{S('dpq')}", "invd": f"={X('inv')}/{X('acogs')}*{S('dpq')}",
    }
    return m.get(key)


def build_quarterly(wb):
    ws = wb["Quarterly"]
    title(ws, "Quarterly model: Q1'26A, Q2'26A, Q3'26E - Q4'27E (8 quarters, 2 actual)",
          "Forecast cells are formulas on the Drivers tab (selected scenario). Actual columns link to Historical (green). USD m except per-share.")
    header_row(ws, 4, ["USD m", "Q1'26A", "Q2'26A", "Q3'26E", "Q4'26E", "Q1'27E", "Q2'27E", "Q3'27E", "Q4'27E", "FY2026E", "FY2027E", "Notes"])
    for rr, it in enumerate(LAYOUT):
        r = 5 + rr
        if it[0] == "sec":
            section(ws, r, it[1], 12)
            continue
        key, lab, fmt, bold = it
        label(ws, r, lab, bold=bold)
        for c in Q_ALL:
            f = quarterly_formula(key, c)
            if f is None:
                continue
            W(ws, f"{c}{r}", f, fmt=fmt, bold=bold)
        # FY columns
        for fc, (a, b) in (("J", ("B", "E")), ("K", ("F", "I"))):
            f = None
            if key in FY_SUM:
                if key == "oda" and fc == "J":
                    f = None
                else:
                    f = f"=SUM({a}{r}:{b}{r})"
            elif key in FY_LAST:
                f = f"={b}{r}"
            elif key == "bbeg":
                f = f"={a}{r}"
            elif key == "shares":
                f = f"=AVERAGE({a}{r}:{b}{r})"
            elif key == "invd":
                f = f"={fc}{LROW['inv']}/{fc}{LROW['acogs']}*{S('dpy')}"
            else:
                f = ratio_formula(key, fc)
            if f is not None:
                W(ws, f"{fc}{r}", f, fmt=fmt, bold=bold)
    notes = {
        "mod": "Q1'26 modules estimated (not disclosed)", "aero": "KEY #1. Mgmt FY27 1,400 / Base 1,230",
        "power": "KEY #3. 2026 = 0 (first units 'prudent to expect' 2027)", "bbeg": "Q2'26 ending book 1,146.4 is the 6/30/26 balance sheet",
        "seg": "Ties to guide: FY26 1,525 / FY27 2,300 in Mgmt Guide scenario", "adj": "Actual = reported pretax less (EBITDA - D&A - interest); calibration 1H26 on Drivers tab",
        "c_inv": "KEY #2: days-based inventory, driven by conversion %", "adjfcf": "Actual: Q1 158, Q2 97 (1H26 255) per company; forecast uses FY25-style add-backs",
        "clean": "Actual 1H26: 250.4 - 175.7 seed - 48.3 insurance = 26.4", "total": "Actual = reported CFO + CFI (Q1 157.0, Q2 93.5)",
        "shares": "Buyback toggle default OFF", "rev": "Revolver undrawn at 6/30/26", "eps": "Actual = reported diluted EPS",
    }
    for k, t in notes.items():
        ws[f"L{LROW[k]}"].value = t
        ws[f"L{LROW[k]}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    # back-test block
    r0 = LAST_ROW + 1
    section(ws, r0, "BACK-TEST of the EPS bridge on actual quarters (driver-based pretax vs reported)", 12)
    labels = ["Predicted pre-tax (EBITDA - D&A - interest - [pro-rata x (1 - equity conv.) + other adj.])", "Predicted net income attributable", "Predicted diluted EPS ($)",
              "Reported diluted EPS ($)", "Difference ($)"]
    for j, t in enumerate(labels):
        label(ws, r0 + 1 + j, t, bold=(j == 4))
    for c in ("B", "C"):
        W(ws, f"{c}{r0 + 1}", f"={x('tot', c)}-{x('da', c)}-{x('int', c)}-({x('prorata', c)}*(1-{S('eqconv')})+{S('othadj')})", fmt=F_NUM)
        W(ws, f"{c}{r0 + 2}", f"={c}{r0 + 1}*(1-{S('tax')})-{x('pnci', c)}", fmt=F_NUM)
        W(ws, f"{c}{r0 + 3}", f"={c}{r0 + 2}/{x('shares', c)}", fmt=F_USD)
        W(ws, f"{c}{r0 + 4}", f"={x('eps', c)}", fmt=F_USD)
        W(ws, f"{c}{r0 + 5}", f"={c}{r0 + 3}-{c}{r0 + 4}", fmt='$0.00;($0.00)', bold=True)
    ws[f"L{r0 + 1}"].value = "Pro-rata for Q1'26 is assumed equal to Q2'26 (components not disclosed). Calibrated on 1H26 combined, so each quarter is an out-of-sample test"
    ws[f"L{r0 + 1}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    global BT_ROW
    BT_ROW = r0
    setw(ws, {"A": 74, "L": 70, **{CL(i): 11 for i in range(2, 12)}})
    wrap_col(ws, "L", 70, 5, r0 + 5)
    setup_print(ws, r0 + 5, 12, freeze="B5")


BT_ROW = None

# ---------------------------------------------------------------- annual
A_COLS = ["B", "C", "D", "E", "F", "G", "H", "I"]
A_YEAR = {"B": "FY2023", "C": "FY2024", "D": "FY2025"}
A_DRV = {"G": "J", "H": "K", "I": "L"}


def annual_formula(key, c):
    i = A_COLS.index(c)
    p = A_COLS[i - 1] if i > 0 else None
    n = A_COLS[i + 1] if i + 1 < len(A_COLS) else None
    X = lambda k, col=c: x(k, col)
    if c in A_YEAR:
        hp = A_YEAR[c]
        m = {
            "aerorev": f"={hc('aerorev', hp)}", "mre": f"={hc('mre', hp)}" if c != "B" and c != "C" else None, "aero": f"={hc('e_aero', hp)}", "acogs": f"={hc('aerocogs', hp)}",
            "bend": f"={hc('leq', hp)}", "leas": f"={hc('e_leas', hp)}", "leasrev": f"={hc('leaserev', hp)}", "corp": f"={hc('e_corp', hp)}", "elim": f"={hc('e_elim', hp)}",
            "tot": f"={X('aero')}+{X('leas')}+{X('corp')}+{X('elim')}", "seg": f"={X('aero')}+{X('leas')}", "totrev": f"={hc('totrev', hp)}",
            "b_ebitda": f"={X('tot')}", "da": f"={hc('da', hp)}", "int": f"={hc('int', hp)}", "niattr": f"={hc('niattr', hp)}", "shares": f"={hc('shares', hp)}", "eps": f"={hc('eps', hp)}",
            "total": f"={hc('cfocfi', hp)}", "seed": f"={hc('seed', hp)}", "insm": f"={hc('insproc', hp)}", "clean": f"={X('total')}-N({X('seed')})-N({X('insm')})",
            "cash": f"={hc('cash', hp)}", "notes": f"={hc('debt', hp)}", "netdebt": f"={X('notes')}-{X('cash')}", "inv": f"={hc('inv', hp)}",
            "gains": f"={hc('g_tot', hp)}", "adjfcf": f"={hc('adjfcf', hp)}" if c == "D" else None,
        }
        if c == "D":
            m.update({"pretax": f"={hc('pretax', hp)}", "taxes": f"={hc('tax', hp)}", "ni": f"={hc('ni', hp)}", "pnci": f"={hc('prefnci', hp)}",
                      "adj": f"={X('pretax')}-({X('tot')}-{X('da')}-{X('int')})"})
        if key == "mre" and c in ("B", "C"):
            return None
        if key in m:
            return m[key]
        if key in ("revpm", "mrep", "epm", "amarg", "tmarg"):
            if key in ("mrep",) and c in ("B", "C"):
                return None
            if key in ("revpm", "epm"):
                return None
            return ratio_formula(key, c)
        if key == "invd":
            return f"={X('inv')}/{X('acogs')}*{S('dpy')}"
        return None
    if c in ("E", "F"):
        qa, qb = ("B", "E") if c == "E" else ("F", "I")
        if key in FY_SUM:
            if key == "oda" and c == "E":
                return None
            return f"=SUM(Quarterly!{qa}{LROW[key]}:{qb}{LROW[key]})"
        if key in FY_LAST:
            return f"=Quarterly!{qb}{LROW[key]}"
        if key == "bbeg":
            return f"=Quarterly!{qa}{LROW[key]}"
        if key == "shares":
            return f"=AVERAGE(Quarterly!{qa}{LROW[key]}:{qb}{LROW[key]})"
        if key == "invd":
            return f"={X('inv')}/{X('acogs')}*{S('dpy')}"
        if key in ("revpm", "mrep", "epm", "amarg", "tmarg", "eps"):
            return ratio_formula(key, c)
        return None
    # ---- FY28-30 projections
    dc = A_DRV[c]
    un = x("units", n) if n else x("units", c)
    face28, cpn28 = f"Drivers!$D${DRV['notes']['first']}", f"Drivers!$E${DRV['notes']['first']}"
    if c == "G":
        intf = (f"=({S('cpnint')}-{face28}*{cpn28})+{face28}*({cpn28}*{S('n28m')}+{S('refi')}*({S('mpy')}-{S('n28m')}))/{S('mpy')}+{S('othint')}*{S('qpy')}"
                f"+{x('rev', p)}*{S('revrate')}")
    else:
        intf = f"=({S('cpnint')}-{face28}*{cpn28})+{face28}*{S('refi')}+{S('othint')}*{S('qpy')}+{x('rev', p)}*{S('revrate')}"
    m = {
        "mod": f"={x('mod', p)}*(1+{dq('modg', dc)})", "revpm": f"={x('revpm', p)}*(1+{dq('revpmg', dc)})", "aerorev": f"={X('mod')}*{X('revpm')}",
        "mrep": f"={dq('mre', dc)}", "mre": f"={X('aerorev')}*{X('mrep')}",
        "amarg": f"=MIN({dq('acap', 'D')},{x('amarg', p)}+{S('aelast')}*{dq('modg', dc)})", "aero": f"={X('aerorev')}*{X('amarg')}", "epm": f"={X('aero')}/{X('mod')}",
        "acogs": f"={X('aerorev')}-{X('aero')}",
        "units": f"={dq('units', dc)}", "epu": f"={dq('epu', dc)}", "power": f"={X('units')}*{X('epu')}", "powrev": f"={X('units')}*{S('pprice')}",
        "bbeg": f"={x('bend', p)}", "sold": f"={dq('sold', dc)}", "dep": f"={S('deprate')}*{S('qpy')}*{X('bbeg')}", "acq": f"={dq('acq', dc)}",
        "bend": f"={X('bbeg')}-{X('sold')}-{X('dep')}+{X('acq')}", "gains": f"={S('gain')}*{X('sold')}", "aum": f"={dq('aum', dc)}",
        "prorata": f"={X('leas')}*{x('prorata', p)}/{x('leas', p)}", "leas": f"={x('leas', p)}*(1+{dq('lgrow', dc)})", "leasrev": f"={X('leas')}*{S('leasrev')}",
        "corp": f"={x('corp', p)}*(1+{dq('corp', dc)})", "elim": f"=-{S('elimp')}*{X('mre')}",
        "tot": f"={X('aero')}+{X('power')}+{X('leas')}+{X('corp')}+{X('elim')}", "seg": f"={X('aero')}+{X('power')}+{X('leas')}",
        "totrev": f"={X('aerorev')}+{X('powrev')}+{X('leasrev')}", "tmarg": f"={X('tot')}/{X('totrev')}",
        "b_ebitda": f"={X('tot')}", "da": f"={X('dep')}+{X('oda')}", "oda": f"={x('oda', p)}+{X('capex')}/{S('life')}", "capex": f"={dq('capex', dc)}",
        "int": intf, "adj": f"=-({X('prorata')}*(1-{S('eqconv')})+{S('othadj')}*{S('qpy')}+(1-{S('ppre')})*{X('power')})",
        "pretax": f"={X('tot')}-{X('da')}-{X('int')}+{X('adj')}", "taxes": f"={X('pretax')}*{S('tax')}", "ni": f"={X('pretax')}-{X('taxes')}",
        "pnci": f"={S('pnci')}*{S('qpy')}", "niattr": f"={X('ni')}-{X('pnci')}", "shares": (f"=Quarterly!I{LROW['shares']}" if c == "G" else f"={x('shares', p)}"),
        "eps": f"={X('niattr')}/{X('shares')}",
        "c_ebitda": f"={X('tot')}", "c_gain": f"=-{X('gains')}", "c_pro": f"=-{X('prorata')}", "c_dist": f"={S('dist')}*{X('prorata')}",
        "c_pow": f"=-(1-{S('pcash')})*{X('power')}", "c_int": f"=-{X('int')}", "c_tax": f"=-{X('taxes')}", "c_inv": f"=-({X('inv')}-{x('inv', p)})",
        "c_powinv": f"=-{S('pcost')}*{un}", "c_powrel": f"={S('pcost')}*{X('units')}", "c_sold": f"={X('sold')}", "c_acq": f"=-{X('acq')}",
        "c_coinv": f"=-{S('coinv')}*({X('aum')}-{x('aum', p)})", "c_capex": f"=-{X('capex')}",
        "total": f"=SUM({X('c_ebitda')}:{X('c_insp')})", "seed": f"={S('seedsh')}*{X('sold')}*(1+{S('gain')})",
        "clean": f"={X('total')}-N({X('seed')})-N({X('insm')})", "adjfcf": f"={X('total')}-{X('c_coinv')}+MAX(0,-({X('c_powinv')}+{X('c_powrel')}))+{S('hotp')}*{S('qpy')}",
        "div": f"=-{S('dps')}*{S('qpy')}*{X('shares')}", "pncic": f"=-{X('pnci')}",
        "precash": f"={x('cash', p)}+{X('total')}+{X('div')}+{X('pncic')}", "revchg": f"=MAX(-{x('rev', p)},{S('mincash')}-{X('precash')})",
        "cash": f"={X('precash')}+{X('revchg')}", "rev": f"={x('rev', p)}+{X('revchg')}", "notes": f"={x('notes', p)}", "netdebt": f"={X('notes')}+{X('rev')}-{X('cash')}",
        "invd": (f"={x('invd', p)}+{dq('daych', dc)}"), "inv": f"={X('invd')}*{X('acogs')}/{S('dpy')}",
    }
    return m.get(key)


def build_annual(wb):
    ws = wb["Annual"]
    title(ws, "Annual model: FY2023A - FY2025A history, FY2026E - FY2030E projections (5 years)",
          "FY26 and FY27 are summed from Quarterly; FY28-FY30 are driven by annual growth, margin-scale (capped) and unit drivers on the Drivers tab. USD m except per-share.")
    header_row(ws, 4, ["USD m", "FY2023A", "FY2024A", "FY2025A", "FY2026E", "FY2027E", "FY2028E", "FY2029E", "FY2030E", "Notes"])
    for rr, it in enumerate(LAYOUT):
        r = 5 + rr
        if it[0] == "sec":
            section(ws, r, it[1], 10)
            continue
        key, lab, fmt, bold = it
        label(ws, r, lab, bold=bold)
        for c in A_COLS:
            f = annual_formula(key, c)
            if f is None:
                continue
            W(ws, f"{c}{r}", f, fmt=fmt, bold=bold)
    notes = {"amarg": "FY28+: margin = MIN(cap, prior + elasticity x volume growth): economies of scale up to a cap",
             "aero": "FY26/27 = sum of Quarterly. History: segment Adj. EBITDA", "seg": "FY26 guide 1,525; FY27 guide 2,300",
             "int": "FY28: 2028 notes ($1.0B, 5.5%) mature 5/1/28 and are refinanced at the refi coupon",
             "adjfcf": "FY25 reported 724 vs CFO+CFI 412.6 (see FCF_Quality). FY26 = model (1H26 reported 255 + 2H26 model: see FCF_Quality)",
             "total": "History: reported CFO + CFI. Projection: model build (no financing lines)", "pretax": "History FY23/FY24 not parsed"}
    for k, t in notes.items():
        ws[f"J{LROW[k]}"].value = t
        ws[f"J{LROW[k]}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    setw(ws, {"A": 74, "J": 70, **{CL(i): 11 for i in range(2, 10)}})
    wrap_col(ws, "J", 70, 5, LAST_ROW)
    setup_print(ws, LAST_ROW, 10, freeze="B5")


# ================================================================= FCF_QUALITY
FQ = {}


def build_fcf_quality(wb):
    ws = wb["FCF_Quality"]
    title(ws, "FCF quality: the thesis tab (three ways to count cash)",
          "(a) company 'Adjusted FCF'; (b) GAAP CFO + CFI; (c) clean CFO + CFI excluding seed-sale proceeds and insurance recoveries. Projection columns follow the selected scenario.")
    header_row(ws, 4, ["USD m", "FY2023A", "FY2024A", "FY2025A", "FY2026E", "FY2027E", "FY2028E", "FY2029E", "FY2030E", "Notes"])
    r = 5
    section(ws, r, "Three definitions by year", 10)
    r += 1
    rows = {}

    def line(key, text, fmt=F_NUM, bold=False):
        nonlocal r
        rows[key] = r
        label(ws, r, text, bold=bold)
        r += 1
        return rows[key]

    line("cfo", "Reported CFO (history) / n.a. in projections (model builds CFO + CFI combined)")
    line("cfi", "Reported CFI (history)")
    line("b", "(b) GAAP CFO + CFI", bold=True)
    line("seed", "  less: seed-sale proceeds to 2025 Partnership / SCI")
    line("ins", "  less: insurance proceeds (Russia)")
    line("c", "(c) Clean CFO + CFI", bold=True)
    line("a", "(a) Company-defined Adjusted FCF", bold=True)
    line("gap", "Gap: (a) less (b) = add-backs of growth investment")
    line("gapc", "Gap: (a) less (c)")
    line("ebitda", "Total Adjusted EBITDA (company basis)")
    line("k_b", "(b) / Adjusted EBITDA", fmt=F_PCT)
    line("k_c", "(c) / Adjusted EBITDA", fmt=F_PCT)
    line("k_a", "(a) / Adjusted EBITDA", fmt=F_PCT)
    line("yield_a", "(a) yield on market cap", fmt=F_PCT)
    line("yield_c", "(c) yield on market cap", fmt=F_PCT)
    for c, p in zip("BCDEFGHI", ["FY2023", "FY2024", "FY2025", None, None, None, None, None]):
        a = lambda k: f"Annual!{c}{LROW[k]}"
        if p:
            W(ws, f"{c}{rows['cfo']}", f"={hc('cfo', p)}", fmt=F_NUM)
            W(ws, f"{c}{rows['cfi']}", f"={hc('cfi', p)}", fmt=F_NUM)
        W(ws, f"{c}{rows['b']}", f"={a('total')}", fmt=F_NUM, bold=True)
        W(ws, f"{c}{rows['seed']}", f"=-N({a('seed')})", fmt=F_NUM)
        W(ws, f"{c}{rows['ins']}", f"=-N({a('insm')})", fmt=F_NUM)
        W(ws, f"{c}{rows['c']}", f"={c}{rows['b']}+{c}{rows['seed']}+{c}{rows['ins']}", fmt=F_NUM, bold=True)
        if c not in "BC":
            W(ws, f"{c}{rows['a']}", f"={a('adjfcf')}", fmt=F_NUM, bold=True)
            W(ws, f"{c}{rows['gap']}", f"={c}{rows['a']}-{c}{rows['b']}", fmt=F_NUM)
            W(ws, f"{c}{rows['gapc']}", f"={c}{rows['a']}-{c}{rows['c']}", fmt=F_NUM)
            W(ws, f"{c}{rows['k_a']}", f"={c}{rows['a']}/{c}{rows['ebitda']}", fmt=F_PCT)
            W(ws, f"{c}{rows['yield_a']}", f"={c}{rows['a']}/{S('mcap')}", fmt=F_PCT)
        W(ws, f"{c}{rows['ebitda']}", f"={a('tot')}", fmt=F_NUM)
        W(ws, f"{c}{rows['k_b']}", f"={c}{rows['b']}/{c}{rows['ebitda']}", fmt=F_PCT)
        W(ws, f"{c}{rows['k_c']}", f"={c}{rows['c']}/{c}{rows['ebitda']}", fmt=F_PCT)
        W(ws, f"{c}{rows['yield_c']}", f"={c}{rows['c']}/{S('mcap')}", fmt=F_PCT)
    ws[f"J{rows['a']}"].value = "FY25 724 reported (call). FY26 = 1H26 reported 255 + 2H26 model on FY25-style add-backs"
    ws[f"J{rows['b']}"].value = "FY25 CFO -310.7 and CFI +723.3 tie to filings"
    ws[f"J{rows['yield_a']}"].value = "Management guide 878 / market cap 18,430 = 4.8% (vs peers 2.4-3.3%)"
    for k in ("a", "b", "yield_a"):
        ws[f"J{rows[k]}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    r += 1
    # ---- SCI gap
    section(ws, r, "SCI: pro-rata EBITDA counted in Adj. EBITDA vs cash actually distributed", 10)
    r += 1
    rows["sci_pro"] = r
    label(ws, r, "Pro-rata SCI EBITDA and co-invest returns (non-cash)")
    r += 1
    rows["sci_dist"] = r
    label(ws, r, "Cash distributions from SCI (return of capital, CFI)")
    r += 1
    rows["sci_gap"] = r
    label(ws, r, "Gap: EBITDA counted but not received in cash", bold=True)
    r += 1
    rows["sci_pct"] = r
    label(ws, r, "Cash distributions as % of pro-rata EBITDA")
    r += 1
    for c in "DEFGHI":
        if c == "D":
            W(ws, f"D{rows['sci_dist']}", f"={hc('roc', 'FY2025')}", fmt=F_NUM)
            ws[f"J{rows['sci_dist']}"].value = "FY25 27.1 'return of capital' (carried from prior research). Pro-rata EBITDA for FY25 not disclosed by component"
            ws[f"J{rows['sci_dist']}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
            continue
        W(ws, f"{c}{rows['sci_pro']}", f"=Annual!{c}{LROW['prorata']}", fmt=F_NUM)
        W(ws, f"{c}{rows['sci_dist']}", f"=Annual!{c}{LROW['c_dist']}" if c not in "E" else f"={hc('roc', 'Q1-2026')}+{hc('roc', 'Q2-2026')}+SUM(Quarterly!D{LROW['c_dist']}:E{LROW['c_dist']})", fmt=F_NUM)
        W(ws, f"{c}{rows['sci_gap']}", f"={c}{rows['sci_pro']}-{c}{rows['sci_dist']}", fmt=F_NUM, bold=True)
        W(ws, f"{c}{rows['sci_pct']}", f"={c}{rows['sci_dist']}/{c}{rows['sci_pro']}", fmt=F_PCT)
    ws[f"J{rows['sci_pro']}"].value = "FY26 includes 1H26 assumed 28.0/qtr (call 35 less 7.0 fees)"
    ws[f"J{rows['sci_pro']}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    W(ws, f"E{rows['sci_pro']}", f"=Annual!E{LROW['prorata']}", fmt=F_NUM)
    r += 1
    # ---- FY25 reconciliation
    section(ws, r, "FY25 reconciliation: $724M Adjusted FCF to $412.6M CFO + CFI", 10)
    r += 1
    rec = {}

    def rl(key, text, v, fmt=F_NUM, src="", bold=False, comment=None):
        nonlocal r
        rec[key] = r
        label(ws, r, text, bold=bold)
        W(ws, f"B{r}", v, fmt=fmt, bold=bold, comment=comment)
        ws[f"J{r}"].value = src
        ws[f"J{r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
        r += 1

    rl("adj", "Company Adjusted FCF, FY25", f"={hc('adjfcf', 'FY2025')}", src="Q4-25 call (Motley Fool transcript 2026-02-26), secondary")
    rl("cfocfi", "less: GAAP CFO + CFI", f"=-{hc('cfocfi', 'FY2025')}", src="CFO -310.7 + CFI +723.3 (10-K FY25)")
    rl("gap", "Gap to explain", f"=B{rec['adj']}+B{rec['cfocfi']}", bold=True)
    rl("sci", "  named by CFO: increase in SCI co-investment", 52.0, src="Q4-25 call: 'further adjusted for 3 key investments'")
    rl("pow", "  named by CFO: Power turbines", 150.0, src="Q4-25 call")
    rl("parts", "  named by CFO: hot-section parts", 50.0, src="Q4-25 call")
    rl("named", "  subtotal named by the CFO", f"=SUM(B{rec['sci']}:B{rec['parts']})", bold=True)
    rl("resid", "  residual: INFERRED (probably acquisitions 49.1 + ~10 JV item), NOT CONFIRMED", f"=B{rec['gap']}-B{rec['named']}", bold=True,
       comment="Inferred, not confirmed. Candidates: $49.1M acquisition of business line plus a ~$10M JV item (data notes gap #2). Investor-deck check timed out.")
    ws[f"A{rec['resid']}"].font = Font(name="Calibri", size=10, bold=True, color=RED)
    rl("addb", "  of the gap, inventory-type purchases (Power turbines + hot-section parts)", f"=B{rec['pow']}+B{rec['parts']}", src="~$200M of the add-backs are the same inventory-type items that drive negative GAAP CFO")
    r += 1
    # ---- 1H26
    section(ws, r, "1H26: what cash looks like without the one-offs", 10)
    r += 1
    h = {}

    def hl(key, text, f, fmt=F_NUM, src="", bold=False):
        nonlocal r
        h[key] = r
        label(ws, r, text, bold=bold)
        W(ws, f"B{r}", f, fmt=fmt, bold=bold)
        ws[f"J{r}"].value = src
        ws[f"J{r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
        r += 1

    hl("cfo", "1H26 CFO", f"={hc('cfo', 'Q1-2026')}+{hc('cfo', 'Q2-2026')}", src="-160.1 + -105.2 = -265.3")
    hl("cfi", "1H26 CFI", f"={hc('cfi', 'Q1-2026')}+{hc('cfi', 'Q2-2026')}", src="317.0 + 198.7 = 515.7")
    hl("tot", "1H26 CFO + CFI", f"=B{r - 2}+B{r - 1}", bold=True, src="250.4")
    hl("seed", "  less: seed-sale proceeds (15 aircraft to 2025 Partnership)", f"=-({hc('seed', 'Q1-2026')}+{hc('seed', 'Q2-2026')})", src="175.7; 10-Q: sales 'non-recurring in nature'")
    hl("ins", "  less: Russia insurance proceeds", f"=-({hc('insproc', 'Q1-2026')}+{hc('insproc', 'Q2-2026')})", src="48.3 (CFI proceeds, not the CFO gain add-back of 49.5)")
    hl("clean", "1H26 clean CFO + CFI", f"=B{h['tot']}+B{h['seed']}+B{h['ins']}", bold=True, src="~26.4, AFTER the inventory build below")
    hl("invb", "memo: inventory build 1H26 (balance sheet)", f"={hc('inv', 'Q2-2026')}-{hc('inv', 'Q4-2025')}", src="1,544.6 - 1,193.8 = 350.8. Includes 63 engines transferred in from leasing (non-cash)")
    hl("adj", "Company-reported Adjusted FCF, 1H26", 255.0, src="Q2-26 call (secondary): 255; Q1 158")
    hl("adjgap", "  Adjusted FCF less CFO + CFI in 1H26 (add-backs actually applied)", f"=B{h['adj']}-B{h['tot']}", src="Only ~4.6 in 1H26 despite ~99 of SCI investment: the add-back definition is NOT consistent with FY25's")
    hl("guide", "FY26 Adjusted FCF guide (cut from 915 on 7/29/26)", 878.0, src="Q2-26 call (secondary)")
    hl("need", "2H26 Adjusted FCF required to hit the guide", f"=B{h['guide']}-B{h['adj']}", bold=True, src="~623")
    hl("q2rr", "Q2'26 Adjusted FCF run-rate x 2", f"={S('nq')}*{hc('adjfcf', 'Q2-2026')}", src="~194: the guide needs ~3.2x the Q2 run-rate")
    hl("mult", "Required / run-rate", f"=B{h['need']}/B{h['q2rr']}", fmt='0.0"x"')
    hl("m_adj", "Model 2H26: company-defined Adjusted FCF (FY25-style add-backs)  [selected scenario]", f"=SUM(Quarterly!D{LROW['adjfcf']}:E{LROW['adjfcf']})", bold=True,
       src="Back-solved to hit 878 in the Mgmt Guide scenario via KEY #2 (inventory conversion)")
    hl("m_b", "Model 2H26: GAAP CFO + CFI  [selected scenario]", f"=SUM(Quarterly!D{LROW['total']}:E{LROW['total']})", src="Compare with the 623 required: on the narrow 1H26-style definition (add-backs ~5) the guide needs ~619-623 of GAAP CFO + CFI in 2H")
    hl("m_c", "Model 2H26: clean CFO + CFI  [selected scenario]", f"=SUM(Quarterly!D{LROW['clean']}:E{LROW['clean']})")
    hl("narrow", "2H26 GAAP CFO + CFI required if add-backs stay at the 1H26 level", f"=B{h['guide']}-B{h['adjgap']}-B{h['tot']}", bold=True, src="Narrow basis: 878 less 4.6 less 250.4 = ~623")
    FQ.update(rows=rows, rec=rec, h=h)
    setw(ws, {"A": 82, "J": 80, **{CL(i): 11 for i in range(2, 10)}})
    wrap_col(ws, "J", 80, 5, r)
    setup_print(ws, r, 10, freeze="B5")


# ================================================================= VALUATION
VAL = {}
PEERS = [("HEICO", 30.2, 44.0, 0.024), ("AAR", 13.8, 17.7, 0.033), ("StandardAero", 11.7, 15.9, 0.032), ("AerSale", 17.4, 18.1, -0.167),
         ("AerCap", 12.4, 8.5, -0.014), ("FTAI (at $179.44)", 21.7, 20.2, None)]
SNAP_KEYS = [("fy26", "FY26E segment-basis EBITDA ($M)", F_NUM), ("fy27", "FY27E segment-basis EBITDA ($M)", F_NUM), ("tot27", "FY27E total Adj. EBITDA, company basis ($M)", F_NUM),
             ("eps26", "FY26E diluted EPS ($)", F_USD), ("eps27", "FY27E diluted EPS ($)", F_USD), ("sotp", "SOTP value per share ($)", F_USD),
             ("pe", "P/E value per share, midpoint multiple ($)", F_USD), ("dcf", "DCF value per share ($)", F_USD), ("blend", "Blended value per share ($)", F_USD),
             ("adj26", "FY26E company-defined Adjusted FCF ($M)", F_NUM), ("clean26", "FY26E clean CFO + CFI ($M)", F_NUM), ("clean27", "FY27E clean CFO + CFI ($M)", F_NUM)]


def build_valuation(wb, snapshot=None):
    ws = wb["Valuation"]
    title(ws, "Valuation: SOTP, P/E cross-check, DCF, blended price target",
          "SOTP is live for all four scenarios (Leasing at book). P/E, DCF and blended are live for the SELECTED scenario; the snapshot block stores all four (regenerated by build_model.py).")
    r = 4
    section(ws, r, "1. Market data and equity bridge", 8)
    r += 1
    md = {}

    def ml(key, text, f, fmt=F_NUM, src=""):
        nonlocal r
        md[key] = r
        label(ws, r, text)
        W(ws, f"B{r}", f, fmt=fmt)
        ws[f"G{r}"].value = src
        ws[f"G{r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
        r += 1

    ml("price", "Share price 10/6/26 ($)", f"={S('price')}", F_USD)
    ml("sh", "Shares (M)", f"={S('vsh')}", F_3)
    ml("mcap", "Market cap (stockanalysis)", f"={S('mcap')}", F_NUM0)
    ml("ev", "Enterprise value (stockanalysis)", f"={S('evsa')}", F_NUM0)
    ml("ndsa", "Net debt per stockanalysis (EV - market cap)", f"={S('ndsa')}")
    ml("ndbs", "Net debt per balance sheet 6/30/26 (debt 3,496.4 - cash 337.2)", f"={S('ndbs')}", src="Used in all bridges")
    ml("recon", "Reconciliation difference", f"=B{r - 1}-B{r - 2}", src="Within ~1: stockanalysis uses face debt 3,500")
    ml("pref", "Preferred at liquidation (deducted)", f"={S('prefon')}*{S('prefliq')}")
    ml("book", "Leasing book: equipment net 1,146.4 + SCI I stake 365.5", f"={S('book')}")
    r += 1
    section(ws, r, "2. Sum-of-the-parts on 2027E (TTM peer multiples applied to 2027E: 2027 is the trailing year at a 12-month horizon)", 8)
    r += 1
    header_row(ws, r, ["USD m"] + SCEN + ["Selected", "Notes"])
    r += 1
    so = {}
    names = [("a27", "2027E Aerospace EBITDA"), ("ma", "  x multiple"), ("eva", "Aerospace EV"), ("p27", "2027E Power EBITDA (pro-rata)"), ("mp", "  x multiple"), ("evp", "Power EV"),
             ("bk", "Leasing book value"), ("ml", "  x book multiple"), ("evl", "Leasing value"), ("corp", "Corporate costs capitalised (2027E x blended multiple)"), ("ev", "Enterprise value"),
             ("nd", "less: net debt"), ("pf", "less: preferred"), ("eq", "Equity value"), ("ps", "SOTP value per share ($)"), ("tgt", "Spec / thesis target ($)"), ("dev", "Difference vs target ($)"),
             ("up", "Upside vs current price")]
    for k, t in names:
        so[k] = r
        label(ws, r, t, bold=k in ("ev", "eq", "ps"))
        r += 1
    for i in range(4):
        c = CL(2 + i)
        W(ws, f"{c}{so['a27']}", f"={sumcell('a27', i)}", fmt=F_NUM)
        W(ws, f"{c}{so['ma']}", f"={dsc('mult_a', i, 'D')}", fmt=F_X)
        W(ws, f"{c}{so['eva']}", f"={c}{so['a27']}*{c}{so['ma']}", fmt=F_NUM)
        W(ws, f"{c}{so['p27']}", f"={sumcell('p27', i)}", fmt=F_NUM)
        W(ws, f"{c}{so['mp']}", f"={dsc('mult_p', i, 'D')}", fmt=F_X)
        W(ws, f"{c}{so['evp']}", f"={c}{so['p27']}*{c}{so['mp']}", fmt=F_NUM)
        W(ws, f"{c}{so['bk']}", f"={S('book')}", fmt=F_NUM)
        W(ws, f"{c}{so['ml']}", f"={dsc('mult_l', i, 'D')}", fmt='0.00"x"')
        W(ws, f"{c}{so['evl']}", f"={c}{so['bk']}*{c}{so['ml']}", fmt=F_NUM)
        W(ws, f"{c}{so['corp']}", f"={S('corpcap')}*SUM(Drivers!F${DRV['corp']['live']}:I${DRV['corp']['live']})*{c}{so['up']+1}", fmt=F_NUM)
        W(ws, f"{c}{so['ev']}", f"={c}{so['eva']}+{c}{so['evp']}+{c}{so['evl']}+{c}{so['corp']}", fmt=F_NUM, bold=True)
        W(ws, f"{c}{so['nd']}", f"=-{S('ndbs')}", fmt=F_NUM)
        W(ws, f"{c}{so['pf']}", f"=-{S('prefon')}*{S('prefliq')}", fmt=F_NUM)
        W(ws, f"{c}{so['eq']}", f"={c}{so['ev']}+{c}{so['nd']}+{c}{so['pf']}", fmt=F_NUM, bold=True)
        W(ws, f"{c}{so['ps']}", f"={c}{so['eq']}/{S('vsh')}", fmt=F_USD, bold=True)
        W(ws, f"{c}{so['up']}", f"={c}{so['ps']}/{S('price')}-1", fmt=F_PCT)
    for i, t in enumerate([115, 172, 280]):
        c = CL(2 + i)
        W(ws, f"{c}{so['tgt']}", t, fmt=F_USD)
        W(ws, f"{c}{so['dev']}", f"={c}{so['up']+2}-{c}{so['tgt']}", fmt='$0.00;($0.00)')
    ws[f"G{so['tgt']}"].value = "thesis.md section 2 (Bear ~115, Base ~172, Bull ~280); thesis excludes preferred and uses book ~1.5B"
    for k in so:
        W(ws, f"F{so[k]}", f"=INDEX(B{so[k]}:E{so[k]},{'Drivers!$E$4'})", fmt=ws[f"B{so[k]}"].number_format, bold=k in ("ev", "eq", "ps")) if k not in ("tgt", "dev") else None
    ws[f"G{so['corp']}"].value = "2027E corporate costs x blended Aero+Power multiple (memo row below)"
    ws[f"G{so['ml']}"].value = "Leasing valued at book because the book is being sold down and EBITDA is gain-heavy"
    for k in ("corp", "ml", "tgt"):
        ws[f"G{so[k]}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    label(ws, r, "Memo: blended Aero+Power multiple")
    so["bm"] = r
    for i in range(4):
        c = CL(2 + i)
        W(ws, f"{c}{r}", f"=({c}{so['eva']}+{c}{so['evp']})/({c}{so['a27']}+{c}{so['p27']})", fmt=F_X)
    r += 1
    label(ws, r, "Memo: SOTP value/share EXCLUDING corporate costs (ties to thesis.md v0.2 targets) ($)")
    so["cm"] = r
    for i in range(4):
        c = CL(2 + i)
        W(ws, f"{c}{r}", f"={c}{so['ps']}-{c}{so['corp']}/{S('vsh')}", fmt=F_USD)
    ws[f"G{r}"].value = "Headline SOTP includes corporate costs. This memo excludes them, for comparison with the thesis.md v0.2 targets"
    ws[f"G{r}"].font = Font(name="Calibri", size=8, italic=True, color=RED)
    r += 2
    # ---- P/E
    section(ws, r, "3. Forward P/E cross-check (selected scenario)", 8)
    r += 1
    pe = {}
    for k, t in [("eps", "Model FY2027E diluted EPS ($)"), ("lo", "  at low P/E"), ("mid", "  at midpoint P/E"), ("hi", "  at high P/E"), ("ceps", "Consensus FY2027E EPS implied (price / 20.2x) ($)"),
                 ("clo", "  consensus at low P/E ($)"), ("chi", "  consensus at high P/E ($)"), ("gap", "Model EPS vs consensus-implied")]:
        pe[k] = r
        label(ws, r, t, bold=k in ("eps", "mid"))
        r += 1
    W(ws, f"B{pe['eps']}", f"=Annual!F{LROW['eps']}", fmt=F_USD, bold=True)
    W(ws, f"B{pe['lo']}", f"=B{pe['eps']}*{S('pelo')}", fmt=F_USD)
    W(ws, f"B{pe['mid']}", f"=B{pe['eps']}*AVERAGE({S('pelo')},{S('pehi')})", fmt=F_USD, bold=True)
    W(ws, f"B{pe['hi']}", f"=B{pe['eps']}*{S('pehi')}", fmt=F_USD)
    W(ws, f"B{pe['ceps']}", f"={S('consfy27')}", fmt=F_USD)
    W(ws, f"B{pe['clo']}", f"=B{pe['ceps']}*{S('pelo')}", fmt=F_USD)
    W(ws, f"B{pe['chi']}", f"=B{pe['ceps']}*{S('pehi')}", fmt=F_USD)
    W(ws, f"B{pe['gap']}", f"=B{pe['eps']}/B{pe['ceps']}-1", fmt=F_PCT)
    ws[f"G{pe['ceps']}"].value = "CAVEAT: stockanalysis forward P/E 20.2x conflicts with its own FY26 EPS (30.8x); the $8.87 is an implied, not published, figure"
    ws[f"G{pe['ceps']}"].font = Font(name="Calibri", size=8, italic=True, color=RED)
    r += 1
    # ---- DCF
    section(ws, r, "4. DCF on clean FCF (selected scenario). Valuation date 6/30/26 balance sheet; mid-period discounting", 8)
    r += 1
    header_row(ws, r, ["USD m", "2H FY2026E", "FY2027E", "FY2028E", "FY2029E", "FY2030E", "Terminal"])
    r += 1
    dc = {}
    for k, t in [("clean", "Clean CFO + CFI (after interest)"), ("int", "  plus: interest expense"), ("atint", "  plus: after-tax interest add-back = interest x (1 - tax)"), ("ufcf", "Unlevered clean FCF"),
                 ("norm", "Terminal normalisation (see note)"), ("t", "Discount period (years from 6/30/26, mid-period)"), ("df", "Discount factor"), ("pv", "Present value")]:
        dc[k] = r
        label(ws, r, t, bold=k in ("ufcf", "pv"))
        r += 1
    W(ws, f"B{dc['clean']}", f"=SUM(Quarterly!D{LROW['clean']}:E{LROW['clean']})", fmt=F_NUM)
    W(ws, f"B{dc['int']}", f"=SUM(Quarterly!D{LROW['int']}:E{LROW['int']})", fmt=F_NUM)
    for c, ac in zip("CDEF", "FGHI"):
        W(ws, f"{c}{dc['clean']}", f"=Annual!{ac}{LROW['clean']}", fmt=F_NUM)
        W(ws, f"{c}{dc['int']}", f"=Annual!{ac}{LROW['int']}", fmt=F_NUM)
    for c in "BCDEF":
        W(ws, f"{c}{dc['atint']}", f"={c}{dc['int']}*(1-{S('tax')})", fmt=F_NUM)
        W(ws, f"{c}{dc['ufcf']}", f"={c}{dc['clean']}+{c}{dc['atint']}", fmt=F_NUM, bold=True)
        W(ws, f"{c}{dc['df']}", f"=1/(1+{S('wacc')})^{c}{dc['t']}", fmt="0.000")
    for c, t in zip("BCDEFG", [0.25, 1.0, 2.0, 3.0, 4.0, 4.5]):
        W(ws, f"{c}{dc['t']}", t, fmt="0.00")
    ws[f"H{dc['t']}"].value = "ASSUMPTION: 2H26 cash mid-point 0.25y; FY27 mid-year 1.0y ... FY30 4.0y; terminal at end FY30 (4.5y)"
    ws[f"H{dc['t']}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    # terminal
    W(ws, f"G{dc['norm']}", f"=F{dc['ufcf']}-Annual!I{LROW['c_inv']}-Annual!I{LROW['c_powinv']}-Annual!I{LROW['c_powrel']}-{S('tg')}*Annual!I{LROW['inv']}", fmt=F_NUM)
    ws[f"H{dc['norm']}"].value = ("Fixed before viewing output: terminal FCF = FY30 unlevered FCF with the FY30 inventory change replaced by a growth-consistent build (g x inventory) "
                                  "and Power WC net set to zero (flat units)")
    ws[f"H{dc['norm']}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    W(ws, f"G{dc['ufcf']}", f"=G{dc['norm']}*(1+{S('tg')})/({S('wacc')}-{S('tg')})", fmt=F_NUM, bold=True)
    ws[f"H{dc['ufcf']}"].value = "Terminal value = normalised FCF x (1+g) / (WACC - g)"
    ws[f"H{dc['ufcf']}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    W(ws, f"G{dc['df']}", f"=1/(1+{S('wacc')})^G{dc['t']}", fmt="0.000")
    W(ws, f"G{dc['pv']}", f"=G{dc['ufcf']}*G{dc['df']}", fmt=F_NUM, bold=True)
    for c in "BCDEF":
        W(ws, f"{c}{dc['pv']}", f"={c}{dc['ufcf']}*{c}{dc['df']}", fmt=F_NUM, bold=True)
    r += 1
    for k, t in [("ev", "DCF enterprise value"), ("tvp", "  terminal value share of EV"), ("nd", "less: net debt (6/30/26)"), ("pf", "less: preferred"), ("eq", "DCF equity value"), ("ps", "DCF value per share ($)")]:
        dc[k] = r
        label(ws, r, t, bold=k in ("ev", "ps"))
        r += 1
    W(ws, f"B{dc['ev']}", f"=SUM(B{dc['pv']}:G{dc['pv']})", fmt=F_NUM, bold=True)
    W(ws, f"B{dc['tvp']}", f"=G{dc['pv']}/B{dc['ev']}", fmt=F_PCT)
    W(ws, f"B{dc['nd']}", f"=-{S('ndbs')}", fmt=F_NUM)
    W(ws, f"B{dc['pf']}", f"=-{S('prefon')}*{S('prefliq')}", fmt=F_NUM)
    W(ws, f"B{dc['eq']}", f"=B{dc['ev']}+B{dc['nd']}+B{dc['pf']}", fmt=F_NUM)
    W(ws, f"B{dc['ps']}", f"=B{dc['eq']}/{S('vsh')}", fmt=F_USD, bold=True)
    r += 1
    # ---- blended
    section(ws, r, "5. Blended price target (selected scenario)", 8)
    r += 1
    header_row(ws, r, ["Method", "Value / share", "Weight", "Contribution"])
    r += 1
    bl = {}
    for k, t, v, w in [("sotp", "SOTP", f"=F{so['ps']}", S("w_sotp")), ("pe", "P/E at midpoint multiple", f"=B{pe['mid']}", S("w_pe")), ("dcf", "DCF", f"=B{dc['ps']}", S("w_dcf"))]:
        bl[k] = r
        label(ws, r, t)
        W(ws, f"B{r}", v, fmt=F_USD)
        W(ws, f"C{r}", f"={w}", fmt=F_PCT)
        W(ws, f"D{r}", f"=B{r}*C{r}", fmt=F_USD)
        r += 1
    bl["blend"] = r
    label(ws, r, "Blended value per share ($)", bold=True)
    W(ws, f"C{r}", f"=SUM(C{bl['sotp']}:C{bl['dcf']})", fmt=F_PCT)
    W(ws, f"D{r}", f"=SUM(D{bl['sotp']}:D{bl['dcf']})/C{r}", fmt=F_USD, bold=True)
    r += 1
    bl["up"] = r
    label(ws, r, "Upside / (downside) vs current price")
    W(ws, f"D{r}", f"=D{bl['blend']}/{S('price')}-1", fmt=F_PCT, bold=True)
    r += 2
    # ---- peers
    section(ws, r, "6. Peer table (stockanalysis, 10/6/26)", 8)
    r += 1
    header_row(ws, r, ["Company", "EV/EBITDA TTM", "Forward P/E", "FCF yield"])
    r += 1
    for nm, ev, pf, fy in PEERS:
        label(ws, r, nm)
        W(ws, f"B{r}", ev, fmt=F_X)
        W(ws, f"C{r}", pf, fmt=F_X)
        if fy is not None:
            W(ws, f"D{r}", fy, fmt=F_PCT)
        r += 1
    ws[f"G{r - 6}"].value = "Source: stockanalysis.com per thesis.md section 2 (10/6/26)"
    ws[f"G{r - 6}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    r += 1
    # ---- snapshot
    section(ws, r, "7. Scenario snapshot: all four scenarios (static values regenerated by build_model.py from four full recalculations)", 8)
    r += 1
    header_row(ws, r, ["Output"] + SCEN + ["", "Notes"])
    r += 1
    sn = {}
    for k, t, fm in SNAP_KEYS:
        sn[k] = r
        label(ws, r, t, bold=k in ("sotp", "blend", "eps27"))
        for i, s in enumerate(SCEN):
            v = (snapshot or {}).get(s, {}).get(k)
            W(ws, f"{CL(2 + i)}{r}", 0.0 if v is None else round(v, 4), fmt=fm, bold=k in ("sotp", "blend", "eps27"), color=BLUE)
        r += 1
    ws[f"G{sn['fy26']}"].value = "STATIC: re-run `python -I build_model.py` after changing any driver"
    ws[f"G{sn['fy26']}"].font = Font(name="Calibri", size=8, italic=True, color=RED)
    sn["prob"] = r
    label(ws, r, "Scenario probability weight (input on Drivers)")
    for i in range(4):
        W(ws, f"{CL(2 + i)}{r}", f"={dsc('prob', i, 'D')}", fmt=F_PCT)
    W(ws, f"F{r}", f"=SUM(B{r}:E{r})", fmt=F_PCT)
    r += 1
    sn["pw"] = r
    label(ws, r, "Probability-weighted blended value per share ($)", bold=True)
    W(ws, f"B{r}", f"=SUMPRODUCT(B{sn['blend']}:E{sn['blend']},B{sn['prob']}:E{sn['prob']})/F{sn['prob']}", fmt=F_USD, bold=True)
    r += 1
    sn["pwsotp"] = r
    label(ws, r, "Probability-weighted SOTP (live) ($)")
    W(ws, f"B{r}", f"=SUMPRODUCT(B{so['ps']}:E{so['ps']},B{sn['prob']}:E{sn['prob']})/F{sn['prob']}", fmt=F_USD)
    r += 1
    sn["pwup"] = r
    label(ws, r, "Probability-weighted upside vs current price")
    W(ws, f"B{r}", f"=B{sn['pw']}/{S('price')}-1", fmt=F_PCT, bold=True)
    r += 1
    sn["stale"] = r
    label(ws, r, "Snapshot freshness: live blended (selected) vs snapshot for the same scenario")
    W(ws, f"B{r}", f'=IF(ABS(D{bl["blend"]}-INDEX(B{sn["blend"]}:E{sn["blend"]},Drivers!$E$4))<0.05,"OK: snapshot current","STALE: re-run build_model.py")', bold=True)
    r += 1
    VAL.update(md=md, so=so, pe=pe, dc=dc, bl=bl, sn=sn)
    setw(ws, {"A": 78, "G": 70, "H": 40, **{CL(i): 13 for i in range(2, 7)}})
    wrap_col(ws, "G", 70, 4, r)
    wrap_col(ws, "H", 40, 4, r)
    setup_print(ws, r, 8, freeze="B4")


# ================================================================= BRIDGE
BR = {}


def build_bridge(wb):
    ws = wb["Bridge"]
    title(ws, "Bridge: Management guide ($2,300M 2027E EBITDA) to our Base case",
          "Live formulas independent of the scenario selector (read the scenario engine and SOTP columns). Leasing is valued at book in the SOTP, so its EBITDA gap lowers EPS and FCF but not SOTP value.")
    header_row(ws, 4, ["Segment (2027E)", "Mgmt Guide EBITDA", "Our Base EBITDA", "Delta EBITDA", "Multiple (Base)", "Value impact ($/share)", "Notes"])
    segs = [("Aerospace", "a27", "mult_a", True), ("Power", "p27", "mult_p", True), ("Leasing", "l27", None, False)]
    r = 5
    rr = {}
    for nm, key, mk, cap in segs:
        rr[key] = r
        label(ws, r, nm)
        W(ws, f"B{r}", f"={sumcell(key, 3)}", fmt=F_NUM)
        W(ws, f"C{r}", f"={sumcell(key, 1)}", fmt=F_NUM)
        W(ws, f"D{r}", f"=C{r}-B{r}", fmt=F_NUM)
        if mk:
            W(ws, f"E{r}", f"={dsc(mk, 1, 'D')}", fmt=F_X)
            W(ws, f"F{r}", f"=D{r}*E{r}/{S('vsh')}", fmt='$0.00;($0.00)')
        else:
            W(ws, f"E{r}", "book", color=BLACK)
            W(ws, f"F{r}", 0, fmt='$0.00;($0.00)', color=BLACK)
            ws[f"G{r}"].value = "Valued at book: EBITDA gap hits EPS/FCF (see bottom), not SOTP. Guide equals Bull on Leasing"
        r += 1
    rr["tot"] = r
    label(ws, r, "Total 2027E segment EBITDA", bold=True)
    for c in "BCD":
        W(ws, f"{c}{r}", f"=SUM({c}5:{c}{r - 1})", fmt=F_NUM, bold=True)
    W(ws, f"F{r}", f"=SUM(F5:F{r - 1})", fmt='$0.00;($0.00)', bold=True)
    r += 2
    section(ws, r, "Value per share: guide to our Base (SOTP)", 7)
    r += 1
    vs = {}
    for k, t, f in [("guide", "SOTP value per share at the Mgmt guide ($)", f"=Valuation!E{VAL['so']['ps']}"),
                    ("a", "  less: Aerospace EBITDA shortfall impact", f"=F{rr['a27']}"), ("p", "  less: Power EBITDA shortfall impact", f"=F{rr['p27']}"),
                    ("l", "  less: Leasing EBITDA shortfall impact (valued at book)", f"=F{rr['l27']}"),
                    ("base", "Our Base SOTP value per share ($)", None), ("chk", "  check vs Valuation tab Base SOTP (should be 0)", None)]:
        vs[k] = r
        label(ws, r, t, bold=k in ("guide", "base"))
        if f:
            W(ws, f"B{r}", f, fmt='$0.00;($0.00)')
        r += 1
    W(ws, f"B{vs['base']}", f"=SUM(B{vs['guide']}:B{vs['l']})", fmt=F_USD, bold=True)
    W(ws, f"B{vs['chk']}", f"=B{vs['base']}-Valuation!C{VAL['so']['ps']}", fmt='0.00')
    r += 1
    # waterfall data
    section(ws, r, "EBITDA waterfall data (for chart): 2027E segment EBITDA, Mgmt guide to Base", 7)
    r += 1
    header_row(ws, r, ["Step", "Invisible base", "Amount"])
    r += 1
    w0 = r
    steps = [("Mgmt guide", "0", f"=B{rr['tot']}"),
             ("Aerospace", f"=B{rr['tot']}+D{rr['a27']}", f"=-D{rr['a27']}"),
             ("Power", f"=B{rr['tot']}+D{rr['a27']}+D{rr['p27']}", f"=-D{rr['p27']}"),
             ("Leasing", f"=C{rr['tot']}", f"=-D{rr['l27']}"),
             ("Our Base", "0", f"=C{rr['tot']}")]
    for nm, b, a in steps:
        label(ws, r, nm)
        W(ws, f"B{r}", 0 if b == "0" else b, fmt=F_NUM, color=BLACK)
        W(ws, f"C{r}", a, fmt=F_NUM)
        r += 1
    ch = BarChart()
    ch.type = "col"
    ch.grouping = "stacked"
    ch.overlap = 100
    ch.title = "2027E segment EBITDA: Mgmt guide to Base ($M)"
    ch.add_data(Reference(ws, min_col=2, min_row=w0 - 1, max_row=r - 1), titles_from_data=True)
    ch.add_data(Reference(ws, min_col=3, min_row=w0 - 1, max_row=r - 1), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=w0, max_row=r - 1))
    ch.series[0].graphicalProperties.noFill = True
    ch.series[0].graphicalProperties.line.noFill = True
    ch.series[1].graphicalProperties.solidFill = "1F3864"
    ch.legend = None
    ch.height, ch.width = 8, 16
    ws.add_chart(ch, f"E{w0 - 2}")
    r += 8
    # EPS and PT bridge (snapshot)
    section(ws, r, "From the guide to our numbers (snapshot values, all four scenarios)", 7)
    r += 1
    header_row(ws, r, ["Metric"] + SCEN)
    r += 1
    for k, t, fm in [("tot27", "FY27E total Adj. EBITDA (company basis)", F_NUM), ("eps27", "FY27E diluted EPS ($)", F_USD), ("sotp", "SOTP value per share ($)", F_USD),
                     ("pe", "P/E value per share ($)", F_USD), ("dcf", "DCF value per share ($)", F_USD), ("blend", "Blended value per share ($)", F_USD)]:
        label(ws, r, t)
        for i in range(4):
            W(ws, f"{CL(2 + i)}{r}", f"=Valuation!{CL(2 + i)}{VAL['sn'][k]}", fmt=fm)
        r += 1
    r += 1
    section(ws, r, "Second bridge: Street mean PT (~$330, methodology not public) to our price target (narrative table)", 7)
    r += 1
    header_row(ws, r, ["Step", "$/share", "Explanation"])
    r += 1
    st = {}
    items = [
        ("street", "Street mean price target (7 dated post-June PTs)", f"={S('streetpt')}", "Mean of 290/300/310/350/360/375/325. All Buy-rated; methodology not public"),
        ("guide", "SOTP at the full 2027 guide (our multiples)", f"=B{vs['guide']}", "What management's $2.3B is worth on our peer-based multiples and book-value Leasing"),
        ("gap1", "  Street premium to guide-SOTP: not explained by any public methodology", f"=B{r}-B{r + 1}", "Implies a premium multiple, 2028+ growth, or Power/SCI franchise value beyond the 2027 guide. Cannot be reproduced from sourced data"),
        ("delta", "  Our haircut: guide to Base EBITDA (Aerospace volume, Power timing, Leasing run-rate)", f"=B{vs['base']}-B{vs['guide']}", "Aerospace 1,500 vs 1,700 modules; Power 44 vs 60 units; Leasing at Q2 run-rate plus partial SCI II"),
        ("sotp", "Our Base SOTP", f"=B{vs['base']}", ""),
        ("pw", "Our probability-weighted blended value", f"=Valuation!B{VAL['sn']['pw']}", "SOTP / P/E / DCF blend, weighted over Bear/Base/Bull/Mgmt scenarios"),
        ("tot", "Total gap: Street mean PT to our probability-weighted value", f"=B{r + 5}-B{r}", ""),
    ]
    for k, t, f, ex in items:
        st[k] = r
        label(ws, r, t, bold=k in ("street", "pw", "tot"))
        W(ws, f"B{r}", f, fmt='$#,##0.00;($#,##0.00)')
        ws[f"C{r}"].value = ex
        ws[f"C{r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
        r += 1
    # fix self references in gap1 / tot
    W(ws, f"B{st['gap1']}", f"=B{st['guide']}-B{st['street']}", fmt='$#,##0.00;($#,##0.00)')
    W(ws, f"B{st['tot']}", f"=B{st['pw']}-B{st['street']}", fmt='$#,##0.00;($#,##0.00)')
    BR.update(rr=rr, vs=vs, st=st)
    setw(ws, {"A": 74, "B": 16, "C": 16, "D": 14, "E": 14, "F": 18, "G": 80})
    wrap_col(ws, "G", 80, 5, r + 1)
    wrap_col(ws, "C", 16, st["street"], r + 1)
    setup_print(ws, r + 1, 7, freeze="B5")


# ================================================================= SENSITIVITY
SENS = {}


def build_sensitivity(wb):
    ws = wb["Sensitivity"]
    title(ws, "Sensitivity: explicit formula grids (Excel Data Tables are not available from openpyxl)",
          "Grids 1-2 use the Base scenario's other segments and the SOTP bridge. Grid 3 recomputes FY26 clean FCF analytically around the selected scenario. Green = above current price (grids 1-2) / above zero (grid 3); red = below.")
    price = S("price")
    nd = f"{S('ndbs')}+{S('prefon')}*{S('prefliq')}"
    pw_b = sumcell("p27", 1)
    mp_b = dsc("mult_p", 1, "D")
    ml_b = dsc("mult_l", 1, "D")
    ma_b = dsc("mult_a", 1, "D")
    a_b = sumcell("a27", 1)
    r = 4
    section(ws, r, "Grid 1: SOTP value per share ($): 2027E Aerospace EBITDA (rows) x Aerospace EV/EBITDA multiple (columns); Base Power and Leasing", 9)
    r += 1
    mults = [10.0, 11.7, 13.0, 14.5, 16.0, 18.0]
    label(ws, r, "Aerospace EBITDA ($M)  \\  multiple", bold=True)
    for j, m in enumerate(mults):
        W(ws, f"{CL(2 + j)}{r}", m, fmt=F_X, bold=True)
    g1h = r
    r += 1
    g1 = r
    for e in [900, 1050, 1150, 1230, 1300, 1400, 1430, 1550, 1700]:
        W(ws, f"A{r}", e, fmt=F_NUM0, bold=True)
        ws[f"A{r}"].alignment = Alignment(horizontal="right")
        for j in range(len(mults)):
            c = CL(2 + j)
            W(ws, f"{c}{r}", f"=($A{r}*{c}${g1h}+{pw_b}*{mp_b}+{S('book')}*{ml_b}-({nd}))/{S('vsh')}", fmt=F_USD)
        r += 1
    g1e = r - 1
    ws.conditional_formatting.add(f"B{g1}:{CL(1 + len(mults))}{g1e}", CellIsRule(operator="greaterThan", formula=[price], fill=PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE")))
    ws.conditional_formatting.add(f"B{g1}:{CL(1 + len(mults))}{g1e}", CellIsRule(operator="lessThan", formula=[price], fill=PatternFill("solid", bgColor="FFC7CE", fgColor="FFC7CE")))
    r += 1
    section(ws, r, "Grid 2: SOTP value per share ($): 2027E Power units (rows) x EBITDA per unit $M (columns); Base Aerospace and Leasing", 9)
    r += 1
    epus = [4.0, 5.0, 6.0, 7.5, 9.0, 10.0]
    label(ws, r, "Power units delivered in 2027  \\  EBITDA per unit ($M)", bold=True)
    for j, m in enumerate(epus):
        W(ws, f"{CL(2 + j)}{r}", m, fmt="0.0", bold=True)
    g2h = r
    r += 1
    g2 = r
    for u in [0, 10, 20, 30, 44, 60, 80, 100]:
        W(ws, f"A{r}", u, fmt=F_NUM0, bold=True)
        ws[f"A{r}"].alignment = Alignment(horizontal="right")
        for j in range(len(epus)):
            c = CL(2 + j)
            W(ws, f"{c}{r}", f"=({a_b}*{ma_b}+$A{r}*{c}${g2h}*{mp_b}+{S('book')}*{ml_b}-({nd}))/{S('vsh')}", fmt=F_USD)
        r += 1
    g2e = r - 1
    ws.conditional_formatting.add(f"B{g2}:{CL(1 + len(epus))}{g2e}", CellIsRule(operator="greaterThan", formula=[price], fill=PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE")))
    ws.conditional_formatting.add(f"B{g2}:{CL(1 + len(epus))}{g2e}", CellIsRule(operator="lessThan", formula=[price], fill=PatternFill("solid", bgColor="FFC7CE", fgColor="FFC7CE")))
    r += 1
    section(ws, r, "Grid 3: FY26E clean CFO + CFI ($M): inventory conversion % (rows) x 2H26 Aerospace EBITDA margin (columns), selected scenario", 9)
    r += 1
    margins = [0.24, 0.26, 0.28, 0.30, 0.32]
    label(ws, r, "Inventory conversion %  \\  2H26 Aerospace margin", bold=True)
    for j, m in enumerate(margins):
        W(ws, f"{CL(2 + j)}{r}", m, fmt=F_PCT, bold=True)
    g3h = r
    r += 1
    g3 = r
    Q = lambda k, c: f"Quarterly!${c}${LROW[k]}"
    m0 = f"(({Q('aero', 'D')}+{Q('aero', 'E')})/({Q('aerorev', 'D')}+{Q('aerorev', 'E')}))"
    d0, td, ph = S("d0"), S("tdays"), f"Drivers!$E${DRV['phase']['live']}"
    for cv in [0.0, 0.10, 0.20, 0.30, 0.40, 0.50]:
        W(ws, f"A{r}", cv, fmt=F_PCT, bold=True)
        ws[f"A{r}"].alignment = Alignment(horizontal="right")
        for j in range(len(margins)):
            c = CL(2 + j)
            dm = f"({c}${g3h}-{m0})"
            f = (f"=Quarterly!$J${LROW['clean']}+{dm}*({Q('aerorev', 'D')}+{Q('aerorev', 'E')})*(1-{S('tax')})"
                 f"-(({d0}-$A{r}*({d0}-{td})*{ph})*({Q('acogs', 'E')}-{dm}*{Q('aerorev', 'E')})/{S('dpq')}-{Q('inv', 'E')})")
            W(ws, f"{c}{r}", f, fmt=F_NUM)
        r += 1
    g3e = r - 1
    ws.conditional_formatting.add(f"B{g3}:{CL(1 + len(margins))}{g3e}", CellIsRule(operator="greaterThan", formula=["0"], fill=PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE")))
    ws.conditional_formatting.add(f"B{g3}:{CL(1 + len(margins))}{g3e}", CellIsRule(operator="lessThan", formula=["0"], fill=PatternFill("solid", bgColor="FFC7CE", fgColor="FFC7CE")))
    ws[f"A{r}"].value = ("Grid 3 holds all other selected-scenario drivers fixed: margin changes EBITDA after tax and cost of sales (inventory base); "
                         "conversion changes Q4'26 inventory days. Exact at the selected scenario's own conversion and margin. "
                         "Limitation: a higher margin also lowers the cost-of-sales proxy and so the days-based inventory balance, which amplifies the margin sensitivity.")
    ws[f"A{r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
    SENS.update(g1=g1, g2=g2, g3=g3, g3h=g3h)
    setw(ws, {"A": 56, **{CL(i): 12 for i in range(2, 9)}})
    setup_print(ws, r + 1, 8, freeze="B4")


# ================================================================= CHECKS
CHK = {}


def build_checks(wb):
    ws = wb["Checks"]
    title(ws, "Checks and tie-outs (formula-driven pass/fail)",
          "Model integrity checks for the spec's Verification section. 'By construction' means the Q4 data are derived as FY less 9M, so the check is an identity, not independent verification.")
    header_row(ws, 4, ["Check", "Model value", "Expected / comparator", "Tolerance", "Result", "Notes"])
    r = 5
    res_rows = []

    def chk(text, model, expected, tol, note="", fmt=F_NUM, mode="abs"):
        nonlocal r
        label(ws, r, text)
        W(ws, f"B{r}", model, fmt=fmt)
        W(ws, f"C{r}", expected, fmt=fmt)
        W(ws, f"D{r}", tol, fmt="0.000")
        W(ws, f"E{r}", f'=IF(ISERROR(B{r}-C{r}),"FAIL",IF(ABS(B{r}-C{r})<=D{r},"PASS","FAIL"))', bold=True)
        ws[f"F{r}"].value = note
        ws[f"F{r}"].font = Font(name="Calibri", size=8, italic=True, color="595959")
        res_rows.append(r)
        r += 1

    def sec(t):
        nonlocal r
        section(ws, r, t, 6)
        r += 1

    HC = lambda k, p: hc(k, p)
    sec("1. Historical quarters sum to FY (FY2024 and FY2025; Q4 derived as FY less 9M, so by construction)")
    for key, nm in [("totrev", "Total revenues"), ("cogs", "Cost of sales"), ("da", "D&A"), ("int", "Interest expense"), ("e_aero", "Aerospace Adj. EBITDA"), ("e_leas", "Leasing Adj. EBITDA"),
                    ("e_corp", "Corporate EBITDA"), ("e_elim", "Eliminations"), ("e_tot", "Total Adj. EBITDA"), ("cfo", "CFO"), ("cfi", "CFI"), ("niattr", "Net income attributable")]:
        for yr, qs in (("FY2024", ["Q1-2024", "Q2-2024", "Q3-2024", "Q4-2024"]), ("FY2025", ["Q1-2025", "Q2-2025", "Q3-2025", "Q4-2025"])):
            chk(f"{nm}: sum of quarters vs {yr}", "=" + "+".join(HC(key, q) for q in qs), f"={HC(key, yr)}", 0.1, "by construction for derived Q4" if key not in ("cfo", "cfi") else "CFO/CFI quarters derived from YTD")
    sec("2. Quarterly sums to Annual (FY2026E, FY2027E)")
    for key, nm in [("aero", "Aerospace EBITDA"), ("power", "Power EBITDA"), ("leas", "Leasing EBITDA"), ("seg", "Segment-basis EBITDA"), ("tot", "Total Adj. EBITDA"), ("niattr", "Net income to common"),
                    ("total", "CFO + CFI"), ("clean", "Clean CFO + CFI"), ("adjfcf", "Adjusted FCF"), ("da", "D&A"), ("int", "Interest")]:
        chk(f"{nm}: Quarterly Q1'26-Q4'26 vs Annual FY26", f"=SUM(Quarterly!B{LROW[key]}:E{LROW[key]})", f"=Annual!E{LROW[key]}", 0.001)
        chk(f"{nm}: Quarterly Q1'27-Q4'27 vs Annual FY27", f"=SUM(Quarterly!F{LROW[key]}:I{LROW[key]})", f"=Annual!F{LROW[key]}", 0.001)
    sec("3. Scenario engine ties to guidance and to A_2027_guide_segment_build.csv")
    chk("Mgmt Guide FY2027E segment EBITDA = $2,300M", f"={sumcell('t27', 3)}", 2300, 1.0)
    chk("Mgmt Guide FY2027E Aerospace = $1,400M", f"={sumcell('a27', 3)}", 1400, 1.0)
    chk("Mgmt Guide FY2027E Power = $450M", f"={sumcell('p27', 3)}", 450, 1.0)
    chk("Mgmt Guide FY2027E Leasing = $450M", f"={sumcell('l27', 3)}", 450, 1.0)
    chk("Mgmt Guide FY2026E segment EBITDA = $1,525M", f"={sumcell('t26', 3)}", 1525, 1.0)
    chk("Mgmt Guide FY2026E Aerospace = $1,050M", f"={sumcell('a26', 3)}", 1050, 1.0)
    chk("Mgmt Guide FY2026E Leasing = $475M", f"={sumcell('l26', 3)}", 475, 1.0)
    chk("Base FY2027E segment EBITDA ~ $1,920M", f"={sumcell('t27', 1)}", 1920, 5.0)
    chk("Bear FY2027E segment EBITDA ~ $1,470M", f"={sumcell('t27', 0)}", 1470, 5.0)
    chk("Bull FY2027E segment EBITDA ~ $2,480M", f"={sumcell('t27', 2)}", 2480, 5.0)
    chk("Engine (selected) FY27 segment EBITDA = Quarterly FY27 (no logic drift)", f"=Drivers!$H${ENG['SUMR']['t27']}", f"=Quarterly!K{LROW['seg']}", 0.01)
    chk("Engine (selected) FY26 segment EBITDA = Quarterly FY26", f"=Drivers!$H${ENG['SUMR']['t26']}", f"=Quarterly!J{LROW['seg']}", 0.01)
    sec("4. Valuation targets (thesis.md section 2: Base ~172, Bear ~115, Bull ~280)")
    so = VAL["so"]
    chk("Base SOTP ex-corporate ~ $172", f"=Valuation!C{so['cm']}", 172, 2.0, "Difference mainly the $65M preferred deduction and book 1,511.9", fmt=F_USD)
    chk("Bear SOTP ex-corporate ~ $115", f"=Valuation!B{so['cm']}", 115, 2.0, fmt=F_USD)
    chk("Bull SOTP ex-corporate ~ $280", f"=Valuation!D{so['cm']}", 280, 2.0, fmt=F_USD)
    chk("Net debt: balance sheet vs stockanalysis (EV - market cap)", f"={S('ndbs')}", f"={S('ndsa')}", 5.0)
    sec("5. Cash flow facts from the filings")
    chk("FY25 CFO = -310.7", f"={HC('cfo', 'FY2025')}", -310.7, 0.1)
    chk("FY25 CFI = +723.3", f"={HC('cfi', 'FY2025')}", 723.3, 0.1)
    chk("FY25 CFO + CFI = 412.6", f"={HC('cfocfi', 'FY2025')}", 412.6, 0.1)
    chk("1H26 CFO + CFI = 250.4", f"={HC('cfocfi', 'Q1-2026')}+{HC('cfocfi', 'Q2-2026')}", 250.4, 0.1)
    chk("1H26 seed-sale proceeds = 175.7", f"={HC('seed', 'Q1-2026')}+{HC('seed', 'Q2-2026')}", 175.7, 0.1)
    chk("1H26 insurance proceeds = 48.3", f"={HC('insproc', 'Q1-2026')}+{HC('insproc', 'Q2-2026')}", 48.3, 0.1)
    chk("1H26 clean CFO + CFI ~ 26 (after ~351 inventory build)", f"={HC('k_clean', 'Q1-2026')}+{HC('k_clean', 'Q2-2026')}", 26.4, 0.2)
    chk("FY25: 724 - 412.6 - 252 = 59.4 inferred residual", f"=FCF_Quality!B{FQ['rec']['resid']}", 59.4, 0.2, "INFERRED, not confirmed")
    chk("Mgmt Guide FY2026E company-defined Adjusted FCF = $878M (snapshot, back-solved)", f"=Valuation!E{VAL['sn']['adj26']}", 878, 1.0, "KEY #2 conversion back-solved to the guide")
    sec("6. EPS bridge back-test on actual quarters (driver-based vs reported)")
    chk("Q1'26 predicted EPS vs reported 1.29 (within $0.10)", f"=Quarterly!B{BT_ROW + 3}", f"=Quarterly!B{BT_ROW + 4}", 0.10, fmt=F_USD)
    chk("Q2'26 predicted EPS vs reported 1.13 (within $0.10)", f"=Quarterly!C{BT_ROW + 3}", f"=Quarterly!C{BT_ROW + 4}", 0.10, fmt=F_USD)
    chk("1H26 predicted EPS vs reported (within $0.05)", f"=Quarterly!B{BT_ROW + 3}+Quarterly!C{BT_ROW + 3}", f"=Quarterly!B{BT_ROW + 4}+Quarterly!C{BT_ROW + 4}", 0.05, fmt=F_USD)
    sec("7. Leasing book guards and error scan")
    for s in SCEN:
        e = ENG[s]
        chk(f"Leasing book never negative, {s} (min of book end rows, floor 0)", f"=MAX(0,-MIN(Drivers!D{e['book']}:I{e['book']}))", 0, 0.001)
    chk("Book sold <= beginning book in every selected-scenario quarter (count of violations)", f"=SUMPRODUCT(--(Quarterly!D{LROW['sold']}:I{LROW['sold']}>Quarterly!D{LROW['bbeg']}:I{LROW['bbeg']}))", 0, 0.001)
    chk("Annual: leasing book end >= 0 FY28-30 (min)", f"=MAX(0,-MIN(Annual!G{LROW['bend']}:I{LROW['bend']}))", 0, 0.001)
    chk("Error cells in Quarterly (count)", f"=SUMPRODUCT(--ISERROR(Quarterly!B5:K{BT_ROW + 5}))", 0, 0.001)
    chk("Error cells in Annual (count)", f"=SUMPRODUCT(--ISERROR(Annual!B5:I{LAST_ROW}))", 0, 0.001)
    chk("Error cells in Valuation (count)", f"=SUMPRODUCT(--ISERROR(Valuation!B4:F{VAL['sn']['stale']}))", 0, 0.001)
    chk("Probability weights sum to 100%", f"=Valuation!F{VAL['sn']['prob']}", 1, 0.0001, fmt=F_PCT)
    chk("Blend weights sum to 100%", f"={S('w_sotp')}+{S('w_pe')}+{S('w_dcf')}", 1, 0.0001, fmt=F_PCT)
    chk("Revolver never drawn above 0 in selected scenario (info)", f"=MAX(Quarterly!D{LROW['rev']}:I{LROW['rev']},Annual!G{LROW['rev']}:I{LROW['rev']})", 0, 0.001, "Cash stays above the minimum balance")
    r += 1
    label(ws, r, "SUMMARY: checks passed", bold=True)
    W(ws, f"B{r}", f'=COUNTIF(E5:E{r - 2},"PASS")', fmt="0", bold=True)
    label(ws, r + 1, "SUMMARY: checks failed", bold=True)
    W(ws, f"B{r + 1}", f'=COUNTIF(E5:E{r - 2},"FAIL")', fmt="0", bold=True)
    ws.conditional_formatting.add(f"E5:E{r - 2}", CellIsRule(operator="equal", formula=['"PASS"'], fill=PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE")))
    ws.conditional_formatting.add(f"E5:E{r - 2}", CellIsRule(operator="equal", formula=['"FAIL"'], fill=PatternFill("solid", bgColor="FFC7CE", fgColor="FFC7CE")))
    CHK.update(first=5, last=r - 2, passrow=r, failrow=r + 1)
    setw(ws, {"A": 84, "B": 14, "C": 18, "D": 10, "E": 9, "F": 70})
    wrap_col(ws, "F", 70, 5, r + 2)
    setup_print(ws, r + 2, 6, freeze="B5")


# ================================================================= SUMMARY
SUMM = {}


def build_summary(wb):
    ws = wb["Summary"]
    title(ws, "FTAI Aviation (NASDAQ: FTAI): valuation summary",
          f"{TEAM} | Point72 Academy pitch | market data as of 10/6/26 | USD m except per-share | Scenario selected on Drivers tab")
    sn, so, bl, pe, dcv = VAL["sn"], VAL["so"], VAL["bl"], VAL["pe"], VAL["dc"]
    r = 4
    label(ws, r, "RECOMMENDATION (formula-driven)", bold=True)
    W(ws, f"B{r}", (f'=IF(Valuation!B{sn["pwup"]}>{S("thr")},"LONG",IF(Valuation!B{sn["pwup"]}<-{S("thr")},"SHORT","NEUTRAL / marginal"))'
                    f'&": probability-weighted value $"&TEXT(Valuation!B{sn["pw"]},"0")&" vs price $"&TEXT({S("price")},"0.00")&" ("&TEXT(Valuation!B{sn["pwup"]},"0%")&")"&IF(ABS(ABS(Valuation!B{sn["pwup"]})-{S("thr")})<{S("marg")}," - MARGINAL call","")'),
      bold=True, fill=YEL)
    ws.merge_cells(f"B{r}:H{r}")
    SUMM["rec"] = r
    r += 1
    label(ws, r, "Current price ($)")
    W(ws, f"B{r}", f"={S('price')}", fmt=F_USD)
    r += 1
    label(ws, r, "Probability-weighted blended price target ($)", bold=True)
    W(ws, f"B{r}", f"=Valuation!B{sn['pw']}", fmt=F_USD, bold=True)
    r += 1
    label(ws, r, "Upside / (downside) vs current price", bold=True)
    W(ws, f"B{r}", f"=Valuation!B{sn['pwup']}", fmt=F_PCT, bold=True)
    r += 1
    label(ws, r, "Base-case blended price target ($) and upside")
    W(ws, f"B{r}", f"=Valuation!C{sn['blend']}", fmt=F_USD)
    W(ws, f"C{r}", f"=B{r}/{S('price')}-1", fmt=F_PCT)
    r += 1
    label(ws, r, "Street mean PT ($, methodology not public)")
    W(ws, f"B{r}", f"={S('streetpt')}", fmt=F_USD)
    r += 2
    section(ws, r, "Price target by method: selected scenario (live)", 8)
    r += 1
    label(ws, r, "Scenario currently selected")
    W(ws, f"B{r}", "=Drivers!$C$4")
    r += 1
    header_row(ws, r, ["Method", "Value / share", "Weight", "vs price"])
    r += 1
    for k, t in (("sotp", "SOTP (2027E, Leasing at book)"), ("pe", "Forward P/E x FY27E EPS"), ("dcf", "DCF (clean FCF)")):
        label(ws, r, t)
        W(ws, f"B{r}", f"=Valuation!B{bl[k]}", fmt=F_USD)
        W(ws, f"C{r}", f"=Valuation!C{bl[k]}", fmt=F_PCT)
        W(ws, f"D{r}", f"=B{r}/{S('price')}-1", fmt=F_PCT)
        r += 1
    label(ws, r, "Blended (weights are inputs on Drivers)", bold=True)
    W(ws, f"B{r}", f"=Valuation!D{bl['blend']}", fmt=F_USD, bold=True)
    W(ws, f"C{r}", f"=Valuation!C{bl['blend']}", fmt=F_PCT)
    W(ws, f"D{r}", f"=B{r}/{S('price')}-1", fmt=F_PCT, bold=True)
    r += 1
    label(ws, r, "Model FY27E EPS ($) vs consensus-implied ($8.87)")
    W(ws, f"B{r}", f"=Valuation!B{pe['eps']}", fmt=F_USD)
    W(ws, f"C{r}", f"=Valuation!B{pe['ceps']}", fmt=F_USD)
    W(ws, f"D{r}", f"=Valuation!B{pe['gap']}", fmt=F_PCT)
    r += 2
    section(ws, r, "Scenario table (SOTP is live; EPS, P/E, DCF, blended come from the snapshot of four full recalculations)", 8)
    r += 1
    header_row(ws, r, ["Metric"] + SCEN + ["Prob-weighted"])
    r += 1
    t0 = r
    rows = [("prob", "Probability weight", F_PCT, "prob"), ("fy26", "FY26E segment EBITDA ($M)", F_NUM0, "fy26"), ("fy27", "FY27E segment EBITDA ($M)", F_NUM0, "fy27"),
            ("eps27", "FY27E diluted EPS ($)", F_USD, "eps27"), ("sotp", "SOTP value / share ($)", F_USD, "sotp"), ("pe", "P/E value / share ($)", F_USD, "pe"),
            ("dcf", "DCF value / share ($)", F_USD, "dcf"), ("blend", "Blended value / share ($)", F_USD, "blend")]
    SR = {}
    for k, t, fm, sk in rows:
        SR[k] = r
        label(ws, r, t, bold=k == "blend")
        for i in range(4):
            c = CL(2 + i)
            W(ws, f"{c}{r}", f"=Valuation!{c}{so['ps'] if k == 'sotp' else sn[sk]}", fmt=fm, bold=k == "blend")
        if k != "prob":
            W(ws, f"F{r}", f"=SUMPRODUCT(B{r}:E{r},$B${SR['prob']}:$E${SR['prob']})/SUM($B${SR['prob']}:$E${SR['prob']})", fmt=fm, bold=k == "blend")
        else:
            W(ws, f"F{r}", f"=SUM(B{r}:E{r})", fmt=fm)
        r += 1
    label(ws, r, "Upside / (downside) vs price (blended)")
    SR["up"] = r
    for i in range(5):
        c = CL(2 + i)
        W(ws, f"{c}{r}", f"={c}{SR['blend']}/{S('price')}-1", fmt=F_PCT)
    r += 1
    ws.conditional_formatting.add(f"B{SR['up']}:F{SR['up']}", CellIsRule(operator="greaterThan", formula=["0"], fill=PatternFill("solid", bgColor="C6EFCE", fgColor="C6EFCE")))
    ws.conditional_formatting.add(f"B{SR['up']}:F{SR['up']}", CellIsRule(operator="lessThan", formula=["0"], fill=PatternFill("solid", bgColor="FFC7CE", fgColor="FFC7CE")))
    r += 1
    section(ws, r, "The 3 KEY ASSUMPTIONS (flagged; values by scenario)", 8)
    r += 1
    header_row(ws, r, ["Key assumption"] + SCEN + ["Selected"])
    r += 1
    for j, (t, fm) in enumerate([("KEY #1: 2027E Aerospace EBITDA ($M) = modules x EBITDA/module (guide is a volume call)", F_NUM0),
                                 ("KEY #2: inventory conversion % (2H26 FCF ramp; Mgmt value back-solved to the $878M guide)", F_PCT),
                                 ("KEY #3: 2027E Power EBITDA ($M) = units x $7.5M/unit (unverified)", F_NUM0)]):
        label(ws, r, t, key=True)
        for i in range(4):
            W(ws, f"{CL(2 + i)}{r}", f"=Drivers!{CL(4 + i)}{9 + j}", fmt=fm, fill=YEL)
        W(ws, f"F{r}", f"=Drivers!H{9 + j}", fmt=fm, fill=YEL, bold=True)
        r += 1
    r += 1
    section(ws, r, "Thesis in three bullets", 8)
    r += 1
    bullets = [
        "1. Cash quality: FY25 Adjusted FCF of $724M vs CFO+CFI of $412.6M; 1H26 clean cash was about $26M after $176M of non-recurring seed sales and $48M of insurance, and the $878M FY26 guide needs ~$623M in 2H26 (about 3x the Q2 run-rate).",
        "2. Growth runs through affiliates: 25% of 1H26 Aerospace revenue was sold to the 19%-owned SCI vehicle, Power sits in a JV that Jereh consolidates, and pro-rata SCI/JV EBITDA is counted in Adj. EBITDA but arrives as cash only via distributions.",
        "3. Valuation: the 2027 guide is roughly our Bull case. On Base (1,920 EBITDA) SOTP and P/E sit near the current price, far below the Street's ~$330; the call depends on the 2027 EBITDA delivery and the Q3 (10/28) FCF test.",
    ]
    for b in bullets:
        W(ws, f"A{r}", b, color=BLACK, wrap=True)
        ws.merge_cells(f"A{r}:H{r}")
        ws.row_dimensions[r].height = 40
        r += 1
    r += 1
    ch = BarChart()
    ch.type = "col"
    ch.title = "Blended value per share by scenario ($)"
    ch.add_data(Reference(ws, min_col=1, max_col=5, min_row=SR["blend"], max_row=SR["blend"]), from_rows=True, titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=2, max_col=5, min_row=t0 - 1, max_row=t0 - 1))
    ch.legend = None
    ch.height, ch.width = 7.5, 15
    ws.add_chart(ch, f"A{r}")
    r += 17
    setw(ws, {"A": 82, **{CL(i): 14 for i in range(2, 9)}})
    setup_print(ws, r, 8, freeze=None)
    SUMM.update(SR=SR)


# ================================================================= SOURCES
def build_sources(wb):
    ws = wb["Sources"]
    title(ws, "Sources, inferred / unverified items, and method note", "Every typed input in Historical and Drivers carries a source or rationale in its row. Dates are retrieval or filing dates.")
    header_row(ws, 4, ["Source", "URL / accession", "Date", "Used for"])
    src = [
        ("SEC EDGAR, FTAI Aviation Ltd. (CIK 1590364): Q2-26 10-Q", "acc 0001628280-26-051412; https://www.sec.gov/Archives/edgar/data/1590364/000162828026051412/ftai-20260630.htm", "Period ended 2026-06-30; pulled 2026-10-06", "Segment, IS, BS, CF, debt note, related party"),
        ("Q2-26 earnings release (8-K Ex99.1)", "acc 0001628280-26-050622; https://www.sec.gov/Archives/edgar/data/1590364/000162828026050622/ftai6302026earningsrelease.htm", "2026-07-29", "2026/2027 guidance (1,525 / 2,300; Leasing cut to 475), Adj. EBITDA definition"),
        ("Q1-26 earnings release (8-K Ex99.1)", "acc 0001628280-26-028390", "2026-04-29", "Q1-26 results, Jereh JV bullet, 100-unit Power target"),
        ("Q4-25 earnings release (8-K Ex99.1)", "acc 0001628280-26-011685", "2026-02-25", "2026 guide 1,625 (Aero 1,050 + Leasing 575)"),
        ("Q3-25 earnings release (8-K Ex99.1)", "acc 0001590364-25-000038", "2025-10-29", "2026 guide 1,525"),
        ("Q4-24 earnings release (8-K Ex99.1)", "acc 0001140361-25-006099", "2025-02-26", "2025 FCF target 650, module assumption"),
        ("10-Qs 2023-2025, 10-K FY23/FY24/FY25 (segment notes, cash flow statements, balance sheets)", "acc 0001590364-24-000011 (Q1-24), 0001590364-24-000016 (Q2-24), 0001590364-23-000013 (Q1-23), others per phase2/data CSV source columns", "2023-2026", "Historical tab"),
        ("Q4-25 earnings call transcript (Motley Fool)", "https://www.fool.com/earnings/call-transcripts/2026/02/26/ftai-ftai-q4-2025-earnings-call-transcript/", "2026-02-26", "FY25 Adjusted FCF 724, three named investments (52 / 150 / 50), Power margin comment (secondary)"),
        ("Q2-26 earnings call transcript (Investing.com)", "investing.com transcript", "2026-07-30", "FY26 FCF guide 878 (from 915), 1,200 modules 2026, 1,700 modules 2027, Power range 450-750, Leasing components 5 / 48 / 35 (secondary)"),
        ("stockanalysis.com /forecast and /statistics", "https://stockanalysis.com/stocks/ftai/statistics/ ; https://stockanalysis.com/stocks/ftai/forecast/", "2026-10-06", "Price 179.44, market cap, EV, shares, peer multiples, forward P/E, FY26 EPS 5.83"),
        ("MarketBeat itemised price targets", "https://www.marketbeat.com/stocks/NASDAQ/FTAI/price-target/", "2026-10-06", "Seven dated post-June PTs, mean 330 / median 325"),
        ("Jereh Group (002353) notice 2026-048 and 2026 half-year report", "https://stock.10jqka.com.cn/20260723/c678378497.shtml ; http://static.cninfo.com.cn/finalpage/2026-08-14/1225472540.PDF", "2026-07-22 / 2026-08-14", "J&F Power Systems consolidated by Jereh (control); $1.465B PO"),
        ("WestJet 737-700 sale-leaseback (finviz)", "https://finviz.com/news/395776/ftai-acquires-27-boeing-737-700-aircraft-from-westjet", "2026-09-28", "SCI II purchases, feedstock"),
        ("Team research files", "research/FTAI/thesis.md; phase2/A_2027_guide.md; phase2/A_2027_guide_segment_build.csv; phase2/B_data_notes.md; phase2/data/*.csv", "2026-10-06", "Scenario builds, thesis, peer multiples, data notes"),
    ]
    r = 5
    for row in src:
        for j, v in enumerate(row):
            c = ws.cell(row=r, column=1 + j, value=v)
            c.font = Font(name="Calibri", size=9)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    r += 1
    section(ws, r, "Inferred, unverified or assumed items (blue inputs with rationale on the Drivers tab)", 4)
    r += 1
    items = [
        "INFERRED: FY25 Adjusted FCF residual of ~$59M (probably $49.1M acquisitions + ~$10M JV item). Not confirmed.",
        "UNVERIFIED: Power EBITDA per unit $7.5M and revenue per unit ~$25M (secondary reports); J&F ownership split and FTAI's accounting for Power economics.",
        "UNVERIFIED: $500M buyback (model toggle default OFF). UNVERIFIED: 2027 module target of 1,700 (truncated transcript read).",
        "SECONDARY: module counts (Q4-25 228, Q2-26 296) and Q1-25 (~138) back-solved. Q1-26 modules are an ESTIMATE (EBITDA / 0.84).",
        "ASSUMED (not in provided data): common dividend $0.30/quarter; SCI AUM path and ~6,000 starting AUM; fee rate derived from $7.0M servicing fees; revolver rate 6%, refinancing coupon 7%, minimum cash $300M.",
        "ASSUMED: Power cash conversion 75% and EBITDA-to-pretax conversion 75% (invented); pro-rata SCI EBITDA Q1-26 equal to Q2-26 (28.0); other pre-tax adjustments calibrated on 1H26.",
        "ASSUMED: leasing yield 8.5%, gain on sale 15%, seed share 30%, book sold paths, FY28-30 growth, margin cap/elasticity, inventory target days 150, tax rate 18%, DCF WACC 10% and terminal growth 3%, blend weights 40/30/30.",
        "CAVEAT: consensus FY27 EPS of ~$8.87 is implied from stockanalysis's 20.2x forward P/E, which conflicts with its own FY26 EPS (30.8x). Use as an indication only.",
        "NOT DISCLOSED: gains by segment (company-level only), SCI fee/promote terms, Q3-25 and Q1-26 module counts.",
        "Q4 flows in Historical are derived as FY less 9M; quarters therefore sum to FY by construction.",
    ]
    for t in items:
        W(ws, f"A{r}", t, color=BLACK, wrap=True)
        ws.merge_cells(f"A{r}:D{r}")
        ws.row_dimensions[r].height = 28
        r += 1
    r += 1
    W(ws, f"A{r}", "Method note: this model was built with GenAI assistance (Claude, Anthropic) from a blank workbook via a reproducible Python/openpyxl script (build_model.py) and "
                   "verified against filings and the team's sourced data files; no external or outside-research models were used or copied.", color=BLACK, wrap=True, bold=True)
    ws.merge_cells(f"A{r}:D{r}")
    ws.row_dimensions[r].height = 42
    setw(ws, {"A": 70, "B": 90, "C": 26, "D": 70})
    setup_print(ws, r, 4, freeze="A5")


# ================================================================= ORCHESTRATION
MGMT_CONV = 0.113     # back-solved so Mgmt Guide FY26 company-defined Adjusted FCF = 878 (run with --calibrate to re-derive)


def build(path=OUT, scenario="Base", snapshot=None):
    global SNAP_USED
    wb = new_book()
    build_historical(wb)
    build_drivers(wb, scenario)
    build_quarterly(wb)
    build_annual(wb)
    build_fcf_quality(wb)
    build_valuation(wb, snapshot)
    build_bridge(wb)
    build_sensitivity(wb)
    build_checks(wb)
    build_summary(wb)
    build_sources(wb)
    wb.calculation.fullCalcOnLoad = True
    wb.save(path)
    return wb


def recalc(path, scenario, extra=None):
    import formulas
    xl = formulas.ExcelModel().loads(path).finish()
    fn = os.path.basename(path)
    inp = {f"'[{fn}]DRIVERS'!C4": scenario}
    for k, v in (extra or {}).items():
        inp[f"'[{fn}]{k}"] = v
    sol = xl.calculate(inputs=inp)

    def get(sheet, addr):
        k = f"'[{fn}]{sheet.upper()}'!{addr}"
        try:
            return sol[k].value[0][0]
        except KeyError:
            return None
    return get, sol, fn


def read_outputs(get):
    so, pe, dc, bl = VAL["so"], VAL["pe"], VAL["dc"], VAL["bl"]
    f = lambda v: float(v)
    return dict(
        fy26=f(get("Annual", f"E{LROW['seg']}")), fy27=f(get("Annual", f"F{LROW['seg']}")), tot27=f(get("Annual", f"F{LROW['tot']}")),
        eps26=f(get("Annual", f"E{LROW['eps']}")), eps27=f(get("Annual", f"F{LROW['eps']}")), sotp=f(get("Valuation", f"F{so['ps']}")),
        pe=f(get("Valuation", f"B{pe['mid']}")), dcf=f(get("Valuation", f"B{dc['ps']}")), blend=f(get("Valuation", f"D{bl['blend']}")),
        adj26=f(get("Annual", f"E{LROW['adjfcf']}")), clean26=f(get("Annual", f"E{LROW['clean']}")), clean27=f(get("Annual", f"F{LROW['clean']}")))


def calibrate_mgmt_conv():
    tmp = os.path.join(HERE, "_calib.xlsx")
    build(tmp, "Mgmt Guide", None)
    cell = f"D{DRV['conv']['rows'][3]}"
    pts = []
    for x0 in (0.0, 0.5):
        get, _, _ = recalc(tmp, "Mgmt Guide", {f"DRIVERS'!{cell}": x0})
        pts.append((x0, float(get("Annual", f"E{LROW['adjfcf']}"))))
    (xa, ya), (xb, yb) = pts
    x_star = xa + (878.0 - ya) * (xb - xa) / (yb - ya)
    os.remove(tmp)
    return x_star, pts


def main():
    args = sys.argv[1:]
    if "--calibrate" in args:
        xs, pts = calibrate_mgmt_conv()
        print("Mgmt conversion that yields FY26 Adj FCF = 878:", round(xs, 4), pts)
        return
    build(OUT, "Base", None)
    snap = None
    try:
        import formulas  # noqa: F401
        snap = {}
        for s in SCEN:
            get, _, _ = recalc(OUT, s)
            snap[s] = read_outputs(get)
            print(s, {k: round(v, 2) for k, v in snap[s].items()})
        with open(SNAP_JSON, "w") as f:
            json.dump(snap, f, indent=1)
    except ImportError:
        if os.path.exists(SNAP_JSON):
            snap = json.load(open(SNAP_JSON))
    build(OUT, "Base", snap)
    print("saved", OUT)


if __name__ == "__main__":
    main()
