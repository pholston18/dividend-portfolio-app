from datetime import datetime
import time
import asyncio
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from pprint import *

"""
************************************************************************

Data-Compiling Function(s):
- This section contains the function that will compile all the data from 
  the various sources and return a dictionary with all the relevant data.
  
*************************************************************************
"""


def load_data(ticker):
    return ticker


"""
**********************************************************************************************************

Data-Sourcing Function(s):
- This section of functions are used to source information on individual
  dividend-yielding stocks from numerous websites, each function sourcing
  data from a specific site.

Functions:
  > load_dividend_information_data(ticker):
    - This function sources data on dividend-yielding stocks from 'https://www.dividendinformation.com/'.
    
  > load_seeking_alpha_data(ticker):
    - This function sources data on dividend-yielding stocks from 'https://seekingalpha.com/'.
    
  > load_dividend_investor_data(ticker):
    - This function sources data on dividend-yielding stocks from 'https://www.dividendinvestor.com/'.
    
  > load_dividata_data(ticker):
    - This function sources data on dividend-yielding stocks from 'https://dividata.com/'.
    
**********************************************************************************************************
"""


def load_dividend_information_data(ticker):
    return ticker


def load_seeking_alpha_data(ticker):
    try:

        url = 'https://seekingalpha.com/symbol/{0}/dividends/scorecard'.format(ticker.upper())

        parsed = []

        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        with webdriver.Chrome('chromedriver.exe') as driver:
            driver.get(url)

            html = driver.find_elements_by_css_selector('div div')

            for index, item in enumerate(html):
                parsed.append(str(index) + " " + item.text)

        data = {
            'div-yield': auth(parsed[138].replace('%', ''), 'f'),
            'annual-div': auth(parsed[141].replace('$', ''), 'f'),
            'payout-ratio': auth(parsed[144].replace('%', ''), 'f'),
            '5-yr-growth': auth(parsed[147].replace('%', ''), 'f'),
            'div-growth': auth(parsed[150].replace(" Years", ''), 'i'),
            'div-amount': auth(parsed[159].replace('$', ''), 'f'),
            'ex-div-date': None if (parsed[162] == '-') else datetime.strptime(parsed[162], "%m/%d/%Y"),
            'payout-date': None if (parsed[165] == '-') else datetime.strptime(parsed[165], "%m/%d/%Y"),
            'record-date': None if (parsed[168] == '-') else datetime.strptime(parsed[168], "%m/%d/%Y"),
            'declare-date': None if (parsed[171] == '-') else datetime.strptime(parsed[171], "%m/%d/%Y"),
            'div-frequency': auth(parsed[174], 's')
        }

    except (StaleElementReferenceException, ValueError):

        data = {
            'div-yield': None,
            'annual-div': None,
            'payout-ratio': None,
            '5-yr-growth': None,
            'div-growth': None,
            'div-amount': None,
            'ex-div-date': None,
            'payout-date': None,
            'record-date': None,
            'declare-date': None,
            'div-frequency': None
        }

    return data


def load_dividend_investor_data(ticker):
    company_info = []
    dividend_info = []
    price_info = []

    url = 'https://www.dividendinvestor.com/dividend-quote/{0}/'.format(ticker.lower())

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    with webdriver.Chrome('chromedriver.exe') as driver:

        driver.get(url)

        company = driver.find_element_by_css_selector('div.company').text.replace(' Dividend Information', '')
        dividend_information = driver.find_element_by_id('dividend').find_elements_by_css_selector('span.data')
        price_information = driver.find_element_by_id('stock').find_elements_by_css_selector('span.data')
        company_information = driver.find_element_by_id('other-left').find_elements_by_css_selector('span.data')

        for element in dividend_information:
            dividend_info.append(element.text)

        for element in price_information:
            price_info.append(element.text)

        for element in company_information:
            company_info.append(element.text)

    data = {
        'company-name': auth(format_name(company), 's'),
        'last-price': auth(price_info[0].replace('$', ''), 'f'),
        'div-yield': auth(dividend_info[0].replace('%', ''), 'f'),
        'annual-div': auth(dividend_info[4].replace('$', ''), 'f'),
        '3-yr-growth': auth(dividend_info[7].replace('%', ''), 'f'),
        '5-yr-growth': auth(dividend_info[8].replace('%', ''), 'f'),
        'dec-date': None if (dividend_info[14] == 'None') else datetime.strptime(dividend_info[14], "%b. %d, %Y"),
        'ex-date': None if (dividend_info[15] == 'None') else datetime.strptime(dividend_info[15], "%b. %d, %Y"),
        'rec-date': None if (dividend_info[16] == 'None') else datetime.strptime(dividend_info[16], "%b. %d, %Y"),
        'pay-date': None if (dividend_info[17] == 'None') else datetime.strptime(dividend_info[17], "%b. %d, %Y"),
        'consecutive-growth': auth(dividend_info[10].replace(" Years", ''), 'i'),
        'div-freq': auth(dividend_info[20], 'i'),
        'eps': auth(price_info[6].replace('%', ''), 'f'),
        'pe-ratio': auth(price_info[8], 'f'),
        'website': auth(company_info[0]),
        'sector': auth(company_info[1]),
        'industry': auth(company_info[3])
    }

    return data


def load_dividata_data(ticker):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    url = 'https://dividata.com/stock/{}'.format(ticker.upper())

    with webdriver.Chrome('chromedriver.exe') as driver:
        driver.get(url)


