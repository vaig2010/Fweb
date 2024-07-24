from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
from sqlalchemy import create_engine, text
from csv_to_sql import get_links
from sqlalchemy.orm import sessionmaker


def get_exercises(driver, m1: str, m2: str):
    driver.find_elements(by='xpath', value=r'//*[@id="tab_m_3"]')[0].click()
    driver.implicitly_wait(0.5)
    gr_mishc = driver.find_elements(by='xpath', value=r'//*[@id="gr_mishc"]')[0]
    gr_mishc.click()
    driver.implicitly_wait(0.5)
    test = driver.find_elements(by='xpath', value=r'//*[@id="gr_mishc_g"]')[0]
    for d in test.find_elements(By.TAG_NAME, 'div'):
        class_name = d.get_attribute('class')
        if class_name is not None and class_name in ('menmen1', 'menmen2', 'menmen3', 'menmen4', 'menmen5', 'menmen6'):
            d.click()
            driver.implicitly_wait(0.5)
            
    menmen1 = test.find_elements(By.CLASS_NAME, 'menmen1')
    for m in menmen1:
        print(m.get_attribute('id'))
            
         
    return
    driver.find_elements(by='xpath', value=fr'//*[@id="{m1}"]')[0].click()
    driver.implicitly_wait(0.5)
    if m2 == '':
        return driver.find_elements(by='xpath', value=fr'//*[@id="{m1}2"]/ol/div')
    driver.find_elements(by='xpath', value=fr'//*[@id="{m2}"]')[0].click()
    driver.implicitly_wait(0.5)
    exes = driver.find_elements(by='xpath', value=fr'//*[@id="{m2}2"]/ol/div')
    return exes

def links_to_sql(csv_file_path: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    engine = create_engine('sqlite:///api_db.sqlite3')
    Session = sessionmaker(bind=engine)
    session = Session()

    links = get_links(csv_file_path)
    
    for l in links:
        driver.get(l)
        
        # Click and gather data
        try:
            bloki_ves = driver.find_elements(By.ID, 'bloki_ves')
            if bloki_ves:
                bloki_ves[0].click()
                for_beginners_elements = driver.find_elements(By.ID, 'bloki_ves3')
                for_begginers = ' '.join([i.get_attribute("innerText").replace('\n', ' ') for i in for_beginners_elements])
            else:
                for_begginers = ""
            
            bloki_opis = driver.find_elements(By.ID, 'bloki_opis')
            if bloki_opis:
                bloki_opis[0].click()
                desc_elements = driver.find_elements(By.ID, 'bloki_opis2')
                desc = ' '.join([i.get_attribute("innerText").replace('\n', ' ') for i in desc_elements])
            else:
                desc = ""
            
            bloki_ogran = driver.find_elements(By.ID, 'bloki_ogran')
            ogran_text = ""
            if bloki_ogran:
                ograns = driver.find_elements(By.ID, 'bloki_ogran2')[0].find_elements(By.TAG_NAME, 'tr')
                ogran_text = ' '.join(['. '.join([i.get_attribute("innerText").replace('\n', ' ') for i in o.find_elements(By.TAG_NAME, 'td')]) for o in ograns])
            
            query = text('UPDATE exercises SET description = :description, restriction = :restriction, for_begginers = :for_begginers WHERE link = :link')
            session.execute(query, {'description': desc, 'restriction': ogran_text, 'for_begginers': for_begginers, 'link': l})
        
        except Exception as e:
            print(f"Error processing link {l}: {e}")

    session.commit()
    driver.quit()
if __name__ == "__main__":
    links_to_sql('app/api/shoulders/zad.csv')
    # URL = 'https://tvoytrener.com/www/nast.html'
    # options = webdriver.EdgeOptions()

    # options.add_argument("--headless=new")
    # options.add_argument('--log-level=3')
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # driver = webdriver.Edge(options=options)
    # driver.get(URL)

    # exes = get_exercises(driver, 'nogi', 'golen')
    # with open('golen.csv', 'w', newline='') as csvfile:
    #     spamwriter = csv.writer(csvfile, delimiter=',')
    #     for i in exes:
    #         tag_a = i.find_elements(By.TAG_NAME, 'a')
    #         for i in tag_a:
    #             link = i.get_attribute('href')
    #             text = i.text
    #             if text != '':
    #                 spamwriter.writerow([text, link])

    #driver.quit()
    