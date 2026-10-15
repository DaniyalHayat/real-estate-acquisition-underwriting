# Sources and data decisions

I use FY2025 financial disclosures and December 31, 2025 stock prices. This is a retrospective historical case study with an information cutoff of February 25, 2026, not a backtest claiming those full-year results were available at year-end. Research was assembled in October 2026; later operating results are deliberately outside the historical model.

- **PK10K** — [Park 2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1617406/000161740626000006/pk-20251231.htm), 2026-02-20. pp. 56–58 financial statements; pp. 14, 21–22 insurance and risk factors.
- **PKER** — [Park FY2025 earnings release](https://www.pkhotelsandresorts.com/~/media/Files/P/Park-Hotels/reports-and-presentations/q4-2025-earnings-press-release.pdf), 2026-02-19. pp. 3, 6, 12–16; non-GAAP reconciliations and debt.
- **PKSUP** — [Park Q4 2025 supplement](https://www.pkhotelsandresorts.com/~/media/Files/P/Park-Hotels/reports-and-presentations/q4-25-supplemental-data.pdf), 2026-02-19. pp. 19–20 current portfolio; p. 24 full-year core hotel results.
- **HSTER** — [Host FY2025 earnings release](https://www.hosthotels.com/-/media/HostHotels/Files/DownloadLinksAssets/QuarterlyEarnings/2025/Host_Hotels_Resorts_Inc_2025_Q4_Earnings.pdf), 2026-02-18. financial highlights and balance sheet.
- **HSTSUP** — [Host Q4 2025 supplement](https://www.hosthotels.com/-/media/HostHotels/Files/DownloadLinksAssets/QuarterlySupplementals/2025/Host_Hotels_Resorts_Inc_2025_Q4_Supplemental.pdf), 2026-02-18. Shares/Units, Security pricing and Capitalization table.
- **PEBER** — [Pebblebrook FY2025 results](https://investor.pebblebrookhotels.com/news-1/news-releases/news-details/2026/Pebblebrook-Hotel-Trust-Reports-2025-Results-and-Provides-2026-Outlook/default.aspx), 2026-02-25. balance sheet, results and LaPlaya recovery update.
- **PKPRICE** — [PK historical unadjusted closing price](https://www.quiverquant.com/stock/PK/historical-prices/), 2025-12-31. December 31, 2025 row; secondary market-data source.
- **PEBPRICE** — [PEB historical unadjusted closing price](https://www.quiverquant.com/stock/PEB/historical-prices/), 2025-12-31. December 31, 2025 row; secondary market-data source.
- **HERSHA** — [KSL acquisition of Hersha — transaction counsel announcement](https://www.stblaw.com/about-us/news/view/2023/08/28/ksl-capital-partners-to-acquire-hersha-hospitality-trust), 2023-08-28. $1.4bn transaction and 3,811 rooms.
- **WATERMARK** — [Watermark issuer acquisition announcement](https://www.prnewswire.com/news-releases/watermark-lodging-trust-to-be-acquired-by-brookfield-real-estate-funds-301542036.html), 2022-05-06. $3.8bn including debt and preferred equity; over 8,100 rooms.

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
