from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
  

element_list = []
df = pd.read_csv('input.csv')
cty = df.get("city")
cities = cty.tolist()
for page in range(1, 6, 1):
    for city in cities:
        page_url = f"https://www.swiggy.com/city/{city}?page=" + str(page)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(page_url)
        names = driver.find_elements(
            By.CLASS_NAME, 'nA6kb'
        )
        rate = driver.find_elements(
            By.XPATH, "//span[@class='icon-star _537e4']/following-sibling::span"
        )
        ftype = driver.find_elements(
           By.CLASS_NAME, "_1gURR"
        )
        price_range = driver.find_elements(
            By.CLASS_NAME, "nVWSi"
        )
        link = driver.find_elements(
            By.CLASS_NAME, "_1j_Yo"
        )
        for i in range(len(names)):
            element_list.append({
                "Name" : names[i].text, 
                "Rate" : rate[i].text, 
                "Food Type" : ftype[i].text, 
                "Price Range" :price_range[i].text,
                "City" : city,
                "URL" : link[i].get_attribute("href")
                })
df = pd.DataFrame(element_list)
df.sort_values(["City"],axis=0, ascending=True,inplace=True,na_position='first')
df.to_csv("restaurants.csv", index=False)


  
driver.close()

    