#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *

def Refilter_common_hotels_df_by_ctrip():
    ctrip_db_df = get_Ctrip_db2_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_df()
    ctrip_hotel_ids = ctrip_db_df.HotelID.unique()
    common_hotels_path = make_data_path("hotels_in_common_ctrip_db2_tripadvisor.csv")
    common_hotels_df = pandas.read_csv(common_hotels_path)
    common_hotels_df = common_hotels_df[common_hotels_df["Ctrip_HotelID"].isin(ctrip_hotel_ids)]
    common_hotels_df.to_csv(common_hotels_path, index=False)

def Refilter_tripadvisor_to_match_ctrip_commons():
    tagged_path = make_data_path("tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db2_date_hotel-name.csv")
    tagged_df = pandas.read_csv(tagged_path)
    # tagged_df = get_Tripadvisor_tagged_english_sentences__ctrip_db_filtered_date_hotel_name_df() 
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db2_tripadvisor.csv"))
    filtered_df = tagged_df[tagged_df.hotel_id.isin(common_hotels_df.tripadvisor_hotel_id)]
    filtered_df.to_csv(tagged_path, index=False)

if __name__ == '__main__':
    # Refilter_common_hotels_df_by_ctrip()
    # Refilter_tripadvisor_to_match_ctrip_commons()


