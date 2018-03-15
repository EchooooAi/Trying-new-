import requests
from requests.exceptions import RequestException
from lxml import etree
import re 
from bs4 import BeautifulSoup
from openpyxl import Workbook

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',}

def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        return response
    except RequestException:
        return None

def parse_the_page(html):
    soup = BeautifulSoup(html,'lxml')

    # get everyone book's info
    #get_info = soup.find_all(name='dd')

    # get book's name and add to the list
    get_names = []
    for dd in soup.find_all(name='dd'):
        get_name = dd.find_all(name = 'a')
        for name in get_name:
             get_names.append(name.string)

    # get book's describe
    get_describes =[]
    for dd in soup.find_all(name = 'dd'):
        get_describes.append(dd.find_all(attrs = {'class':'desc'}))
    #正则 信息详细归类 暂时失败
    str_desc =''
    for describes in get_describes:
        for list_desc in describes:
            str_desc += list_desc.string
    #print(str_desc)
    # add the describe in list in order
    get_desc_list = (re.findall('\n.{8}(.*?)\n',str_desc,re.S))

    # using xpath to get the score
    #此处 最开始写成了 etree.parse(html,etree.HTMLParser()) 不正确 第一个形参应该传入的是一个本地html文件地址路径
    Xpath_html = etree.HTML(html)
    get_score = Xpath_html.xpath('//div[@class="rating"]//span[@class="rating_nums"]/text()')
    for i in range(10):
        yield {
            'name' : get_names[i] ,
            'describe' : get_desc_list[i] ,
            'score' : get_score[i],
            }

def write_to_xlsx:
    wb = Workbook()
    ws = wb.active
    return 1

def main():
    url = 'https://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book?start=0'
    html = get_one_page(url).text
    results = parse_the_page(html)
    for i in results:
        print(i)

main()