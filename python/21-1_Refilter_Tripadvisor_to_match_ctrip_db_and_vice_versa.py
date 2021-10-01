#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *

def Refilter_common_hotels_df_by_ctrip():
    ctrip_db_df = get_Ctrip_db_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_df()
    ctrip_hotel_ids = ctrip_db_df.HotelID.unique()
    common_hotels_path = make_data_path("hotels_in_common_ctrip_db_tripadvisor.csv")
    common_hotels_df = pandas.read_csv(common_hotels_path)
    common_hotels_df = common_hotels_df[common_hotels_df["Ctrip_HotelID"].isin(ctrip_hotel_ids)]
    common_hotels_df = common_hotels_df[common_hotels_df["Ctrip_HotelID"]!=85835]
    # Remove duplicate
    #
    # >>> common_hotels_df[common_hotels_df.tripadvisor_hotel_id == 450]
    #     RID  Ctrip_HotelID                     HotelName    EnglishHotelName  HotelScore  HotelPrice  ...   street ext_address                  address  price_lower  price_upper rooms
    # 3    57          85835  Smile Hotel Sugamo(东京巢鸭微笑酒店)  Smile Hotel Sugamo         0.0      6089.0  ...  巣鴨2-4-7         NaN  〒170-0002 東京都豊島区巣鴨2-4-7         5330        18545   126
    # 4  5178        1649312   Smile Hotel Sugamo(微笑酒店 巢鸭)  Smile Hotel Sugamo         4.1      7014.0  ...  巣鴨2-4-7         NaN  〒170-0002 東京都豊島区巣鴨2-4-7         5330        18545   126
    #
    common_hotels_df.to_csv(common_hotels_path, index=False)

def Refilter_tripadvisor_to_match_ctrip_commons():
    tagged_path = make_data_path("tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db_date_hotel-name.csv")
    tagged_df = pandas.read_csv(tagged_path)
    # tagged_df = get_Tripadvisor_tagged_english_sentences__ctrip_db_filtered_date_hotel_name_df() 
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db_tripadvisor.csv"))
    filtered_df = tagged_df[tagged_df.hotel_id.isin(common_hotels_df.tripadvisor_hotel_id)]
    filtered_df.to_csv(tagged_path, index=False)

def Refilter_ctrip_unpredicted_by_filtered_tripadvisor():
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db_tripadvisor.csv"))
    tagged_path = make_data_path("ctrip/ctrip_db/sentences_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv")
    tagged_df = pandas.read_csv(tagged_path)
    filtered = tagged_df[tagged_df.HotelID.isin(common_hotels_df.Ctrip_HotelID)]
    filtered.to_csv(tagged_path,index=False)

def Refilter_ctrip_predicted_by_filtered_tripadvisor():
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db_tripadvisor.csv"))
    tagged_path = make_data_path("ctrip/ctrip_db/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv")
    tagged_df = pandas.read_csv(tagged_path)
    filtered = tagged_df[tagged_df.HotelID.isin(common_hotels_df.Ctrip_HotelID)]
    filtered.to_csv(tagged_path,index=False)

if __name__ == '__main__':
    # Refilter_common_hotels_df_by_ctrip()
    # Refilter_tripadvisor_to_match_ctrip_commons()
    # Refilter_ctrip_unpredicted_by_filtered_tripadvisor()
    # Refilter_ctrip_predicted_by_filtered_tripadvisor()