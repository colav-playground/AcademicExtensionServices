import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions

import pandas as pd 

#options = FirefoxOptions()
#options.add_argument("--headless")
driver =  webdriver.Firefox()#options=options)

_range = range(1,31)

basic_url = 'https://asone.udea.edu.co/portafolio/#/catalog?events=true&lines=7,9&filters=activities,ages,modalities,sectionals&dependencies=%s'

data = []

for i in _range:
    # wait
    # get catalog
    driver.get(basic_url % i)
    driver.implicitly_wait(8)
    #if i>1:
    #wait = WebDriverWait(driver, 15)
    #wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='ng-star-inserted']/button")))
    
    driver.execute_script("window.scrollTo(0,2000);")
    #driver.implicitly_wait(3)
    # wait = WebDriverWait(driver, 15)
    # wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='ng-star-inserted']/button/span[@class='mat-button-wrapper']")))
    
    # validate
    try:
        try:
            validate = driver.find_element(By.XPATH,"//div//p").text
        except selenium.common.exceptions.StaleElementReferenceException:
            validate = "No hay ofertas que mostrar"
        
        if validate == "No hay ofertas que mostrar":
                continue
    except selenium.common.exceptions.NoSuchElementException:
        pass

    # iterate 
    urls = driver.find_elements(By.XPATH,"//mat-grid-tile//button")
    length = len(urls)
    print(length)
    c=0
    for e in range(length):
        driver.implicitly_wait(5)
        try:
            ee = driver.find_elements(By.XPATH,"//mat-grid-tile//button")[c]
        except IndexError:
            break
        driver.execute_script("arguments[0].click();", ee)
        # wait = WebDriverWait(driver, 10)
        # wait.until(EC.element_to_be_clickable((By.XPATH,"//mat-grid-tile//button")))
        # ee.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='rightSection']//button")))
        # routes for dependencies
        # $x("//div[@class="srongGreen"]/text()")
        entidad = driver.find_element(By.XPATH, "//div[@class='grid-item strongGreen']").text
        print(entidad)
        # routes for title services
        # $x("//div/h2/text()")
        linea = driver.find_element(By.XPATH,"//div/h2").text
        print(linea)
        # route for def service
        # $x("//div/span/text()")
        descripcion_servicio = driver.find_element(By.XPATH,"//div/span").text
        print(descripcion_servicio)
        # route for content services
        servicios=driver.find_element(By.XPATH, "//div[@class='parent-container']").get_attribute('outerText')
        print(servicios)
        #route for regiones and contact
        #$x("//mat-list")[0]
        r_c = driver.find_elements(By.XPATH,"//mat-list")

        regiones = r_c[0].get_attribute('outerText')
        print(regiones.replace('done',''))
        regiones = regiones.replace('done','')
        contacto = r_c[1].get_attribute('outerText')
        print(contacto.replace('done',''))
        contacto = contacto.replace('done', '')
        driver.implicitly_wait(5)
        driver.back()
        if c == length:
            break
        print("ITEM:",c)
        c+=1
        time.sleep(3)
        print("\n")
    # close collect'''
        with open('report_services.txt','a') as file_handler:
            file_handler.write('\n'+'########'+'\n'+entidad+'\n'+linea+'\n'+descripcion_servicio+'\n'+servicios+'\n'+regiones+'\n'+contacto)

        data.append({'entidad':entidad,'linea':linea,'descripcion:servicio':descripcion_servicio,'servicios':servicios,'regiones':regiones,'contacto':contacto })

    print("RANGE:", i)
print('end of collect')
df = pd.DataFrame(data)
print(df.shape)
df.to_excel('report_services_udea.xlsx')
###
'''driver.get('https://asone.udea.edu.co/portafolio/#/catalog?events=true&lines=7,9&filters=activities,ages,modalities,sectionals&dependencies=8')

# wait until load
driver.implicitly_wait(3)

#collect
#tits = driver.find_elements(By.XPATH,"//mat-grid-tile//div[@class='title']")

#print("current_url:",driver.current_url)

# driver.current_url

#print('titles')
#for e in tits:
#    print(e.text)

#print('buttons')
urls = driver.find_elements(By.XPATH,"//mat-grid-tile//button")
length = len(urls)
print(length)
c=0
for e in range(length):
    driver.implicitly_wait(5)
    ee = driver.find_elements(By.XPATH,"//mat-grid-tile//button")[c]
    driver.execute_script("arguments[0].click();", ee)
    # wait = WebDriverWait(driver, 10)
    # wait.until(EC.element_to_be_clickable((By.XPATH,"//mat-grid-tile//button")))
    # ee.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//div[@class='rightSection']//button")))
    # routes for dependencies
    # $x("//div[@class="srongGreen"]/text()")
    entidad = driver.find_element(By.XPATH, "//div[@class='grid-item strongGreen']").text
    print(entidad)
    # routes for title services
    # $x("//div/h2/text()")
    linea = driver.find_element(By.XPATH,"//div/h2").text
    print(linea)
    # route for def service
    # $x("//div/span/text()")
    descripcion_servicio = driver.find_element(By.XPATH,"//div/span").text
    print(descripcion_servicio)
    # route for content services
    servicios=driver.find_element(By.XPATH, "//div[@class='parent-container']").get_attribute('outerText')
    print(servicios)
    #route for regiones and contact
    #$x("//mat-list")[0]
    r_c = driver.find_elements(By.XPATH,"//mat-list")

    regiones = r_c[0].get_attribute('outerText')
    print(regiones.replace('done',''))
    contacto = r_c[1].get_attribute('outerText')
    print(contacto.replace('done',''))
    driver.implicitly_wait(5)
    driver.back()
    if c == length:
        break
    print(c)
    c+=1
    time.sleep(3)
    print("\n")'''
driver.close()