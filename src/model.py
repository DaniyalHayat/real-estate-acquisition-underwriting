"""Independent, standard-library underwriting engine; annual end-of-year cash flows."""
import json, csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name): return json.loads((ROOT/'data'/f'{name}.json').read_text(encoding='utf-8'))
def irr(flows):
    if not (any(x<0 for x in flows) and any(x>0 for x in flows)): return None
    def npv(rate): return sum(v/(1+rate)**i for i,v in enumerate(flows))
    lo,hi=-.999,10.
    if npv(lo)*npv(hi)>0: return None
    for _ in range(180):
        mid=(lo+hi)/2
        if npv(mid)>0: lo=mid
        else: hi=mid
    return (lo+hi)/2
def insurance(a):
    gross=a['property_damage']+a['bi_loss']
    recovery=min(max(gross-a['property_deductible'],0),a['combined_property_bi_limit'])
    gl_gross=a['claim_count']*a['claim_severity']
    gl_recovery=a['claim_count']*min(max(a['claim_severity']-a['gl_retention'],0),a['gl_limit'])
    return {'property_gross':gross,'property_recovery':recovery,'property_retained':gross-recovery,
            'gl_gross':gl_gross,'gl_recovery':gl_recovery,'gl_retained':gl_gross-gl_recovery,
            'premium_increment':a['assumed_premium']*a['premium_increase'],
            'cash_cost':gross-recovery+gl_gross-gl_recovery+a['assumed_premium']*a['premium_increase']}
