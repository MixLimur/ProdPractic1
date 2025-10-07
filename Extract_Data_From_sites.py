from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from matplotlib import pyplot
from datetime import date

driver = webdriver.Chrome()
driver.implicitly_wait(5)

def saveToCSV(bankName, curName, curBuy, curSale):
    with open(f"./Exchanges_CSV/{bankName}_{date.today().strftime("%d_%m_%Y")}.csv", "w", encoding="UTF-8") as f:
        f.write("Name,buy,sale\n")
        for i in range(len(curName)):
            csv_format = f"{curName[i]},{curBuy[i]},{curSale[i]}\n"
            f.write(csv_format)


def extractor(bank, link, container, names, buy, sale, doBefore = None):
    driver.get(link)

    if doBefore != None:
        doBefore()

    currencyTable_d = driver.find_element(By.CSS_SELECTOR, container)
    currencyNames_d = currencyTable_d.find_elements(By.CSS_SELECTOR, names)
    currencyBuy_d = currencyTable_d.find_elements(By.CSS_SELECTOR, buy)
    currencySale_d = currencyTable_d.find_elements(By.CSS_SELECTOR, sale)

    currencyNames = [name.get_attribute("innerHTML")[0:3] for name in currencyNames_d];
    currencyBuy = [price.get_attribute("innerHTML") for price in currencyBuy_d];
    currencySale = [price.get_attribute("innerHTML") for price in currencySale_d];

    saveToCSV(bank, currencyNames, currencyBuy, currencySale)

#ПУМБ
extractor("Pumba", "https://about.pumb.ua/info/currency_converter",
          "#single-page-rate-1 tbody",
          "tr td:first-child",
          "tr td:nth-child(2)",
          "tr td:last-child"
          )
#Ощад банк
extractor("Zaochadluvui", "https://www.oschadbank.ua/currency-rate",
          "table.heading-block-currency-rate__table tbody",
          "tr td:nth-child(2) span",
          "tr td:nth-child(4) span",
          "tr td:nth-child(5) span"
          )

extractor("Priv", "https://privatbank.ua/obmin-valiut",
          "#swift-currency-block .table_block table.table_show tbody",
          ".tbody-swift .currency-swift",
          ".buy-swift",
          ".sale-swift",
          lambda : driver.find_element(By.ID, "swift-block").send_keys(Keys.RETURN)
          )


# driver.get("https://privatbank.ua/obmin-valiut")
#
# # click SWIFT
# driver.find_element(By.ID, "swift-block").send_keys(Keys.RETURN)
#
# # get table
# currencyTable_d = driver.find_element(By.CSS_SELECTOR, "#swift-currency-block .table_block table.table_show tbody")
#
# currencyNames_d = currencyTable_d.find_elements(By.CSS_SELECTOR, ".tbody-swift .currency-swift")
# currencyBuy_d = currencyTable_d.find_elements(By.CSS_SELECTOR, ".buy-swift")
# currencySale_d = currencyTable_d.find_elements(By.CSS_SELECTOR, ".sale-swift")
#
# currencyNames = [name.get_attribute("innerHTML")[0:3] for name in currencyNames_d];
# currencyBuy = [price.get_attribute("innerHTML") for price in currencyBuy_d];
# currencySale = [price.get_attribute("innerHTML") for price in currencySale_d];
#
# saveToCSV("Privatik", currencyNames, currencyBuy, currencySale)
#
#
# # pyplot.plot(currencyBuy)
# # pyplot.plot(currencySale)
# # pyplot.grid()
# #
# # pyplot.show()
#
# #driver.close()
#
#
# #ПУМБ
#
# # driver.get("https://about.pumb.ua/info/currency_converter")
# #
# # currencyTable_d = driver.find_element(By.CSS_SELECTOR, "#single-page-rate-1 tbody")
# #
# # currencyNames_d = currencyTable_d.find_elements(By.CSS_SELECTOR, "tr td:first-child")
# # currencyBuy_d = currencyTable_d.find_elements(By.CSS_SELECTOR, "tr td:nth-child(2)")
# # currencySale_d = currencyTable_d.find_elements(By.CSS_SELECTOR, "tr td:last-child")
# #
# # for i in currencySale_d:
# #     print(i.get_attribute("innerHTML"))
# #
# # currencyNames = [name.get_attribute("innerHTML")[0:3] for name in currencyNames_d];
# # currencyBuy = [price.get_attribute("innerHTML") for price in currencyBuy_d];
# # currencySale = [price.get_attribute("innerHTML") for price in currencySale_d];
#
#
# # saveToCSV("PUMB", currencyNames, currencyBuy, currencySale)
#
# # driver.get("https://www.oschadbank.ua/currency-rate")
# #
# # currencyTable_d = driver.find_element(By.CSS_SELECTOR, "table.heading-block-currency-rate__table tbody")
# # currencyNames_d = currencyTable_d.find_elements(By.CSS_SELECTOR, "tr td:nth-child(2) span")
# # currencyBuy_d = currencyTable_d.find_elements(By.CSS_SELECTOR, "tr td:nth-child(4) span")
# # currencySale_d = currencyTable_d.find_elements(By.CSS_SELECTOR, "tr td:nth-child(5) span")
# #
# # currencyNames = [name.get_attribute("innerHTML")[0:3] for name in currencyNames_d];
# # currencyBuy = [price.get_attribute("innerHTML") for price in currencyBuy_d];
# # currencySale = [price.get_attribute("innerHTML") for price in currencySale_d];
# #
# # saveToCSV("Oschad", currencyNames, currencyBuy, currencySale)
