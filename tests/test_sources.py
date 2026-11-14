"""既有来源接口及拒绝错误资料的测试。"""
import unittest,tempfile
from pathlib import Path
from common import read,money,number,release,latest
class CommonTests(unittest.TestCase):
    def test_precise_money_and_finite_measurement(self):
        self.assertEqual(money('0.1')+money('0.2'),money('0.3'))
        with self.assertRaises(ValueError):number(float('nan'))
        with self.assertRaises(ValueError):money(.1)
    def test_release_reuse_and_corruption(self):
        with tempfile.TemporaryDirectory() as folder:
            key=release(folder,{'x':1});self.assertEqual(release(folder,{'x':1}),key)
            Path(folder,key+'.json').write_text('{"x":2}')
            with self.assertRaises(ValueError):release(folder,{'x':1})

from selection import joined,categorical_support
from trial import descriptive
from population import population
class DomainTests(unittest.TestCase):
    def test_fixed_frame_and_unrepresented_target(self):
        d=read();self.assertEqual(len(joined(d)),90);self.assertFalse(population(d)['sampling_error'])
        self.assertEqual(sum(not r['observed_category_support'] for r in categorical_support(d)),30)
        self.assertEqual(descriptive(d)['1']['n'],30)
    def test_join_refuses_unknown_trial_and_duplicate(self):
        d=read();d['trial'][0]['firm']='outside'
        with self.assertRaises(ValueError):joined(d)
        d=read();d['population'].append(d['population'][0])
        with self.assertRaises(ValueError):joined(d)
