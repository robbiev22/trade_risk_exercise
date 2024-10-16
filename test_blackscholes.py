import unittest
import pandas as pd
import numpy as np
from solutions import BlackScholes  


class TestBlackScholes(unittest.TestCase):

    def setUp(self):
        """
        Create common variables used across multiple tests.
        This method is run before each test.
        """
        self.trade_date = '2022-11-23' 
        self.expiry_date = '2023-05-10'
        self.S = 19
        self.K = 17
        self.r = 0.005
        self.sigma = 0.3  

        # Initializes an instance of the class
        self.option = BlackScholes(self.trade_date, self.expiry_date, self.S, self.K, self.r, self.sigma)

    def test_date_validation(self):
        """
        Test that ValueError is raised when an invalid market_rate is passed (non-numpy array).
        """
        with self.assertRaises(ValueError):
            BlackScholes(20221123, self.expiry_date, self.S, self.K, self.r, self.sigma)

        with self.assertRaises(ValueError):
            BlackScholes('invalid', self.expiry_date, self.S, self.K, self.r, self.sigma)
        
        with self.assertRaises(ValueError):
            BlackScholes("20222-11-23", self.expiry_date, self.S, self.K, self.r, self.sigma)

    def test_S_K_r_sigma_validation(self):
        """
        Test that ValueError is raised when non-numeric S1 or S2 is provided.
        """
        with self.assertRaises(ValueError):
            BlackScholes(self.trade_date, self.expiry_date, "invalid", self.K, self.r, self.sigma)
        
        with self.assertRaises(ValueError):
            BlackScholes(self.trade_date, self.expiry_date, self.S,"invalid", self.r, self.sigma)

        with self.assertRaises(ValueError):
            BlackScholes(self.trade_date, self.expiry_date, self.S, self.K, "invalid" , self.sigma)
        
        with self.assertRaises(ValueError):
            BlackScholes(self.trade_date, self.expiry_date, self.S, self.K, self.sigma, "invalid")

    def test_at_the_money(self):
        """
        Test at-the-money Call / out-the-money Put
        """

        # calculation from provided Excel
        expected_C = 1.39597
        expected_P = 1.35699

        # Spot equal to strike price
        self.option.S = 17

        print(self.option)

        self.assertAlmostEqual(self.option.C(), expected_C, places=3)
        self.assertAlmostEqual(self.option.P(), expected_P, places=3)

    def test_in_the_money(self):
        """
        Test it-the-money Call / out-the-money Put
        """

        # calculation from provided Excel
        expected_C = 2.69688
        expected_P = 0.65790

        self.assertAlmostEqual(self.option.C(), expected_C, places=3)
        self.assertAlmostEqual(self.option.P(), expected_P, places=3)

    def test_out_the_money(self):
        """
        Test out-the-money Call / in-the-money Put
        """
        # calculation from provided Excel
        expected_C = 0.54279
        expected_P = 2.50381

        # change spot price to smaller than exercise price
        self.option.S = 15

        self.assertAlmostEqual(self.option.C(), expected_C, places=3)
        self.assertAlmostEqual(self.option.P(), expected_P, places=3)

if __name__ == '__main__':
    unittest.main()
