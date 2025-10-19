from collections import defaultdict
from datetime import datetime

from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.bankSelectors import getBanksList
import utils.fileInteraction as fileIO
import utils.graphic as gr
# from utils.graphic import createGraphics

# 1. Create Options object
options = Options()

# 2. Add the headless argument
# Use '--headless=new' for modern Chrome versions (v109+)
# You might use just '--headless' for older versions, but 'new' is better.
options.add_argument("--headless=new")

# Optional: Set a window size, as some sites adapt to screen resolution
options.add_argument("--window-size=1920,1080")

# 3. Pass the options to the WebDriver
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)

def extractData():
    itemsToAdd = list()
    banks = getBanksList()
    total = len(banks)
    for i, bank in enumerate(banks,1):
        print(f"Extracting data from [{i}/{total}] source")
        itemsToAdd.extend(extractDataFromSite(bank))
        print(f"Data from [{i}/{total}] is extracted\n")
    fileIO.saveToCSV(itemsToAdd, fileIO.FILE_PATH)
    print(f"Data saved in file:{fileIO.FILE_PATH}")
    driver.close()

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
            # print("No more 'Show More' button found or data loaded.")
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

def extractDataFromSite(bankDictionary):
    driver.get(bankDictionary["link"])
    actions(bankDictionary)
    lst = extractDataFromTable(bankDictionary)
    return lst

def toActualFormats(stringsList):
    for sublist in stringsList:
        sublist[0] = datetime.strptime(sublist[0], '%d.%m.%Y')
        sublist[3] = float(sublist[3])
        sublist[4] = float(sublist[4])

def toGraphic():
    globalList = fileIO.readFromCSV(fileIO.FILE_PATH)
    toActualFormats(globalList)

    bankCurrencyDictionary = defaultdict(list)

    for record in globalList:
        bank = record[1]
        currency = record[2]
        key = (bank, currency)
        bankCurrencyDictionary[key].append(record)

    gr.createGraphics(bankCurrencyDictionary)

def changeFilePath():
    print(f"Current file path is: {fileIO.FILE_PATH}")
    newPath = input("Enter new file path:")
    fileIO.setPath(newPath)

def graphicWorkMenu():
    menu_actions = {
        '1': toGraphic,
        '2': gr.showFigure,
        '3': gr.saveFigure,
        '4': exit
    }
    while True:
        print("1.Build graphic 2.Show graphic 3.Save graphic as image 4.Previous menu")
        choice = input("Enter your choice (1-4): ").strip()

        if choice in menu_actions:
            if choice == '4':
                break
            else:
                menu_actions[choice]()  # Call the function
        else:
            # Handle invalid input
            print(f"\nInvalid option: '{choice}'. Please enter a number between 1 and 4.")


def menu():
    menu_actions = {
        '1': extractData,
        '2': graphicWorkMenu,
        '3': changeFilePath,
        '4': exit
    }
    while True:
        print("1.Get data from sites 2.Graphic 3.Change file path 4.Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice in menu_actions:
            if choice == '1':
                print("\nData extraction in progress...")
            if choice == '4':
                print("\nGoodbye")
                break
            else:
                menu_actions[choice]()  # Call the function
        else:
            # Handle invalid input
            print(f"\nInvalid option: '{choice}'. Please enter a number between 1 and 4.")

menu()