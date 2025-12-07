#! python

import datetime as dt
from google.oauth2.service_account import Credentials
import gspread
import yfinance as yf

from bist30_defs import BIST30

# 1) Servis account kimlik bilgilerini yükle
SCOPES = [
   "https://www.googleapis.com/auth/spreadsheets",
   "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
   "keys/bist30-historical-2d62d7c02a90.json",
   scopes = SCOPES
)

SPREADSHEET_NAME = "Bist30 Hist"


def test():
    client = gspread.authorize( creds )


    sh = client.open( SPREADSHEET_NAME )
    ws = sh.sheet1

    headers = [ "Tarih", "Sembol", "Fiyat" ]
    ws.insert_row( headers, 1 )

    rows = [
        [ "2025-12-07", "USDTRY=X", "36.25" ],
        [ "2025-12-07", "AEFES.IS", "120.50" ],
    ]

    for i, row in enumerate( rows, start = 2 ):
        ws.insert_row( row, i )


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
    # main()
    test()



