from collections import defaultdict
from datetime import datetime

import numpy
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from matplotlib import pyplot, ticker
import copy

driver = webdriver.Chrome()
# driver.implicitly_wait(25)
wait = WebDriverWait(driver, 10)
# bankList = list()
# class BankSelector:
#     def __init__(self, name, link, container, currency, buy, sale, date, doBefore = None):
#         self.name = name
#         self.link = link
#         self.container = container
#         self.currency = currency
#         self.buy = buy
#         self.sale = sale
#         self.date = date
#         self.doBefore = doBefore
#
#     def giveInfo(self):
#         return (self.name, self.link, self.container, self.currency,
#                 self.buy, self.sale, self.date, self.doBefore)
#
#
#
# # PUMB = BankSelector("PUMB", "https://about.pumb.ua/info/currency_converter",
# #           "#single-page-rate-1 tbody",
# #           "tr td:first-child",
# #           "tr td:nth-child(2)",
# #           "tr td:last-child")
#
# # def saveToCSV(bankName, curName, curBuy, curSale):
# #     with open(f"./Exchanges_CSV/{bankName}_{date.today().strftime("%d_%m_%Y")}.csv", "w", encoding="UTF-8") as f:
# #         f.write("Name,buy,sale\n")
# #         for i in range(len(curName)):
# #             csv_format = f"{curName[i]},{curBuy[i]},{curSale[i]}\n"
# #             f.write(csv_format)
# #
# # def saveToCSV(bankName, currency, curBuy, curSale, curDate):
# #     with open(f"./Exchanges_CSV/{bankName}_{date.today().strftime("%d_%m_%Y")}.csv", "w", encoding="UTF-8") as f:
# #         f.write("date,bank,name,buy,sale\n")
# #         for i in range(len(curBuy)):
# #             csv_format = f"{curDate[i]},{bankName},{currency},{curBuy[i]},{curSale[i]}\n"
# #             f.write(csv_format)
# #

def uniqueSetFromFile(filePath):
    uniqueItems = set()
    try:
        with open(filePath, "r", encoding = "UTF-8") as fr:
            next(fr) #skip first (header) line of csv
            for line in fr:
                uniqueItems.add(tuple(line.strip().split(",")[:3]))
    except FileNotFoundError:
        with open(filePath, 'w', encoding = "UTF-8") as file:
            file.write("date,bank,currency,buy,sale")
    return uniqueItems

def saveToOneCSV(itemsToAdd):
    filePath = "./Exchanges_CSV/Exchanges3.csv"
    uniqueCSVItems = uniqueSetFromFile(filePath)

    itemsToAdd = [item for item in itemsToAdd if tuple(item[:3]) not in uniqueCSVItems]

    uniqueListItems = set()
    itemsToFile = list()

    for item in itemsToAdd:
        key = tuple(item[:3])
        if key not in uniqueListItems:
            uniqueListItems.add(key)
            itemsToFile.append(item)

    with open(filePath, "a", encoding = "UTF-8") as fa:
        for line in itemsToFile:
            fa.write(f"\n{line[0]},{line[1]},{line[2]},{line[3]},{line[4]}")


def toDotNotation(string):
    return string.replace(',', '.').replace('-', '.')

def listToStr(lst, lengthLimit = None):
     lst[:] = [toDotNotation(item.get_attribute("innerHTML"))[:lengthLimit] for item in lst]
