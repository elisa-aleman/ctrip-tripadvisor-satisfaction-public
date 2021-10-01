#-*- coding: utf-8 -*-
#!python3

import sys
import os
import os.path
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
from retry import retry

#########################################
######## HTML Parsing Methods   #########
#########################################

@retry(tries =-1, delay=10)
def load_page(pagenum, driver):
    url = 'http://hotels.ctrip.com/international/'+str(pagenum)+'.html'
    driver.get(url)
    # time.sleep(5)

@retry(tries =-1, delay=100)
def load_Google(driver):
    driver.get('http://www.google.com')

def isRedirect(pagenum, driver):
    url = 'http://hotels.ctrip.com/international/'+str(pagenum)+'.html'
    currenturl = driver.current_url
    if (url!= currenturl): return True
    else: return False

def get_page_num(driver):
    currenturl = driver.current_url
    newpagenum=currenturl.rsplit('/',1)[1].split('.')[0]
    return newpagenum

def click_next_comments(driver):
    element = driver.find_element_by_class_name('c_down')
    driver.execute_script("return arguments[0].scrollIntoView();", element)
    driver.execute_script("window.scrollBy(0,-150);")
    element.click()
    time.sleep(2)

def get_soup(driver):
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    return soup

def save_soup(soup, halfpath):
    hotelid = getHotelID(soup)
    cpagenum = getCurrentCommentPage(soup)
    foldernum=(hotelid//1000)+1
    minw=((foldernum-1)*1000)
    maxw=minw+999
    path1=str(minw)+' - '+str(maxw)
    path2= str(hotelid).zfill(7)
    filename=str(hotelid).zfill(7)+'-'+str(cpagenum).zfill(3)+'.html'
    newhalfpath=os.path.join(halfpath, path1, path2)
    if not os.path.isdir(halfpath): os.makedirs(newhalfpath)
    fullpath = os.path.join(newhalfpath, filename)
    with codecs.open(fullpath, "w", 'utf-8') as html:
        html.write(soup.prettify())

def load_soup(pagenum,commentpage, halfpath):
    hotelid = pagenum
    cpagenum = commentpage
    foldernum=(hotelid//1000)+1
    minw=((foldernum-1)*1000)
    maxw=minw+999
    path1=str(minw)+' - '+str(maxw)
    path2= str(hotelid).zfill(7)
    filename=str(hotelid).zfill(7)+'-'+str(cpagenum).zfill(3)+'.html'
    newhalfpath=os.path.join(halfpath, path1, path2)
    if not os.path.isdir(newhalfpath): os.makedirs(newhalfpath)
    fullpath = os.path.join(newhalfpath, filename)
    with codecs.open(fullpath, "r", 'utf-8') as html:
        data = html.read()
        soup = BeautifulSoup(data, "lxml")
    return soup

def isEmpty(soup):
    if (soup.find("input",{"id":"hotel"})):
        return False
    else: return True

def get_HotelID(soup):
    hotelid=0
    idblock=soup.find("input",{"id":"hotel"})
    hotel=idblock.get("value")
    hotelid=int(hotel)
    return hotelid

def get_hotel_name(soup):
    n_block=soup.find(["h1","h2"],{"itemprop":"name"})
    name=n_block.text
    name=name.strip()
    name = name.replace("  ","")
    return name

def isJapan(soup):
    country_block=soup.find("a", {"id":"lnkCountryName"})
    countryID=country_block.get("href")
    if (countryID=="/international/country78/"):
        return True
    else: 
        return False

def get_total_pages(soup):
    if soup.find("input", {"id":"cTotalPageNum"}):
        tp_block = soup.find("input", {"id":"cTotalPageNum"})
        tpages=tp_block.get("value")
        pages = int(tpages)
        return pages
    else: return None

def get_hotel_scores(soup):
    #Location, services, facilities, health, average
    location = 0
    services = 0
    facilities = 0
    health = 0
    average = 0
    if soup.find("span",{"class":"v2_reveiws_total_n"}):
        score_span=soup.find("span",{"class":"v2_reveiws_total_n"})
        score=0
        score_t=score_span.text.strip()
        if len(score_t)>0:
            score=float(score_t)
            average =score
        else:
            score = None
            average = None
    else:
        average = None
    if soup.find("span",{"class":"v2_reveiws_option_n"}):
        score_blocks=soup.find_all("span",{"class":"v2_reveiws_option_n"})
        location = float(score_blocks[0].text.strip())
        services = float(score_blocks[1].text.strip())
        facilities = float(score_blocks[2].text.strip())
        health = float(score_blocks[3].text.strip())
    else:
        location = None
        services = None
        facilities = None
        health = None
        average = None
    scores = [location, services, facilities, health, average]
    return scores

def get_hotel_original_price(soup):
    price_block = soup.find("p", {"id":"detail_originalprice", "class":"mlt_price"})
    price = None
    currency = None
    if price_block:
        currency_block = price_block.find("dfn")
        if currency_block:
            currency = currency_block.text
        price_span = price_block.find("span")
        if price_span:
            str_price = price_span.text.strip()
            price = int(float(str_price))
    return price, currency

def get_hotel_price_RMB(soup):
    price_block = soup.find("span", {"id":"detail_price"})
    price = None
    if price_block:
        price_span = price_block.find("span", {"class":"price"})
        if price_span:
            str_price = price_span.text.strip()
            if str_price.isdigit():
                price = int(float(str_price))
            else:
                price_span = soup.find("span", {"class":"base_pricediv"})
                str_price = price_span.text.strip()
                if str_price.isdigit():
                    price = int(float(str_price))
    return price

def RMB_to_Yen(rmb):
    yen = None
    if rmb:
        yen = rmb * 16.8832
        yen = int(yen)
    return yen
    
def get_hotel_price_Google(name, driver):
    load_Google(driver)
    search = driver.find_element_by_name('q')
    search.send_keys(name)
    search.send_keys(Keys.RETURN)
    time.sleep(10)
    soup = get_soup(driver)
    price_spans = soup.find_all("span", text=lambda value: value and value.startswith(u"\uffe5"))
    # price_spans = soup.find_all("span",{"class":"_V0p"})
    if price_spans:
        prices = []
        for price_span in price_spans:
            str_price = price_span.text.strip()
            new_str_price = ''
            for char in str_price:
                if char.isdigit():
                    new_str_price += char
            int_price = int(new_str_price)
            prices.append(int_price)
        # prices = [int(i.text.strip()[1:].replace(",","")) for i in price_spans]
        price = sum(prices)/len(prices)
    else:
        price = None
    return price

def get_current_comment_page(soup):
    page = int(soup.find("input",{"class":"c_page_num"}).get("value"))
    return page

def get_Usernames(soup):
    user_blocks=soup.find_all("div",{"class":"v2_reviewsitem_col2"})
    usernames=[]
    for i in user_blocks:
            user=i.text.strip()
            usernames.append(user)
    return usernames

def get_CommentIDs(soup):
    comment_blocks=soup.find_all("div",{"class":"v2_reviewsitem_col3"})
    commentids = []
    for i in comment_blocks:
        idblock = i.find("span", {"class":"small_c"})
        if idblock is not None:
            commentids.append(int(idblock.get("cid")))
    return commentids

def get_Comments(soup):
    comment_blocks=soup.find_all("div",{"class":"v2_reviewsitem_col3"})
    comments= []
    for block in comment_blocks:
        if block.find_all("div",{"class":"v2_reviewsitem_desc"}):
            comment = ""
            comment_p = block.find_all("div",{"class":"v2_reviewsitem_desc"})
            for i in comment_p:
                comment += i.text.strip()+" "
            comments.append(comment)
    return comments

def get_review_types(soup):
    comment_blocks=soup.find_all("div",{"class":"v2_reviewsitem_col3"})
    types = []
    for i in comment_blocks:
        type_block_true = i.find("span",{"class":"v2_reviewsitem_type"})
        if type_block_true:
            types.append(type_block_true.text.strip())
        else:
            types.append(None)
    return types

def get_user_scores(soup):
    s_blocks=soup.find_all("span", {"class":"v2_reviewsitem_score"})
    scores = []
    for i in s_blocks:
        text = i.text.strip()
        if (len(text)==4):
            uscore = text[:3]
        else:
            uscore = text[0]
        score=float(uscore)
        scores.append(score)
    return scores

def extract_dates(soup):
    if soup.find_all("a", {"class":"v2_reviewsitem_date"}):
        date_blocks = soup.find_all("a", {"class":"v2_reviewsitem_date"})
    else:
        date_blocks = None
    dates = []
    if date_blocks:
        for block in date_blocks:
            date = block.text.strip()
            dates.append(date)
    else:
        dates = None
    return dates

if __name__ == "__main__":
    pass