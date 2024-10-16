import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime


class BlackScholes:

    def __init__(self, trade_date: str, expiry_date: str, S: float, K: float, r: float, sigma: float):
        """
        Initialize the Black-Scholes model with trade and expiry dates, 
        current stock price, strike price, risk-free rate, and volatility.

        Parameters:
        trade_date (str): The date when the option is traded (YYYY-MM-DD).
        expiry_date (str): The expiry date of the option (YYYY-MM-DD).
        S (float): Current stock price.
        K (float): Strike price of the option.
        r (float): Risk-free interest rate (as a decimal).
        sigma (float): Volatility of the stock (as a decimal).
        """
        self.trade_date = trade_date 
        self.expiry_date = expiry_date 
        self.S = S
        self.K = K
        self.r = r
        self.sigma = sigma

    @property
    def trade_date(self):
        """Gets the trading date"""
        return self._trade_date

    @trade_date.setter
    def trade_date(self, value):
        """Sets and asserts the trading date"""
        if not isinstance(value, (str)):

            raise ValueError("trade_date should be a string")
        try:
            value = datetime.strptime(value, "%Y-%m-%d")
        except:
            raise ValueError("trade_date should be correctly formmated: '%Y-%m-%d (e.g '2024-10-15')")
            
        self._trade_date = value

    @property
    def expiry_date(self):
        """Gets the expiry date"""
        return self._expiry_date

    @expiry_date.setter
    def expiry_date(self, value):
        """Sets and asserts the expiry date"""
        if not isinstance(value, (str)):
            raise ValueError("trade_date should be a string")       
        # cheks if the format of the date is correct
        try:
            value = datetime.strptime(value, "%Y-%m-%d")
        except:
            raise ValueError("trade_date should be correctly formmated: '%Y-%m-%d (e.g '2024-10-15')")
            
        self._expiry_date = value

    @property
    def S(self):
        """gets the spot price"""
        return self._S

    @S.setter
    def S(self, value):
        """sets and asserts the trading date"""
        if not isinstance(value, (int, float)):
            raise ValueError("Spot price (S) must be an integer or float")
        self._S = value

    @property
    def K(self):
        """gets the strike price"""
        return self._K

    @K.setter
    def K(self, value):
        """sets and asserts the spot price"""
        if not isinstance(value, (int, float)):
            raise ValueError("Exercise price (K) must be an integer or float")
        self._K = value
        
    @property
    def r(self):
        """gets the risk free rate"""
        return self._r

    @r.setter
    def r(self, value):
        """sets the risk free rate and asserts the value"""        
        if not isinstance(value, (int, float)):
            raise ValueError("Risk free rate (r) must be an integer or float")
        self._r = value

    @property
    def sigma(self):
        """gets the sigma"""
        return self._sigma

    @sigma.setter
    def sigma(self, value):
        """sets and asserts the sigma"""
        if not isinstance(value, (int, float)):
            raise ValueError("sigma must be an integer or float")
        self._sigma = value

    def T(self):
        """Calculate the time to expiry in years."""
        return (self.expiry_date - self.trade_date).days / 365

    def F(self):
        """Calculate the forward price."""
        return self.S * np.exp(self.r * self.T())

    def d1(self):
        """Calculate d1 used in the Black-Scholes formula."""
        return (np.log(self.F() / self.K) + (self.sigma ** 2 / 2) * self.T()) / (self.sigma * np.sqrt(self.T()))

    def d2(self):
        """Calculate d2 used in the Black-Scholes formula."""
        return self.d1() - self.sigma * np.sqrt(self.T())

    def C(self):
        """Calculate the call option price."""
        return np.exp(-self.r * self.T()) * (self.F() * norm.cdf(self.d1()) - self.K * norm.cdf(self.d2()))

    def P(self):
        """Calculate the put option price."""
        return self.C() - self.S + self.K * np.exp(-self.r * self.T())

    def __str__(self) -> str:
        """Return a string representation of the option."""
        return (f'Option: \ntrade_date: {self.trade_date} \nexpiry_date: {self.expiry_date}\nspot_price: {self.S}\nd1: {self.d1()} '
                f'\nd2: {self.d2()} \nstrike_price (K): {self.K} \ncall_price (C): {self.C()} \nput_price (P): {self.P()}')
    

