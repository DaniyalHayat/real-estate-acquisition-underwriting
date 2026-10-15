"""Generate the published narrative from the model's saved results."""
import json
from pathlib import Path
from model import run, load, ROOT
def save(name,text):
 p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.strip()+'\n',encoding='utf-8')
def main():
 results=[run(c) for c in ['Base','Upside','Downside']];base=results[0]
 table='| Case | Five-year IRR | MOIC | Minimum DSCR | Peak debt / EBITDA | Additional equity |\n|---|---:|---:|---:|---:|---:|\n'
 for x in results:table+=f"| {x['case']} | {x['irr']:.1%} | {x['moic']:.2f}x | {x['min_dscr']:.2f}x | {x['max_leverage']:.2f}x | ${x['total_equity_calls']:,.1f}m |\n"
 sources=load('sources')
 source_text='\n'.join(f"- **{k}** — [{v['title']}]({v['url']}), {v['date']}. {v['location']}." for k,v in sources.items())
 save('docs/SOURCES.md',f'''# Sources and data decisions

I use FY2025 financial disclosures and December 31, 2025 stock prices. This is a retrospective historical case study with an information cutoff of February 25, 2026, not a backtest claiming those full-year results were available at year-end. Research was assembled in October 2026; later operating results are deliberately outside the historical model.

{source_text}

## Input classification

| Data | Treatment |
|---|---|
| Historical statements, hotel revenue, hotel EBITDA and rooms | Public issuer facts, manually transcribed and reconciled |
| PK and PEB year-end prices | Secondary price-history data; unadjusted closes, not total-return adjusted prices |
| HST price and economic shares | Issuer supplement; includes OP units in economic equity |
| Operating growth, margins, financing, WACC and cap rates | My editable underwriting assumptions |
| Insurance terms, severity, frequency and premium | Illustrative stress assumptions; not disclosed Park policy terms |
| Property exposure tags | My geographic screening categories, not insurer hazard scores |

The model includes selected numerical facts and citations rather than redistributing full annual reports. I do not claim Bloomberg access or use. The core-property roster is dated February 19, 2026 and its operating results cover 2025. The comparable universe includes Park, Host and Pebblebrook; the two other companies are directional peers, not a statistically robust valuation sample.

Park reports $609m adjusted EBITDA, comprising $644m hotel adjusted EBITDA, $19m affiliate EBITDA and a $54m corporate/other deduction. That bridge is distinct from GAAP operating income. Reported FFO is shown in the comparable screen; the taxable acquisition forecast is not presented as issuer FFO or AFFO.
''')
 save('docs/METHODOLOGY.md','''# Modeling methodology and limits

## Scope and accounting

I evaluate a hypothetical acquisition of Park as an aggregated operating platform. The 13-sheet Excel model contains an income statement on Operating, cash-flow and balance-sheet schedules on Statements, a two-tranche financing schedule, DCF, LBO returns, trading comparisons, transaction references, and core-property valuations. These are analytical pro forma statements, not a GAAP acquisition accounting opinion.

The acquisition assumes a taxable corporate structure with 25% cash tax on positive pretax income. It does not preserve REIT tax treatment or apply a REIT distribution requirement. A real transaction would need tax counsel, taxable REIT subsidiary analysis, state taxes, interest deduction limits, NOLs, transfer taxes and transaction-specific structuring. These could materially change returns.

Sources and uses treat entry EV as a cash-free/debt-free economic purchase price, add $100m opening cash and 2% fees, then fund uses with senior debt, junior debt and sponsor equity. The property-basis adjustment equals entry EV less historical net operating assets; it is allocated to PP&E and can be negative. Fees are expensed at closing and reduce opening book equity. This is an explicit simplifying allocation, not an appraisal, goodwill test or arbitrary balance-sheet plug. All operating equity is treated as acquired; no separate minority distribution schedule is projected.

The operating model is aggregated: it uses corporate adjusted EBITDA as its starting valuation metric but consolidates projections into one platform. Unconsolidated JV distributions, debt and minority interests are not separately modeled. The indicative offer-price and public-comps bridges include JV debt where disclosed; the DCF bridge subtracts consolidated face debt only. Consequently DCF per-share values are a consolidated proxy, not a directly comparable pro rata fair-value opinion. This scope difference is deliberate and must be resolved before any executable bid. Assumed EV multiples are not claimed to be quoted acquisition terms.

## Operating drivers and cash conversion

Rooms, food and beverage, ancillary, and other revenue grow separately. Annual normalized EBITDA margins incorporate an assumed recovery and cost structure; I do not extrapolate impairment losses as recurring expenses. The forecast does not explicitly underwrite individual dispositions or renovation reopenings. The reported FY2025 portfolio is the anchor and scenario assumptions are my own, not management guidance.

Capex is an editable percentage of revenue. Depreciation uses the allocated opening property basis over 25 years and new capex over 15 years with a half-year convention. This simplifies land, asset classes and remaining useful lives. Working capital is receivables plus prepaids less operating payables; a negative balance represents operating funding. Receivable and prepaid ratios remain at 2025 levels and payables reconcile to the selected working-capital target. Other assets and liabilities are held constant and clearly identified.

Debt interest uses beginning-of-year balances to avoid circularity. Mandatory amortization is 1% of original senior and junior balances, capped at outstanding debt. Excess cash above the $100m minimum is swept 75%, senior first, then junior. Cash deficits generate explicit sponsor equity calls rather than negative cash or hidden borrowing. There are no interim distributions. Exit occurs at the end of 2030; IRR includes closing equity, later equity calls and exit proceeds. MOIC divides proceeds by all invested equity. The return bridge reconciles dollar value; equity-funded cash retention is not described as investment profit.

## Credit interpretation

DSCR = (EBITDA − cash taxes − capex − increase in operating working capital) / (cash interest + mandatory principal). Gross leverage = ending debt / annual EBITDA. The 1.25x minimum DSCR and 6.0x maximum leverage are assumed screening thresholds, not Park's actual loan covenants. Coverage below one means the modeled annual cash flow does not fund scheduled debt service without support. Year-end leverage can understate intrayear stress; timing of hotel seasonality, insurance collections and collateral release remains diligence work.

## Valuation

DCF uses year-end unlevered free cash flows, 9.5% WACC and 2.5% perpetual growth. Tax is applied to positive EBIT for the unlevered calculation. Terminal cash flow grows the final forecast year; normalization of maintenance capex and depreciation should be revisited in a real underwriting.

The native Excel two-input Data Table changes the actual entry and exit multiple cells on Valuation. Its other operating and financing inputs remain at the selected scenario. The Base/Upside/Downside selector recalculates one model; CSV and README scenario comparisons are saved results that must be regenerated after edits.

Trading EV uses each issuer's disclosed capital structure where possible. HST includes OP-unit equity and pro rata JV debt. PEB includes preferred liquidation value and a book-NCI proxy. PK uses issuer net debt, including restricted cash and JV debt. The different EBITDA definitions, NCI measurement and cash treatment limit precision. I do not average peers into a definitive offer.

Transaction references use announced consideration and rooms to calculate approximate value per key. Watermark's disclosed room count is 'over 8,100'; using 8,100 provides an approximate upper bound. EBITDA multiples are not invented. Neither precedent is directly comparable without adjustments for location, quality, leaseholds, capex and transaction date.

Property NAV values only 20 core hotels using hotel adjusted EBITDA less a 4% revenue FF&E reserve, capitalized at 8.5%. This is an analyst NOI proxy and a gross core-property value. It excludes non-core hotels, JVs, corporate overhead, sale costs and debt, so it is not whole-company equity NAV. The worksheet title identifies the analysis category; the output labels define the narrower quantity.

## Property and casualty stress

The owner-side stress assumes $100m damage plus $20m business interruption, a $10m combined deductible and $75m combined insurer limit. The resulting $45m retained loss is supplemented by $3m retained general-liability losses and $3m premium inflation: $51m incremental cost in downside 2027. These are assumed contract terms, not verified Park coverage. Base operating expenses already contain ordinary insurance costs; only incremental stress is added.

The model assumes immediate insurance recovery and cash-funded restoration, expensing the net event cost. It does not separately capitalize restoration costs or reduce property basis for damage, avoiding a second charge in this simplified treatment. Real claims require policy-specific valuation, waiting periods, exclusions, aggregates, sublimits, recovery delays and accounting analysis.

This work supports questions asked in real-estate credit and commercial insurance reviews. It is not carrier pricing, actuarial reserving, a middle-market loss model, or a claim that a large public REIT is itself a middle-market insured.
''')
 lo,hi=5.,12.
 for _ in range(60):
  mid=(lo+hi)/2
  if run(overrides={'entry_multiple':mid})['irr']>.2:lo=mid
  else:hi=mid
 threshold=(lo+hi)/2
 save('docs/INVESTMENT_COMMITTEE.md',f'''# Investment committee memorandum

**Park Hotels & Resorts | Historical acquisition case study**  
**Author: Daniyal Hayat | Financial base: FY2025 | Information cutoff: February 25, 2026**

## My recommendation

**Reprice or restructure before advancing.** At an assumed 10.5x entry and exit multiple, the base case generates a {base['irr']:.1%} five-year sponsor IRR and {base['moic']:.2f}x MOIC, below my assumed 20% return hurdle. The upside case also misses that hurdle. The downside case requires $295.4m of additional equity and produces a capital loss. I would not support approval on these terms without stronger evidence of operating recovery, a lower purchase price, and a credible liquidity plan.

{table}

These are model outputs, not achieved investment returns. Entry EV is $6,394.5m; closing sponsor equity is $3,881.9m. The financing assumes 3.5x senior and 1.0x junior leverage against $609m reported adjusted EBITDA, at 7.5% and 10.5% interest respectively.

## Investment thesis and evidence

I chose a hotel REIT because property quality alone does not establish investment value: capital expenditure, debt service and cyclical demand determine how much cash reaches owners. Park's disclosed core portfolio gives me a way to compare property earnings with consolidated financing needs. The 20 core hotels generated $586m of hotel adjusted EBITDA on $2,006m of revenue in 2025. Hawaii, Florida and Puerto Rico introduce meaningful geographic and weather exposure. The core hotel list supports property-level screening; it does not prove insurability or replace catastrophe modeling. [Park supplemental data]({sources['PKSUP']['url']})

Park's 2025 revenue was $2,541m, adjusted EBITDA $609m, operating cash flow $398m and capex $296m. The $277m reported net loss included substantial impairment expense, so I distinguish operating recovery from accounting charges. The gap between EBITDA and cash after capex is central to my debt-capacity assessment. [2025 Form 10-K]({sources['PK10K']['url']}), [earnings reconciliation]({sources['PKER']['url']})

The thesis is that improving hotel demand and renovation productivity could expand margins and fund debt repayment. I encode that as a testable assumption, not a guaranteed catalyst. The base margin rises from 24.5% in 2026 to 27.0% in 2030, while capex declines from 11.0% to 7.0% of revenue. If assets need sustained elevated investment, that thesis weakens.

## Valuation and capital structure

The base DCF indicates approximately ${base['dcf_ev']:,.1f}m enterprise value, below assumed entry EV. It uses a taxable corporate structure; retaining REIT status would need a different tax and distribution model. Trading comparisons with Host and Pebblebrook and two announced hotel acquisition precedents provide context, with explicit differences in capital structure and asset mix. I do not treat a median multiple as sufficient support for a purchase price.

Holding the base operating forecast, 4.5x initial debt and 10.5x exit multiple constant, the independent model reaches the assumed 20% hurdle near **{threshold:.2f}x entry EBITDA**. This is a sensitivity result, not a recommended executable bid; the model's purchase-basis simplification also changes depreciation with entry price.

## Credit and insurance downside

The base minimum DSCR is only 1.27x versus a 1.25x screening threshold. In the downside, recessionary revenue and margins, a 200bp rate increase and the illustrative $51m retained insurance cost lower minimum DSCR to 0.46x; peak gross leverage reaches 7.21x. This requires sponsor support even though the spreadsheet keeps cash above its minimum.

The insurance scenario links property damage, business interruption, general liability retentions and premium inflation to liquidity. Public filings establish that these exposures exist, but they do not provide the loss runs or detailed policy terms needed to price a commercial casualty account. Pebblebrook's public LaPlaya discussion offers a real example of operational disruption and insurance recoveries, without being used as Park loss experience. [Park 10-K]({sources['PK10K']['url']}), [Pebblebrook results]({sources['PEBER']['url']})

## Diligence conditions

1. Validate hotel-level operating budgets, renovation schedules, maintenance capex and the effect of planned dispositions.
2. Obtain lender terms, debt payoff and change-of-control provisions, collateral valuations and monthly liquidity forecasts.
3. Reconcile consolidated versus JV economics, minority interests and cash distributions before converting enterprise value into a binding equity bid.
4. Determine viable REIT / taxable corporate structure and quantify transfer taxes, interest limitations and purchase accounting.
5. Review five years of loss runs, property schedules, construction and protection details, policy wording, retentions, aggregates and insurer recoverability.
6. Reassess entry price against downside cash needs and negotiate financing that does not depend on uninterrupted recovery.

My decision would change with verified operating improvements, lower total purchase cost or financing that materially reduces downside funding needs. See [methodology](METHODOLOGY.md) for the full scope and accounting limitations.
''')
 save('docs/EXCEL_GUIDE.md','''# Using the Excel model

1. Open `excel/Park_Acquisition_Underwriting.xlsx` on GitHub, then click the **download arrow next to Raw**. Open the downloaded file in desktop Excel. GitHub does not provide an interactive Excel preview.
2. Start on Summary. Change **Assumptions!D5**: 1 = Base, 2 = Upside, 3 = Downside.
3. Edit blue inputs on Assumptions. Annual case drivers begin at row 44. The green Active Selection rows feed one forecast model.
4. Change entry and exit multiples on **Valuation!L7:L8**. Assumptions links to these actual input cells. The adjacent native two-variable Data Table recalculates IRR across entry/exit combinations.
5. In Excel, use **Formulas → Calculation Options → Automatic**. Avoid “Automatic Except for Data Tables” if you want the sensitivity matrix refreshed. Press **Ctrl+Alt+F9** to force a full recalculation on Windows.
6. Inspect Checks, the Debt covenant headroom rows and the required equity injections. A balanced spreadsheet can still describe an unattractive transaction.

This workbook has no Power Query or live market-data connection. **Data → Refresh All does not fetch new filings.** Update documented source cells manually after reviewing a new filing, or update the JSON/CSV source inputs and rebuild. The source register is on Historical and in docs/SOURCES.md.

README tables and PNG previews are saved views; they do not change when you edit your downloaded workbook. Regenerate published reports when assumptions change. The delivered workbook was recalculated and independently verified with the artifact engine; native desktop Excel execution was not available for verification.
''')
 save('docs/VALIDATION.md','''# Validation

- 14 Python tests cover historical controls, all-case balance sheets, debt and cash roll-forwards, IRR NPV, return bridges, sweep priority, direction of interest/valuation changes, insurance limits and invalid DCF assumptions.
- 24 key outputs (8 per scenario) reconcile between independent Python calculations and Excel formulas within 0.00001.
- A later-year growth edit was confirmed to change forecast returns, then restored.
- The native sensitivity base point and an off-base corner reconcile to actual model input changes.
- Exported workbook checks inspect formula caches, errors, chart presence, data-table XML and all-case controls. Worksheet previews were reviewed for legibility.
- All 13 worksheets and two additional long-sheet sections have saved previews. These are rendered workbook previews, not screenshots of native Excel.

These checks establish internal consistency within stated assumptions, not that forecasts or valuation inputs will prove correct. Native desktop Excel was not executed in this environment.
''')
 gallery=[('summary','Selected-case decision','Returns, liquidity and the five-year operating profile.'),('assumptions','Underwriting assumptions','Editable financial and insurance inputs.'),('scenario_drivers','Scenario drivers','One selected case flows through the model.'),('transaction','Sources and uses','Purchase funding and explicit property-basis allocation.'),('operating','Operating statement','Revenue drivers, margins, taxes and free cash flow.'),('debt','Debt and coverage','Amortization, senior-first sweep, equity calls and assumed covenant headroom.'),('statements','Cash flow and balance sheet','Integrated schedules with visible reconciliation.'),('valuation','DCF and LBO valuation','IRR, MOIC, return attribution and native Excel sensitivity.'),('property_nav','Core-property valuation','20 real hotels with reserve-adjusted earnings and illustrative cap rates.'),('insurance','Insurance cash-flow stress','Assumed coverage recoveries, retained losses and incremental premiums.'),('comps','Public trading comparisons','PK, HST and PEB with dated capital-structure inputs.'),('precedents','Transaction references','Hersha and Watermark announced value-per-key context.'),('historical','Historical operating data','2023–2025 public financial statement inputs.'),('balance_inputs','Historical balance sheet inputs','2025 balance sheet and REIT metrics.'),('checks','Reconciliation checks','Funding, cash, debt, statements and return bridge controls.')]
 gallery_md='\n'.join(f'<details>\n<summary><strong>{title}</strong> — {desc}</summary>\n\n![{title}](assets/{name}.png)\n\n</details>\n' for name,title,desc in gallery)
 save('README.md',f'''# Real Estate Acquisition Underwriting & Investment Analysis

## Park Hotels & Resorts | Public-company case study

I built this project to connect investment valuation with the questions that matter after a deal closes: how properties generate cash, how much debt that cash can support, and how operating or insurance losses affect equity value. I use Park Hotels & Resorts' public disclosures to examine a hypothetical acquisition from investment, real-estate, credit and risk perspectives.

**Excel · Python · Three-statement modeling · DCF · LBO · REIT analysis · Property valuation · Credit coverage · Insurance exposure**

[Download the Excel model](excel/Park_Acquisition_Underwriting.xlsx) · [Read my investment committee memo](docs/INVESTMENT_COMMITTEE.md) · [Sources](docs/SOURCES.md) · [Methodology](docs/METHODOLOGY.md) · [Excel guide](docs/EXCEL_GUIDE.md)

**To open Excel:** on the workbook's GitHub page, click the **download arrow next to Raw**, then open the downloaded file in desktop Excel. The previews below let you inspect every sheet without downloading.

![Acquisition analysis summary](assets/summary.png)

## My conclusion

**Reprice or restructure.** At the assumed 10.5x entry/exit multiples, the base case falls short of my 20% sponsor IRR hurdle. The downside requires additional equity and breaches assumed coverage and leverage thresholds. I kept that outcome visible because the purpose of underwriting is to test a transaction, not manufacture a target return.

{table}

Results are illustrative, not realized. The model uses FY2025 disclosures with a February 25, 2026 information cutoff and December 31, 2025 pricing. It is a retrospective case study, not a current stock recommendation or point-in-time backtest.

## How I approached the work

- **Start with evidence.** I separated issuer financial facts, historical stock prices and my assumptions. Numerical inputs trace to a source register.
- **Connect earnings to cash.** I projected revenue, EBITDA, taxes, working capital and capex, then linked financing to the cash-flow and balance-sheet schedules.
- **Make downside funding visible.** Two debt tranches amortize and sweep cash in priority order; shortfalls generate explicit sponsor equity calls.
- **Look through to properties.** I analyzed 20 core hotels using disclosed property earnings and a reserve-adjusted NOI proxy, alongside trading comparisons and two acquisition references.
- **Translate risk into dollars.** I connected assumed property damage, business interruption and liability retentions to cash flow and debt coverage.
- **Check the model independently.** I compared Excel outputs against a separate Python engine and tested sensitivities, balance sheets, debt roll-forwards and insurance limits.

The acquisition assumes a taxable corporate structure. The property table is a gross **core-property** valuation, not whole-company NAV. The insurance module is an **owner-side stress assessment**, not insurer pricing or actuarial reserving. The model aggregates JV economics and uses a simplified purchase-basis allocation; those limits are documented in the [methodology](docs/METHODOLOGY.md).

## Workbook walkthrough

There are 13 formula-driven worksheets. Long sheets include additional section previews. These images are saved workbook renders; changing an Excel input does not update the images or this README.

{gallery_md}

## Reproduce the analysis

Python 3.11+ is sufficient for the independent financial model; it has no third-party dependencies.

```bash
python src/model.py
python -m unittest discover -s tests -v
python src/write_docs.py
```

Curated inputs live in `data/`. `src/prepare_data.py` recreates the original public-data snapshot and resets assumptions to the delivered version; do not run it over inputs you intend to preserve. `reports/` contains generated results and workbook validation receipts.

The supplied `.xlsx` works without Python. Its authoring source, `src/build_workbook.mjs`, uses `@oai/artifact-tool` in the Codex bundled runtime. That authoring dependency is not needed to use Excel or reproduce the Python results; it must be available to regenerate the workbook and previews. After changing data: run the Python engine, rebuild the workbook in that runtime, run verification, then regenerate the memo/README.

## Files and evidence

| Folder | Contents |
|---|---|
| `excel/` | Editable 13-sheet model |
| `data/` | Historical inputs, assumptions, properties, peers and source register |
| `src/` | Independent model, workbook authoring and narrative generation |
| `tests/` | 14 financial consistency and stress tests |
| `reports/` | Scenario results and validation records |
| `docs/` | Investment memo, methodology, sources and Excel instructions |
| `assets/` | Every worksheet preview |

I use public company data and clearly labeled assumptions. This is my independent portfolio case study; it is not sponsored by Park or presented as a completed transaction or an institutional investment recommendation.
''')
 save('.gitignore','node_modules/\n__pycache__/\n*.pyc\n*.inspect.ndjson\n.DS_Store\n')
 save('.github/workflows/model-tests.yml','''name: Financial model checks
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python -m unittest discover -s tests -v
      - run: python src/model.py
''')
 print('Generated first-person README, IC memo, sources, methodology and Excel guide.')
if __name__=='__main__':main()
