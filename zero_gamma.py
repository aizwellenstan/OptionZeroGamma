import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import seaborn as sns
from datetime import timedelta, date
import datetime
from itertools import *

df = pd.read_csv('data.csv', sep='\s+', header=None, skiprows=0)

df.columns = ['1stCol']

spot_price = df['1stCol'][0].split(',')[1]
spot_price = float(spot_price.split('Last:')[1])

df = df.iloc[3:]

new = df["1stCol"].str.split(",", n = 21, expand = True)
new.columns = ['ExpirationDate','Calls','CallLastSale','CallNet','CallBid','CallAsk','CallVol','CallIV','CallDelta','CallGamma','CallOpenInt','CallStrike','Puts','PutLastSale','PutNet','PutBid','PutAsk','PutVol','PutIV','PutDelta','PutGamma','PutOpenInt']

callStrike = [x[-6:-3] for x in new.Calls]
new['StrikePrice'] = callStrike 

new['CallGamma'] = new['CallGamma'].astype(float)
new['CallOpenInt'] = new['CallOpenInt'].astype(float)
new['CallGEX'] = new['CallGamma'] * new['CallOpenInt'] * 100 * spot_price

new['PutGamma'] = new['PutGamma'].astype(float)
new['PutOpenInt'] = new['PutOpenInt'].astype(float)
new['PutGEX'] = new['PutGamma'] * new['PutOpenInt'] * 100 * spot_price * -1



new['TotalGamma'] = new.CallGEX + new.PutGEX
count = 0
strikeWithGamma = []
for a, b in zip(new.StrikePrice, new.TotalGamma):
    strikesPlusGamma = (a,b)
    strikeWithGamma.append(strikesPlusGamma)
new['StrikeAndGamma'] = strikeWithGamma
new = new[(new['TotalGamma'] != 0.0)]

new.sort_values('StrikePrice').plot(x = 'StrikePrice', y = 'TotalGamma', grid = True)
plt.show()

def zero_gex(strikes):
    def add(a, b):
        return (b[0], a[1] + b[1])

    cumsum = list(accumulate(strikes, add))
    if cumsum[len(strikes) // 10][1] < 0:
        op = min
    else:
        op = max
    return op(cumsum, key=lambda i: i[1])[0]

print(zero_gex(new.StrikeAndGamma))