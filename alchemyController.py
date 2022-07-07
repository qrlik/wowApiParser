from wowApi import apiHandler
import json

class shadowlandsAlchemy:
    _apiController = apiHandler.apiController()
    _potions = {}
    _deathBlossom = 0.
    _risingGlory = 0.
    _vigilsTorch = 0.
    _marrowroot = 0.
    _widowbloom = 0.
    _nightshade = 0.
    _runeEtchedVial = 0.04

    def __init__(self):
        self.__initBasicHerbs()
        self.__initRecipes()
        self.__calculateProfit()

    def __initBasicHerbs(self):
        basicHerbs = self._apiController.auctionData['herbs']
        self._deathBlossom = basicHerbs['Death Blossom']
        self._risingGlory = basicHerbs['Rising Glory']
        self._vigilsTorch = basicHerbs['Vigil\'s Torch']
        self._marrowroot = basicHerbs['Marrowroot']
        self._widowbloom = basicHerbs['Widowbloom']
        self._nightshade = basicHerbs['Nightshade']

    def __initRecipes(self):
        _2DeathBlossom = self._runeEtchedVial + 2 * self._deathBlossom
        _covenantsHerbs = self._risingGlory + self._marrowroot + self._widowbloom + self._vigilsTorch
        _3risingGlory_3vigilTorch = self._runeEtchedVial + 3 * self._risingGlory + 3 * self._vigilsTorch
        _3risingGlory_3marrowroot = self._runeEtchedVial + 3 * self._risingGlory + 3 * self._marrowroot
        _5vigilTorch = self._runeEtchedVial + 5 * self._vigilsTorch

        self._potions['Embalmer\'s Oil'] = _2DeathBlossom
        self._potions['Potion of Deathly Fixation'] = self._runeEtchedVial + 3 * self._widowbloom + 3 * self._vigilsTorch
        self._potions['Potion of Divine Awakening'] = _3risingGlory_3vigilTorch
        self._potions['Potion of Empowered Exorcisms'] = self._runeEtchedVial + 3 * self._marrowroot + 3 * self._widowbloom
        self._potions['Potion of Hardened Shadows'] = _3risingGlory_3vigilTorch
        self._potions['Potion of the Hidden Spirit'] = _2DeathBlossom + 3 * self._risingGlory
        self._potions['Potion of Phantom Fire'] = _3risingGlory_3marrowroot
        self._potions['Potion of Sacrificial Anima'] = self._runeEtchedVial + 6 * self._widowbloom
        self._potions['Potion of Shaded Sight'] = _2DeathBlossom + 3 * self._widowbloom
        self._potions['Potion of Soul Purity'] = _2DeathBlossom + 3 * self._vigilsTorch
        self._potions['Potion of Specter Swiftness'] = _2DeathBlossom + 3 * self._marrowroot
        self._potions['Potion of Spectral Agility'] = self._runeEtchedVial + 5 * self._widowbloom
        self._potions['Potion of Spectral Intellect'] = self._runeEtchedVial + 5 * self._marrowroot
        self._potions['Potion of Spectral Stamina'] = _5vigilTorch
        self._potions['Potion of Spectral Strength'] = self._runeEtchedVial + 5 * self._risingGlory
        self._potions['Potion of Spiritual Clarity'] = _5vigilTorch
        self._potions['Potion of the Psychopomp\'s Speed'] = _3risingGlory_3vigilTorch
        self._potions['Potion of Unhindered Passing'] = self._runeEtchedVial + _covenantsHerbs
        self._potions['Shadowcore Oil'] = _2DeathBlossom
        self._potions['Spectral Flask of Power'] = self._runeEtchedVial + 3 * self._nightshade + 4 * _covenantsHerbs
        self._potions['Spectral Flask of Stamina'] = _3risingGlory_3marrowroot + self._nightshade
        self._potions['Spiritual Anti-Venom'] = _2DeathBlossom
        self._potions['Spiritual Healing Potion'] = _2DeathBlossom
        self._potions['Spiritual Mana Potion'] = _2DeathBlossom
        self._potions['Spiritual Rejuvenation Potion'] = 2 * _2DeathBlossom

        with open('craftData.json', 'w') as outfile:
            json.dump(self._potions, outfile, indent=4, sort_keys=True)

    def __calculateProfit(self):
        profitDict = {}
        potionsAuctionData = self._apiController.auctionData['potions']
        for potion, craftPrice in self._potions.items():
            profitDict[round(potionsAuctionData[potion] - craftPrice, 2)] = potion

        with open('profitData.json', 'w') as outfile:
            json.dump(profitDict, outfile, indent=4, sort_keys=True)


def main():
    shadowlands = shadowlandsAlchemy()

if __name__ == '__main__':
    main()