import copy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from matplotlib import pyplot
from datetime import date

driver = webdriver.Chrome()
driver.implicitly_wait(5)
bankList = list()
class BankSelector:
    def __init__(self, name, link, container, currencies, buy, sale, doBefore = None):
        self.name = name
        self.link = link
        self.container = container
        self.currencies = currencies
        self.buy = buy
        self.sale = sale
        self.doBefore = doBefore

    def giveInfo(self):
        return (self.name, self.link, self.container, self.container, self.currencies,
                self.buy, self.sale, self.doBefore)

Private = BankSelector("PrivateBank", "https://privatbank.ua/obmin-valiut",
         "#swift-currency-block .table_block table.table_show tbody",
         ".tbody-swift .currency-swift",
         ".buy-swift",
         ".sale-swift",
         lambda: driver.find_element(By.ID, "swift-block").send_keys(Keys.RETURN))

# PUMB = BankSelector("PUMB", "https://about.pumb.ua/info/currency_converter",
#           "#single-page-rate-1 tbody",
#           "tr td:first-child",
#           "tr td:nth-child(2)",
#           "tr td:last-child")

# def saveToCSV(bankName, curName, curBuy, curSale):
#     with open(f"./Exchanges_CSV/{bankName}_{date.today().strftime("%d_%m_%Y")}.csv", "w", encoding="UTF-8") as f:
#         f.write("Name,buy,sale\n")
#         for i in range(len(curName)):
#             csv_format = f"{curName[i]},{curBuy[i]},{curSale[i]}\n"
#             f.write(csv_format)


def getSel():
    banks = list()
    with open("./bankSelectorsDay.csv", "r", encoding="UTF-8") as fr:
        next(fr)
        for line in fr:
            banks.append(line.strip().split("|"))

    print(banks)

    itemsToAdd = list()
    for bank in banks:
        itemsToAdd.extend(extractSiteData(*bank))
    print(itemsToAdd)
    saveToOneCSV(itemsToAdd)

def saveToCSV(bankName, curName, curBuy, curSale, curDate):
    with open(f"./Exchanges_CSV/{bankName}_{date.today().strftime("%d_%m_%Y")}.csv", "w", encoding="UTF-8") as f:
        f.write("date,bank,name,buy,sale\n")
        for i in range(len(curName)):
            csv_format = f"{curDate[i]},{bankName},{curName[i]},{curBuy[i]},{curSale[i]}\n"
            f.write(csv_format)

def saveToOneCSV(itemsToAdd):
    unique_items = set()
    try:
        with open("./Exchanges_CSV/Exchanges.csv", "r", encoding = "UTF-8") as fr:
            next(fr) #skip first (header) line of csv
            for line in fr:
                unique_items.add(tuple(line.strip().split(",")[:3]))
    except FileNotFoundError:
        with open("./Exchanges_CSV/Exchanges.csv", 'w', encoding = "UTF-8") as file:
            file.write("date,bank,currency,buy,sale")

    itemsToAdd = [item for item in itemsToAdd if tuple(item[:3]) not in unique_items]

    with open("./Exchanges_CSV/Exchanges.csv", "a", encoding = "UTF-8") as fa:
        for line in itemsToAdd:
            fa.write(f"\n{line[0]},{line[1]},{line[2]},{line[3]},{line[4]}")

def listToStr(lst, lengthLimit = None):
     lst[:] = [item.get_attribute("innerHTML")[:lengthLimit] for item in lst];

def extractFromSite(driver, selectorsDictionary):
    currencyTable = driver.find_element(By.CSS_SELECTOR, selectorsDictionary["container"])
    currencyNames = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["names"])
    currencyBuy = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["buy"])
    currencySale = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["sale"])
    currencyDate = list()
    if selectorsDictionary.get("date") != None:
        currencyDate = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["date"])
    return currencyNames, currencyBuy, currencySale, currencyDate

# def extractSiteData(bank, link, container, names, buy, sale, doBefore = None, test = False):
#     driver.get(link)
#
#     if doBefore != None:
#         doBefore()
#
#     selectorsDictionary = {"container": container, "names":names, "buy":buy, "sale":sale}
#     currencyNames, currencyBuy, currencySale = extractFromSite(driver, selectorsDictionary)
#
#     listToStr(currencyNames, 3)
#     listToStr(currencyBuy)
#     listToStr(currencySale)
#
#     itemsList = list()
#     for name, buy, sale in zip(currencyNames, currencyBuy, currencySale):
#         itemsList.append([date.today().strftime("%d.%m.%Y"), bank, name, buy, sale])
#     return itemsList