# #
# # def extractFromSite(driver, selectorsDictionary):
# #     currencyTable = driver.find_element(By.CSS_SELECTOR, selectorsDictionary["container"])
# #     currencyNames = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["names"])
# #     currencyBuy = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["buy"])
# #     currencySale = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["sale"])
# #     currencyDate = list()
# #     if selectorsDictionary.get("date") != None:
# #         currencyDate = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["date"])
# #     return currencyNames, currencyBuy, currencySale, currencyDate
# #
# # # def extractSiteData(bank, link, container, names, buy, sale, doBefore = None, test = False):
# # #     driver.get(link)
# # #
# # #     if doBefore != None:
# # #         doBefore()
# # #
# # #     selectorsDictionary = {"container": container, "names":names, "buy":buy, "sale":sale}
# # #     currencyNames, currencyBuy, currencySale = extractFromSite(driver, selectorsDictionary)
# # #
# # #     listToStr(currencyNames, 3)
# # #     listToStr(currencyBuy)
# # #     listToStr(currencySale)
# # #
# # #     itemsList = list()
# # #     for name, buy, sale in zip(currencyNames, currencyBuy, currencySale):
# # #         itemsList.append([date.today().strftime("%d.%m.%Y"), bank, name, buy, sale])
# # #     return itemsList
# #
# # def extractSiteData(bank, link, container, names, buy, sale, date = None, doBefore = None, *, currency = None):
# #
# #     driver.get(link)
# #
# #     if doBefore != None:
# #         doBefore()
# #
# #     selectorsDictionary = {"container": container, "names":names, "buy":buy, "sale":sale, "date":date}
# #     currencyNames, currencyBuy, currencySale, currencyDates = extractFromSite(driver, selectorsDictionary)
# #
# #     print("rASd")
# #     print(currencyNames)
# #     listToStr(currencyNames, 3)
# #     print("rASd")
# #     print(currencyNames)
# #     listToStr(currencyBuy)
# #     listToStr(currencySale)
# #     listToStr(currencyDates)
# #
# #     if currency != None:
# #         currencyNames = [currency for _ in currencyNames]
# #
# #     print(currencyNames)
# #     print(currencyBuy)
# #     print(currencySale)
# #     print(currencyDates)
# #
# #     itemsList = list()
# #     for name, buy, sale, date in zip(currencyNames, currencyBuy, currencySale, currencyDates):
# #         itemsList.append([date, bank, name, buy, sale])
# #
# #     saveToCSV("Pr",currencyNames,currencyBuy,currencySale,currencyDates)
# #     return itemsList
# #
# #
# #     # saveToCSV("PrivateMonthff",currencyNames,currencyBuy,currencySale,currencyDates)
# #
# #     # saveToCSV(bank, currencyNames, currencyBuy, currencySale)
# #
# # def extractAllDataFromPeriod(time):
# #
# #     banks = [
# #         ["PUMB", "https://about.pumb.ua/info/currency_converter",
# #          "#single-page-rate-1 tbody",
# #          "tr td:first-child",
# #          "tr td:nth-child(2)",
# #          "tr td:last-child"],
# #         ["OschadBank", "https://www.oschadbank.ua/currency-rate",
# #          "table.heading-block-currency-rate__table tbody",
# #          "tr td:nth-child(2) span",
# #          "tr td:nth-child(4) span",
# #          "tr td:nth-child(5) span"],
# #         ["PrivateBank", "https://privatbank.ua/obmin-valiut",
# #          "#swift-currency-block .table_block table.table_show tbody" ,
# #          ".tbody-swift .currency-swift",
# #          ".buy-swift",
# #          ".sale-swift",
# #          # PrivateFunc
# #          ]
# #     ]
# #
# #     itemsToAdd  = list()
# #     for bank in banks:
# #         itemsToAdd.extend(extractSiteData(*bank))
# #     saveToOneCSV(itemsToAdd)
#
#
# # #ПУМБ
# # extractSiteData("PUMB", "https://about.pumb.ua/info/currency_converter",
# #           "#single-page-rate-1 tbody",
# #           "tr td:first-child",
# #           "tr td:nth-child(2)",
# #           "tr td:last-child"
# #                 )
# # #Ощад банк
# # extractSiteData("OschadBank", "https://www.oschadbank.ua/currency-rate",
# #           "table.heading-block-currency-rate__table tbody",
# #           "tr td:nth-child(2) span",
# #           "tr td:nth-child(4) span",
# #           "tr td:nth-child(5) span"
# #                 )
# #
# # extractSiteData("PrivateBank", "https://privatbank.ua/obmin-valiut",
# #           "#swift-currency-block .table_block table.table_show tbody",
# #           ".tbody-swift .currency-swift",
# #           ".buy-swift",
# #           ".sale-swift",
# #                 lambda : driver.find_element(By.ID, "swift-block").send_keys(Keys.RETURN)
# #                 )
#
# # extractAllDataFromPeriod("t")
# def funcToextract():
#     # driver.find_element(By.ID, "swift-block").send_keys(Keys.RETURN)
#     driver.find_element(By.CSS_SELECTOR, "#archive-block").send_keys(Keys.RETURN)
#     driver.find_element(By.CSS_SELECTOR, "#table-currency").send_keys(Keys.RETURN)
#     driver.find_element(By.CSS_SELECTOR, "#one_month_by_table").send_keys(Keys.RETURN)
#
# def preparationActions(lstOfSelectors):
#     for selector in lstOfSelectors:
#         element = driver.find_element(By.CSS_SELECTOR, selector)
#         try:
#             wait = WebDriverWait(driver, 10)
#             # Ensure the element is present, visible, and enabled to receive a click.
#             wait.until(EC.element_to_be_clickable(element)).click()
#         except:
#             element.send_keys(Keys.RETURN)
#
#     # driver.find_element(By.CSS_SELECTOR, ".download-more").send_keys(Keys.RETURN)
# # extractSiteData(ч
# # "PrivateBank", "https://privatbank.ua/obmin-valiut",
# #          "#controls-by-table .toolbar-btn .table_container .table_block .rounded-table #table-archive tbody",
# #          "tr td:nth-child(3)",
# #          "tr td:nth-child(4)",
# #          "tr td:nth-child(5)",
# #          "tr td:first-child",
# #          funcToextract,
# #         currency="USD"
# # )
#
# # itemsToAdd = list()
# # itemsToAdd.extend(extractSiteData("PrivateBank", "https://privatbank.ua/obmin-valiut",
# #          "#controls-by-table .toolbar-btn .table_container .table_block .rounded-table #table-archive tbody",
# #          "tr td:nth-child(3)",
# #          "tr td:nth-child(4)",
# #          "tr td:nth-child(5)",
# #          "tr td:first-child",
# #          funcToextract,
# #         currency="USD"))
# # saveToOneCSV(itemsToAdd)
#
# # getSel()
#
# Private = BankSelector("PrivateBank", "https://privatbank.ua/obmin-valiut",
#          "#controls-by-table .toolbar-btn .table_container .table_block .rounded-table #table-archive tbody",
#        "USD",
#          "tr td:nth-child(4)",
#          "tr td:nth-child(5)",
#          "tr td:first-child",
#          funcToextract
#            )
#
# def oschadFunc():
#     el = wait.until(
#         EC.presence_of_element_located(
#             (By.CSS_SELECTOR, ".rates-archive .tabs__wrap div:nth-child(2)"))
#     )
#     el.click()
#     driver.find_element(By.CSS_SELECTOR, ".rates-archive .tabs__wrap div:nth-child(2)").click()
#     driver.find_element(By.CSS_SELECTOR, ".rates-archive__content .tabs__wrap div:nth-child(2)").click()
#     driver.find_element(By.CSS_SELECTOR, ".rate-toolbar__filter-period .rate-toolbar__filter-list li:nth-child(2)").click()
#     el = wait.until(
#         EC.presence_of_element_located(
#             (By.CSS_SELECTOR, ".rate-table__section-buttons button"))
#     )
#     el.click()
#     print("ELEMENT")
#     print(el)
#     print("ELEMENT")
#     el.click()
#     print("s")
#
# Oschad = BankSelector("Oschad", "https://www.oschadbank.ua/rates-archive",
#          ".rate-table__table tbody",
#        "USD",
#          "tr td:nth-child(3) span",
#          "tr td:nth-child(4) span",
#          "tr td:first-child span",
#          oschadFunc
#            )
#
#  # new Version
# def extractFromSite(driver, selectorsDictionary):
#     currencyTable = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selectorsDictionary["container"])))
#
#     # currencyTable = driver.find_element(By.CSS_SELECTOR, selectorsDictionary["container"])
#     wait.until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, selectorsDictionary["container"] + " " + selectorsDictionary["buy"]))
#     )
#
#     currencyBuy = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["buy"])
#     currencySale = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["sale"])
#     currencyDate = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["date"])
#     return currencyBuy, currencySale, currencyDate
#
# def saveToCSV(bankName, currency, curBuy, curSale, curDate):
#     with open(f"./Exchanges_CSV/{bankName}_{date.today().strftime("%d_%m_%Y")}.csv", "w", encoding="UTF-8") as f:
#         f.write("date,bank,name,buy,sale\n")
#         for i in range(len(curBuy)):
#             csv_format = f"{curDate[i]},{bankName},{currency},{curBuy[i]},{curSale[i]}\n"
#             f.write(csv_format)
#
# def extractSiteData(bank, link, container, currency, buy, sale, date, doBefore = None):
#     driver.get(link)
#
#     if doBefore != None:
#         doBefore()
#
#     selectorsDictionary = {"container": container, "buy":buy, "sale":sale, "date":date}
#     currencyBuy, currencySale, currencyDates = extractFromSite(driver, selectorsDictionary)
#
#
#     listToStr(currencyBuy)
#     print(currencyBuy)
#     print(currencySale)
#     print("---")
#     listToStr(currencySale)
#     print(currencySale)
#     print(currencyDates)
#     print("---")
#
#     listToStr(currencyDates)
#     print(currencyDates)
#     print("Dates number")
#     print(len(currencyDates))
#
#     itemsList = list()
#     for  buy, sale, date in zip(currencyBuy, currencySale, currencyDates):
#         itemsList.append([date, bank, currency, buy, sale])
#
#     saveToCSV("Pril",currency,currencyBuy,currencySale,currencyDates)
#     return itemsList