def run(case='Base', overrides=None):
    a=load('assumptions'); b=load('balance_2025'); h=load('historical')
    a.update(overrides or {}); s=a['scenarios'][case]
    if not a['wacc']>a['terminal_growth']: raise ValueError('WACC must exceed terminal growth')
    ev=b['adjusted_ebitda']*a['entry_multiple']; fees=ev*a['fees_pct']
    initial_senior=b['adjusted_ebitda']*a['senior_leverage']; initial_junior=b['adjusted_ebitda']*a['junior_leverage']
    sponsor=ev+fees+a['min_cash']-initial_senior-initial_junior
    if sponsor<=0: raise ValueError('Sponsor equity must be positive')
    net_operating_assets=b['assets']-b['cash']-(b['liabilities']-b['debt_book'])
    purchase_adjustment=ev-net_operating_assets
    opening_ppe=b['ppe']+purchase_adjustment
    if opening_ppe<=0: raise ValueError('Invalid allocated property basis')
    senior,junior,cash=initial_senior,initial_junior,a['min_cash']
    ppe,equity,nwc=opening_ppe,sponsor-fees,b['ar']+b['prepaids']-b['ap']-b['managers_payable']
    revenues=[h[k][-1] for k in ['room_revenue','food_revenue','ancillary_revenue','other_revenue']]
    flows=[-sponsor]; years=[]; capex_so_far=0
    for i,year in enumerate(range(2026,2031)):
        revenues=[revenues[j]*(1+s[['room_growth','food_growth','other_growth','other_growth'][j]][i]) for j in range(4)]
        revenue=sum(revenues); insurance_cost=s['insured_event'][i]*insurance(a)['cash_cost']
        ebitda=revenue*s['margin'][i]-insurance_cost
        capex=revenue*s['capex_pct'][i]
        da=min(ppe+capex,opening_ppe/a['asset_life']+capex_so_far/a['new_capex_life']+capex/(2*a['new_capex_life']))
        interest=senior*(a['senior_rate']+s['rate_shock'][i])+junior*(a['junior_rate']+s['rate_shock'][i])
        ebit=ebitda-da; taxes=max(ebit-interest,0)*a['tax_rate']; net_income=ebit-interest-taxes
        new_nwc=revenue*s['nwc_pct'][i]; dnwc=new_nwc-nwc
        cfo=net_income+da-dnwc; pre_debt_cash=cfo-capex
        senior_amort=min(senior,initial_senior*a['senior_amort']); junior_amort=min(junior,initial_junior*a['junior_amort'])
        mandatory=senior_amort+junior_amort
        equity_call=max(a['min_cash']-(cash+pre_debt_cash-mandatory),0)
        sweep_budget=max(cash+pre_debt_cash+equity_call-mandatory-a['min_cash'],0)*a['cash_sweep']
        senior_sweep=min(senior-senior_amort,sweep_budget)
        junior_sweep=min(junior-junior_amort,sweep_budget-senior_sweep)
        repayment=mandatory+senior_sweep+junior_sweep
        senior-=senior_amort+senior_sweep; junior-=junior_amort+junior_sweep
        end_cash=cash+pre_debt_cash+equity_call-repayment
        ppe+=capex-da; equity+=net_income+equity_call
        ar=revenue*b['ar']/h['revenue'][-1]; prepaid=revenue*b['prepaids']/h['revenue'][-1]
        operating_payables=ar+prepaid-new_nwc
        assets=end_cash+ppe+ar+prepaid+337
        liabilities=senior+junior+operating_payables+454
        ufcf=ebit-max(ebit,0)*a['tax_rate']+da-capex-dnwc
        dscr=(ebitda-taxes-capex-dnwc)/(interest+mandatory)
        debt=senior+junior; leverage=debt/ebitda if ebitda>0 else None
        years.append(dict(year=year,revenue=revenue,ebitda=ebitda,insurance_cost=insurance_cost,capex=capex,da=da,ebit=ebit,
          interest=interest,taxes=taxes,net_income=net_income,nwc=new_nwc,dnwc=dnwc,cfo=cfo,ufcf=ufcf,
          senior_amort=senior_amort,junior_amort=junior_amort,senior_sweep=senior_sweep,junior_sweep=junior_sweep,
          equity_call=equity_call,senior=senior,junior=junior,debt=debt,cash=end_cash,ppe=ppe,equity=equity,ar=ar,prepaid=prepaid,
          payables=operating_payables,assets=assets,liabilities=liabilities,balance_check=assets-liabilities-equity,dscr=dscr,leverage=leverage))
        flows.append(-equity_call); cash=end_cash;nwc=new_nwc;capex_so_far+=capex
    exit_ev=years[-1]['ebitda']*a['exit_multiple']; exit_equity=max(exit_ev+cash-senior-junior,0)
    flows[-1]+=exit_equity
    terminal=years[-1]['ufcf']*(1+a['terminal_growth'])/(a['wacc']-a['terminal_growth'])
    dcf=sum(y['ufcf']/(1+a['wacc'])**(i+1) for i,y in enumerate(years))+terminal/(1+a['wacc'])**5
    invested=sponsor+sum(y['equity_call'] for y in years)
    bridge={'initial_equity':sponsor,'ebitda_growth':(years[-1]['ebitda']-b['adjusted_ebitda'])*a['entry_multiple'],
       'multiple_change':years[-1]['ebitda']*(a['exit_multiple']-a['entry_multiple']),
       'deleveraging':initial_senior+initial_junior-senior-junior,'cash_change':cash-a['min_cash'],'fees':-fees}
    return dict(case=case,entry_ev=ev,fees=fees,sponsor_equity=sponsor,purchase_adjustment=purchase_adjustment,opening_ppe=opening_ppe,
       initial_debt=initial_senior+initial_junior,years=years,exit_ev=exit_ev,exit_equity=exit_equity,irr=irr(flows),moic=exit_equity/invested,
       dcf_ev=dcf,dcf_equity=dcf+b['cash']-b['debt_face'],flows=flows,bridge=bridge,insurance=insurance(a),
       min_dscr=min(y['dscr'] for y in years),max_leverage=max(y['leverage'] for y in years),total_equity_calls=invested-sponsor)
def main():
    results=[run(c) for c in ['Base','Upside','Downside']]
    target=ROOT/'reports';target.mkdir(exist_ok=True)
    (target/'model_results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    with (target/'scenario_summary.csv').open('w',newline='',encoding='utf-8') as f:
      keys=['case','entry_ev','sponsor_equity','exit_equity','irr','moic','dcf_ev','min_dscr','max_leverage','total_equity_calls']
      w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:r[k] for k in keys} for r in results)
    for r in results: print(r['case'], {k:round(r[k],4) for k in ['irr','moic','min_dscr','max_leverage','total_equity_calls']})
if __name__=='__main__': main()
