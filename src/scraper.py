from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from car_classes import CarList, Car

PATH = "/sbin/geckodriver"
TIMEOUT = 10

def scrape(brand, model, headless, pages):
    options = Options()

    if headless:
        options.add_argument('-headless')

    browser = webdriver.Firefox(service=Service(PATH),options=options)

    mileages = []
    years = []
    prices = []
    names = []
    fuels = []

    link = "https://www.standvirtual.com/carros/"+brand.lower()+"/" + model.lower() + "/?search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=&page="

    for page in range(1,pages+1):
        browser.get(link+str(page))

        # Wait for the page to load
        try:
            WebDriverWait(browser, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '[data-parameter=\'mileage\']'))
            )
        except:
            print(f"Timeout exceeded after {TIMEOUT} seconds. Exiting...")
            browser.quit()
            return

        mileages.extend([ int(e.text[:-3].replace(' ','')) for e in\
                browser.find_elements(By.CSS_SELECTOR,'[data-parameter=\'mileage\']')])
        years.extend( [ int(e.text) for e in\
                browser.find_elements(By.CSS_SELECTOR,'[data-parameter=\'first_registration_year\']')])
        prices.extend( [ int(element.get_attribute('data-price')) for element \
                in browser.find_elements(By.CSS_SELECTOR,'[data-price]') ])
        names.extend( [ element.get_attribute('data-title') for element \
                in browser.find_elements(By.CSS_SELECTOR,'[data-title]') ])
        fuels.extend([ e.text for e in\
                browser.find_elements(By.CSS_SELECTOR,'[data-parameter=\'fuel_type\']')])
        # Log the page number out of pages
        print(f"Page {page} out of {pages} scraped")

    browser.quit()

    return (mileages, years, prices, names, fuels)

def serialize_scrape(brand,model, mileages, years, prices, names, fuels):
    carlist = CarList(brand+"-"+model)
    for i in range(len(mileages)):
        car = Car(mileages[i], years[i], prices[i], names[i], fuels[i])
        print("Saved: " + str(car))
        carlist.append(car)
    carlist.save()

def scrape_and_serialize(brand, model, headless, pages):
    mileages, years, prices, names, fuels = scrape(brand, model, headless, pages)
    serialize_scrape(brand,model,mileages, years, prices, names, fuels)