# triesLimit = 5
# tries = 0
# success = False
# while(not success and tries <= triesLimit):
#     try:
#         tries += 1
#         print("try N ", tries)
#         extractSiteData(*Oschad.giveInfo())
#         success = True
#     except StaleElementReferenceException:
#         print(StaleElementReferenceException)
def uniClick(elementToClick):
    driver.execute_script("arguments[0].click()", elementToClick)

def clickShowMore(show_more_selector, tr_selector):

    maxClicks = 10  # Safety limit to prevent infinite loop
    localWait = WebDriverWait(driver, 3)
    for _ in range(maxClicks):
        try:

            # Wait for the button to be clickable
            showMoreButton = localWait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, show_more_selector))
            )

            if showMoreButton.value_of_css_property("display") == 'none':
                print("Button is present but hidden by CSS, assuming all data loaded.")
                break
            # Get the current number of rows to wait for new ones
            initialRowCount = len(driver.find_elements(By.CSS_SELECTOR, tr_selector))

            # Click the button
            # show_more_button.click()
            uniClick(showMoreButton)
            # driver.execute_script("arguments[0].click()", show_more_button)

            # --- CRITICAL WAITING STEP ---
            # Wait for the number of rows to increase, indicating new data has loaded
            wait.until(
                lambda driver: len(
                    driver.find_elements(By.CSS_SELECTOR, tr_selector)) > initialRowCount
            )

        except TimeoutException:
            # The button is no longer clickable/present, meaning all data is loaded
            print("No more 'Show More' button found or data loaded.")
            break
        except StaleElementReferenceException:
            # Handle cases where the DOM changes right before clicking/checking
            continue
        except Exception as e:
            # Other errors (e.g., button not visible)
            print(f"Error during 'Show More' click: {e}")
            break


