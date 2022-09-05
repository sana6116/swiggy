import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

df = pd.read_csv('input.csv')
cty = df.get("city")
cities = cty.tolist()

def detail(driver,city):
    names = driver.find_elements(
        By.CLASS_NAME, 'nA6kb'
    )

    restaurants = [
        rest.find_element(
        By.XPATH, './../..'
    )for rest in names
    ]
        
    data = []

    for restaurant in restaurants:
        try:
            name = restaurant.find_element(
                By.XPATH, './div[2]/div[1]'
            )
            rate = restaurant.find_element(
                By.XPATH, './div[3]/div[1]'
            )
            ftype = restaurant.find_element(
                By.XPATH, './div/div[2]'
            )
            price_range =restaurant.find_element(
                By.XPATH,'./div[3]/div[5]'
            )
        except:
            continue

        data.append({
            "Name" : name.text,
            "Rating" : rate.text,
            "Food Type": ftype.text,
            "Price_range" : price_range.text, 
            "area" : city
            })
    return data


def product_page_1(driver,city):
        
    driver.get(f"https://www.swiggy.com/city/{city}?page=1")
     
    return detail(driver,city)

def product_page_2(driver,city):
        
    driver.get(f"https://www.swiggy.com/city/{city}?page=2")
     
    return detail(driver,city)

def product_page_3(driver,city):
        
    driver.get(f"https://www.swiggy.com/city/{city}?page=3")
     
    return detail(driver,city)

def product_page_4(driver,city):
        
    driver.get(f"https://www.swiggy.com/city/{city}?page=4")
    
    return detail(driver,city)

def product_page_5(driver,city):
        
    driver.get(f"https://www.swiggy.com/city/{city}?page=5")
    
    return detail(driver,city)


webdriver = webdriver.Chrome(ChromeDriverManager().install())
df1 = pd.DataFrame(
    list(itertools.chain(*[product_page_1(webdriver,city)for city in cities]))
)
df2 = pd.DataFrame(
    list(itertools.chain(*[product_page_2(webdriver,city)for city in cities]))
)
df3 = pd.DataFrame(
    list(itertools.chain(*[product_page_3(webdriver,city)for city in cities]))
)
df4 = pd.DataFrame(
    list(itertools.chain(*[product_page_4(webdriver,city)for city in cities]))
)
df5 = pd.DataFrame(
    list(itertools.chain(*[product_page_5(webdriver,city)for city in cities]))
)

final_df = [df1,df2,df3,df4,df5]
#print(final_df)
df = pd.concat(final_df, ignore_index=True)
df.sort_values(["area"],axis=0, ascending=True,inplace=True,na_position='first')
df.to_csv("restaurants.csv", index=False)
webdriver.quit()  

 