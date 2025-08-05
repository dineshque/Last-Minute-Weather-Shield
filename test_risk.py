import unittest
from app import detect_risks

class TestRiskDetection(unittest.TestCase):
    def test_high_wind(self):
        sample = {'wind': {'speed': 50}}
        risks = detect_risks(sample)
        self.assertTrue(any(r['type'] == 'wind' for r in risks))

    def test_heavy_rain(self):
        sample = {'rain': {'1h': 25}}
        risks = detect_risks(sample)
        self.assertTrue(any(r['type'] == 'rain' for r in risks))

    def test_hail(self):
        sample = {'weather': [{'description': 'light hail', 'id': 906}]}
        risks = detect_risks(sample)
        self.assertTrue(any(r['type'] == 'hail' for r in risks))

    def test_no_risk(self):
        sample = {'wind': {'speed': 10}, 'rain': {'1h': 2}, 'weather': [{'description': 'clear sky', 'id': 800}]}
        risks = detect_risks(sample)
        self.assertEqual(risks, [])

if __name__ == '__main__':
    unittest.main()