# --- Modified Actions and Extraction ---



def locatedElement(selector, prefix = None):
    element = None
    full_selector = f"{prefix} {selector}" if prefix else selector
    try:
        element = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, full_selector))
            )
    except TimeoutException:
        print(f"Timeout Exception, can be incorrect selector: {full_selector}\nOr element not accessible on the page")
    return element

def locatedElements(selector, prefix = None):
    elements = None
    full_selector = f"{prefix} {selector}" if prefix else selector
    try:
        elements = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, full_selector))
        )
    except TimeoutException:
        print(f"Timeout Exception, can be incorrect selector: {full_selector}\nOr elements not accessible on the page")
    return elements

def actions(bankDictionary):
# def actions(actionSelectorsList, showMoreSelector, trSelector):
    #Oschad
    # uniClick(locatedElement(".rates-archive .tabs__wrap div:nth-child(2)"))
    # uniClick(locatedElement(".rates-archive .tabs__wrap div:nth-child(2)"))
    # uniClick(locatedElement(".rates-archive__content .tabs__wrap div:nth-child(2)"))
    # uniClick(locatedElement(".rate-toolbar__filter-period .rate-toolbar__filter-list li:nth-child(2)"))
    # clickShowMore(".rate-table__section-buttons button", ".rate-table__table tbody tr")
    # Private
    actionSelectorsList = bankDictionary["selectors"]["actions"]
    showMoreSelector = bankDictionary["selectors"]["showMore"]
    trSelector = bankDictionary["selectors"]["tr"]
    print(actionSelectorsList)

    for selector in actionSelectorsList:
        uniClick(locatedElement(selector))

    # uniClick(locatedElement("#archive-block"))
    # uniClick(locatedElement("#table-currency"))
    # uniClick(locatedElement("#one_month_by_table"))
    clickShowMore(showMoreSelector, trSelector)


