from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get('https://www.attop.com/')
driver.find_element_by_link_text("登录").click()
time.sleep(3)
driver.switch_to_frame('pageiframe')
time.sleep(3)
driver.find_element_by_id('username').send_keys('365057')
driver.find_element_by_id('password').send_keys('3557589')
time.sleep(3)

driver.find_element_by_link_text("个人中心").click()
driver.find_element_by_xpath('//*[@id="user_main"]/div[1]/div[2]/div[2]/div[1]/ul/li/a').click()
study_url = driver.find_element_by_xpath('//*[@id="showajaxinfo"]/div/table/tbody/tr[2]/td[5]/a').get_attribute('href')
driver.get(study_url)
driver.find_element_by_link_text("课程学习").click()
driver.find_elements_by_name('zj').click()
id_number = 795
id_str = 'j_'
for id_number in range(795,825):
    id = id_str+str(id_number)
    driver.find_element_by_id(id).click()
    time.sleep(3)