---
icon: 
---
# Base Strategy

The base strategy allows the construction of powerful portoflios based on different kind of signals. You can use it this way:

``` python title="Usage exmple of Base Strategy" linenums="1"
from quantbt.strategies.S_base import S_base

Class MyStrategy(S_base):
    def generate_signals(self):
      # Generate the signals needed

st = MyStrategy(
    data,
    commission=1.2,
    commission_type=CommissionType.FIXED,
    multiplier=4,
    data_type=DataType.OHLC,
    initial_capital=100000,
    default_trade_size=1,
    trade_size_type=TradeSizeType.FIXED,
)
```

PARAMETERS

----

## Commission
QuantBT currently supports 2 type of commissions.

### Fixed:
**Usage:** `CommissionType.FIXED`

This is popular in CFD and Futures contracts where the broker charges a fixed amount.
The amount if a flat fee added to each trade. 
Please note that this is a one way fee, meaning that the resulting fee will be double this amount.


### Percentage:
**Usage:** `CommissionType.PERCENTAGE`

This is popular in crypto currencies where the commission is a percentage of volume traded. 


| Type  | Price  | Volume |   Fee    |
| ----  | ------ | -----  |   ----   |
| Entry | 10000  | 1      |  **2$**  |
| Exit  | 12000  | 1      | **2.4$** |

Total Commission is: **4.4$**

----

## TradeSize
QuantBT currently supports 2 type of trade sized.

### Fixed:
**Usage:** `TradeSize.FIXED`

This is popular in Futures contracts where the contrats have to be full numbers.


### Percentage:
**Usage:** `TradeSize.PERCENTAGE`

This is useful in crypto where you want the trade size to be a percentage of the total portfolio.

----

## DataType
In the quant world, there are generally 2 types of data.

### Bid Ask:
The most raw type is the Bid-Ask data. 

*note*: You can simulate a **tick** line chart, by setting bid and ask to the same value.
**Usage:** `DataType.BID_ASK`

This is popular when scalping of doing HFT.


### OHLC:
**Usage:** `DataType.OHLC`

The most common datatype from which you can build more diverse charts such as renko, range bars, etc...

