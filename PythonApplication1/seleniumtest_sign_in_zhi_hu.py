from selenium import webdriver 
import os

driver = webdriver.Firefox()  

user_name = '**'
user_password = '***'
driver.get('https://www.zhihu.com/')  
driver.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()
driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys(user_name)
driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys(user_password)
driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/form/button').click()
print(driver.title)
os.system("pause")