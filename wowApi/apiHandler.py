import requests
import json

class apiController:
    accessToken = ''
    namesToParse = dict()
    auctionData = dict()

    def __init__(self):
        self.__initNamesToParse()
        self.__updateAccessToken()
        self.__updateAuctionData()

    def __updateAccessToken(self):
        url = 'https://eu.battle.net/oauth/token'
        data = { 'grant_type': 'client_credentials' }
        auth = ('794c63048d594271866b4fffa27a61c7', 'wgmxlFfZ1lA8n5V32IJh491Iy2nT25cl')
        response = requests.post(url, data = data, auth = auth)

        tmpAccessToken = response.json().get('access_token', '')
        if(len(tmpAccessToken) > 0):
            self.accessToken = tmpAccessToken
            return True
        return False

    def __checkAccessToken(self):
        if(len(self.accessToken) == 0):
            return self.__updateAccessToken()
        return True

    def __updateAuctionData(self):
        if(not self.__checkAccessToken()):
            return
        
        url = 'https://eu.api.blizzard.com/data/wow/connected-realm/1396/auctions?namespace=dynamic-eu&access_token=' + self.accessToken
        response = requests.get(url).json()

        tmpAuctionData = response.get('auctions')
        if(len(tmpAuctionData) == 0):
            return

        #with open('auctionJson.json', 'w') as outfile:
        #    json.dump(tmpAuctionData, outfile, indent=4)

        self.auctionData.clear()
        for lot in tmpAuctionData:
            itemId = lot['item']['id']

            itemName = ''
            itemCategory = ''
            for category, items in self.namesToParse.items():
                itemName = items.get(str(itemId), '')
                if len(itemName) > 0:
                    itemCategory = category
                    break

            if len(itemName) > 0:
                lotDict = self.auctionData.setdefault(itemCategory, {}).setdefault(itemName, {})
                lotPrice = lot.get('unit_price', 0)
                if(lotPrice == 0):
                    lotPrice = lot['buyout']
                lotAmount = lot['quantity']
                lotPrice = round(lotPrice / 10000, 2)
                lotDict[lotPrice] = lotDict.get(lotPrice, 0) + lotAmount
        
        tmpDataDict = {}
        for category, _items in self.auctionData.items():
            for key, dict in _items.items():
                medianSize = 200
                summaryPrice = 0
                summaryAmount = 0
                if category == 'herbs':
                    for price, amount in sorted(dict.items()):
                        amountDelta = min(medianSize, amount)
                        summaryPrice += amountDelta * price
                        summaryAmount += amountDelta
                        medianSize -= summaryAmount
                        if medianSize <= 0:
                            break
                else:
                    summaryPrice = sorted(dict.items())[0][0]
                    summaryAmount = 1
                categoryDict = tmpDataDict.setdefault(category, {})
                categoryDict[key] = round(summaryPrice / summaryAmount, 2)

        for category, _items in self.namesToParse.items():
            for itemId, itemName in _items.items():
                if not tmpDataDict[category].get(itemName):
                    tmpDataDict[category].setdefault(itemName)
        self.auctionData = tmpDataDict

        with open('auctionData.json', 'w') as outfile:
            json.dump(self.auctionData, outfile, indent=4, sort_keys=True)

    def __initNamesToParse(self):
        if __name__ == '__main__':
            fname = 'namesToParse.json'
        else:
            fname = 'wowApi/namesToParse.json'
        with open(fname, 'r') as infile:
            self.namesToParse.clear()
            for key, dict in json.load(infile).items():
                self.namesToParse[key] = dict

def main():
    apiHandler = apiController()

if __name__ == '__main__':
    main()

    # def parseActionItems(self):
    #     for itemId in self.auctionData.keys():
    #         url = 'https://eu.api.blizzard.com/data/wow/item/' + str(itemId) + '?namespace=static-eu&locale=en_GB&access_token=' + self.accessToken
    #         response = requests.get(url).json()
    #         print(str(itemId) + 'done\n')
    #         self.idsToNames[itemId] = response.get('name', 'NULL')

    # def __updateConnectedRealms(self):
    #     if(not self.__checkAccessToken()):
    #         return
    #     url = 'https://eu.api.blizzard.com/data/wow/connected-realm/index?namespace=dynamic-eu&locale=en_GB&access_token=' + self.accessToken
    #     headers = { 'Authorization': 'Bearer ' + self.accessToken }
    #     response = requests.get(url, headers = headers)

    #     tmpConnectedRealms = response.json().get('connected_realms', list())
    #     if(len(tmpConnectedRealms) == 0):
    #         return
    #     for href in tmpConnectedRealms:
    #         hrefStr = href['href']
    #         index1 = hrefStr.rfind('/')
    #         index2 = hrefStr.find('?namespace=dynamic-eu')
    #         self.connectedRealms.append(hrefStr[index1 + 1:index2])

    # def __parseRealms(self):
    #     for realmId in self.connectedRealms:
    #         url = 'https://eu.api.blizzard.com/data/wow/connected-realm/' + realmId + '?namespace=dynamic-eu&locale=en_GB&access_token=' + self.accessToken
    #         headers = { 'Authorization': 'Bearer ' + self.accessToken }
    #         response = requests.get(url, headers = headers).json()

    #         for realm in response.get('realms', dict()):
    #             realmName = realm.get('name', '')
    #             if realmName == 'Azjol-Nerub':
    #                 with open('dynamicData/' + realmId + '.json', 'w') as outfile:
    #                     json.dump(response, outfile, indent=4)
    #                 break
