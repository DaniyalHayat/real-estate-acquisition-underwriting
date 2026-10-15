"""Curated public disclosures. Values are USD millions unless noted; no API keys."""
import csv, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
 'PK10K': {'url':'https://www.sec.gov/Archives/edgar/data/1617406/000161740626000006/pk-20251231.htm','date':'2026-02-20','title':'Park 2025 Form 10-K','location':'pp. 56–58 financial statements; pp. 14, 21–22 insurance and risk factors'},
 'PKER': {'url':'https://www.pkhotelsandresorts.com/~/media/Files/P/Park-Hotels/reports-and-presentations/q4-2025-earnings-press-release.pdf','date':'2026-02-19','title':'Park FY2025 earnings release','location':'pp. 3, 6, 12–16; non-GAAP reconciliations and debt'},
 'PKSUP': {'url':'https://www.pkhotelsandresorts.com/~/media/Files/P/Park-Hotels/reports-and-presentations/q4-25-supplemental-data.pdf','date':'2026-02-19','title':'Park Q4 2025 supplement','location':'pp. 19–20 current portfolio; p. 24 full-year core hotel results'},
 'HSTER': {'url':'https://www.hosthotels.com/-/media/HostHotels/Files/DownloadLinksAssets/QuarterlyEarnings/2025/Host_Hotels_Resorts_Inc_2025_Q4_Earnings.pdf','date':'2026-02-18','title':'Host FY2025 earnings release','location':'financial highlights and balance sheet'},
 'HSTSUP': {'url':'https://www.hosthotels.com/-/media/HostHotels/Files/DownloadLinksAssets/QuarterlySupplementals/2025/Host_Hotels_Resorts_Inc_2025_Q4_Supplemental.pdf','date':'2026-02-18','title':'Host Q4 2025 supplement','location':'Shares/Units, Security pricing and Capitalization table'},
 'PEBER': {'url':'https://investor.pebblebrookhotels.com/news-1/news-releases/news-details/2026/Pebblebrook-Hotel-Trust-Reports-2025-Results-and-Provides-2026-Outlook/default.aspx','date':'2026-02-25','title':'Pebblebrook FY2025 results','location':'balance sheet, results and LaPlaya recovery update'},
 'PKPRICE': {'url':'https://www.quiverquant.com/stock/PK/historical-prices/','date':'2025-12-31','title':'PK historical unadjusted closing price','location':'December 31, 2025 row; secondary market-data source'},
 'PEBPRICE': {'url':'https://www.quiverquant.com/stock/PEB/historical-prices/','date':'2025-12-31','title':'PEB historical unadjusted closing price','location':'December 31, 2025 row; secondary market-data source'},
 'HERSHA': {'url':'https://www.stblaw.com/about-us/news/view/2023/08/28/ksl-capital-partners-to-acquire-hersha-hospitality-trust','date':'2023-08-28','title':'KSL acquisition of Hersha — transaction counsel announcement','location':'$1.4bn transaction and 3,811 rooms'},
 'WATERMARK': {'url':'https://www.prnewswire.com/news-releases/watermark-lodging-trust-to-be-acquired-by-brookfield-real-estate-funds-301542036.html','date':'2022-05-06','title':'Watermark issuer acquisition announcement','location':'$3.8bn including debt and preferred equity; over 8,100 rooms'},
}
# Historical facts, not projections. Sign convention: expense/capex rows positive;
# net income and net cash flows retain reported signs.
HIST = {
 'room_revenue':[1653,1569,1505], 'food_revenue':[696,688,685], 'ancillary_revenue':[264,256,259], 'other_revenue':[85,86,92],
 'revenue':[2698,2599,2541], 'room_expense':[449,419,411], 'food_expense':[501,474,478], 'support_expense':[635,605,596],
 'property_expense':[241,231,216], 'management_fees':[126,125,118], 'impairment_casualty':[204,14,319], 'da':[287,257,336],
 'corporate_expense':[65,69,72], 'other_expense':[83,82,88], 'gain_asset_sale':[15,8,2], 'gain_derecognition':[221,60,58],
 'operating_income':[343,391,-33], 'interest_income':[38,21,10], 'interest_expense':[207,214,209], 'receivership_interest':[45,60,58],
 'affiliate_income':[11,31,4], 'other_gain':[4,-4,16], 'pretax_income':[144,165,-270], 'tax_expense':[38,-61,7],
 'net_income':[106,226,-277], 'cfo':[503,429,398], 'capex':[285,227,296], 'cfi':[-217,-166,-209], 'cff':[-475,-573,-365],
 'cash_begin_restricted':[939,750,440], 'cash_end_restricted':[750,440,264]
}
BALANCE = {'ppe':6955,'held_for_sale':14,'intangibles':41,'cash':232,'restricted_cash':32,'ar':116,'prepaids':60,'other_assets':80,'rou_assets':170,
 'debt_book':3838,'ap':198,'dividends_payable':56,'managers_payable':134,'other_liabilities':189,'lease_liabilities':209,'equity':3076,'assets':7700,'liabilities':4624,
 'debt_face':3856,'jv_debt':129,'shares':199.901086,'adjusted_ebitda':609,'jv_ebitda':19,'hotel_ebitda':644,'core_ebitda':586,'core_revenue':2006,'adjusted_ffo':394}
