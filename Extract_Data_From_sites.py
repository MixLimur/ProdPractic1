from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from matplotlib import pyplot
from datetime import date

driver = webdriver.Chrome()
driver.implicitly_wait(5)
global_list = []

def saveToCSV(bankName, curName, curBuy, curSale):
    with open(f"./Exchanges_CSV/{bankName}_{date.today().strftime("%d_%m_%Y")}.csv", "w", encoding="UTF-8") as f:
        f.write("Name,buy,sale\n")
        for i in range(len(curName)):
            csv_format = f"{curName[i]},{curBuy[i]},{curSale[i]}\n"
            f.write(csv_format)

def saveToOneCSV():

    with open(f"./Exchanges_CSV/Exchanges.csv", "a", encoding="UTF-8") as f:
        f.write("Name,buy,sale,bank,date\n")
        for i in range(len(global_list)):
            csv_format = (f"{global_list[i][0]},{global_list[i][1]},"
                          f"{global_list[i][2]},{global_list[i][3]},{global_list[i][4]}\n")
            f.write(csv_format)

def listToStr(lst, lengthLimit = None):
     lst[:] = [item.get_attribute("innerHTML")[:lengthLimit] for item in lst];

def extractFromSite(driver, selectorsDictionary):
    currencyTable = driver.find_element(By.CSS_SELECTOR, selectorsDictionary["container"])
    currencyNames = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["names"])
    currencyBuy = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["buy"])
    currencySale = currencyTable.find_elements(By.CSS_SELECTOR, selectorsDictionary["sale"])
    return currencyNames, currencyBuy, currencySale

def extractData(bank, link, container, names, buy, sale, doBefore = None):
    driver.get(link)

    if doBefore != None:
        doBefore()

    selectorsDictionary = {"container": container, "names":names, "buy":buy, "sale":sale}
    currencyNames, currencyBuy, currencySale = extractFromSite(driver, selectorsDictionary)

    listToStr(currencyNames, 3)
    listToStr(currencyBuy)
    listToStr(currencySale)

    for name, buy, sale in zip(currencyNames, currencyBuy, currencySale):
        global_list.append([name, buy, sale, bank, date.today().strftime("%d_%m_%Y")])

    saveToCSV(bank, currencyNames, currencyBuy, currencySale)

#ПУМБ
extractData("PUMB", "https://about.pumb.ua/info/currency_converter",
          "#single-page-rate-1 tbody",
          "tr td:first-child",
          "tr td:nth-child(2)",
          "tr td:last-child"
            )
#Ощад банк
extractData("OschadBank", "https://www.oschadbank.ua/currency-rate",
          "table.heading-block-currency-rate__table tbody",
          "tr td:nth-child(2) span",
          "tr td:nth-child(4) span",
          "tr td:nth-child(5) span"
            )

extractData("PrivateBank", "https://privatbank.ua/obmin-valiut",
          "#swift-currency-block .table_block table.table_show tbody",
          ".tbody-swift .currency-swift",
          ".buy-swift",
          ".sale-swift",
            lambda : driver.find_element(By.ID, "swift-block").send_keys(Keys.RETURN)
            )