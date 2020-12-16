import requests
from bs4 import BeautifulSoup
import json

# Tsla is on fire these days. Build a price tracker:
def priceTracker():
    # Yahoo finance URL to parse
    url = 'https://finance.yahoo.com/quote/tsla'

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup)
    # Get the price text
    price = soup.find_all('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'})[0].find('span').text
    
    return price

# Function for sending pushbullet message
def pushbullet_message(title, body):
    msg = {"type": "note", "title": title, "body": body}
    TOKEN = '********************' # get TOKEN from https://www.pushbullet.com/#settings
    resp = requests.post('https://api.pushbullet.com/v2/pushes', 
                         data=json.dumps(msg),
                         headers={'Authorization': 'Bearer ' + TOKEN,
                                  'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Error', resp.status_code)
    else:
        print ('Message sent') 
        
# Track and print price continuously..
while True:
    current_price = priceTracker()
    # Print price
    print('Current Price of Tesla: $' + current_price)
    # Send pushbullet message if reaches high price
    if float(current_price) > 630.0:
        pushbullet_message('Tsla price:', '$' + current_price)
        break           

# Or use win10 task scheduler to scheule the program run
# current_price = priceTracker()
# print('Current Price of Tesla: $' + current_price)
# if float(current_price) > 630.0:
#     pushbullet_message('Tsla price:', '$' + current_price)