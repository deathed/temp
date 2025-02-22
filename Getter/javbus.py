import re
from pyquery import PyQuery as pq
from lxml import etree
from bs4 import BeautifulSoup
import json

from pyquery.openers import url_opener
from Function.getHtml import get_html
from Function.getHtml import post_html


def getActorPhoto(htmlcode):
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'star-name'})
    d = {}
    for i in a:
        l = i.a['href']
        t = i.get_text()
        html = etree.fromstring(get_html(l)[1], etree.HTMLParser())
        p = str(html.xpath('//*[@id="waterfall"]/div[1]/div/div[1]/img/@src')).strip(" ['']")
        p = 'https://www.javbus.com' + p
        p2 = {t: p}
        d.update(p2)
    return d


def getTitle(htmlcode):  # 获取标题
    doc = pq(htmlcode)
    title = doc('div.container h3').text()
    try:
        title2 = re.sub('n\d+-', '', title) # 无码 n1111111-
        return title2
    except:
        return title


def getStudio(htmlcode):  # 获取厂商
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//span[contains(text(),"製作商")]/following-sibling::a/text()')).strip(" ['']")
    return result


def getPublisher(htmlcode):  # 获取发行商
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//span[contains(text(),"發行商")]/following-sibling::a/text()')).strip(" ['']")
    return result


def getYear(getRelease):  # 获取年份
    try:
        result = str(re.search('\d{4}', getRelease).group())
        return result
    except:
        return getRelease


def getCover(htmlcode):  # 获取封面链接
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    url = html.xpath('//a[@class="bigImage"]/@href')
    if url:
        cover_url = 'https://javbus.com' + str(url[0])
    else:
        cover_url = ''
    return cover_url


def getExtraFanart(htmlcode):  # 获取封面链接
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    extrafanart_list = html.xpath("//div[@id='sample-waterfall']/a/@href")
    return extrafanart_list


def getRelease(htmlcode):  # 获取出版日期
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//span[contains(text(),"發行日期")]/../text()')).strip(" ['']")
    return result


def getRuntime(htmlcode):  # 获取分钟
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//span[contains(text(),"長度")]/../text()')).strip(" ['']")
    return result


def getActor(htmlcode):  # 获取女优
    b = []
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'star-name'})
    for i in a:
        b.append(i.get_text())
    return str(b)


def getNum(htmlcode):  # 获取番号
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//span[contains(text(),"識別碼")]/following-sibling::span/text()')).strip(" ['']")
    return result


def getDirector(htmlcode):  # 获取导演
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//span[contains(text(),"導演")]/following-sibling::a/text()')).strip(" ['']")
    return result


def getOutlineScore(number):  # 获取简介
    outline = ''
    score = ''
    try:
        result, response = post_html("https://www.jav321.com/search", query={"sn": number})
        detail_page = etree.fromstring(response, etree.HTMLParser())
        outline = str(detail_page.xpath('/html/body/div[2]/div[1]/div[1]/div[2]/div[3]/div/text()')).strip(" ['']")
        if re.search(r'<b>评分</b>: <img data-original="/img/(\d+).gif" />', response):
            score = re.findall(r'<b>评分</b>: <img data-original="/img/(\d+).gif" />', response)[0]
            score = str(float(score) / 10.0)
        else:
            score = str(re.findall(r'<b>评分</b>: ([^<]+)<br>', response)).strip(" [',']").replace('\'', '')
        if outline == '':
            result, dmm_htmlcode = get_html(
                "https://www.dmm.co.jp/search/=/searchstr=" + number.replace('-', '') + "/sort=ranking/")
            if 'に一致する商品は見つかりませんでした' not in dmm_htmlcode:
                dmm_page = etree.fromstring(dmm_htmlcode, etree.HTMLParser())
                url_detail = str(dmm_page.xpath('//*[@id="list"]/li[1]/div/p[2]/a/@href')).split(',', 1)[0].strip(
                    " ['']")
                if url_detail != '':
                    result, dmm_detail = get_html(url_detail)
                    html = etree.fromstring(dmm_detail, etree.HTMLParser())
                    outline = str(html.xpath('//*[@class="mg-t0 mg-b20"]/text()')).strip(" ['']").replace('\\n', '').replace('\n', '')
    except Exception as error_info1:
        print('Error in javbus.getOutlineScore : ' + str(error_info1))
    return outline, score


