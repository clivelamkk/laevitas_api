from laevitas_api import utilities as ut
from os import getenv
import requests
import pandas as pd
import time
from requests.exceptions import RequestException
import random
from datetime import datetime

def get_OptTrades(exchange, theCoin, theDate, max_retries=20):
    # exchange: DERIBIT, BINANCE, BITFINEX, BITMEX, BYNIT, HUOBI, KRAKEN, OKX
    # theCoin: BTC, ETH, SOL, etc...
    # theDate: "2025-01-06"
    api_key = getenv("api_lav") # Get Key
    headers = {"accept": "application/json", "apiKey": api_key} # Gen Header
    all_items = []
    page = 0
    maxSize = 144
    thisSize = maxSize
    while thisSize >= maxSize: # Loop until the page with thisSize less than maxSize
        page = page + 1
        url = f"https://api.laevitas.ch/historical/options/trades/{exchange}/{theCoin}?date={theDate}&limit={maxSize}&page={page}"
        for attemp in range(max_retries):
            req = requests.get(url, headers=headers)
            if req.status_code == 200:
                # request is good
                json = req.json()
                thisItems = list(json['items'])
                all_items.extend(thisItems)
                thisSize = len(thisItems)
                break
            else:
                print(f"Download unsuccessful: trades - {exchange} {theCoin} datet={theDate} page={page}")
                # request error, wait for 1 second
                time.sleep(10)
        if attemp > max_retries:
            print(f"Failed to fetch {page} after {max_retries} attempts.")
            thisSize = 0 # exit while loop
    if len(all_items)>0:
        df = pd.DataFrame(all_items)
    else:
        df = pd.DataFrame()
    return df

