import random
import requests
cities_data = {
    1: ["Paris", "", "FR", 1],
    2: ["Madrid", "", "ES", 1],
    3: ["Tokyo", "", "JP", 1],
    4: ["Rome", "", "IT", 1],
    5: ["Milan", "", "IT", 1],
    6: ["New York", "NY", "US", 1],
    7: ["Amsterdam", "", "NL", 1],
    8: ["Sydney", "", "AU", 1],
    9: ["Singapore", "", "SG", 1],
    10: ["Barcelona", "", "ES", 1],
    11: ["Taipei", "", "TW", 1],
    12: ["Seoul", "", "KR", 1],
    13: ["London", "", "GB", 1],
    14: ["Dubai", "", "AE", 1],
    15: ["Berlin", "", "DE", 1],
    16: ["Osaka", "", "JP", 1],
    17: ["Bangkok", "", "TH", 1],
    18: ["Los Angeles", "CA", "US", 1],
    19: ["Istanbul", "", "TR", 1],
    20: ["Melbourne", "", "AU", 1],
    21: ["Hong Kong", "", "HK", 1],
    22: ["Munich", "", "DE", 1],
    23: ["Las Vegas", "NV", "US", 1],
    24: ["Florence", "", "IT", 1],
    25: ["Prague", "", "CZ", 1],
    26: ["Dublin", "", "IE", 1],
    27: ["Kyoto", "", "JP", 1],
    28: ["Vienna", "", "AT", 1],
    29: ["Lisbon", "", "PT", 1],
    30: ["Venice", "", "IT", 1],
    31: ["Kuala Lumpur", "", "MY", 1],
    32: ["Athens", "", "GR", 1],
    33: ["Orlando", "FL", "US", 1],
    34: ["Toronto", "", "CA", 1],
    35: ["Miami", "FL", "US", 1],
    36: ["San Francisco", "CA", "US", 1],
    37: ["Shanghai", "", "CN", 1],
    38: ["Frankfurt", "", "DE", 1],
    39: ["Copenhagen", "", "DK", 1],
    40: ["Zurich", "", "CH", 1],
    41: ["Washington", "DC", "US", 1],
    42: ["Pattaya", "", "TH", 1],
    43: ["Vancouver", "", "CA", 1],
    44: ["Stockholm", "", "SE", 1],
    45: ["Mexico City", "", "MX", 1],
    46: ["Oslo", "", "NO", 1],
    47: ["São Paulo", "", "BR", 1],
    48: ["Phuket", "", "TH", 1],
    49: ["Helsinki", "", "FI", 1],
    50: ["Brussels", "", "BE", 1],
    51: ["Budapest", "", "HU", 1],
    52: ["Guangzhou", "", "CN", 1],
    53: ["Nice", "", "FR", 1],
    54: ["Palma", "", "ES", 1],
    55: ["Honolulu", "HI", "US", 1],
    56: ["Beijing", "", "CN", 1],
    57: ["Warsaw", "", "PL", 1],
    58: ["Seville", "", "ES", 1],
    59: ["Valencia", "", "ES", 1],
    60: ["Shenzhen", "", "CN", 1],
    61: ["Doha", "", "QA", 1],
    62: ["Abu Dhabi", "", "AE", 1],
    63: ["Antalya", "", "TR", 1],
    64: ["Fukuoka", "", "JP", 1],
    65: ["Sapporo", "", "JP", 1],
    66: ["Busan", "", "KR", 1],
    67: ["Macau", "", "MO", 1],
    68: ["Edinburgh", "", "GB", 1],
    69: ["Montreal", "", "CA", 1],
    70: ["Cancún", "", "MX", 1],
    71: ["Bologna", "", "IT", 1],
    72: ["Rhodes", "", "GR", 1],
    73: ["Verona", "", "IT", 1],
    74: ["Delhi", "", "IN", 1],
    75: ["Porto", "", "PT", 1],
    76: ["Ho Chi Minh City", "", "VN", 1],
    77: ["Buenos Aires", "", "AR", 1],
    78: ["Marne-la-Vallée", "", "FR", 1],
    79: ["Rio de Janeiro", "", "BR", 1],
    80: ["Kraków", "", "PL", 1],
    81: ["Heraklion", "", "GR", 1],
    82: ["Johor Bahru", "", "MY", 1],
    83: ["Hanoi", "", "VN", 1],
    84: ["Tel Aviv", "", "IL", 1],
    85: ["Sharjah", "", "AE", 1],
    86: ["Thessaloniki", "", "GR", 1],
    87: ["Lima", "", "PE", 1],
    88: ["Medina", "", "SA", 1],
    89: ["Tbilisi", "", "GE", 1],
    90: ["Riyadh", "", "SA", 1],
    91: ["Tallinn", "", "EE", 1],
    92: ["Marrakech", "", "MA", 1],
    93: ["Mecca", "", "SA", 1],
    94: ["Denpasar", "", "ID", 1],
    95: ["Punta Cana", "", "DO", 1],
    96: ["Santiago", "", "CL", 1],
    97: ["Vilnius", "", "LT", 1],
    98: ["Jerusalem", "", "IL", 1],
    99: ["Zhuhai", "", "CN", 1],
    100: ["Cairo", "", "EG", 1]
}


openWeatherAPIKey = "40485748d0b1c814e3b69687e60fd4f1"


def accessWeather():
    cityNo = randInt(1,100)
    cityArray = cities_data[cityNo]
    city = cityArray[0]
    stateCode = cityArray[1]
    countryCode = cityArray[2]
    location = f"{city},{stateCode},{countryCode}" if stateCode else f"{city},{countryCode}"
    f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={openWeatherAPIKey}"



def toy_hash(input_str):
    hash_val = 0xABCDEF  # random starting value
    for ch in input_str:
        hash_val ^= (ord(ch) * 16777619)
        hash_val = (hash_val << 5 | hash_val >> 27) & 0xFFFFFFFF  # circular shift
    return hex(hash_val)


input_str = ""
print(toy_hash(input_str))