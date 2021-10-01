#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *

def Add_English_hotel_name_to_Ctrip_db2():
    ctrip_hotels = get_Ctrip_db2_hotels_df()
    ctrip_hotel_names = ctrip_hotels.HotelName
    ctrip_hotel_names_clean = [name.split("\n")[1] for name in ctrip_hotel_names]
    ctrip_hotels.insert(3,"EnglishHotelName",ctrip_hotel_names_clean)
    ctrip_hotels.to_csv(make_data_path("ctrip/ctrip_db2/hotels.csv"), index=False)

def Make_common_hotels_ctrip_db2_tripadvisor():
    trip_name_df = get_Tripadvisor_english_sentences__ctrip_db2_filtered_date_hotel_name_df()
    hotel_ids = trip_name_df.hotel_id.unique()
    trip_hotels = get_Tripadvisor_hotels_df()
    common_hotels_trip = trip_hotels[trip_hotels.hotel_id.isin(hotel_ids)]
    ctrip_hotels = get_Ctrip_db2_hotels_df()
    ctrip_hotels_filtered = ctrip_hotels[ctrip_hotels.EnglishHotelName.isin(common_hotels_trip.hotel_name)]
    name_to_trip_id_dict = dict(zip(common_hotels_trip.hotel_name,common_hotels_trip.hotel_id))
    trip_ids_ctrip = [name_to_trip_id_dict[name] for name in ctrip_hotels_filtered.EnglishHotelName]
    ctrip_hotels_filtered.insert(6,"tripadvisor_hotel_id",trip_ids_ctrip)
    common_hotels_trip.rename(columns={"hotel_id":"tripadvisor_hotel_id"}, inplace=True)
    common_hotels_df = pandas.merge(ctrip_hotels_filtered, common_hotels_trip, on="tripadvisor_hotel_id")
    common_hotels_df.rename(columns={"HotelID":"Ctrip_HotelID"},inplace=True)
    common_hotels_df.to_csv(make_data_path("hotels_in_common_ctrip_db2_tripadvisor.csv"),index=False)


def Filter_ctrip2_by_filtered_tripadvisor():
    common_hotels_df = pandas.read_csv(make_data_path("hotels_in_common_ctrip_db2_tripadvisor.csv"))
    ctrip_df = get_Ctrip_db2_chinese_sentences_df()
    filtered = ctrip_df[ctrip_df.HotelID.isin(common_hotels_df.Ctrip_HotelID)]
    filtered_path = make_data_path("ctrip/ctrip_db2/sentences_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv")
    filtered.to_csv(filtered_path,index=False)


if __name__ == '__main__':
    # Add_English_hotel_name_to_Ctrip_db2()
    # Make_common_hotels_ctrip_db2_tripadvisor()
    # Filter_ctrip2_by_filtered_tripadvisor()