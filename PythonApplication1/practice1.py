import json
import os
import requests
import re
import time
from requests.exceptions import RequestException

headers = {
    #'Connection': 'keep-alive',
    #'Pragma': 'no-cache',
    #'Cache-Control': 'no-cache',
    #'Upgrade-Insecure-Requests': '1',
    #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                  }

def get_one_page(url):
    try:
      response = requests.get(url,headers = headers)
      if response.status_code == 200:
          return response
      return None
    except RequestException:
        return None

def parse_one_page(html):
    #  含yield函数为生成器函数 (generator function)，被调用时将返回一个迭代器（iterator）
    #  每一次调用都继续（接着）上一次继续
    #  next()每一次产生一部电影
    #名次，海报，名称
    result1 = '<dd>.*?board-index.*?>(.*?)</i>.*?img data-src="(.*?)".*?data-val=".*?>(.*?)</a>'
    #主演
    #result2.1 = re.findall('.*?主演：(.*?)\s*</p>',html,re.S)
    result2 = '.*?<p class="star">\s*(.*?)\s*</p>'
    #上映时间
    result3 = '.*?releasetime">(.*?)</p>'
    #分数
    result4 = re.findall('.*?class="integer">(.*?)</i>.*?fraction">(.*?)</i>',html,re.S)
    #plus
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?img data-src="(.*?)".*?data-val=".*?>(.*?)</a>.*?<p class="star">\s*(.*?)\s*</p>.*?releasetime">(.*?)</p>.*?class="integer">(.*?)</i>.*?fraction">(.*?)</i>',re.S)
    results = re.findall(pattern,html)
    #结果每一页有十部电影，每部电影逻辑上有六个指标,但分数分为两部分所以共七个
    #一个result是一部电影
    for result in results:
        yield{
            'rank':result[0],
            'image':result[1],
            'name':result[2],
            'actor':result[3].strip()[3:] if len(result[3])> 3 else '',
            'time':result[4].strip()[5:] if len(result[4])>5 else '',
            'score':result[5].strip()+result[6].strip()
}

def write_to_json(content):
    with open('result.txt','a',encoding='utf-8') as f:
        #json 库的dumps()实现字典的序列化
        #ensure_ascii false保证中文 而不是unicode编码
        f.write(json.dumps(content,ensure_ascii=False) + '\n')

def get_the_picture(picurl,n):
    rank = n+ '.jpg'
    image = get_one_page(picurl)
    picpath = os.path.join('movie100',rank)
    with open(picpath,'wb') as b:
        print('output: ',picpath)
        b.write(image.content)

def main(url,offset):
    html = get_one_page(url)
    newhtml = html.text
    i = offset-9
    for item in parse_one_page(newhtml):
        print(item)
        write_to_json(item)
        sn = str(i)
        get_the_picture(item['image'],sn)
        i = int(i)
        i = i + 1
        

    #print(parse_one_page)
    # 结果：<generator object pars_one_page at 0x000001E6FFEC6C50>

if __name__ == '__main__':
    for i in range(10):
        offset = (i+1) * 10
        urlNumber =i *10
        urll = 'http://maoyan.com/board/4?offset=' + str(urlNumber)
        main(url = urll,offset=offset)
        time.sleep(1)
    #urll = 'http://maoyan.com/board/4'
    #main(url = urll)