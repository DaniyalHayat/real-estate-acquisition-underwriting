"""Inspect exported XLSX XML without modifying the workbook."""
import json,zipfile,xml.etree.ElementTree as E
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NS={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def main():
 with zipfile.ZipFile(ROOT/'excel/Park_Acquisition_Underwriting.xlsx') as z:
  errors=[];formulas=0;data_tables=0;empty_cache=[]
  sheets=[x for x in z.namelist() if x.startswith('xl/worksheets/sheet') and x.endswith('.xml')]
  for p in sheets:
   xml=E.fromstring(z.read(p))
   for c in xml.findall('.//s:c',NS):
    if c.attrib.get('t')=='e':errors.append([p,c.attrib['r'],c.findtext('s:v',namespaces=NS)])
    f=c.find('s:f',NS)
    if f is not None:
     formulas+=1
     if f.attrib.get('t')=='dataTable':data_tables+=1
     elif c.find('s:v',NS) is None and c.attrib.get('t')!='inlineStr':empty_cache.append([p,c.attrib['r']])
  assert len(sheets)==13 and formulas>600 and data_tables==1,(len(sheets),formulas,data_tables)
  assert not errors,errors
  # All visible base-case check cells must have numerical zero caches.
  checks=E.fromstring(z.read('xl/worksheets/sheet13.xml'));checked=0
  for c in checks.findall('.//s:c',NS):
   address=c.attrib['r'];col=''.join(x for x in address if x.isalpha());r=int(''.join(x for x in address if x.isdigit()))
   if col in 'DEFGH' and 7<=r<=16:
    assert abs(float(c.findtext('s:v',namespaces=NS)))<.01,address;checked+=1
  assert checked==50
  charts=[p for p in z.namelist() if '/charts/chart' in p and p.endswith('.xml')]
  assert len(charts)==1
  result={'worksheets':len(sheets),'formulas':formulas,'native_data_tables':data_tables,'charts':len(charts),'formula_errors':errors,'base_case_zero_checks':checked,'formula_cells_without_numeric_cache':empty_cache,'native_excel_executed':False}
  (ROOT/'reports/export_validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
  print(json.dumps(result))
if __name__=='__main__':main()