def extractDataFromTable(bankDictionary):

    currencyBuy = locatedElements(bankDictionary["selectors"]["buy"], bankDictionary["selectors"]["table"])
    currencySale = locatedElements(bankDictionary["selectors"]["sale"], bankDictionary["selectors"]["table"])
    currencyDate = locatedElements(bankDictionary["selectors"]["date"], bankDictionary["selectors"]["table"])

    listToStr(currencyBuy)
    listToStr(currencySale)
    listToStr(currencyDate)

    itemsList = list()
    for date, buy, sale in zip(currencyDate, currencyBuy, currencySale):
        itemsList.append([date, bankDictionary["name"], bankDictionary["currency"], buy, sale])

    return itemsList



# driver.get("https://www.oschadbank.ua/rates-archive")
# driver.get("https://privatbank.ua/obmin-valiut")
# OschadDict = {"table": ".rate-table__table tbody",
#               "buy": "tr td:nth-child(3) span",
#               "sale": "tr td:nth-child(4) span",
#               "date": "tr td:nth-child(1) span"}
OschadBank = {"name": "OschadBank",
              "link": "https://www.oschadbank.ua/rates-archive",
              "currency": "USD",
              "selectors":
                {"table": ".rate-table__table tbody",
                "buy": "tr td:nth-child(3) span",
                "sale": "tr td:nth-child(4) span",
                "date": "tr td:nth-child(1) span",
                "actions": [".rates-archive .tabs__wrap div:nth-child(2)",
                            ".rates-archive__content .tabs__wrap div:nth-child(2)",
                            ".rate-toolbar__filter-period .rate-toolbar__filter-list li:nth-child(2)"],
                "showMore": ".rate-table__section-buttons button",
                "tr": ".rate-table__table tbody tr"
                }
}



PrivateBank = {"name": "PrivateBank",
               "link": "https://privatbank.ua/obmin-valiut",
               "currency": "USD",
               "selectors" :
                    {"table": "#table-archive tbody",
                    "buy": "tr td:nth-child(4)",
                    "sale": "tr td:nth-child(5)",
                    "date": "tr td:nth-child(1)",
                    "actions": ["#archive-block",
                                "#table-currency",
                                "#one_month_by_table"],
                    "showMore": "div.download-more",
                    "tr": "#table-archive tbody tr"
                    }
               }
# PrivateDict = {"table": "#table-archive tbody",
#               "buy": "tr td:nth-child(4)",
#               "sale": "tr td:nth-child(5)",
#               "date": "tr td:nth-child(1)"}
# PrivateSelectors = {
#     "actions": ["#archive-block","#table-currency","#one_month_by_table"],
#     "showMore" : "div.download-more",
#     "tr": "#table-archive tbody tr"
# }
# actions()
# extractDataFromSite(PrivateDict)

def globalize(bankDictionary):
    driver.get(bankDictionary["link"])
    actions(bankDictionary)
    lst = extractDataFromTable(bankDictionary)
    return lst