def get_OptSnapshot(exchange, theCoin, dt_beg, dt_end, freq, max_retries=20):
    # exchange: DERIBIT, BINANCE, BITFINEX, BITMEX, BYNIT, HUOBI, KRAKEN, OKX
    # theCoin: BTC, ETH, SOL, etc...
    # dt_beg/dt_end: "2025-01-06"
    # freq: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d
    api_key = getenv("api_lav") # Get Key
    headers = {"accept": "application/json", "apiKey": api_key} # Gen Header
    all_items = []
    theSize = {
        "1m": 1440,
        "5m": 288,
        "15m": 96,
        "30m": 48,
        "1h": 24,
        "2h": 12,
        "4h": 6,
        "6h": 4,
        "12h": 2,
        "1d": 1
    }
    # Get the number of days
    start = datetime.strptime(dt_beg, "%Y-%m-%d")
    end = datetime.strptime(dt_end, "%Y-%m-%d")
    delta = end - start
    num_days = delta.days
    totalSize = theSize.get(freq,1) * num_days
    page = 0
    while page <= totalSize: # Loop until the page with thisSize less than maxSize
        page = page + 1
        if freq == "1m":
            url = f"https://api.laevitas.ch/historical/options/snapshot/{exchange}/{theCoin}?start={dt_beg}&end={dt_end}&limit=1&page={page}"
        else:
            url = f"https://api.laevitas.ch/historical/options/snapshot/{exchange}/{theCoin}?start={dt_beg}&end={dt_end}&limit=1&granularity={freq}&page={page}"
        for attempt in range(max_retries):
            try:
                req = requests.get(url, headers=headers, timeout=30) # Added timeout
                if req.status_code == 200:
                    # Request is successful
                    json_data = req.json()
                    thisItems = list(json_data['items'])
                    for item in thisItems:
                        item['page'] = page
                    all_items.extend(thisItems)
                    break # Exit retry loop on success
                else:
                    # Non-200 status code (e.g., 429, 500, etc.)
                    print(f"Download unsuccessful: options - {exchange} {theCoin} start={dt_beg} end={dt_end} page={page}")
                    print(f"Status code: {req.status_code}")
                    raise RequestException(f"Non-200 status code: {req.status_code}")
            except RequestException as e:
                print(f"Error: {str(e)}")
                if attempt == max_retries - 1: # Last attempt
                    print(f"Failed to fetch page {page} after {max_retries} attempts.")
                    break
                # Exponential backoff with jitter
                sleep_time = (2 ** attempt) + random.uniform(0, 1) # 1, 2, 4, 8 seconds + jitter
                print(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
    if len(all_items)>0:
        df = pd.DataFrame(all_items)
        df['datetime'] = pd.to_datetime(df['date'], unit='ms')
    else:
        df = pd.DataFrame()
    return df

def get_FutSnapshot(exchange, theCoin, dt_beg, dt_end, freq, max_retries=20):
    # exchange: DERIBIT, BINANCE, BITFINEX, BITMEX, BYNIT, HUOBI, KRAKEN, OKX
    # theCoin: BTC, ETH, SOL, etc...
    # dt_beg/dt_end: "2025-01-06"
    # freq: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d
    api_key = getenv("api_lav") # Get Key
    headers = {"accept": "application/json", "apiKey": api_key} # Gen Header
    all_items = []
    theSize = {
        "1m": 1440,
        "5m": 288,
        "15m": 96,
        "30m": 48,
        "1h": 24,
        "2h": 12,
        "4h": 6,
        "6h": 4,
        "12h": 2,
        "1d": 1
    }
    # Get the number of days
    start = datetime.strptime(dt_beg, "%Y-%m-%d")
    end = datetime.strptime(dt_end, "%Y-%m-%d")
    delta = end - start
    num_days = delta.days
    totalSize = theSize.get(freq,1) * num_days
    page = 0
    while page <= totalSize: # Loop until the page with thisSize less than maxSize
        page = page + 1
        if freq == "1m":
            url = f"https://api.laevitas.ch/historical/futures/snapshot/{exchange}/{theCoin}?start={dt_beg}&end={dt_end}&limit=1&page={page}"
        else:
            url = f"https://api.laevitas.ch/historical/futures/snapshot/{exchange}/{theCoin}?start={dt_beg}&end={dt_end}&limit=1&granularity={freq}&page={page}"
        for attempt in range(max_retries):
            try:
                req = requests.get(url, headers=headers, timeout=30) # Added timeout
                if req.status_code == 200:
                    # Request is successful
                    json_data = req.json()
                    thisItems = list(json_data['items'])
                    for item in thisItems:
                        item['page'] = page
                    all_items.extend(thisItems)
                    break # Exit retry loop on success
                else:
                    # Non-200 status code (e.g., 429, 500, etc.)
                    print(f"Download unsuccessful: Futures - {exchange} {theCoin} start={dt_beg} end={dt_end} page={page}")
                    print(f"Status code: {req.status_code}")
                    raise RequestException(f"Non-200 status code: {req.status_code}")
            except RequestException as e:
                print(f"Error: {str(e)}")
                if attempt == max_retries - 1: # Last attempt
                    print(f"Failed to fetch page {page} after {max_retries} attempts.")
                    break
                # Exponential backoff with jitter
                sleep_time = (2 ** attempt) + random.uniform(0, 1) # 1, 2, 4, 8 seconds + jitter
                print(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
    if len(all_items)>0:
        df = pd.DataFrame(all_items)
        df['datetime'] = pd.to_datetime(df['date'], unit='ms')
    else:
        df = pd.DataFrame()
    return df

def get_lav_implied_vol(instrument, dt_str):
    dt = ut.to_timestamp(dt_str)
    if not ut.is_option(instrument):
        return (dt_str, None)
    exchange = ut.get_option_exchange(instrument)
    instrument = ut.convert_option_name(instrument)
    api_key = getenv("api_lav")
    headers = {"accept": "application/json", "apiKey": api_key}
    url = f"https://api.laevitas.ch/historical/options/{exchange}/{instrument}?start={dt}&end={dt}&limit=10&page=1"
    req = requests.get(url, headers=headers)
    json = req.json()
    data = json["items"]
    if not data:
        r = None
    else:
        dc = data[0]
        dc["date"] = ut.convert_uxtimestamp_to_hkt(dc["date"])
        r = dc
    return r