def getSeries(htmlcode):
    html = etree.fromstring(htmlcode, etree.HTMLParser())
    result = str(html.xpath('//span[contains(text(),"系列")]/following-sibling::a/text()')).strip(" ['']")
    return result


def getCover_small(number):  # 从avsox获取封面图
    try:
        result, htmlcode = get_html('https://avsox.website/cn/search/' + number)
        html = etree.fromstring(htmlcode, etree.HTMLParser())
        counts = len(html.xpath("//div[@id='waterfall']/div/a/div"))
        if counts == 0:
            return ''
        for count in range(1, counts + 1):  # 遍历搜索结果，找到需要的番号
            number_get = html.xpath("//div[@id='waterfall']/div[" + str(count) + "]/a/div[@class='photo-info']/span/date[1]/text()")
            if len(number_get) > 0 and number_get[0].upper() == number.upper():
                cover_small = html.xpath("//div[@id='waterfall']/div[" + str(count) + "]/a/div[@class='photo-frame']/img/@src")[0]
                return cover_small
    except Exception as error_info:
        print('Error in javbus.getCover_small : ' + str(error_info))
    return ''


def getTag(htmlcode):  # 获取标签
    tag = []
    soup = BeautifulSoup(htmlcode, 'lxml')
    a = soup.find_all(attrs={'class': 'genre'})
    for i in a:
        if 'onmouseout' in str(i):
            continue
        tag.append(i.get_text())
    if '多選提交' in tag:
        tag.remove('多選提交')
    return tag


