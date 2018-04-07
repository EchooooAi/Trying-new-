import time
from selenium import webdriver
from lxml import etree

friend_Q = '***'
user = '***'
pw = '**'

# use under code to login in QQ 

driver = webdriver.Chrome()
driver.get('https://i.qq.com')
# 选中 登陆的 frame 否则找不到下面所需要的元素
#driver.switch_to.frame("login_frame")
#driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
#driver.find_element_by_xpath('//*[@id="u"]').send_keys(user)
#driver.find_element_by_xpath('//*[@id="p"]').send_keys(pw)
#driver.find_element_by_xpath('//*[@id="login_button"]').click()

##################################
###已经存有cookies#####
#driver.get('https://user.qzone.qq.com/645187984')

#让webdriver操控当前页面
driver.switch_to.default_content()

#跳转道说说的url
driver.get('http://user.qzone.qq.com/'+ friend_Q +'/311')
#driver.switch_to.frame("login_frame")
#driver.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
#driver.find_element_by_xpath('//*[@id="p"]').send_keys(pw)
#driver.find_element_by_xpath('//*[@id="login_button"]').click()
#driver.switch_to.default_content()

next_num = 0 #初始“下一页”的id
while True:

    #下拉滚动条，使浏览器加载出 动态加载 的内容，
    #这里 从 1  开始到 6 结束， 分5次加载完每页的数据
    for i in range(1,6):
        height = 20000*i #每次滚动20000像素
        strWord = 'window.scrollBy(0,"+str(height)+")'
        driver.execute_script(strWord)
        time.sleep(15)

        # 很多网页有多个 <frame>或者<iframe>组成，webdriver 默认定位的是最外层的 frame,
        # 这里 选中 说说 所在的frame ，否则找不下面所需要的网页元素 
        driver.switch_to.frame("app_canvas_frame")
        # get源代码
        selector = etree.HTML(driver.page_source)
        divs = selector.xpath('//*[@id="msgList"]/li/div[3]')

        # 使用a表示内容可以连续不清空写入
        with open('qq_word.txt','a',encoding='utf-8') as f:
            for div in divs:
                qq_name = div.xpath('./div[2]/a/text()')
                qq_content = div.xpath('./div[2]/pre/text()')
                qq_time = div.xpath('./div[4]/div[1]/span/a/text()')
                qq_name = qq_name[0] if len(qq_name)>0 else ''
                qq_content = qq_content[0] if len(qq_content)>0 else ''
                qq_time = qq_time[0] if len(qq_content)>0 else ''
                print(qq_name,qq_time,qq_content)
                f.write(qq_content+'\n')

        # 已经找到了尾页，“下一页”按钮没有id 结束
        if driver.page_source.find('pager_next_' +str(next_num)) == -1: break

        # 找到“下一页”按钮。因为按钮是动态变化的，所以这里需要记录一下
        driver.find_element_by_id('pager_next_' + str(next_num) ).click()

        #“下一页”的id
        next_num += 1

        #因为下一个循环还要把页面下来，所以要跳到 外层frame 上
        driver.switch_to.parent_frame()

      #---------------------------------------------------------------------------------#
        # 1.滚动条控制
          #目的：通过 selenium 控制浏览器滚动条
          #原理：通过 driver.execute_script（）执行 js 代码，达到目的
          #a--->  driver.execute_script（"window.scrollBy(0,1000)"）
          #                             分别：向右，向下
          #b--->  driver.execute_script（"window.scrollTo(0,1000)"）
          #   在文档显示区左上角 显示的 x y坐标
        # 2. frame 切换
          #http://blog.csdn.net/huilan_same/article/details/52200586   

     #----------------------------------------------------------------------------------#
