#-*- coding: utf-8 -*-

import codecs
import os.path
import urllib2
from bs4 import BeautifulSoup
import sqlite3
from Paper3_Methods import *

#####################################
########## SQL Methods ##############
#####################################

def isNewHotel(hotelid, c):
    c.execute("SELECT * FROM 'hotels' WHERE HotelID={}".format(hotelid))
    raw = c.fetchone()
    if raw: 
        return False
    else:
        return True

def isNewComment(commentid, c):
    c.execute("SELECT * FROM 'comments' WHERE CommentID={}".format(commentid))
    raw = c.fetchone()
    if raw: 
        return False
    else:
        return True

def isNewSegmented(commentID, c):
    c.execute("SELECT * FROM 'words' WHERE CommentID={}".format(commentID))
    raw = c.fetchone()
    if raw: 
        return False
    else:
        return True

def isNewWord(commentID, WordNumber, c):
    c.execute("SELECT * FROM 'words' WHERE CommentID={} AND WordNumber={}".format(commentID, WordNumber))
    raw = c.fetchone()
    if raw: 
        return False
    else:
        return True

#########################################
######## HTML Parsing Methods    ########
#########################################

def search_path(pagenum):
    foldernum=(pagenum//1000)+1
    minw=((foldernum-1)*1000)
    maxw=minw+999
    if minw==0:
        minw=1
    path=str(minw)+' - '+str(maxw)
    filename=str(pagenum).zfill(7)+'.html'
    halfpath = make_data_path("ctrip/HTML_extracts/{}".format(path))
    if not os.path.isdir(halfpath): os.makedirs(halfpath)
    fullpath = os.path.join(halfpath, filename)
    return fullpath

def open_soup_HTML(fullpath):
    with codecs.open(fullpath, "r", 'utf-8') as html:
        data = html.read()
        soup = BeautifulSoup(data, "lxml")
    return soup

def isEmpty(soup):
    if (soup.find("span",{"class":"btn_comment float_right"})):
        return False
    else: return True

def extract_HotelID(soup):
    hotelid=0
    idblock=soup.find("span",{"class":"btn_comment float_right"})
    hotel=idblock.get("data-hotel")
    hotelid=int(hotel)
    return hotel

def extract_hotel_name(soup):
    n_block=soup.find(["h1","h2"],{"itemprop":"name"})
    name=n_block.text
    name=name.strip()
    return name

def isJapan(soup):
    country_block=soup.find("a", {"id":"lnkCountryName"})
    countryID=country_block.get("href")
    if (countryID=="/international/country78/"):
        return True
    else: 
        return False

def extract_hotel_score(soup):
    if soup.find("a",{"class":"commnet_score"}):
        s_block=soup.find("a",{"class":"commnet_score"})
        score=0
        score_span=s_block.find("span",{"class":"score_text"})
        score_t=score_span.text
        score=float(score_t)
        return score
    else:
        return None

def extract_usernames(soup):
    user_blocks=soup.find_all("div",{"class":"user_info"})
    usernames=[]
    for i in user_blocks:
        p_block=i.find("p",{"class":"name"})
        if (p_block): 
            user=p_block.text
            usernames.append(user)
        p_block=i.find("p", {"class":"name J_name"})
        if (p_block): 
            user=p_block.text
            usernames.append(user)
    return usernames

def extract_CommentIDs(soup):
    comment_blocks=soup.find_all("div",{"class":"comment_block J_syncCmt"})
    commentids = []
    for i in comment_blocks:
        commentids.append(i.get("data-cid"))
    comment_blocks=soup.find_all("div",{"class":"comment_block"})
    for i in comment_blocks[:-1]:
        idblock = i.find("span", {"class":"small_c"})
        commentids.append(idblock.get("cid"))
    return commentids

def extract_comments(soup):
    comments_p=soup.find_all("p",{"class":"J_commentDetail"})
    comments = []
    for i in comments_p:
        comments.append(i.text)
    comments_div=soup.find_all("div",{"class":"comment_txt"})
    for i in comments_div[:-1]:
        comments.append(i.text)
    return comments

def extract_scores(soup):
    #Location, facilities, services, health, average
    case=0
    c_blocks=soup.find_all("div", {"class":"comment_main"})
    datavalue=[]
    for i in c_blocks:
        average_blocks=i.find_all("span", {"class":"score"})
        counter=0
        score_blocks=i.find_all("span", {"class":"small_c"})
        for j in score_blocks:
            values=[]
            loc=''
            for a in range(3,6)+1:loc+=j.get("data-value")[a]
            location=int(float(loc))
            fac=''
            for a in range(11,14)+1:fac+=j.get("data-value")[a]
            facilities=int(float(fac))
            ser=''
            for a in range(19,22)+1:
                ser+=j.get("data-value")[a]
            services=int(float(ser))
            hea=''
            for a in range(27,30)+1:
                hea+=j.get("data-value")[a]
            health=int(float(hea))
            ave_span=average_blocks[counter].find_all("span", {"class":"n"})
            ave=''
            for k in ave_span:
                ave+=k.text
            average=float(ave)
            values.append(location)
            values.append(facilities)
            values.append(services)
            values.append(health)
            values.append(average)
            datavalue.append(values)
            counter+=1
        counter=0
    c_blocks=soup.find_all("div", {"class":"comment_block"})
    for i in c_blocks[:-1]:
        average_blocks=i.find_all("span", {"class":"score"})
        counter=0
        score_blocks=i.find_all("div", {"class":"score_pop"})
        for j in score_blocks:
            values=[]
            score_item_spans = j.find_all("span", {"class":"score_item"})
            loc = score_item_spans[3].text[3]
            location=int(loc)
            fac = score_item_spans[2].text[3]
            facilities=int(fac)
            ser = score_item_spans[1].text[3]
            services=int(ser)
            hea = score_item_spans[0].text[3]
            health=int(hea)
            ave_span=average_blocks[counter].find_all("span", {"class":"n"})
            ave=''
            for k in ave_span:
                ave+=k.text
            average=float(ave)
            values.append(location)
            values.append(facilities)
            values.append(services)
            values.append(health)
            values.append(average)
            datavalue.append(values)
            counter+=1
        counter=0
    return datavalue

def extract_dates(soup):
    if soup.find_all("a", {"class":"v2_reviewsitem_date"}):
        date_blocks = soup.find_all("a", {"class":"v2_reviewsitem_date"})
    else:
        date_blocks = None
    dates = []
    if date_blocks:
        for block in date_blocks:
            date = block.text.strip()
            else:
                date = None
            dates.append(date)
    else:
        dates = None
    return dates

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
    
def getHotelPriceGoogle(name, driver):
    LoadGoogle(driver)
    search = driver.find_element_by_name('q')
    search.send_keys(name)
    search.send_keys(Keys.RETURN)
    time.sleep(10)
    soup = getSoup(driver)
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

#####################################
######## Saving Methods #############
#####################################

# sqlite_file = 'ctrip_db.sqlite'

#Inserting Data into Tables
def insert_hotel_data(soup):
    hotelID = extract_HotelID(soup)
    hotelName = extract_hotel_name(soup)
    hotelScore = extract_hotel_score(soup)
    
    hotel_price, currency = get_hotel_original_price(soup)
    if not hotel_price:
        hotel_price = RMB_to_Yen(get_hotel_price_RMB(soup))
    values = '{},"{}",{},{}'.format(hotelID,hotelName,hotelScore, hotel_price)
    data_path = make_data_path("ctrip/ctrip_db/hotels.csv")
    printLog(values, data_path)
    # c.execute("INSERT OR IGNORE INTO 'hotels' ('HotelID', 'HotelName', 'HotelScore') VALUES (?,?,?)", (hotelID, hotelName, hotelScore, ))

def insert_comment_data(soup):
    hotelID = extract_HotelID(soup)
    usernames = extract_usernames(soup)
    commentIDs = extract_CommentIDs(soup)
    comments = extract_comments(soup)
    scores = extract_scores(soup)
    location_scores = [i[0] for i in scores]
    facilities_scores = [i[1] for i in scores]
    services_scores = [i[2] for i in scores]
    health_scores = [i[3] for i in scores]
    average_scores = [i[4] for i in scores]
    # normalized_scores = [None for i in scores]
    dates = extract_dates(soup)
    strlist = []
    for i in usernames:
        values = '{},{},"{}",{},{},{},{},{},,{}'.format(usernames[i], commentIDs[i], comments[i], location_scores[i], facilities_scores[i], services_scores[i], health_scores[i], average_scores[i], dates[i])
        strlist.append(values)
    # c.execute("INSERT OR IGNORE INTO 'comments' ('HotelID', 'UserName', 'CommentID', 'Comment', 'LocationScore', 'FacilitiesScore', 'ServicesScore', 'HealthScore', 'AverageScore') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (hotelID, username, commentID, comment, location_score, facilities_score, services_score, health_score, average_score, ))
    data_path = make_data_path("ctrip/ctrip_db/comments.csv")
    print_list_to_log(strlist, data_path)

#########################################
################# MAIN ##################
#########################################
def parse_page(pagenum):
    soup=open_soup_HTML(search_path(pagenum))
    if (isEmpty(soup)==False):
        if (isJapan(soup)==True):
            print "Inserting row for table 'hotels' from hotelID: %s" %(extract_HotelID(soup))
            insert_hotel_data(soup)
            if (len(extract_CommentIDs(soup))>0):
                insert_comment_data(soup)
        else:
            print "Skipped page %s because it is not in Japan" %(str(pagenum).zfill(7)+'.html')
    else:
        print "Skipped page %s because of 404 Not Found" %(str(pagenum).zfill(7)+'.html')

def parse_pages():
    #first
    #pagenum=1
    #first japanese Hotel
    #pagenum=13640
    #first with comments
    #pagenum=14549
    #current
    pagenum = 1278512
    #True value
    #maxpage=9999999

    #Test value
    maxpage=1541424
    for i in range(pagenum,maxpage+1):
        parse_page(i)

##############################################
############## Normalize Scores ##############
##############################################

# same but edit to csv later
# def normalize_scores():
    
#     conn, c = Connect(sqlite_file)
#     c.execute("SELECT * FROM comments ORDER BY UserName ASC")
#     raw = c.fetchall()


#     raw_split = [list(g) for k,g in itertools.groupby(raw, lambda i: i[2])]
#     upd_raw = []
#     print "Normalizing Scores"
#     maxusers = len(raw_split)
#     for userind, user_raw in enumerate(raw_split):
#         print "Normalizing Scores for User {} of {}".format(userind+1, maxusers)
#         up()
#         scores = [comment[9] for comment in user_raw]
#         minscores = min(scores)
#         maxscores = max(scores)
#         rangescores = maxscores-minscores
#         if rangescores>0:
#             normalized_scores = [((float(score)-minscores)/(rangescores)) for score in scores]
#         else:
#             normalized_scores = [float(score)/5.0 for score in scores]
#         for ind,comment in enumerate(user_raw):
#             upd_raw_row = (normalized_scores[ind], comment[0])
#             upd_raw.append(upd_raw_row)
#     down()
#     print "Updating SQL comments"
#     c.executemany("UPDATE comments SET 'NormalizedScore'=? WHERE RID==?", upd_raw)
#     conn.commit()
#     conn.close()


# def Google_price():
#     driver = LoadBrowser()
#     conn, c = Connect("ctrip_db2.sqlite")
#     c.execute("SELECT HotelID, HotelName FROM hotels WHERE HotelPrice IS NULL")
#     hotels = c.fetchall()
#     lennum = len(hotels)
#     for num, hotel in enumerate(hotels):
#         hid, name = hotel
#         name_c, name_e = tuple(name.split("\n"))
#         print(u"Searching for price of {}: {} {}".format(hid,name_c,name_e))
#         print(u" {} out of {}".format(num+1,lennum))
#         price = getHotelPriceGoogle(name_e, driver)
#         if not price:
#             price = getHotelPriceGoogle(name_c, driver)
#         if not price:
#             name_b = name_c+" "+name_e
#             price = getHotelPriceGoogle(name_b, driver)
#         if price:
#             upd = (price,hid)
#             c.execute("UPDATE hotels SET 'HotelPrice'=? WHERE HotelID==?", upd)
#             conn.commit()
#         up()
#         up()
#         print(" "*30)
#         print(" "*50)
#         up()
#         up()
#     conn.close()

def main():
    parse_pages()
    normalize_scores()
    Google_price()

if __name__ == "__main__":
    main()