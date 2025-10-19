from selenium.webdriver.support import expected_conditions as EC
from selenium.common import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = int()
wait = WebDriverWait(driver, 10)

def initDriver(drv):
    global driver, wait
    driver = drv
    wait = WebDriverWait(driver, 10)


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