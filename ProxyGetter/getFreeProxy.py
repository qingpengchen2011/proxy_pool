# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     GetFreeProxy.py
   Description :  抓取免费代理
   Author :       JHao
   date：          2016/11/25
-------------------------------------------------
   Change Activity:
                   2016/11/25:
-------------------------------------------------
"""
import re
import requests

try:
    from importlib import reload  # py3 实际不会实用，只是为了不显示语法错误
except:
    import sys  # py2

    reload(sys)
    sys.setdefaultencoding('utf-8')

from Util.utilFunction import robustCrawl, getHtmlTree
from Util.WebRequest import WebRequest
from Util.LogHandler import LogHandler

# for debug to disable insecureWarning
requests.packages.urllib3.disable_warnings()


class GetFreeProxy(object):
    """
    proxy getter
    """
    log = LogHandler('proxy_manager')

    def __init__(self):
        pass

    @staticmethod
    def compose(ip, port, anony, protocol):
        return {
            'ip': ip,
            'port': port,
            'anony': anony,
            'protocol': protocol
        }

    @staticmethod
    def freeProxyFirst(page=10):
        """
        抓取无忧代理 http://www.data5u.com/
        :param page: 页数
        :return:
        """
        url_list = ['http://www.data5u.com/',
                    'http://www.data5u.com/free/gngn/index.shtml',
                    'http://www.data5u.com/free/gnpt/index.shtml']
        for url in url_list:
            html = getHtmlTree(url)
            for item in html.xpath('//ul[@class="l2"]'):
                try:
                    yield GetFreeProxy.compose(
                        item.xpath('(.//li)[1]/text()')[0],
                        item.xpath('(.//li)[2]/text()')[0],
                        item.xpath('(.//li)[3]/a/text()')[0],
                        item.xpath('(.//li)[4]/a/text()')[0]
                    )
                except Exception as e:
                    self.log.warning("fetch proxy failed: " + str(e))

    @staticmethod
    def freeProxySecond(proxy_number=100):
        """
        抓取代理66 http://www.66ip.cn/
        :param proxy_number: 代理数量
        :return:
        """
        url = "http://www.66ip.cn/mo.php?sxb=&tqsl={}&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea=".format(
            proxy_number)
        request = WebRequest()
        # html = request.get(url).content
        # content为未解码，text为解码后的字符串
        html = request.get(url).text
        for proxy in re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}', html):
            yield proxy

    @staticmethod
    def freeProxyThird(days=1):
        """
        抓取ip181 http://www.ip181.com/
        :param days:
        :return:
        """
        url = 'http://www.ip181.com/'
        html = getHtmlTree(url)
        for item in html.xpath('//tr[position()>1]'):
            try:
                yield GetFreeProxy.compose(
                    item.xpath('./td[1]/text()')[0],
                    item.xpath('./td[2]/text()')[0],
                    item.xpath('./td[3]/text()')[0],
                    item.xpath('./td[4]/text()')[0]
                )
            except Exception as e:
                self.log.warning("fetch proxy failed: " + str(e))

    @staticmethod
    def freeProxyFourth():
        """
        抓取西刺代理 http://api.xicidaili.com/free2016.txt
        :return:
        """
        url_list = [
            'http://www.xicidaili.com/nn',  # 高匿
            'http://www.xicidaili.com/nt',  # 透明
        ]
        for url in url_list:
            html = getHtmlTree(url)
            for item in html.xpath('//table[@id="ip_list"]//tr')[1:]:
                try:
                    yield GetFreeProxy.compose(
                        item.xpath('./td[2]/text()')[0],
                        item.xpath('./td[3]/text()')[0],
                        item.xpath('./td[5]/text()')[0],
                        item.xpath('./td[6]/text()')[0]
                    )
                except Exception as e:
                    self.log.warning("fetch proxy failed: " + str(e))

    @staticmethod
    def freeProxyFifth():
        """
        抓取guobanjia http://www.goubanjia.com/free/gngn/index.shtml
        :return:
        """
        url = "http://www.goubanjia.com/free/gngn/index{page}.shtml"
        for page in range(1, 10):
            page_url = url.format(page=page)
            tree = getHtmlTree(page_url)
            proxy_list = tree.xpath('//td[@class="ip"]')
            # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
            # 需要过滤掉<p style="display:none;">的内容
            xpath_str = """.//*[not(contains(@style, 'display: none'))
                                and not(contains(@style, 'display:none'))
                                and not(contains(@class, 'port'))
                                ]/text()
                        """
            for each_proxy in proxy_list:
                try:
                    # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                    ip_addr = ''.join(each_proxy.xpath(xpath_str))
                    port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                    yield '{}:{}'.format(ip_addr, port)
                except Exception as e:
                    self.log.warning("fetch proxy failed: " + str(e))

    @staticmethod
    def freeProxySixth():
        """
        抓取讯代理免费proxy http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=10
        :return:
        """
        url = 'http://www.xdaili.cn/ipagent/freeip/getFreeIps?page=1&rows=100'
        request = WebRequest()
        try:
            res = request.get(url).json()
            for row in res['RESULT']['rows']:
                yield GetFreeProxy.compose(row['ip'], row['port'], row['anony'], row['type'])
        except Exception as e:
            self.log.warning("fetch proxy failed: " + str(e))

    @staticmethod
    def freeProxySeventh():
        """
        快代理免费https://www.kuaidaili.com/free/inha/1/
        """
        url = 'https://www.kuaidaili.com/free/inha/'
        html = getHtmlTree(url)
        for item in html.xpath('//table//tr')[1:]:
            try:
                yield GetFreeProxy.compose(
                    item.xpath('./td[1]/text()')[0],
                    item.xpath('./td[2]/text()')[0],
                    item.xpath('./td[3]/text()')[0],
                    item.xpath('./td[4]/text()')[0]
                )
            except Exception as e:
                self.log.warning("fetch proxy failed: " + str(e))

if __name__ == '__main__':
    gg = GetFreeProxy()
    # for e in gg.freeProxyFirst():
    #     print(e)
    #
    # for e in gg.freeProxySecond():
    #     print(e)
    #
    # for e in gg.freeProxyThird():
    # print(e)

    # for e in gg.freeProxyFourth():
    #     print(e)

    # for e in gg.freeProxyFifth():
    #    print(e)

    # for e in gg.freeProxySixth():
    #     print(e)
    for e in gg.freeProxySeventh():
        print(e)
