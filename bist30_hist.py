#! python

import datetime as dt
import yfinance as yf

from bist30_defs import BIST30


def main():

    # Current USDTRY
    ticker = yf.Ticker( "USDTRY=X" )

    hist = ticker.history( period = "1y" )
    parityNew = float( hist[ "Close" ].iloc[ -1 ] )
    parityOld = float( hist[ "Close" ].iloc[ 0 ] )
    capitalTry = parityOld * 1000

    print( f"parityOld = {parityOld}, parityNew = {parityNew}, capitalTry={capitalTry}" )

    total = 0

    for ticker in BIST30:
        ticker = yf.Ticker( ticker )

        hist  = ticker.history( period = "1y" )

        sharePriceNew = float( hist[ "Close" ].iloc[ -1 ] )
        sharePriceOld = float( hist[ "Close" ].iloc[ 0 ] )

        numShares = capitalTry / sharePriceOld

        valueTryToday = numShares * sharePriceNew

        valueUsdToday = valueTryToday / parityNew

        profitUsd = ( valueUsdToday - 1000) / 10

        total += profitUsd


        print( f"--- {ticker}: numShares={numShares:.2f}, profitUsd={profitUsd:.2f}" )
        # print( f"      sharePriceOld={sharePriceOld:.2f}, sharePriceNew={sharePriceNew:.2f}, valueTryToday={valueTryToday:.2f}, valueUsdToday={valueUsdToday:.2f}" )

    print( f"total = {total}" )

if __name__ == "__main__":
    main()




