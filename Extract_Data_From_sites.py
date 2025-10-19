from collections import defaultdict
from datetime import datetime
import numpy
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from matplotlib import pyplot, ticker
import copy

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

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

def uniClick(elementToClick):
    driver.execute_script("arguments[0].click()", elementToClick)

def clickShowMore(show_more_selector, tr_selector):
    maxClicks = 10  # Safety limit to prevent infinite loop
    localWait = WebDriverWait(driver, 3)
    for _ in range(maxClicks):
        try:

            showMoreButton = localWait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, show_more_selector))
            )

            if showMoreButton.value_of_css_property("display") == 'none':
                print("Button is present but hidden by CSS, assuming all data loaded.")
                break

            initialRowCount = len(driver.find_elements(By.CSS_SELECTOR, tr_selector))

            uniClick(showMoreButton)

            wait.until(
                lambda driver: len(
                    driver.find_elements(By.CSS_SELECTOR, tr_selector)) > initialRowCount
            )

        except TimeoutException:
            print("No more 'Show More' button found or data loaded.")
            break
        except StaleElementReferenceException:
            continue
        except Exception as e:
            print(f"Error during 'Show More' click: {e}")
            break

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
    actionSelectorsList = bankDictionary["selectors"]["actions"]
    showMoreSelector = bankDictionary["selectors"]["showMore"]
    trSelector = bankDictionary["selectors"]["tr"]

    for selector in actionSelectorsList:
        uniClick(locatedElement(selector))

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
