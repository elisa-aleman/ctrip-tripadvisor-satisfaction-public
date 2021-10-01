#-*- coding: utf-8 -*-

import os
import pathlib
import pandas
from EntropyBasedSVM.useful_methods.UsefulMethods import *
from EntropyBasedSVM.useful_methods.ProjectPaths import *
from collections import Counter


def Common_Hotels_with_price_df():
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db2_tripadvisor__with_price_data.csv"))
    return common_hotels_df

def get_pricelayer_dict(bin_ver=2):
    if bin_ver==1:
        pricedict = dict([
            (0,'0: All Prices'),
            (1, '1: 0 to 5000'),
            (2, '2: 5000 to 10000'),
            (3, '3: 10000 to 15000'),
            (4, '4: 15000 to 20000'),
            (5, '5: 20000 to 100000'),
            (6, '6: 100000 to 200000')])
    if bin_ver==2:
        pricedict = dict([
            (0, '0: All Prices'),
            (1, '1: 0 to 2500'),
            (2, '2: 2500 to 5000'),
            (3, '3: 5000 to 10000'),
            (4, '4: 10000 to 15000'),
            (5, '5: 15000 to 20000'),
            (6, '6: 20000 to 30000'),
            (7, '7: 30000 to 50000'),
            (8, '8: 50000 to 100000'),
            (9, '9: 100000 to 200000')
            ])
    return pricedict

def get_comma_pricelayer_dict(bin_ver=2):
    if bin_ver==1:
        pricedict = dict([
            (0,'0: All Prices'),
            (1, '1: 0 to 5000'),
            (2, '2: 5000 to 10,000'),
            (3, '3: 10,000 to 15,000'),
            (4, '4: 15,000 to 20,000'),
            (5, '5: 20,000 to 100,000'),
            (6, '6: 100,000 to 200,000')])
    if bin_ver==2:
        pricedict = dict([
            (0, '0: All Prices'),
            (1, '1: 0 to 2500'),
            (2, '2: 2500 to 5000'),
            (3, '3: 5000 to 10,000'),
            (4, '4: 10,000 to 15,000'),
            (5, '5: 15,000 to 20,000'),
            (6, '6: 20,000 to 30,000'),
            (7, '7: 30,000 to 50,000'),
            (8, '8: 50,000 to 100,000'),
            (9, '9: 100,000 to 200,000')
            ])
    return pricedict

def get_comma_yen_pricelayer_dict(bin_ver=2):
    if bin_ver==1:
        pricedict = dict([
            (0,'0: All Prices'),
            (1, '1: 0 to 5000 yen'),
            (2, '2: 5000 to 10,000 yen'),
            (3, '3: 10,000 to 15,000 yen'),
            (4, '4: 15,000 to 20,000 yen'),
            (5, '5: 20,000 to 100,000 yen'),
            (6, '6: 100,000 to 200,000 yen')])
    if bin_ver==2:
        pricedict = dict([
            (0, '0: All Prices'),
            (1, '1: 0 to 2500'),
            (2, '2: 2500 to 5000 yen'),
            (3, '3: 5000 to 10,000 yen'),
            (4, '4: 10,000 to 15,000 yen'),
            (5, '5: 15,000 to 20,000 yen'),
            (6, '6: 20,000 to 30,000 yen'),
            (7, '7: 30,000 to 50,000 yen'),
            (8, '8: 50,000 to 100,000 yen'),
            (9, '9: 100,000 to 200,000 yen')
            ])
    return pricedict

def get_price_bins(bin_ver=2):
    if bin_ver in [1,2]:
        if bin_ver==1:
            bins = numpy.array([0,5000,10000,15000,20000,100000,200000])
        if bin_ver==2:
            bins = numpy.array([0,2500,5000,10000,15000,20000,30000,50000,100000,200000])
    else:
        bins = bin_ver
    return bins

# >>> hotel_df.columns
# Index(['RID', 'Ctrip_HotelID', 'HotelName', 'EnglishHotelName', 'HotelScore',
#        'LocationScore', 'tripadvisor_hotel_id', 'ServicesScore',
#        'FacilitiesScore', 'HealthScore', 'HotelPrice', 'hotel_name',
#        'hotel_url', 'hotel_rating', 'city_id', 'postal_code', 'prefecture',
#        'locality', 'street', 'ext_address', 'address', 'price_lower',
#        'price_upper', 'rooms'],
#       dtype='object')

def get_hotel_ids_pricelayer(bin_ver=2, bin_by='price_upper', price_layer=0):
    hotel_df = Common_Hotels_with_price_df()
    if price_layer==0:
        return hotel_df
    elif bin_ver in [1,2]:
        bins = get_price_bins(bin_ver=bin_ver)
        bin_low = bins[price_layer-1]
        bin_high = bins[price_layer]
        hotel_df = hotel_df[hotel_df[bin_by].between(bin_low,bin_high)]
        return hotel_df
    else:
        return hotel_df

def get_ctrip_trans_dict():
    file_path = make_log_file('ctrip/keyword_counts/translations_list.csv')
    trans_df = pandas.read_csv(file_path)
    keywords = trans_df.keyword
    translated = trans_df.translated_keyword
    trans_dict = dict(list(zip(keywords, translated)))
    return trans_dict

