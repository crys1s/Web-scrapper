import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InsecureCertificateException

driver = webdriver.Firefox(executable_path="/home/benzi/Downloads/drivers/geckodriver")

#location of the excel file
import xlrd
loc = ("/home/benzi/Downloads/Domains.xlsx")
 
# To open Workbook
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

Title=[] #List to store rating of the product
Link=[]

conn_timeout = 15
read_timeout = 30
timeouts = (conn_timeout, read_timeout)

for i in range(2000,2180):
    url=("http://"+ sheet.cell_value(i, 0))
    
    try:

        response = requests.get(url, verify = False,timeout=timeouts)
        print(url)
        print(i)
    #The timeout constraint
    #driver.set_page_load_timeout(90)

        try:
            driver.get(url)
            content = driver.page_source
            soup = BeautifulSoup(content)
            for title in soup.find_all('title'): 
                name=title.get_text()
        except WebDriverException:
            name="error"
            Title.append(name)
            Link.append(url)    
            continue    
        except InsecureCertificateException:
            name="error"
            Title.append(name)
            Link.append(url)    
            continue
    except requests.exceptions.Timeout:
        name="Timeout"
        Title.append(name)
        Link.append(url)    
        continue   
    except requests.ConnectionError as exception:
        name="Bad URL"
        Title.append(name)
        Link.append(url)    
        continue
    except requests.exceptions.TooManyRedirects:
        name="TooManyRedirects"
        Title.append(name)
        Link.append(url)
        continue
    except requests.exceptions.InvalidURL:
        name="Bad URL"
        Title.append(name)
        Link.append(url)    
        continue
    except requests.exceptions.ContentDecodingError:
        name="ContentDecodingError"
        Title.append(name)
        Link.append(url)    
        continue
    Title.append(name)
    Link.append(url)    
df = pd.DataFrame({'Website':Link,'Title':Title}) 
df.to_csv('Names-2180.csv', index=False, encoding='utf-8')