def extractSiteData(bank, link, container, names, buy, sale, date = None, doBefore = None, *, currency = None):

    driver.get(link)

    if doBefore != None:
        doBefore()

    selectorsDictionary = {"container": container, "names":names, "buy":buy, "sale":sale, "date":date}
    currencyNames, currencyBuy, currencySale, currencyDates = extractFromSite(driver, selectorsDictionary)

    print("rASd")
    print(currencyNames)
    listToStr(currencyNames, 3)
    print("rASd")
    print(currencyNames)
    listToStr(currencyBuy)
    listToStr(currencySale)
    listToStr(currencyDates)

    if currency != None:
        currencyNames = [currency for _ in currencyNames]

    print(currencyNames)
    print(currencyBuy)
    print(currencySale)
    print(currencyDates)

    itemsList = list()
    for name, buy, sale, date in zip(currencyNames, currencyBuy, currencySale, currencyDates):
        itemsList.append([date, bank, name, buy, sale])

    saveToCSV("Pr",currencyNames,currencyBuy,currencySale,currencyDates)
    return itemsList


    # saveToCSV("PrivateMonthff",currencyNames,currencyBuy,currencySale,currencyDates)

    # saveToCSV(bank, currencyNames, currencyBuy, currencySale)

def extractAllDataFromPeriod(time):

    banks = [
        ["PUMB", "https://about.pumb.ua/info/currency_converter",
         "#single-page-rate-1 tbody",
         "tr td:first-child",
         "tr td:nth-child(2)",
         "tr td:last-child"],
        ["OschadBank", "https://www.oschadbank.ua/currency-rate",
         "table.heading-block-currency-rate__table tbody",
         "tr td:nth-child(2) span",
         "tr td:nth-child(4) span",
         "tr td:nth-child(5) span"],
        ["PrivateBank", "https://privatbank.ua/obmin-valiut",
         "#swift-currency-block .table_block table.table_show tbody" ,
         ".tbody-swift .currency-swift",
         ".buy-swift",
         ".sale-swift",
         # PrivateFunc
         ]
    ]

    itemsToAdd  = list()
    for bank in banks:
        itemsToAdd.extend(extractSiteData(*bank))
    saveToOneCSV(itemsToAdd)


# #ПУМБ
# extractSiteData("PUMB", "https://about.pumb.ua/info/currency_converter",
#           "#single-page-rate-1 tbody",
#           "tr td:first-child",
#           "tr td:nth-child(2)",
#           "tr td:last-child"
#                 )
# #Ощад банк
# extractSiteData("OschadBank", "https://www.oschadbank.ua/currency-rate",
#           "table.heading-block-currency-rate__table tbody",
#           "tr td:nth-child(2) span",
#           "tr td:nth-child(4) span",
#           "tr td:nth-child(5) span"
#                 )
#
# extractSiteData("PrivateBank", "https://privatbank.ua/obmin-valiut",
#           "#swift-currency-block .table_block table.table_show tbody",
#           ".tbody-swift .currency-swift",
#           ".buy-swift",
#           ".sale-swift",
#                 lambda : driver.find_element(By.ID, "swift-block").send_keys(Keys.RETURN)
#                 )

# extractAllDataFromPeriod("t")
def funcToextract():
    # driver.find_element(By.ID, "swift-block").send_keys(Keys.RETURN)
    driver.find_element(By.ID, "archive-block").send_keys(Keys.RETURN)
    driver.find_element(By.ID, "table-currency").send_keys(Keys.RETURN)
    driver.find_element(By.ID, "one_month_by_table").send_keys(Keys.RETURN)
# extractSiteData(
# "PrivateBank", "https://privatbank.ua/obmin-valiut",
#          "#controls-by-table .toolbar-btn .table_container .table_block .rounded-table #table-archive tbody",
#          "tr td:nth-child(3)",
#          "tr td:nth-child(4)",
#          "tr td:nth-child(5)",
#          "tr td:first-child",
#          funcToextract,
#         currency="USD"
# )

# itemsToAdd = list()
# itemsToAdd.extend(extractSiteData("PrivateBank", "https://privatbank.ua/obmin-valiut",
#          "#controls-by-table .toolbar-btn .table_container .table_block .rounded-table #table-archive tbody",
#          "tr td:nth-child(3)",
#          "tr td:nth-child(4)",
#          "tr td:nth-child(5)",
#          "tr td:first-child",
#          funcToextract,
#         currency="USD"))
# saveToOneCSV(itemsToAdd)

# getSel()

extractSiteData(*Private.giveInfo())
 # new Version
def extractFromSite(driver, selectorsDictionary):
    currencyTable = driver.find_element(By.CSS_SELECTOR, selectorsDictionary["container"])
    currencyBuy = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["buy"])
    currencySale = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["sale"])
    currencyDate = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["date"])
    return currencyBuy, currencySale, currencyDate