# created roman_gen_methods.py to test methods under kivy screen
# used random.seed(0) under roman_calculation() to obtain reproducible results

import unittest
from roman_gen_methods import Roman

test_roman = Roman()



class NamesTestCase(unittest.TestCase):

    def test_single_name(self):
        result = test_roman.roman_calculation("Claire")
        self.assertEqual(result, "Clairelium")


    def test_first_last_name(self):
        result = test_roman.roman_calculation("Claire Ricks")
        self.assertEqual(result, "Clairelium Ricksis")


    def test_name_with_special_char(self):
        result = test_roman.roman_calculation("C1a*re_")
        self.assertEqual(result, "C1a*re_us")


    def test_name_all_caps(self):
        result = test_roman.roman_calculation("CLAIRE")
        self.assertEqual(result, "Clairelium")


    def test_name_lower(self):
        result = test_roman.roman_calculation("claire ricks")
        self.assertEqual(result, "Clairelium Ricksis")

if __name__ == '__main__':
    unittest.main()