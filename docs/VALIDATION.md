# Validation

- 14 Python tests cover historical controls, all-case balance sheets, debt and cash roll-forwards, IRR NPV, return bridges, sweep priority, direction of interest/valuation changes, insurance limits and invalid DCF assumptions.
- 24 key outputs (8 per scenario) reconcile between independent Python calculations and Excel formulas within 0.00001.
- A later-year growth edit was confirmed to change forecast returns, then restored.
- The native sensitivity base point and an off-base corner reconcile to actual model input changes.
- Exported workbook checks inspect formula caches, errors, chart presence, data-table XML and all-case controls. Worksheet previews were reviewed for legibility.
- All 13 worksheets and two additional long-sheet sections have saved previews. These are rendered workbook previews, not screenshots of native Excel.

These checks establish internal consistency within stated assumptions, not that forecasts or valuation inputs will prove correct. Native desktop Excel was not executed in this environment.
