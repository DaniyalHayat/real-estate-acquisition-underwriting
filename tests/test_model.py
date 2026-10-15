import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from model import run, load, insurance, irr
class UnderwritingTests(unittest.TestCase):
 def test_historical_controls(self):
  h=load('historical')
  for i in range(3):
   self.assertEqual(h['revenue'][i],sum(h[k][i] for k in ['room_revenue','food_revenue','ancillary_revenue','other_revenue']))
   self.assertEqual(h['cash_end_restricted'][i],h['cash_begin_restricted'][i]+h['cfo'][i]+h['cfi'][i]+h['cff'][i])
   self.assertEqual(h['net_income'][i],h['pretax_income'][i]-h['tax_expense'][i])
 def test_all_cases_balance(self):
  for c in ['Base','Upside','Downside']:
   for y in run(c)['years']: self.assertAlmostEqual(y['balance_check'],0,places=8)
 def test_debt_and_cash(self):
  for c in ['Base','Upside','Downside']:
   r=run(c); previous=r['initial_debt']
   for y in r['years']:
    self.assertGreaterEqual(y['cash'],100-1e-8);self.assertGreaterEqual(y['debt'],0)
    self.assertAlmostEqual(previous-y['debt'],sum(y[k] for k in ['senior_amort','junior_amort','senior_sweep','junior_sweep']))
    previous=y['debt']
 def test_irr_npv(self):
  for c in ['Base','Upside','Downside']:
   r=run(c);self.assertAlmostEqual(sum(v/(1+r['irr'])**i for i,v in enumerate(r['flows'])),0,places=7)
 def test_return_bridge(self):
  for c in ['Base','Upside','Downside']:
   r=run(c);self.assertAlmostEqual(sum(r['bridge'].values()),r['exit_equity'],places=7)
 def test_more_expensive_entry_lowers_returns(self): self.assertLess(run(overrides={'entry_multiple':11.5})['irr'],run()['irr'])
 def test_higher_exit_improves_returns(self): self.assertGreater(run(overrides={'exit_multiple':11.5})['irr'],run()['irr'])
 def test_higher_rate_reduces_returns(self): self.assertLess(run(overrides={'senior_rate':.10})['irr'],run()['irr'])
 def test_sweep_priority(self):
  for y in run()['years']:
   if y['senior']>1e-8:self.assertEqual(y['junior_sweep'],0)
 def test_fully_insured_no_retention(self):
  a=load('assumptions');a.update(property_deductible=0,combined_property_bi_limit=1e6,gl_retention=0,gl_limit=1e6,premium_increase=0)
  self.assertAlmostEqual(insurance(a)['cash_cost'],0)
 def test_no_coverage_gross_retained(self):
  a=load('assumptions');a.update(combined_property_bi_limit=0,gl_limit=0,premium_increase=0)
  self.assertEqual(insurance(a)['cash_cost'],132)
 def test_dcf_invalid_growth(self):
  with self.assertRaises(ValueError):run(overrides={'terminal_growth':.10})
 def test_downside_requires_equity(self): self.assertGreater(run('Downside')['total_equity_calls'],0)
 def test_irr_known_cash_flows(self):self.assertAlmostEqual(irr([-100,0,121]),.10)
if __name__=='__main__':unittest.main()