"""
*****************************************************************************

Recommendation Function(s):
- This section of functions are used to source dividend stock recommendations
  based upon: rating, high-yields, and upcoming ex-dividend dates.
- This data is sourced from 'https://dividata.com/'

Functions:
  > get_top_stocks():
    - This function gets a collection of the highest rated dividend
      stocks from the url referenced above.
      
  > get_high_yield():
    - This function gets a collection of the highest-yielding dividend
      stocks from the url referenced above.
      
  > get_upcoming_ex_dates():
    - This function gets a collection of dividend stocks with upcoming 
      ex-dividend dates from the url referenced above.
      
*****************************************************************************
"""


def get_top_stocks():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    with webdriver.Chrome('chromedriver.exe', options=options) as driver:
        url = 'https://dividata.com/topstocks'

        driver.get(url)

        rows = driver.find_elements_by_tag_name('tr')

        recommended = []
        columns = ["Name", "Symbol", "Last Price", "Dividend Yield", "Years Paying", "Rating"]
        for index, row in enumerate(rows):
            if index != 0:
                symbol = auth(row.find_element_by_css_selector('td.symbol a').text, 's')
                name = auth(row.find_element_by_css_selector('td.name.redundant a').text, 's')
                last_close = auth(row.find_element_by_css_selector('td.number').text.replace('$', ''), 'f')
                div_yield = auth(row.find_element_by_css_selector('td.percent').text.replace('%', ''), 'f')
                years_paying = auth(row.find_element_by_css_selector('td.number').text, 'i')
                rating = auth(row.find_element_by_css_selector('div.progress-mini div').get_attribute('class'), 'r')
                recommended.append([symbol, name, last_close, div_yield, years_paying, rating])

        top_stocks = pd.DataFrame(recommended, columns=columns)

        return top_stocks


def get_high_yield():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    with webdriver.Chrome('chromedriver.exe', options=options) as driver:
        url = 'https://dividata.com/highyields'

        driver.get(url)

        rows = driver.find_elements_by_tag_name('tr')

        recommended = []
        columns = ["Name", "Symbol", "Last Price", "Dividend Yield", "Years Paying", "Rating"]

        for index, row in enumerate(rows):
            if index != 0:
                symbol = auth(row.find_element_by_css_selector('td.symbol a').text, 's')
                name = auth(row.find_element_by_css_selector('td.name.redundant a').text, 's')
                last_close = auth(row.find_element_by_css_selector('td.number').text.replace('$', ''), 'f')
                div_yield = auth(row.find_element_by_css_selector('td.percent').text.replace('%', ''), 'f')
                years_paying = auth(row.find_element_by_css_selector('td.number').text, 'i')
                rating = auth(row.find_element_by_css_selector('div.progress-mini div').get_attribute('class'), 'r')
                recommended.append([symbol, name, last_close, div_yield, years_paying, rating])

        high_yield = pd.DataFrame(recommended, columns=columns)

        return high_yield


def get_upcoming_ex_dates():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    with webdriver.Chrome('chromedriver.exe', options=options) as driver:
        url = 'https://dividata.com/'

        driver.get(url)

        table = driver.find_element_by_css_selector('div#homedividates table')
        rows = table.find_elements_by_css_selector('tr')

        recommended = []
        columns = ["Symbol", "Last Price", "Dividend Yield", "Rating"]

        for index, row in enumerate(rows):
            if index != 0:
                symbol = auth(row.find_element_by_css_selector('td.ticker a').text, 's')
                last_close = auth(row.find_element_by_css_selector('td.money').text.replace('$', ''), 'f')
                div_yield = auth(row.find_element_by_css_selector('td.percent').text.replace('%', ''), 'f')
                rating = auth(row.find_element_by_css_selector('div.progress-mini div').get_attribute('class'), 'r')
                recommended.append([symbol, last_close, div_yield, rating])

        upcoming_ex_dates = pd.DataFrame(recommended, columns=columns)

        return upcoming_ex_dates


"""
***********************************************************************************

Formatter Function(s):
- These functions format and validate various types of input into their 
  desired formats.
  
Functions:
  > format_name(name):
    - This function takes in an un-formatted name, and changes the name to a 
      standard form.
  
  > auth(value, data_type):
    - This function takes in a value of various types and makes sure the value can
      be converted to the desired type.
    
**********************************************************************************
"""


def format_name(name):
    abbrev = ['Company', 'Co', 'Corporation', 'Corp', 'Incorporated', 'Inc', 'Limited', 'Ltd']
    abbrev_format = ['Co.', 'Co.', 'Corp.', 'Corp.', 'Inc.', 'Inc.', 'Ltd.', 'Ltd.']

    if '(' in name:
        open_pos = name.index('(')
        close_pos = name.index(')')
        name = name[:open_pos] + name[close_pos + 1:]

    words = name.split()

    for i, abbr in enumerate(abbrev):
        for j, word in enumerate(words):
            if abbr == word:
                words[j] = abbrev_format[i]

    name = ' '.join(words)

    return name


def auth(value, data_type=''):
    if value and value != 0:
        return None
    if value == "N/A":
        value = 0
    if value == "Currency Mismatch":
        return None
    if value == '-':
        return None

    try:
        if data_type == 'f':
            value = float(value)
        elif data_type == 'i':
            value = int(value)
        elif data_type == 's':
            value = str(value)
        elif data_type == 'r':
            if len(value) > 13:
                value = int(value[13])
            else:
                value = 0
        return value
    except ValueError:
        return None


"""
********************************
Code Section to be run.
********************************
"""


if __name__ == "__main__":
    data = load_seeking_alpha_data('AAPL')
    pprint(data)
