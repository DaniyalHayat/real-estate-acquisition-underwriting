# Using the Excel model

1. Open `excel/Park_Acquisition_Underwriting.xlsx` on GitHub, then click the **download arrow next to Raw**. Open the downloaded file in desktop Excel. GitHub does not provide an interactive Excel preview.
2. Start on Summary. Change **Assumptions!D5**: 1 = Base, 2 = Upside, 3 = Downside.
3. Edit blue inputs on Assumptions. Annual case drivers begin at row 44. The green Active Selection rows feed one forecast model.
4. Change entry and exit multiples on **Valuation!L7:L8**. Assumptions links to these actual input cells. The adjacent native two-variable Data Table recalculates IRR across entry/exit combinations.
5. In Excel, use **Formulas → Calculation Options → Automatic**. Avoid “Automatic Except for Data Tables” if you want the sensitivity matrix refreshed. Press **Ctrl+Alt+F9** to force a full recalculation on Windows.
6. Inspect Checks, the Debt covenant headroom rows and the required equity injections. A balanced spreadsheet can still describe an unattractive transaction.

This workbook has no Power Query or live market-data connection. **Data → Refresh All does not fetch new filings.** Update documented source cells manually after reviewing a new filing, or update the JSON/CSV source inputs and rebuild. The source register is on Historical and in docs/SOURCES.md.

README tables and PNG previews are saved views; they do not change when you edit your downloaded workbook. Regenerate published reports when assumptions change. The delivered workbook was recalculated and independently verified with the artifact engine; native desktop Excel execution was not available for verification.
