"""Reproducible GPK illustrative public-to-private underwriting.
Run: python3 model.py
Historical numbers: GPK FY2025 10-K; forward assumptions: independent analyst estimates.
No dependencies. Not investment advice.
"""
from math import isclose

SALES_2025 = 8617.0
EBIT_2025 = 804.0
DA_2025 = 536.0
EBITDA_2025 = EBIT_2025 + DA_2025
ENTRY_MULTIPLE = 6.25
ENTRY_LEVERAGE = 4.25
ENTRY_EV = EBITDA_2025 * ENTRY_MULTIPLE
INITIAL_DEBT = EBITDA_2025 * ENTRY_LEVERAGE
FEES = 0.02 * ENTRY_EV + 0.01 * INITIAL_DEBT
SPONSOR_EQUITY = ENTRY_EV - INITIAL_DEBT + FEES
TAX = 0.24
DA_PCT = 0.062
COVENANT = 5.5

CASES = {
    "Base": dict(growth=[.01,.02,.025,.025,.025], margins=[.16,.165,.17,.1725,.175],
                 capex=[.075,.065,.06,.055,.05], nwc=.012, interest=.085, exit_multiple=6.25),
    "Upside": dict(growth=[.03,.04,.04,.035,.03], margins=[.17,.18,.185,.19,.195],
                   capex=[.065,.055,.05,.05,.045], nwc=.010, interest=.080, exit_multiple=7.0),
    "Downside": dict(growth=[-.05,-.03,0,.01,.01], margins=[.14,.135,.14,.145,.15],
                     capex=[.09,.08,.07,.065,.06], nwc=.018, interest=.105, exit_multiple=5.0),
}

def model(case):
    sales, debt = SALES_2025, INITIAL_DEBT
    years = []
    for year, growth, margin, capex_pct in zip(
        range(2026,2031), case["growth"], case["margins"], case["capex"]
    ):
        previous_sales = sales
        sales *= 1 + growth
        ebitda = sales * margin
        da = sales * DA_PCT
        ebit = ebitda - da
        interest = debt * case["interest"]
        taxes = max(0., (ebit - interest) * TAX)
        capex = sales * capex_pct
        change_nwc = (sales - previous_sales) * case["nwc"]
        free_cash = ebitda - interest - taxes - capex - change_nwc
        debt = max(0., debt - free_cash)
        years.append(dict(year=year,sales=sales,ebitda=ebitda,ebit=ebit,da=da,
                          interest=interest,taxes=taxes,capex=capex,delta_nwc=change_nwc,
                          free_cash=free_cash,debt=debt,
                          covenant_headroom=COVENANT-debt/ebitda))
    exit_ev = years[-1]["ebitda"] * case["exit_multiple"]
    exit_equity = max(0.,exit_ev-debt)
    moic = exit_equity / SPONSOR_EQUITY
    irr = moic**(1/5)-1 if moic > 0 else -1.
    bridge = {
        "EBITDA growth": (years[-1]["ebitda"]-EBITDA_2025)*ENTRY_MULTIPLE,
        "Exit multiple": (case["exit_multiple"]-ENTRY_MULTIPLE)*years[-1]["ebitda"],
        "Deleveraging": INITIAL_DEBT-debt,
        "Fees": -FEES,
        "Limited-liability equity floor": max(0., debt-exit_ev)
    }
    assert isclose(sum(bridge.values()),exit_equity-SPONSOR_EQUITY,abs_tol=1e-6)
    return dict(years=years,irr=irr,moic=moic,exit_equity=exit_equity,
                exit_ev=exit_ev,bridge=bridge,
                min_headroom=min(y["covenant_headroom"] for y in years))

def dcf(case_result, wacc=.095, g=.02):
    assert wacc>g
    cashflows=[y["ebit"]*(1-TAX)+y["da"]-y["capex"]-y["delta_nwc"]
              for y in case_result["years"]]
    terminal=cashflows[-1]*(1+g)/(wacc-g)
    return sum(cf/(1+wacc)**yr for yr,cf in enumerate(cashflows,1))+terminal/(1+wacc)**5

if __name__=="__main__":
    results={name:model(case) for name,case in CASES.items()}
    for name,r in results.items():
        print(f"{name:8s}  IRR: {r['irr']:.2%} | MOIC: {r['moic']:.2f}x | "
              f"Exit debt: ${r['years'][-1]['debt']:,.0f}m | Covenant headroom: "
              f"{r['min_headroom']:+.2f}x")
    print(f"Base case DCF EV: ${dcf(results['Base']):,.0f}m")
    assert round(results["Base"]["irr"],4) == .1874
    assert round(results["Upside"]["irr"],4) == .3226
    assert results["Downside"]["moic"] == 0
