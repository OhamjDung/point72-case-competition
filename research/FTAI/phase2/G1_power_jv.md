# G1 FTAI Power / J&F JV (Jereh) - DRAFT after 17 calls (2026-10-06)

## Findings
| Fact | Value | Source | Verified |
|---|---|---|---|
| J&F Power Systems LLC = FTAI + Jereh Group JV to package/distribute Mod-1 | confirmed | https://pulse2.com/ftai-secures-1-465-billion-gas-turbine-generator-order-through-jf-power-systems/ (2026-07-22) | Y |
| Q1 Ownership split | NOT disclosed in anything found. Jereh calls J&F 控股子公司 ("controlled subsidiary", cninfo 1H26 2026-08-14, https://static.cninfo.com.cn/finalpage/2026-08-14/1225472539.PDF; PDF text not machine-readable) and the 2026-07 order announcement says "公司控股子公司J&F Power Systems LLC" (https://stock.10jqka.com.cn/20260723/c678378497.shtml). Implies Jereh >50% or de facto control. FTAI transcript's "15% commitment" refers to a 2026 SPV co-invest, NOT J&F (equibles/investing transcript) | partly | N [UNVERIFIED %] |
| $1.465B initial PO from "leading U.S. hyperscaler" (FTAI) / "international cloud provider" (Jereh); 5-yr master agreement; batches through Nov 2027; advance at signing, progress payments, final at commissioning; value can fall up to 10% if output short | yes | pulse2 link (2026-07-22); https://www.investing.com/news/transcripts/earnings-call-transcript-ftai-aviation-q2-2026-eps-miss-clouds-strong-revenue-growth-93CH-4824650 (2026-07-30) | Y |
| Jereh: ~$1.72B cumulative with this customer in 12m = 61.33% of 2025 revenue; >$3.1B (RMB 20.9B) total gas turbine genset orders since Nov-2025 | yes | https://stock.10jqka.com.cn/20260723/c678378497.shtml ; gelonghui 5286477 | Y (secondary) |
| Q2 FTAI sells turbines/cores TO J&F and books it | Per transcript summary: FTAI sells to JV, "you'll see revenue and cost of goods sold" at FTAI, then "unconsolidated earnings" when JV sells to customer. => FTAI books sales into J&F = affiliate channel. Verbatim not confirmed (summarizer output); cores vs complete turbines unspecified | investing.com transcript above (2026-07-30) | Partial [UNVERIFIED verbatim] |
| Jereh's own purchase list: "已与西门子、贝克休斯、川崎重工、FTAI等建立长期合作" (long-term cooperation with Siemens, Baker Hughes, Kawasaki, FTAI) i.e. Jereh treats FTAI as turbine supplier | yes | https://m.gelonghui.com/news/5286477 / 1H26 | Y (secondary) |
| Q3 2027 Power EBITDA guide $450M = "bottom end of $450-750M range, where we have highest conviction"; "does not assume 100 units"; target 100+ units 2027 | yes | equibles https://equibles.com/stocks/ftai/calls/2026-q2 ; marketbeat summary 2026-07-30 | Y (secondary) |
| Q3 pro-rata vs own sales in $450M | transcript summary says no explicit statement; by FTAI definition Adj. EBITDA includes pro-rata share of unconsolidated JV, so $450M is likely BOTH (sales margin to J&F + equity share of J&F). | - | N [UNVERIFIED] |
| Q4 EBITDA/unit, unit price | management declined: "commercially sensitive"; $7-8M/unit not confirmed | equibles above | N |
| Delivery timing | commercial launch Q4 2026; batches through Nov 2027 | pulse2; transcript | Y |
| Q5 US-China regulatory | No public news found linking FTAI/J&F to China export/CFIUS/sanction issues; transcript has no mention. Adjacent: DoJ defending xAI turbine suit on nat-sec grounds (datacenterdynamics 2026-06-17) - not relevant. Note US hyperscaler buying turbines packaged by a Shenzhen-listed Chinese firm is a latent political risk, not an observed one | searches | Y (absence) |

## Investigation Trail
1 ToolSearch. 2-5 web searches (JV, Chinese Jereh, EBITDA guide, regulatory). 6 write. 7-9 fetch marketbeat (no content), pulse2 (ok), qq (ECONNRESET). 10-12 transcript/ownership/short-seller searches. 13-15 fetch investing.com transcript (useful), equibles (useful, mislabels Jereh as "Jera"), cninfo PDF (unreadable fonts). 16 pypdf: only 3 pages/3293 chars, no ownership text. 17-18 Eastmoney / Stockstar lead searches: no new ownership data; Eastmoney report https://data.eastmoney.com/report/info/AP202605011821893512.html surfaced (unread).

## UPDATE after 21 calls: verbatim confirmations
- Q2 VERIFIED (CFO Nicholas McAleese, FTAI Q2-26 call, 2026-07-30, https://www.investing.com/news/transcripts/earnings-call-transcript-ftai-aviation-q2-2026-eps-miss-clouds-strong-revenue-growth-93CH-4824650): "You'll see it in next year's P&L in two places. First is when FTAI sells the turbine to the JV. That will be reflective, similar to how we report aerospace products today, which is you'll see revenue and cost of goods sold. The second piece is ultimately when the JV sells it to the customer. As we are an equity stake in that, you'll see an unconsolidated earnings and other income." Adams: "It will all be under the heading of Power." => FTAI SELLS TURBINES (not just cores) to J&F, books revenue + COGS; J&F is an affiliate channel; double-layer (own sales margin + equity share of J&F earnings). Revenue into an entity Jereh consolidates and FTAI equity-accounts: intercompany profit elimination (ASC 323 deferral of FTAI margin to extent of its ownership) is a diligence question [UNVERIFIED how FTAI treats].
- Q3: $450M therefore almost certainly BOTH (own turbine sales margin + pro-rata JV share). Not stated explicitly. [UNVERIFIED] Risk of double count of the same unit margin in Adj. EBITDA.
- Q1: Eastmoney report (https://data.eastmoney.com/report/info/AP202605011821893512.html, 2026-05) says JV formed 2026-04-30, plan ~100 Mod-1 units/yr in 2027; no percentages. Ownership % still undisclosed publicly in sources reached. 15% in transcript is a different SPV.
- Q4: pricing declined as commercially sensitive. Implied: $1.465B / ~100 units ~ $14.7M per unit J&F selling price IF the PO covers ~100 units (unit count NOT disclosed) [UNVERIFIED].
- Not reached: Stockstar article, 10jqka/cls Chinese pages (not read), FTAI press release (timeout).

## Recommended model inputs (judgment, not sourced facts)
| | Bear | Base | Bull |
|---|---|---|---|
| 2027 Power units delivered | 40 | 70 | 100+ |
| EBITDA per unit (FTAI share, $M) | 4.5 | 6.0 | 7.5 |
| Implied 2027 Power EBITDA ($M) | 180 | 420 | 750 |
| Cash conversion of Power EBITDA | 30% (JV equity income is non-cash; dividends lag) | 50% | 70% (advance payments) |
Rationale: $450M guide is "< 100 units"; $7-8M/unit unconfirmed; 2027 deliveries through Nov-2027 imply back-end loading; equity-method portion not cash until distributed; Jereh controls J&F.
