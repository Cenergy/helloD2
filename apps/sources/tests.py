import requests
import re
import os

def getIntPages(keyword, pages):
    params = []
    for i in range(1, 2):
        params.append({
            'tn':'resultjson_com',
            'ipn': 'rj',
            'ct':'201326592',
            'is': '',
            'fp': 'result',
            'queryWord': keyword,
            'cl': '2',
            'lm': '-1',
            'ie': 'utf-8',
            'oe': 'utf-8',
            'st': '-1',
            'ic': '0',
            'word': keyword,
            'face': '0',
            'istype': '2',
            'nc': '1',
            'pn': i,
            'rn': '30'
        })
    url = 'https://image.baidu.com/search/acjson'
    urls = []
    for i in params:
        content = requests.get(url, params=i).text
        img_urls = re.findall(r'"thumbURL":"(.*?)"', content)#正则获取方法
        # print(img_urls[0])
        urls.append(img_urls)
        #urls.append(requests.get(url,params = i).json().get('data'))开始尝试的json提取方法
        #print("%d times : " % x, img_urls)
    # return urls
    return img_urls[0]

def fetch_img(path,dataList):
    if not os.path.exists(path):
        os.mkdir(path)

    x = 0
    for list in dataList:
        for i in list:
            print("=====downloading %d/1500=====" % (x + 1))
            ir = requests.get(i)
            open(path + '%d.jpg' % x, 'wb').write(ir.content)
            x += 1



if __name__ == '__main__':
    url = 'https://image.baidu.com/search/acjson'

    dataList = getIntPages('ENVI5.2', 1)#依据蔬菜关键词获取50页的图片列表，每页30张图片
    print(dataList)
    # fetch_img("vegetable/", dataList)