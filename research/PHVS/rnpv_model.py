import numpy as np, csv, itertools
S0=71.0; CASH=359.0; PX=31.0
def ramp(peakyr, launch, n=5):
    # fraction of peak by year 2027..2045
    out={}
    for y in range(2027,2046):
        if y<launch: f=0
        elif y<launch+n: f=(y-launch+1)/n
        elif y<=2040: f=1
        else: f=max(0,1-0.25*(y-2040))   # erosion after 2040
        out[y]=f
    return out
def model(p_share=0.18, od_share=0.45, intellia=0.08, price=330.0, raise_usd=250.0, raise_disc=0.10,
          r=0.11, p_xr=0.70, p_ir=0.90, margin=0.55, tax=0.20, od_pt_attacks=10, od_net=12.0,
          exus=0.35, pool_pro=7500, dx=8500, burn_pv=300.0, detail=False):
    # on-demand peak US sales ($M): patients*oral penetration(40% combined)*dpt share*attacks*net per attack($K)
    od_peak=dx*0.40*od_share*od_pt_attacks*od_net/1000*(1+exus)
    pro_pool=pool_pro*(1-intellia*dx/pool_pro) if pool_pro else 0   # intellia removes patients from chronic pool
    xr_peak=pro_pool*p_share*price/1000*(1+exus)
    rIR=ramp(0,2027,5); rXR=ramp(0,2028,5)
    npv_ir=npv_xr=0
    for y in range(2027,2046):
        t=y-2026.75
        d=(1+r)**-t
        npv_ir+=p_ir*od_peak*rIR[y]*margin*(1-tax)*d
        npv_xr+=p_xr*xr_peak*rXR[y]*margin*(1-tax)*d
    burn=burn_pv
    ev=npv_ir+npv_xr-burn
    eq=ev+CASH
    # dilution: need to raise raise_usd at discount to intrinsic per share
    v0=eq/S0
    newsh=raise_usd/(v0*(1-raise_disc)) if raise_usd>0 else 0
    v=(eq+raise_usd)/(S0+newsh) if raise_usd>0 else v0
    # cash raised funds burn already deducted => add back raised cash (done above); if no raise needed, v0
    res=dict(od_peak=od_peak,xr_peak=xr_peak,npv_ir=npv_ir,npv_xr=npv_xr,ev=ev,vps=v)
    return res
base=model()
print(base)
# reverse DCF: scale factor k on peaks so EV=1840
tgt_ev=PX*S0-CASH

class so:
    @staticmethod
    def brentq(f,a,b):
        for _ in range(200):
            m=(a+b)/2
            if f(a)*f(m)<=0: b=m
            else: a=m
        return (a+b)/2

def f(k):
    return model(p_share=0.18*k,od_share=0.45*k)['ev']-tgt_ev
k=so.brentq(f,0.01,5); m=model(p_share=0.18*k,od_share=0.45*k)
print('k',k,m, 'impl total peak', m['od_peak']+m['xr_peak'], 'prob-wtd', 0.9*m['od_peak']+0.7*m['xr_peak'])
# market-as-on-demand-only: what od peak alone (no XR) justifies EV?
def g(sh): return model(p_share=0,od_share=sh)['ev']-tgt_ev
k2=so.brentq(g,0.01,40); m2=model(p_share=0,od_share=k2); print('OD-only', k2,m2['od_peak'],0.9*m2['od_peak'])
def h(sh): return model(p_share=sh,od_share=0)['ev']-tgt_ev
k3=so.brentq(h,0.001,2); m3=model(p_share=k3,od_share=0); print('XR-only',k3,m3['xr_peak'])
rows=[]
def add(name,kw_with,kw_without,ev):
    a=model(**kw_with)['vps']; b=model(**kw_without)['vps']
    rows.append((name,a,b,a-b,ev))
add('Prophylaxis (XR) share 18% vs 0%',{}, dict(p_share=0),3)
add('On-demand (IR) 45% of oral-brand pool vs 0%',{},dict(od_share=0),3)
add('Intellia penetration 8% dx pts (counter) vs 0%',{},dict(intellia=0),2)
add('Net price $330K/pt-yr vs -30% ($231K)',{},dict(price=231.0,od_net=8.4),3)
add('Dilution $250M @10% disc vs none',{},dict(raise_usd=0),3)
for r_ in rows: print(r_)
for sc in [dict(p_share=0.06),dict(p_share=0.18),dict(p_share=0.04,od_share=0.25),dict(p_share=0.2,od_share=0.5,intellia=0.03),dict(r=0.10),dict(r=0.12),dict(p_xr=0.5),dict(intellia=0.15),dict(p_share=0.08,od_share=0.3,intellia=0.12,price=260,raise_usd=350,raise_disc=0.15),dict(p_share=0.18,od_share=0.5,intellia=0.04,price=360)]:
    print(sc, round(model(**sc)['vps'],1), round(model(**sc)['ev']))
