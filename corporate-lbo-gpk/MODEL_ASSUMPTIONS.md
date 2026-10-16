# Model Inputs, Checks and Return Equations

**All values USD millions; historical GPK 10-K unless marked assumption.**

| Input | Value | Nature |
|---|---:|---|
| FY2025 sales | 8,617 | Reported |
| FY2025 EBIT | 804 | Reported |
| FY2025 D&A | 536 | Reported |
| FY2025 unadjusted EBITDA | 1,340 | Calculated, EBIT + D&A |
| Entry EV/EBITDA | 6.25x | Hypothetical |
| Entry acquisition leverage | 4.25x | Hypothetical |
| Transaction fees | 2% EV | Hypothetical |
| Debt financing fees | 1% new debt | Hypothetical |
| Tax rate | 24% | Hypothetical |
| Forecast D&A | 6.2% of revenue | Hypothetical |
| WACC / terminal growth | 9.5% / 2.0% | Hypothetical |
| Illustrative leverage covenant | 5.5x | Hypothetical, **not actual credit agreement** |

## Exact calculations
- Entry EV = 1,340 × 6.25 = **8,375**.
- Acquisition debt = 1,340 × 4.25 = **5,695**.
- Sponsor equity = 8,375 × 1.02 + 5,695 × 0.01 − 5,695 = **2,904.45**.
- Per forecast year: Sales = last-year Sales × (1+growth); EBITDA = Sales × EBITDA margin; D&A = 6.2% × Sales; EBIT = EBITDA − D&A; interest = beginning acquisition debt × case rate; tax = max[0, (EBIT − interest) × 24%]; capex = case % × Sales; cash NWC = case % × (Sales − prior-year Sales); cash available for debt = EBITDA − interest − tax − capex − cash NWC; closing debt = max[0, beginning debt − cash available].
- Exit EV = final-year EBITDA × case exit multiple. Sponsor equity exit = max[0, EV − debt]; MOIC = exit equity / entry sponsor equity; annualized gross IRR = MOIC^(1/5) − 1 (or −100% if equity is fully written off).
- Covenant headroom = 5.5x − ending acquisition debt / current year EBITDA. This is an *illustration*, not a contractual covenant calculation.
- Equity return attribution ($): (Exit EBITDA−Entry EBITDA)×entry multiple + (Exit multiple−Entry multiple)×exit EBITDA + (Entry debt−Exit debt) − transaction and financing fees + limited-liability floor adjustment. This equals exit sponsor equity−entry sponsor equity exactly.
- Unlevered FCF = EBIT×(1−24%) + D&A − capex − ΔNWC. DCF EV = discounted FCF years 1–5 + [FCF year 5×(1+g)/(WACC−g)] discounted by (1+WACC)^5.

**Measured results:** Base 18.74% IRR / 2.3603x; upside 32.26% / 4.0471x; downside -100% / zero. Base ending debt $3,600.8m. Base DCF enterprise value $10,864.5m.

## Known limitations
Not a fully balanced three-statement forecast; debt fees treated as initial cash uses; no dividends or refinancing, optional PIK, ABL, revolver availability, OID, amortization or tax losses; growth in negative working capital is modeled as cash release; no pro forma purchase accounting, management incentive equity or complete equity bridge. The entry EV multiple and covenant limit are assumptions, not observed market pricing. A real investment bank/PE underwriting case would add actual public comps, transaction comps with deal dates/sources, and a QoE / credit-agreement review.

**Public historical source:** https://www.sec.gov/Archives/edgar/data/1408075/000140807526000009/gpk-20251231.htm
