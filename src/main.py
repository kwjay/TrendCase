from market_data import get_daily

if __name__ == "__main__":
    ibm = get_daily("IBM")
    print(ibm.tail())