def find_number(number):
    # =======================================================================有码搜索
    if not (re.match('^\d{4,}', number) or re.match('n\d{4}', number) or 'HEYZO' in number.upper()):
        result, htmlcode = get_html('https://www.javbus.com/search/' + number + '&type=1')
        html = etree.fromstring(htmlcode, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
        counts = len(html.xpath("//div[@id='waterfall']/div[@id='waterfall']/div"))
        if counts != 0:
            for count in range(1, counts + 1):  # 遍历搜索结果，找到需要的番号
                number_get = html.xpath("//div[@id='waterfall']/div[@id='waterfall']/div[" + str(count) + "]/a[@class='movie-box']/div[@class='photo-info']/span/date[1]/text()")[0]
                number_get = number_get.upper()
                number = number.upper()
                if number_get == number or number_get == number.replace('-', '') or number_get == number.replace('_', ''):
                    result_url = html.xpath(
                        "//div[@id='waterfall']/div[@id='waterfall']/div[" + str(count) + "]/a[@class='movie-box']/@href")[0]
                    return result_url
    # =======================================================================无码搜索
    result, htmlcode = get_html('https://www.javbus.com/uncensored/search/' + number + '&type=1')
    html = etree.fromstring(htmlcode, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
    counts = len(html.xpath("//div[@id='waterfall']/div[@id='waterfall']/div"))
    if counts == 0:
        return 'Movie data not found'
    for count in range(1, counts + 1):  # 遍历搜索结果，找到需要的番号
        number_get = html.xpath("//div[@id='waterfall']/div[@id='waterfall']/div[" + str(count) + "]/a[@class='movie-box']/div[@class='photo-info']/span/date[1]/text()")[0]
        number_get = number_get.upper()
        number = number.upper()
        if number_get == number or number_get == number.replace('-', '') or number_get == number.replace('_', ''):
            result_url = html.xpath(
                "//div[@id='waterfall']/div[@id='waterfall']/div[" + str(count) + "]/a[@class='movie-box']/@href")[0]
            return result_url
        elif number_get == number.replace('-', '_') or number_get == number.replace('_', '-'):
            result_url = html.xpath(
                "//div[@id='waterfall']/div[@id='waterfall']/div[" + str(count) + "]/a[@class='movie-box']/@href")[0]
            return result_url
    return 'Movie data not found'


def main(number, appoint_url='', log_info=''):
    log_info += '   >>> JAVBUS-开始使用 javbus 进行刮削\n'
    real_url = appoint_url
    title = ''
    cover_url = ''
    cover_small = ''
    error_type = ''
    error_info = ''
    dic = {}

    try:
        if appoint_url:
            result_url = appoint_url
        else:
            result_url = find_number(number)
        if result_url == 'Movie data not found':
            log_info += '   >>> JAVBUS-搜索结果页匹配番号：未匹配到番号！ \n'
            error_type = '未匹配到番号'
            raise Exception('JAVBUS-搜索结果页：未匹配到番号！')

        result, htmlcode = get_html(result_url)
        if not result:
            log_info += '   >>> JAVBUS-请求详情页：' + htmlcode
            error_type = 'timeout'
            raise Exception('>>> JAVBUS-请求详情页：' + htmlcode)

        actor = str(getActor(htmlcode)).strip(' ['']').replace("'", '')
        title = str(getTitle(htmlcode)).strip(actor).replace(number, '').strip() # 获取标题
        if not title:
            log_info += '   >>> JAVBUS- title 获取失败！ \n'
            error_type = 'need login'
            raise Exception('>>> JAVBUS- title 获取失败！')
        cover_url = getCover(htmlcode) # 获取cover
        if 'http' not in cover_url:
            log_info += '   >>> JAVBUS- cover url 获取失败！ \n'
            error_type = 'Cover Url is None!'
            raise Exception('>>> JAVBUS- cover url 获取失败！')
        cover_small = getCover_small(number)
        outline, score = getOutlineScore(number)

        try:
            dic = {
                'title': str(title).replace('-', '').replace(actor, ''),
                'number': number,
                'actor': actor,
                'outline': str(outline),
                'tag': getTag(htmlcode),
                'release': getRelease(htmlcode),
                'year': getYear(getRelease(htmlcode)),
                'runtime': getRuntime(htmlcode).replace('分鐘', '').strip(),
                'score': str(score),
                'series': getSeries(htmlcode),
                'director': getDirector(htmlcode),
                'studio': getStudio(htmlcode),
                'publisher': getPublisher(htmlcode),
                'source': 'javbus.main',
                'website': str(result_url),
                'actor_photo': getActorPhoto(htmlcode),
                'cover': str(cover_url),
                'cover_small': str(cover_small),  # 从avsox获取封面图
                'extrafanart': getExtraFanart(htmlcode),
                'imagecut': 1,
                'log_info': str(log_info),
                'error_type': '',
                'error_info': str(error_info),
            }
            log_info += '   >>> JAVBUS-数据获取成功！\n'
            dic['log_info'] = log_info
        except Exception as error_info:
            log_info += '   >>> JAVBUS-生成数据字典：出错！ 错误信息：%s \n' % str(error_info)
            error_info = str(error_info)
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
    js = json.dumps(dic, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js


def main_uncensored(number, appoint_url='', log_info=''):
    log_info += '   >>> JAVBUS-开始使用 javbus 进行刮削\n'
    real_url = appoint_url
    title = ''
    cover_url = ''
    cover_small = ''
    error_type = ''
    error_info = ''
    dic = {}
    try:
        result_url = ''
        if appoint_url == '':
            result_url = find_number(number)
        else:
            result_url = appoint_url
        if result_url == 'Movie data not found':
            log_info += '   >>> JAVBUS-搜索结果页匹配番号：未匹配到番号！ \n'
            error_type = 'Movie data not found'
            raise Exception('Movie data not found')
        result, htmlcode = get_html(result_url)
        if not result:
            log_info += '   >>> JAVBUS-请求详情页：' + str(htmlcode)
            error_type = 'timeout'
            raise Exception('>>> JAVBUS-请求详情页：' + str(htmlcode))

        actor = str(getActor(htmlcode)).strip(' ['']').replace("'", '')
        title = str(getTitle(htmlcode)).strip(actor).replace(number, '').strip() # 获取标题
        if not title:
            log_info += '   >>> JAVBUS- title 获取失败！ \n'
            error_type = 'need login'
            raise Exception('>>> JAVBUS- title 获取失败！')
        cover_url = getCover(htmlcode) # 获取cover
        if 'http' not in cover_url:
            log_info += '   >>> JAVBUS- cover url 获取失败！ \n'
            error_type = 'Cover Url is None!'
            raise Exception('>>> JAVBUS- cover url 获取失败！')
        cover_small = getCover_small(number)
        # if 'http' not in cover_small:
        #     log_info += '   >>> JAVBUS- cover url 获取失败！\n'
        #     error_type = 'Cover_small Url is None!'
        #     raise Exception('>>> JAVBUS- cover_small url 获取失败！')
        outline = ''
        score = ''
        if 'HEYZO' in number.upper():
            outline, score = getOutlineScore(number)
        studio = getStudio(htmlcode)
        try:
            dic = {
                'title': str(title),
                'number': number,
                'actor': actor,
                'outline': str(outline),
                'tag': getTag(htmlcode),
                'release': getRelease(htmlcode),
                'year': getYear(getRelease(htmlcode)),
                'runtime': getRuntime(htmlcode).replace('分鐘', '').strip(),
                'score': str(score),
                'series': getSeries(htmlcode),
                'director': getDirector(htmlcode),
                'studio': studio,
                'publisher': studio,
                'source': 'javbus.main_uncensored',
                'website': str(result_url),
                'actor_photo': getActorPhoto(htmlcode),
                'cover': str(cover_url),
                'cover_small': str(cover_small),  # 从avsox获取封面图
                'extrafanart': getExtraFanart(htmlcode),
                'imagecut': 3,
                'log_info': str(log_info),
                'error_type': '',
                'error_info': str(error_info),
            }
            if dic['cover_small'] == '':
                dic['imagecut'] = 0
            log_info += '   >>> JAVBUS-数据获取成功！\n'
            dic['log_info'] = log_info
        except Exception as error_info:
            log_info += '   >>> JAVBUS-生成数据字典：出错！ 错误信息：%s \n' % str(error_info)
            error_info = str(error_info)
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
    js = json.dumps(dic, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js


def main_us(number, appoint_url='', log_info=''):
    log_info += '   >>> JAVBUS-开始使用 javbus 进行刮削\n'
    real_url = appoint_url
    title = ''
    cover_url = ''
    cover_small = ''
    error_type = ''
    error_info = ''
    dic = {}

    try:
        result_url = ''
        if appoint_url:
            result_url = appoint_url
        else:
            result, htmlcode = get_html('https://www.javbus.one/search/' + number)
            if not result:
                log_info += '   >>> JAVBUS-请求搜索页：' + (htmlcode)
                error_type = 'timeout'
                raise Exception('>>> JAVBUS-请求搜索页：' + (htmlcode))
            html = etree.fromstring(htmlcode, etree.HTMLParser())  # //table/tr[1]/td[1]/text()
            counts = len(html.xpath("//div[@class='row']/div[@id='waterfall']/div"))
            if counts == 0:
                log_info += '   >>> JAVBUS-搜索结果页匹配番号：未匹配到番号！ \n'
                error_type = 'Movie data not found'
                raise Exception('Movie data not found')
            result_url = ''
            cover_small = ''
            for count in range(1, counts + 1):  # 遍历搜索结果，找到需要的番号
                number_get = html.xpath("//div[@id='waterfall']/div[" + str(
                    count) + "]/a[@class='movie-box']/div[@class='photo-info']/span/date[1]/text()")[0]
                if number_get.upper() == number.upper() or number_get.replace('-', '').upper() == number.upper():
                    result_url = html.xpath(
                        "//div[@id='waterfall']/div[" + str(count) + "]/a[@class='movie-box']/@href")[0]
                    cover_small = html.xpath(
                        "//div[@id='waterfall']/div[" + str(
                            count) + "]/a[@class='movie-box']/div[@class='photo-frame']/img[@class='img']/@src")[0]
                    break
            if result_url == '':
                log_info += '   >>> JAVBUS-搜索结果页匹配番号：未匹配到番号！ \n'
                error_type = 'Movie data not found'
                raise Exception('Movie data not found')
        result, htmlcode = get_html(result_url)
        if not result:
            log_info += '   >>> JAVBUS-请求详情页：' + htmlcode
            error_type = 'timeout'
            raise Exception('>>> JAVBUS-请求详情页：' + htmlcode)

        actor = str(getActor(htmlcode)).strip(' ['']').replace("'", '')
        title = str(getTitle(htmlcode)).strip(actor).replace(number, '').strip()    # 获取标题
        if not title:
            log_info += '   >>> JAVBUS- title 获取失败！ \n'
            error_type = 'need login'
            raise Exception('>>> JAVBUS- title 获取失败！')
        cover_url = getCover(htmlcode) # 获取cover
        if 'http' not in cover_url:
            log_info += '   >>> JAVBUS- cover url 获取失败！ \n'
            error_type = 'Cover Url is None!'
            raise Exception('>>> JAVBUS- cover url 获取失败！')
        cover_small = getCover_small(number)
        # if 'http' not in cover_small:
        #     log_info += '   >>> JAVBUS- cover_small url 获取失败！\n'
        #     error_type = 'Cover_small Url is None!'
        #     raise Exception('>>> JAVBUS- cover_small url 获取失败！')
        try:
            dic = {
                'title': str(title),
                'number': number,
                'actor': actor,
                'outline': '',
                'tag': getTag(htmlcode),
                'release': getRelease(htmlcode),
                'year': getYear(getRelease(htmlcode)),
                'runtime': getRuntime(htmlcode).replace('分鐘', '').strip(),
                'score': '',
                'series': getSeries(htmlcode),
                'director': getDirector(htmlcode),
                'studio': '',
                'publisher': '',
                'source': 'javbus.us',
                'website': str(result_url),
                'actor_photo': getActorPhoto(htmlcode),
                'cover': str(cover_url),
                'cover_small': str(cover_small),  # 从avsox获取封面图
                'extrafanart': getExtraFanart(htmlcode),
                'imagecut': 0,
                'log_info': str(log_info),
                'error_type': '',
                'error_info': str(error_info),
            }
            log_info += '   >>> JAVBUS-数据获取成功！\n'
            dic['log_info'] = log_info
        except Exception as error_info:
            log_info += '   >>> JAVBUS-生成数据字典：出错！ 错误信息：%s \n' % str(error_info)
            error_info = str(error_info)
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
    js = json.dumps(dic, ensure_ascii=False, sort_keys=False, indent=4, separators=(',', ':'), )  # .encode('UTF-8')
    return js


'''
print(find_number('KA-001'))
print(main_uncensored('010115-001'))
print(main('ssni-644'))
print(main_uncensored('012715-793'))
print(main_us('sexart.15.06.10'))
print(main_uncensored('heyzo-1031'))
'''

# print(main('ssni-644', "https://www.javbus.com/SSNI-644"))
# print(main('ssni-802', ""))
# print(main_us('DirtyMasseur.20.07.26', "https://www.javbus.one/DirtyMasseur-20-07-26"))
