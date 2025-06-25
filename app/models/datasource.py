from enum import Enum

class DataSource(str, Enum):
    COINGECKO = "coingecko"
    COINMARKETCAP = "coinmarketcap"
    LUNARCRUSH = "lunarcrush"
