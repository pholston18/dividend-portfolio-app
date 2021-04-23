import robin_stocks.robinhood as robin
import credentials as cred


def login():
    # login_period = 60 * 24 * 60 * 60
    robin.login(cred.USERNAME, cred.PASSWORD, by_sms=True)


def logout():
    robin.logout()


def get_positions():
    login()
    return list(robin.build_holdings(with_dividends=True).keys())


def get_dividend_positions():
    login()
    div_positions = []
    positions = get_positions()
    fundamentals = robin.get_fundamentals(positions)

    for data in fundamentals:
        if data['dividend_yield'] is not None:
            div_positions.append(data['symbol'])

    return div_positions


dividend_positions = get_dividend_positions()
print(dividend_positions)