PROPS = [
 ['Hilton Hawaiian Village','HI',2872,405,142,'Coastal'],['Hilton Waikoloa Village','HI',661,117,33,'Coastal'],
 ['Signia Orlando Bonnet Creek','FL',1009,173,65,'Inland FL'],['Waldorf Astoria Orlando','FL',502,102,32,'Inland FL'],
 ['New York Hilton Midtown','NY',1878,309,58,'Urban'],['Hilton New Orleans Riverside','LA',1622,150,54,'Coastal'],
 ['Caribe Hilton','PR',652,92,25,'Coastal'],['Hilton Boston Logan','MA',604,64,16,'Urban'],['Hyatt Regency Boston','MA',502,52,18,'Urban'],
 ['Hilton Santa Barbara','CA',360,48,21,'Coastal'],['Hyatt Regency Mission Bay','CA',438,53,11,'Coastal'],
 ['Casa Marina Key West','FL',311,79,34,'Coastal'],['The Reach Key West','FL',150,32,12,'Coastal'],
 ['Hilton Chicago','IL',1544,140,25,'Urban'],['Hilton Denver City Center','CO',613,42,13,'Urban'],
 ['Royal Palm South Beach','FL',393,19,5,'Coastal'],['DoubleTree Crystal City','VA',627,39,8,'Urban'],
 ['Hilton McLean Tysons','VA',458,38,7,'Suburban'],['JW Marriott San Francisco','CA',344,38,5,'Urban'],
 ['Juniper Cupertino','CA',224,14,2,'Suburban']]
ASSUMPTIONS = {
 'entry_multiple':10.5,'exit_multiple':10.5,'senior_leverage':3.5,'junior_leverage':1.0,'senior_rate':0.075,'junior_rate':0.105,
 'senior_amort':0.01,'junior_amort':0.01,'cash_sweep':0.75,'min_cash':100,'fees_pct':0.02,'tax_rate':0.25,'wacc':0.095,'terminal_growth':0.025,
 'cap_rate':0.085,'reserve_pct':0.04,'max_leverage':6.0,'min_dscr':1.25,'hurdle':0.20,'asset_life':25,'new_capex_life':15,
 'property_damage':100,'bi_loss':20,'property_deductible':10,'combined_property_bi_limit':75,'claim_count':30,'claim_severity':0.4,'gl_retention':0.1,'gl_limit':2,
 'assumed_premium':15,'premium_increase':0.20,
 'scenarios': {
   'Base':{'room_growth':[.035,.04,.03,.025,.025],'food_growth':[.025,.03,.025,.025,.025],'other_growth':[.025]*5,'margin':[.245,.255,.265,.27,.27],'capex_pct':[.11,.09,.075,.07,.07],'nwc_pct':[-.06]*5,'rate_shock':[0]*5,'insured_event':[0]*5},
   'Upside':{'room_growth':[.055,.06,.045,.035,.03],'food_growth':[.04,.045,.035,.03,.03],'other_growth':[.04]*5,'margin':[.26,.275,.285,.29,.29],'capex_pct':[.10,.085,.07,.065,.065],'nwc_pct':[-.06]*5,'rate_shock':[-.005]*5,'insured_event':[0]*5},
   'Downside':{'room_growth':[-.08,-.03,.03,.03,.025],'food_growth':[-.07,-.03,.025,.025,.025],'other_growth':[-.05,-.02,.02,.02,.02],'margin':[.20,.185,.215,.23,.24],'capex_pct':[.11,.10,.08,.075,.075],'nwc_pct':[-.05]*5,'rate_shock':[.02]*5,'insured_event':[0,1,0,0,0]}
 }
}
def main():
 data=ROOT/'data'; data.mkdir(exist_ok=True)
 for name,obj in [('sources',SOURCES),('historical',HIST),('balance_2025',BALANCE),('assumptions',ASSUMPTIONS)]:
  (data/f'{name}.json').write_text(json.dumps(obj,indent=2)+'\n',encoding='utf-8')
 with (data/'properties.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['hotel','state','rooms','revenue_2025_m','hotel_ebitda_2025_m','analyst_exposure_category']);w.writerows(PROPS)
 with (data/'historical.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.writer(f);w.writerow(['metric','2023','2024','2025','source_id']);w.writerows([k,*v,'PK10K'] for k,v in HIST.items())
 peers=[{'ticker':'PK','price':10.46,'shares_m':199.901086,'net_debt_m':3721,'preferred_m':0,'nci_m':0,'ebitda_m':609,'ffo_ps':1.97,'basis':'Issuer pro rata net debt including JV debt and restricted cash; NCI immaterial book deficit excluded','source':'PKER;PK10K;PKPRICE'},
 {'ticker':'HST','price':17.73,'shares_m':697.4,'net_debt_m':4638,'preferred_m':0,'nci_m':0,'ebitda_m':1757,'ffo_ps':2.07,'basis':'Common shares including OP units; net debt includes $329m share of JV debt','source':'HSTSUP;HSTER'},
 {'ticker':'PEB','price':11.32,'shares_m':113.188134,'net_debt_m':1939.907,'preferred_m':676.724,'nci_m':94.117,'ebitda_m':342.5,'ffo_ps':1.58,'basis':'Book debt less unrestricted cash; preferred at liquidation value; NCI at book proxy, not market value','source':'PEBER;PEBPRICE'}]
 (data/'peers.json').write_text(json.dumps(peers,indent=2)+'\n',encoding='utf-8')
 print('Wrote curated facts, source register, assumptions, and property dataset.')
if __name__=='__main__': main()
