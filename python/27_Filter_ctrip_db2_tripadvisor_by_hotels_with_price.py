#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *

# Since we chose Experiment 3, We're no longer updating Ctrip_db, only ctrip_db2
# We got a major revision and our goal is to split the hotels by price layers, so we need hotels with price data
# Hotels without price_lower data get removed
# We don't need to predict again with SVM, just filter
# We need to split and recount frequencies
# We need to consider adjectives
# Basically, start repeating from files 22, 23, 24, 25, 26, but with also price layers

def Remove_no_price_from_common_hotels_ctrip_db2_tripadvisor():
    common_hotels = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db2_tripadvisor.csv")) #580 rows
    filtered = common_hotels[common_hotels["price_lower"].notnull()] #557 rows
    filtered_path = make_data_path("hotels_in_common_ctrip_db2_tripadvisor__with_price_data.csv")
    filtered.to_csv(filtered_path,index=False)

#######
# ctrip_db2

# Also filter original comments, before segmentation, for the sentence grammar parsing?
# Not necessary, parser can handle single sentences with a property to avoid segmenting it further.

def Filter_ctrip2_by_common_hotels():
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db2_tripadvisor__with_price_data.csv"))
    ctrip_df = get_Ctrip_db2_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_df() #105076
    filtered = ctrip_df[ctrip_df.HotelID.isin(common_hotels_df.Ctrip_HotelID)] #101963
    filtered_path = make_data_path("ctrip/ctrip_db2/sentences_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv")
    filtered.to_csv(filtered_path,index=False)

def Filter_ctrip2_predicted_by_common_hotels():
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db2_tripadvisor__with_price_data.csv"))
    ctrip_df = get_Ctrip_db2_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_df() #105076
    filtered = ctrip_df[ctrip_df.HotelID.isin(common_hotels_df.Ctrip_HotelID)] #101963
    filtered_path = make_data_path("ctrip/ctrip_db2/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv")
    filtered.to_csv(filtered_path,index=False)

########
# tripadvisor

def Filter_tripadvisor_predicted_by_common_hotels():
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db2_tripadvisor__with_price_data.csv"))
    tripad_df = get_Tripadvisor_english_sentences__ctrip_db2_filtered_date_hotel_name_df() #363332
    filtered = tripad_df[tripad_df.hotel_id.isin(common_hotels_df.tripadvisor_hotel_id)] #348039
    filtered_path = make_data_path("tripadvisor/tripadvisor_db/sentences_english_only_filtered_ctrip_db2_date_hotel-name_price.csv")
    filtered.to_csv(filtered_path,index=False)

def Filter_tripadvisor_predicted_by_common_hotels():
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db2_tripadvisor__with_price_data.csv"))
    tripad_df = get_Tripadvisor_tagged_english_sentences__ctrip_db2_filtered_date_hotel_name_df() #352022
    filtered = tripad_df[tripad_df.hotel_id.isin(common_hotels_df.tripadvisor_hotel_id)] #348039
    filtered_path = make_data_path("tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db2_date_hotel-name_price.csv")
    filtered.to_csv(filtered_path,index=False)


if __name__ == '__main__':
    # Remove_no_price_from_common_hotels_ctrip_db2_tripadvisor()
    # Filter_ctrip2_by_common_hotels()
    # Filter_ctrip2_predicted_by_common_hotels()
    # Filter_tripadvisor_predicted_by_common_hotels()
    # Filter_tripadvisor_predicted_by_common_hotels()
