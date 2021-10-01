#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.SeleniumBrowser_proxy.SeleniumBrowser import *
from Ctrip_HTMLParsing import *
from csv_sql_methods import *

from retry import retry
import codecs
import sys
import os
import os.path
import time

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

#########################################
######## SQL Saving Methods #############
#########################################

# sqlite_file = 'ctrip_db2.sqlite'

#Inserting Data into Tables
def insert_hotel_data(soup, c):
    hotelID = get_HotelID(soup)
    hotelName = get_hotel_name(soup)
    hotel_scores = get_hotel_scores(soup)
    hotelScore = hotel_scores[0]
    location_score = hotel_scores[1]
    services_score = hotel_scores[2]
    facilities_score = hotel_scores[3]
    health_score = hotel_scores[4]
    hotel_price, currency = get_hotel_original_price(soup)
    if not hotel_price:
        hotel_price = RMB_to_Yen(get_hotel_price_RMB(soup))
    isnew = isNewHotel(hotelID, c)
    if isnew:
        # newrow = (hotelID, hotelName, hotelScore, location_score, services_score, facilities_score, health_score, hotel_price)
        # c.execute("INSERT INTO 'hotels' ('HotelID', 'HotelName', 'HotelScore', 'LocationScore', 'ServicesScore', 'FacilitiesScore', 'HealthScore', 'HotelPrice') VALUES (?,?,?,?,?,?,?,?)", (newrow))
        values = '{},"{}",{},{},{},{},{},{}'.format(hotelID, hotelName, hotelScore, location_score, services_score, facilities_score, health_score, hotel_price)
        data_path = make_data_path("ctrip/ctrip_db2/hotels.csv")
        printLog(values, data_path)

def insert_comment_data(soup, c):
    totalpages = get_total_pages(soup)
    if totalpages:
        commentpage = get_current_comment_page(soup)
    else:
        commentpage = 1
    hotelID = get_HotelID(soup)
    commentIDs = get_CommentIDs(soup)
    usernames = get_Usernames(soup)
    comments = get_Comments(soup)
    review_types = get_review_types(soup)
    scores = get_user_scores(soup)
    dates = extract_dates(soup)
    if len(commentIDs)>0:
        isnew = isNewComment(commentIDs[0], c)
        if isnew:
            insrows = []
            for i, _ in enumerate(commentIDs):
                newrow = (hotelID, commentpage, usernames[i], commentIDs[i], comments[i], review_types[i], scores[i], dates[i])
                insrows.append(newrow)
            statement = "INSERT INTO 'comments' ('HotelID', 'CommentPage', 'UserName', 'CommentID', 'Comment', 'ReviewType', 'Score', 'Date') VALUES (?,?,?,?,?,?,?,?)"
            c.executemany(statement, insrows)

##############################################
################### MAIN #####################
##############################################

def Crawling(hotels):
    halfpath= make_data_path('html_gets')
    if not os.path.isdir(halfpath): os.makedirs(halfpath)
    driver = load_browser(use_proxy="REDACTED")
    for hotel in hotels:
        load_page(hotel, driver)
        soup = get_soup(driver)
        totalpages = get_total_pages(soup)
        for i in xrange(1, totalpages+1):
            save_soup(soup, halfpath)
            if i<totalpages: 
                click_next_comments(driver)
                time.sleep(5)
            soup = get_soup(driver)

def crawl_one(hotel, pagenum, halfpath):
    halfpath= make_data_path('html_gets')
    if not os.path.isdir(halfpath): os.makedirs(halfpath)
    driver = load_browser(use_proxy="REDACTED")
    load_page(hotel, driver)
    i=1
    while (i<pagenum):
        click_next_comments(driver)
        time.sleep(5)
        i=i+1
    soup = get_soup(driver)
    save_soup(soup, halfpath)