def prepareBanks():
    OschadBankUSD = {"name": "OschadBank",
                  "link": "https://www.oschadbank.ua/rates-archive",
                  "currency": "USD",
                  "selectors":
                      {"table": ".rate-table__table tbody",
                       "buy": "tr td:nth-child(3) span",
                       "sale": "tr td:nth-child(4) span",
                       "date": "tr td:nth-child(1) span",
                       "actions": [".rates-archive .tabs__wrap div:nth-child(2)",
                                   ".rates-archive__content .tabs__wrap div:nth-child(2)",
                                   ".rate-toolbar__filter-period .rate-toolbar__filter-list li:nth-child(2)"],
                       "showMore": ".rate-table__section-buttons button",
                       "tr": ".rate-table__table tbody tr"
                       }
                  }

    PrivateBankUSD = {"name": "PrivateBank",
                   "link": "https://privatbank.ua/obmin-valiut",
                   "currency": "USD",
                   "selectors":
                       {"table": "#table-archive tbody",
                        "buy": "tr td:nth-child(4)",
                        "sale": "tr td:nth-child(5)",
                        "date": "tr td:nth-child(1)",
                        "actions": ["#archive-block",
                                    "#table-currency",
                                    "#one_month_by_table"],
                        "showMore": "div.download-more",
                        "tr": "#table-archive tbody tr"
                        }
                   }
    PrivateBankEUR = copy.deepcopy(PrivateBankUSD)
    PrivateBankEUR["currency"] = "EUR"
    PrivateBankEUR["selectors"]["actions"].append("#bs-select-2-2")

    OschadBankEUR = copy.deepcopy(OschadBankUSD)
    OschadBankEUR["currency"] = "EUR"
    OschadBankEUR["selectors"]["actions"].append(".rate-toolbar__currencies-select div.base-select__field")
    OschadBankEUR["selectors"]["actions"].append(".rate-toolbar__currencies-select .base-select__list ul li:nth-child(2)")
    banksList = [PrivateBankUSD, OschadBankUSD, PrivateBankEUR, OschadBankEUR]
    return banksList

def main():
    itemsToAdd = list()
    banks = prepareBanks()
    for bank in banks:
        itemsToAdd.extend(globalize(bank))
    saveToOneCSV(itemsToAdd)

# main()


globalList = list()
with open("./Exchanges_CSV/Exchanges3.csv", "r", encoding="UTF-8") as fr:
    next(fr)  # skip first (header) line of csv
    for line in fr:
        globalList.extend([line.strip().split(",")])
print(globalList)
print(len(globalList))
for sublist in globalList:
    date_string = sublist[0]

    # Convert the string to a datetime object
    date_object = datetime.strptime(date_string, '%d.%m.%Y')

    # Replace the string in the sublist with the datetime object
    sublist[0] = date_object


grouped_data = defaultdict(list)



for record in globalList:
    bank = record[1]
    currency = record[2]
    # Create a unique key (e.g., 'bank1_currency1')
    key = f"{bank}{currency}"
    # Append the entire record to the list associated with this key
    grouped_data[key].append(record)
final_results = dict(grouped_data)
for key, value_list in final_results.items():
    print(f"\nGroup: {key}")
    print(value_list)


# print(globalList)
# date = [item[0] for item in globalList]
# buy = [item[3] for item in globalList]
# sale = [item[4] for item in globalList]
# print(date)
# print(buy)
# print(sale)

# dates = [datetime.strptime(d, '%d.%m.%Y') for d in date]
pyplot.figure(figsize=(12, 8))

pyplot.plot([record[0] for record in grouped_data["PrivateBankUSD"]], [float(record[3]) for record in grouped_data["PrivateBankUSD"]], label = "PrivateBankUSD Buy", ls='--', marker='o')
pyplot.plot([record[0] for record in grouped_data["PrivateBankUSD"]], [float(record[4]) for record in grouped_data["PrivateBankUSD"]], label = "PrivateBankUSD Sale" ,ls='--', marker='o')
pyplot.plot([record[0] for record in grouped_data["OschadBankUSD"]], [float(record[3]) for record in grouped_data["OschadBankUSD"]], label = "OschadBankUSD Buy", marker='*')
pyplot.plot([record[0] for record in grouped_data["OschadBankUSD"]], [float(record[4]) for record in grouped_data["OschadBankUSD"]], label = "OschadBankUSD Sale", marker='*')
pyplot.grid()

desired_ticks = numpy.arange(40.0, 43.25, 0.25)
pyplot.yticks(desired_ticks)

pyplot.xticks(rotation=45, ha='right')
pyplot.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
pyplot.tight_layout()
pyplot.show()


# pyplot.show()
