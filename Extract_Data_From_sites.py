from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from matplotlib import pyplot

#open driver
driver = webdriver.Chrome()
driver.get("https://privatbank.ua/obmin-valiut")
driver.implicitly_wait(5)

# click SWIFT
elem = driver.find_element(By.ID, "swift-block")
elem.send_keys(Keys.RETURN)

# get table
currencyTable_d = driver.find_element(By.CSS_SELECTOR, "#swift-currency-block .table_block table.table_show tbody")

currencyNames_d = currencyTable_d.find_elements(By.CSS_SELECTOR, ".tbody-swift .currency-swift")
currencyBuy_d = currencyTable_d.find_elements(By.CSS_SELECTOR, ".buy-swift")
currencySale_d = currencyTable_d.find_elements(By.CSS_SELECTOR, ".sale-swift")

currencyNames = [name.text for name in currencyNames_d];
currencyBuy = [price.text for price in currencyBuy_d];
currencySale = [price.text for price in currencySale_d];

print("---------------")
for i in range(len(currencyNames_d)):
    print(currencyNames_d[i].text, " ", currencyBuy_d[i].text, " ", currencySale_d[i].text)

with open("./Exchanges_CSV/PrivateBank.csv", "w", encoding="UTF-8") as f:
    f.write("Name,buy,sale\n")
    for i in range(len(currencyNames_d)):
        csv_format = f"{currencyNames_d[i].text[0:3]},{currencyBuy_d[i].text},{currencySale_d[i].text}\n"
        f.write(csv_format)

pyplot.plot(currencyBuy)
pyplot.plot(currencySale)
pyplot.grid()

pyplot.show()

driver.close()
