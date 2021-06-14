import re
from PIL.ImageFilter import DETAIL, RankFilter
from lxml import etree
import json
from Function.getHtml import get_html

# https://fc2hub.com/search?kw=1760182

def getTitle(html):  # 获取标题
    result = html.xpath('//h1/text()')
    if result:
        result = result[1]
    else:
        result = ''
    return result


def getNum(html):  # 获取番号
    result = html.xpath('//h1/text()')
    if result:
        result = result[0]
    else:
        result = ''
    return result


def getCover(html):  # 获取封面
    result = html.xpath('//a[@data-fancybox="gallery"]/@href')
    if result:
        result = result[0]
    else:
        result = ''
    return result


def getExtraFanart(html):  # 获取剧照
    result = html.xpath('//div[@style="padding: 0"]/a/@href')
    return result


def getTag(html):  # 获取标签
    result = html.xpath('//p[contains(text(), "タグ :")]/a/text()')
    return result

def getOutline(html):  # 获取简介
    result = str(html.xpath('//div[@class="col des"]/text()')).strip('['']').replace("',", '').replace('\\n', '').replace("'", '').replace('・', '')
    return result

def main(number, appoint_url='', log_info=''):
    log_info += '   >>> FC2HUB-开始使用 fc2hub 进行刮削\n'
    real_url = appoint_url
    title = ''
    cover_url = ''
    cover_small = ''
    error_type = ''
    error_info = ''
    number = number.upper().replace('FC', '').replace('PPV', '').replace('FC2PPV', '').replace('-', '')
    dic = {}
    try: # 捕获主动抛出的异常
        if not real_url:
            # 通过搜索获取real_url
            url_search = 'https://fc2hub.com/search?kw=' + number
            log_info += '   >>> FC2HUB-生成搜索页地址: %s \n' % url_search
            # ========================================================================搜索番号
            result, html_search = get_html(url_search)
            if result == 'error':
                log_info += '   >>> FC2HUB-请求搜索页：错误！信息：' + html_search
                error_type = 'timeout'
                raise Exception('>>> FC2HUB-请求搜索页：错误！信息：' + html_search)
            html = etree.fromstring(html_search, etree.HTMLParser())
            # web_cache_url = etree.tostring(html,encoding="utf-8").decode() # 将element对象转化为字符串
            # print(web_cache_url)
            # with open('11.txt', 'wt') as f:
            #     f.write(web_cache_url)
            real_url = html.xpath("//link[contains(@href, $number)]/@href", number='id' + number)

            if not real_url:
                log_info += '   >>> FC2HUB-搜索结果页匹配番号：未匹配到番号！ \n'
                error_type = 'Movie not found'
                raise Exception('Movie not found')
            else:
                real_url = real_url[0]
                log_info += '   >>> FC2HUB-匹配详情页地址： %s \n' % real_url
        if real_url:
            try:
                result, html_content = get_html(real_url)
            except Exception as error_info:
                log_info += '   >>> FC2HUB-请求详情页：出错！错误信息：%s \n' % error_info
                error_type = 'timeout'
                raise Exception('>>> FC2HUB-请求详情页：出错！错误信息：%s \n' % error_info)            
            html_info = etree.fromstring(html_content, etree.HTMLParser())

            title = getTitle(html_info) # 获取标题
            if not title:
                log_info += '   >>> FC2HUB- title 获取失败！ \n'
                error_type = 'need login'
                raise Exception('>>> FC2HUB- title 获取失败!')
            cover_url = getCover(html_info) # 获取cover
            if 'http' not in cover_url:
                log_info += '   >>> FC2HUB- cover url 获取失败！ \n'
                error_type = 'Cover Url is None!'
                raise Exception('>>> FC2HUB- cover url 获取失败!')
            try:
                dic = {
                    'number': 'FC2-' + str(number),
                    'title': str(title),
                    'actor': 'FC2系列',
                    'actor_photo': {},
                    'cover': str(cover_url),
                    'extrafanart': getExtraFanart(html_info),
                    'cover_small': 'https://fc2hub.com/images/luscio-quad.png',
                    'release': '',
                    'year': '',
                    'score': '',
                    'runtime': '',
                    'studio': '',
                    'tag': getTag(html_info),
                    'imagecut': 0,
                    'director': '',
                    'series': '',
                    'publisher': '',
                    'outline': getOutline(html_info),
                    'website': str(real_url).strip('[]'),
                    'source': 'fc2hub.main',
                    'log_info': str(log_info),
                    'error_type': '',
                    'error_info': str(error_info),
                }
                log_info += '   >>> FC2HUB-数据获取成功！\n'
                dic['log_info'] = log_info
            except Exception as error_info:
                log_info += '   >>> FC2HUB-生成数据字典：出错！ 错误信息：%s \n' % error_info
                error_info = error_info
                raise Exception(log_info)        
    except Exception as error_info:
        dic = {
            'title': '',
            'cover': '',
            'website': str(real_url).strip('[]'),
            'log_info': str(log_info),
            'error_type': str(error_type),
            'error_info': str(error_info),
        }
    js = json.dumps(dic, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':'), )
    return js



# print(main('1860858', ''))
# print(main('1599412', ''))
# print(main('1131214', ''))
# print(main('1837553', ''))
# print(main('1613618', ''))
# print(main('1837553', ''))
# print(main('1837589', ""))
# print(main('1760182', ''))
# print(main('1251689', ''))
# print(main('674239', ""))
# print(main('674239', "))
