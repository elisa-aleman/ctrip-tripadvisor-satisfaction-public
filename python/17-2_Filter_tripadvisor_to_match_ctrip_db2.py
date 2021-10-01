#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *

def get_Ctrip_db2_date_range():
    ctrip_df = get_Ctrip_db2_comments_df()
    dates = pandas.to_datetime(ctrip_df.Date)
    earliest = dates.min()
    latest = dates.max()
    return earliest,latest

def filter_Tripadvisor_by_Ctrip_db2_date():
    earliest,latest = get_Ctrip_db2_date_range()
    trip_df = get_Tripadvisor_english_sentences_df()
    trip_df.date = pandas.to_datetime(trip_df.date)
    filtered_trip = trip_df[(trip_df.date<=latest) & (trip_df.date>=earliest)]
    filtered_path = make_data_path("tripadvisor/tripadvisor_db/sentences_english_only_filtered_ctrip_db2_date.csv")
    filtered_trip.to_csv(filtered_path, index=False)

def filter_Tripadvisor_by_Ctrip_db2_date_hotel_name():
    ctrip_hotels = get_Ctrip_db2_hotels_df()
    ctrip_hotel_names = ctrip_hotels.HotelName
    trip_hotels = get_Tripadvisor_hotels_df()
    ctrip_hotel_names_clean = [name.split("\n")[1] for name in ctrip_hotel_names]
    filtered_trip_hotels_by_name = trip_hotels[trip_hotels.hotel_name.isin(ctrip_hotel_names_clean)]
    # Load sentences
    sentences_path = make_data_path("tripadvisor/tripadvisor_db/sentences_english_only_filtered_ctrip_db2_date.csv")
    sentences_trip = pandas.read_csv(sentences_path)
    filtered = sentences_trip[sentences_trip.hotel_id.isin(filtered_trip_hotels_by_name.hotel_id)]
    filtered_path = make_data_path("tripadvisor/tripadvisor_db/sentences_english_only_filtered_ctrip_db2_date_hotel-name.csv")
    filtered.to_csv(filtered_path,index=False)

def filter_Tripadvisor_by_Ctrip_db2_date_hotel_price():
    ctrip_hotels = get_Ctrip_db2_hotels_df()
    ctrip_hotel_prices = ctrip_hotels.HotelPrice
    min_price = ctrip_hotel_prices.min()
    max_price = ctrip_hotel_prices.max()
    trip_hotels = get_Tripadvisor_hotels_df()
    trip_hotels.price_lower = pandas.to_numeric(trip_hotels.price_lower, errors="coerce")
    trip_hotels.price_upper = pandas.to_numeric(trip_hotels.price_upper, errors="coerce")
    filtered_trip_hotels_by_price = trip_hotels[(trip_hotels.price_lower>=min_price) & (trip_hotels.price_upper<=max_price)]
    # Load sentences
    sentences_path = make_data_path("tripadvisor/tripadvisor_db/sentences_english_only_filtered_ctrip_db2_date.csv")
    sentences_trip = pandas.read_csv(sentences_path)
    filtered = sentences_trip[sentences_trip.hotel_id.isin(filtered_trip_hotels_by_price.hotel_id)]
    filtered_path = make_data_path("tripadvisor/tripadvisor_db/sentences_english_only_filtered_ctrip_db2_date_hotel-price.csv")
    filtered.to_csv(filtered_path,index=False)


if __name__ == '__main__':
    # filter_Tripadvisor_by_Ctrip_db2_date()
    # filter_Tripadvisor_by_Ctrip_db2_date_hotel_name()
    # filter_Tripadvisor_by_Ctrip_db2_date_hotel_price()