def get_ctrip_remove_list():
    remove_these = read_dict(make_log_file('ctrip/keyword_counts/remove_keywords_list.txt'))
    return remove_these

def get_tripadvisor_remove_list():
    remove_these = read_dict(make_log_file('tripadvisor/keyword_counts/remove_keywords_list.txt'))
    return remove_these


def selected_keyword_count_logs(db='tripadvisor', status='general', view='most_common', filtered=True):
    bin_by = 'price_upper'
    bin_ver = 2
    if db=='ctrip':
        if filtered:
            file_path = make_log_file('ctrip/keyword_counts/{3}_filtered/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by, view))
        else:    
            file_path = make_log_file('ctrip/keyword_counts/{3}/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by, view))
    elif db=='tripadvisor':
        if filtered:
            file_path = make_log_file('tripadvisor/keyword_counts/{3}_filtered/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by, view))
        else:
            file_path = make_log_file('tripadvisor/keyword_counts/{3}/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by, view))
    log_df = pandas.read_csv(file_path)
    return log_df

def selected_keyword_count_logs_no_doubles(db='tripadvisor', status='general', view='most_common', filtered=True):
    bin_by = 'price_upper'
    bin_ver = 2
    key_counts_sorted_df = pandas.DataFrame()
    pricedict = get_comma_yen_pricelayer_dict(bin_ver=bin_ver)
    price_layer_strs = sorted(pricedict.values())
    if db == 'ctrip':
        trans_dict = get_ctrip_trans_dict()
        if filtered:
            file_path = make_log_file('ctrip/keyword_counts/raw_counts_filtered/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by))
        else:
            file_path = make_log_file('ctrip/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by))
        log_df = pandas.read_csv(file_path)
        log_df = log_df[~log_df['keyword'].str.contains(' ')]
        db_counts = [(column,dict(list(zip(log_df['keyword'],log_df[column])))) for column in log_df[price_layer_strs]]
        for price_layer_str,x in db_counts:
            x = Counter(x)
            ins_col = ['{} ({}) : {}'.format(k,trans_dict[k],v) for k,v in x.most_common()]
            key_counts_sorted_df[price_layer_str] = ins_col
    elif db == 'tripadvisor':
        if filtered:
            file_path = make_log_file('tripadvisor/keyword_counts/raw_counts_filtered/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
        else:
            file_path = make_log_file('tripadvisor/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
        log_df = pandas.read_csv(file_path)
        log_df = log_df[~log_df['keyword'].str.contains(' ')]
        db_counts = [(column,dict(list(zip(log_df['keyword'],log_df[column])))) for column in log_df[price_layer_strs]]
        for price_layer_str,x in db_counts:
            x = Counter(x)
            ins_col = ['{} : {}'.format(k,v) for k,v in x.most_common()]
            key_counts_sorted_df[price_layer_str] = ins_col
    return key_counts_sorted_df


def select_adjective_logs_most_common(adj='大', db='ctrip', status='general', filtered=True):
    bin_by = 'price_upper'
    bin_ver = 2
    key_counts_sorted_df = pandas.DataFrame()
    pricedict = get_comma_yen_pricelayer_dict(bin_ver=bin_ver)
    price_layer_strs = sorted(pricedict.values())
    if db == 'ctrip':
        trans_dict = get_ctrip_trans_dict()
        if filtered:
            file_path = make_log_file('ctrip/keyword_counts/raw_counts_filtered/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by))
        else:
            file_path = make_log_file('ctrip/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by))
        log_df = pandas.read_csv(file_path)
        log_df = log_df[log_df['keyword'].str.contains(adj)]
        db_counts = [(column,dict(list(zip(log_df['keyword'],log_df[column])))) for column in log_df[price_layer_strs]]
        for price_layer_str,x in db_counts:
            x = Counter(x)
            ins_col = ['{} ({}) : {}'.format(k,trans_dict[k],v) for k,v in x.most_common()]
            key_counts_sorted_df[price_layer_str] = ins_col
    elif db == 'tripadvisor':
        if filtered:
            file_path = make_log_file('tripadvisor/keyword_counts/raw_counts_filtered/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
        else:
            file_path = make_log_file('tripadvisor/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
        log_df = pandas.read_csv(file_path)
        log_df = log_df[log_df['keyword'].str.contains(adj)]
        db_counts = [(column,dict(list(zip(log_df['keyword'],log_df[column])))) for column in log_df[price_layer_strs]]
        for price_layer_str,x in db_counts:
            x = Counter(x)
            ins_col = ['{} : {}'.format(k,v) for k,v in x.most_common()]
            key_counts_sorted_df[price_layer_str] = ins_col
    return key_counts_sorted_df

def get_hard_soft_df(db='ctrip'):
    if db=='ctrip':
        hard_soft_df = pandas.read_csv(make_log_file("ctrip/keyword_counts/hard_soft_dict.csv"))
    elif db == 'tripadvisor':
        hard_soft_df = pandas.read_csv(make_log_file("tripadvisor/keyword_counts/hard_soft_dict.csv"))
    return hard_soft_df

if __name__ == '__main__':
    pass

