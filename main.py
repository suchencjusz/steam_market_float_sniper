import argparse
from ast import arg
import time
import os
from types import NoneType
import ujson
import time
import requests
import requests_cache
import static
import utils
import concurrent.futures
from datetime import timedelta


class SkinInfo():
    def __init__(self, listing_id, asset_id, item_price, float_value, js_link, pattern_id):
        self.listing_id = listing_id
        self.asset_id = asset_id
        self.item_price = item_price
        self.float_value = float_value
        self.js_link = js_link
        self.pattern_id = pattern_id

    def encode(self):
        return self.__dict__


class SellerRequest():
    def __init__(self, listing_id, asset_id, item_price, inspect_link):
        self.listing_id = listing_id
        self.asset_id = asset_id
        self.item_price = item_price
        self.inspect_link = inspect_link

    def encode(self):
        return self.__dict__


class MarketMachine():

    def ValidUrl(url):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        return url

    def InspectLinkParser(url, listingid, assetid):
        link = url.split("%20M")[0]
        link = link + "%20M" + str(listingid) + "A" + \
            str(assetid) + url.split("%assetid%")[1]

        return link

    def JavaScriptLink(assetid, listingid):
        return f"javascript:BuyMarketListing('listing', '{listingid}', 730, '2', '{assetid}')"

    items = []

    def appendRequest(listing_id, asset_id, item_price, inspect_link):
        MarketMachine.items.append(SellerRequest(listing_id, asset_id,
                                                 item_price, inspect_link))

    def GetAllRequestsData(item_link, currency):
        link = MarketMachine.ValidUrl(item_link)
        link = link + "/render/?currency=" + str(static.CURRENCY[currency][0])

        master_count = 0
        initial_count = 0
        attempt = 0

        while initial_count < 1:    
            try:
                initial_count = int(ujson.loads(
                    requests.get(link).text)["total_count"])
                print("Getting total count of items from market...         ", end="\r")
            except:
                attempt += 1
                print(f"Failed to get total count of items from market... Retrying... {attempt}       ", end="\r")
                time.sleep(5)
            time.sleep(1)
        
        master_count = initial_count

        print("Items on market: " + str(initial_count), end="\r")

        start = 0

        while initial_count > 100:

            print(f"Getting data from steam market - {round((start / master_count) * 100)}%                 ", end="\r")

            r = requests.get(link + f"&start={start}&count=100")

            if type(r.text) == str:
                if len(r.text) > 1069:

                    initial_count -= 100

                    _requests = ujson.loads(r.text.split('"listinginfo":')[
                                            1].split(',"assets":')[0])

                    for i in _requests:

                        try:
                            price = int(
                                _requests[i]['converted_price']) + int(_requests[i]['converted_fee'])
                            padded = "%03d" % (price,)
                            price = padded[0:-2] + '.' + padded[-2:]
                        except KeyError:
                            price = 'SOLD'

                        # items.append(SellerRequest(_requests[i]["listingid"],
                        #                            _requests[i]["asset"]["id"],
                        #                            price,
                        #                            MarketMachine.InspectLinkParser(_requests[i]["asset"]["market_actions"][0]["link"],                                                                              _requests[i]["listingid"], _requests[i]["asset"]["id"])))

                        MarketMachine.appendRequest(_requests[i]["listingid"],
                                                    _requests[i]["asset"]["id"],
                                                    price,
                                                    MarketMachine.InspectLinkParser(_requests[i]["asset"]["market_actions"][0]["link"],                                                                              _requests[i]["listingid"], _requests[i]["asset"]["id"]))

                    start += 100
                else:
                    time.sleep(5)
            else:
                time.sleep(5)

        else:

            print(f"Getting items from steam market - {round((start / master_count) * 100)}%               ", end="\r")

            r = requests.get(link + f"&start={start}&count={initial_count}")

            if type(r.text) == str:
                if len(r.text) > 1069:

                    _requests = ujson.loads(r.text.split('"listinginfo":')[
                                            1].split(',"assets":')[0])

                    for i in _requests:

                        try:
                            price = int(
                                _requests[i]['converted_price']) + int(_requests[i]['converted_fee'])
                            padded = "%03d" % (price,)
                            price = padded[0:-2] + '.' + padded[-2:]
                        except KeyError:
                            price = 'SOLD'

                        MarketMachine.appendRequest(_requests[i]["listingid"], _requests[i]["asset"]["id"], price, MarketMachine.InspectLinkParser(
                            _requests[i]["asset"]["market_actions"][0]["link"], _requests[i]["listingid"], _requests[i]["asset"]["id"]))
                else:
                    time.sleep(5)
            else:
                time.sleep(5)

        return MarketMachine.items


skinsParsed = []


class SkinMachine():

    cached_req = requests_cache.CachedSession(
        'cache',
        expire_after=timedelta(days=9999),
        allowable_codes=[200],
        allowable_methods=['GET', 'POST']
    )

    def getSkinFloat(sr):
        global skinsParsed

        _sr = sr
        key = 0
        headers = {}

        try:
            key = os.environ.get('CSGO_FLOAT_API_KEY')
            headers = {'Authorization': key}
        except:
            pass
        

        r = SkinMachine.cached_req.get(
            "https://api.csgofloat.com/?url=" + _sr.inspect_link, headers=headers)

        _skinInfo = SkinInfo(_sr.listing_id, _sr.asset_id, _sr.item_price, ujson.loads(r.text)[
                             "iteminfo"]["floatvalue"], MarketMachine.JavaScriptLink(_sr.asset_id, _sr.listing_id), ujson.loads(r.text)[
                             "iteminfo"]["paintseed"])

        skinsParsed.append(_skinInfo.encode())

    def GetAllSkinsFloat(sr):
        global skinsParsed
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for request in sr:
                executor.submit(SkinMachine.getSkinFloat, request)

        return skinsParsed

output_file_name = ""

parser = argparse.ArgumentParser(description='CSGO Market Float Sniper')
parser.add_argument('-l', help='Link to the item on the market', required=True)
parser.add_argument('-c', help='Currency to use (-c list - to show all currencies)', required=True)
parser.add_argument('-o', help='Output file', required=False)
# parser.add_argument('-w', help='Watch mode', required=False)
# parser.add_argument('-f', '--float', help='Get float of the item', required=False)
args = parser.parse_args()

output_file_name = str(args.o)

if args.c == "list":
    utils.displayAllCurrencies()
    
st = time.time()

x = MarketMachine.GetAllRequestsData(args.l, args.c)
x = SkinMachine.GetAllSkinsFloat(x)

utils.SaveDataToCSV(x, output_file_name)

# x = MarketMachine.GetAllRequestsData(
    # item_link='https://steamcommunity.com/market/listings/730/AWP%20%7C%20Electric%20Hive%20%28Field-Tested%29', currency='PLN')
# 
# x = SkinMachine.GetAllSkinsFloat(x)

print("Done in " + str(round(time.time() - st, 1)) + f" seconds! Data saved in {output_file_name}.csv                            ")