def scraping(hotels, currenthotel=0, currentcommentpage=1, crawl=False):
    halfpath = make_data_path("ctrip/HTML_extracts")
    if not os.path.isdir(halfpath): os.makedirs(halfpath)
    conn, c = Connect('ctrip_db2.sqlite')
    driver = load_browser(use_proxy="REDACTED")
    skiphotel = True
    skipcommentpage = True
    if (currenthotel==0):
        skiphotel=False
    if (currentcommentpage==0):
        skipcommentpage=False
    maxhotels = len(hotels)
    for counter, hotel in enumerate(hotels):
        print("scraping Hotel {} out of {} with the HotelID {}      ".format(counter+1, maxhotels, hotel))
        if currenthotel==0:
            skiphotel=False
        elif (hotel == currenthotel):
            skiphotel = False
        if not skiphotel:
            if crawl:
                soup = load_soup(hotel, 1)
            else:
                load_page(hotel, driver)
                time.sleep(3)
                soup = get_soup(driver)
            if not isEmpty(soup):
                if isJapan(soup)==True:
                    totalpages = get_total_pages(soup)
                    insert_hotel_data(soup, c)
                    if totalpages:
                        for i in range(1, totalpages+1):
                            print("scraping Comment page {} out of {}...".format(i, totalpages))
                            if (i == currentcommentpage):
                                skipcommentpage = False
                            if not skipcommentpage:
                                if crawl:
                                    soup = load_soup(hotel, i)
                                    insert_comment_data(soup, c)
                                    conn.commit()
                                else:
                                    insert_comment_data(soup, c)
                                    conn.commit()
                                    if i<totalpages:
                                        time.sleep(5)
                                        while True:
                                            try: 
                                                click_next_comments(driver)
                                                break
                                            except StaleElementReferenceException:
                                                time.sleep(5)
                                        soup = get_soup(driver)
                            up()
                    else:
                        insert_comment_data(soup, c)
                        conn.commit()
        print(" "*50)
        up()
        up()
    conn.close()

def carry_price():
    tconn, tc = Connect('ctrip_db.sqlite')
    tc.execute("SELECT HotelID FROM hotels WHERE HotelPrice IS NOT NULL")
    raw = tc.fetchall()
    hotels = [item[0] for item in raw]
    conn, c = Connect("ctrip_db2.sqlite")
    c.execute("SELECT HotelID FROM hotels WHERE HotelPrice IS NULL")
    raw = c.fetchall()
    photels = [item[0] for item in raw]
    pos = tuple(sorted(list(set(hotels).intersection(set(photels)))))
    placeholders = ','.join("?"*len(pos))
    tc.execute("SELECT HotelPrice, HotelID FROM hotels WHERE HotelID IN ({})".format(placeholders), pos)
    upd = tc.fetchall()
    c.executemany("UPDATE hotels SET 'HotelPrice'=? WHERE HotelID==?", upd)
    conn.commit()
    conn.close()
    tconn.close()

def Google_price():
    driver = load_browser(use_proxy="REDACTED")
    conn, c = Connect("ctrip_db2.sqlite")
    c.execute("SELECT HotelID, HotelName FROM hotels WHERE HotelPrice IS NULL")
    hotels = c.fetchall()
    lennum = len(hotels)
    for num, hotel in enumerate(hotels):
        hid, name = hotel
        name_c, name_e = tuple(name.split("\n"))
        print(u"Searching for price of {}: {} {}".format(hid,name_c,name_e))
        print(u" {} out of {}".format(num+1,lennum))
        price = get_hotel_price_Google(name_e, driver)
        if not price:
            price = get_hotel_price_Google(name_c, driver)
        if not price:
            name_b = name_c+" "+name_e
            price = get_hotel_price_Google(name_b, driver)
        if price:
            upd = (price,hid)
            c.execute("UPDATE hotels SET 'HotelPrice'=? WHERE HotelID==?", upd)
            conn.commit()
        up()
        up()
        print(" "*30)
        print(" "*50)
        up()
        up()
    conn.close()

def crawl_scrape_hotels():
    tconn, tc = Connect('ctrip_db.sqlite')
    tc.execute("SELECT HotelID from hotels")
    raw = tc.fetchall()
    hotels = [item[0] for item in raw]
    tconn.close()
    currenthotel = hotels[7029-1]
    currentcommentpage = 1
    scraping(hotels, currenthotel,currentcommentpage)

def main():
    crawl_scrape_hotels()
    Google_price()
    carry_price()

if __name__ == "__main__":
    main()