class VaR():

    def __init__(self, market_rate_1: np.array, market_rate_2: np.array, S1 : float, S2: float):
        """
        Initialize the Value-at-Risk model with market rates and spot prices of two currencies.

        Parameters:
        market_rate_1 (np.array): The market rates per day of currency 1.
        market_rate_2 (np.array): The market rates per day of currency 2.
        S1: Spot price of holdings in currency 1.
        S2: Spot price of holdings in currency 2. 
        """
        self.market_rate_1 = market_rate_1
        self.market_rate_2 = market_rate_2
        self.S1 = S1
        self.S2 = S2

    @property
    def market_rate_1(self):
        """ Get the market rates of currency 1"""
        return self._market_rate_1

    @market_rate_1.setter
    def market_rate_1(self, value):
        """ Sets the market rates of currency 1"""
        if not isinstance(value, np.ndarray):
            raise ValueError("The market rates of currency 1 (market_rate_1) should be a numpy array.")
        self._market_rate_1 = value

    @property
    def market_rate_2(self):
        """ Get the market rates of currency 2"""
        return self._market_rate_2

    @market_rate_2.setter
    def market_rate_2(self, value):
        """ Sets the market rates of currency 2"""
        if not isinstance(value, np.ndarray):
            raise ValueError("The market rates of currency 2 (market_rate_2) should be a numpy array.")
        self._market_rate_2 = value    

    @property
    def S1(self):
        """ Get the spot price of holdings incurrency 1"""
        return self._S1

    @S1.setter
    def S1(self, value):
        """ Sets the spot price of holdings incurrency 1"""
        if not isinstance(value, (int, float)):
            raise ValueError("Total value of holdings in currency 1 (S1) should be integer or float")
        self._S1 = value 
    
    @property
    def S2(self):
        """ Get the spot price of holdings in currency 2"""
        return self._S2

    @S2.setter
    def S2(self, value):
        """ Sets the spot price of holdings in currency 2"""
        if not isinstance(value, (int, float)):
            raise ValueError("Total value of holdings in currency 2 (S2) hould be integer or float")
        self._S2 =  value

    def pnl_vector(self, S, market_rate) -> np.array:
        """
        Calculate the profit and loss (PnL) vector.

        Parameters:
        S (float): The spot price of the holdings.
        market_rate (np.array): The market rates to use for calculation.

        Returns:
        np.array: The calculated PnL vector.
        """
        return (np.exp(np.log(market_rate[:-1] / market_rate[1:])) -1) * S
    
    @property
    def total_pnl(self) -> np.array:
        """
        Calculate the total profit and loss (PnL) for both currencies.

        Returns:
        np.array: The sorted total PnL.
        """
        return np.sort(self.pnl_vector(self.S1, self.market_rate_1) + self.pnl_vector(self.S2, self.market_rate_2))

    @property
    def var_1d(self) -> float:
        """
        Calculate the 1-dimensional Value-at-Risk (VaR).

        Returns:
        float: The calculated VaR value.
        """  
        return (0.4 * self.total_pnl[1]) + (0.6 * self.total_pnl[2])
    
    def __str__(self):
        return (f'S1: {self.S1}\n S2: {self.S2} VaR-1Day: {self.var_1d}\n')

def import_data() -> np.array:
    """Imports the data as provided and returns numpy arrays with the market rates."""
    df = pd.read_excel('var_data.xlsx')
    ccy1 = np.array(df['market_rate_ccy1'].to_list())
    ccy2 = np.array(df['market_rate_ccy2'].to_list())

    return ccy1, ccy2

if __name__ == "__main__":

    # imports the data
    ccy1, ccy2 = import_data()
    # instantiates an instance of the BlackScholes Class containing example data
    option = BlackScholes('2022-11-23', '2023-05-10', 19, 17, 0.005, 0.3)
    # intantiates an instance of the VaR Class containing exampl data
    var = VaR(ccy1, ccy2, 153084.81, 95891.51)
    # print out results
    print(option)
    print("VaR 1-Day:\n" + str(var.var_1d))

