#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *

# Take note of Date range, number of hotels, number of sentences, pos,neg, price range

##############
### Ctrip_db2 and Tripadvisor: mutual filter date, hotel name, price:

def Experiment_Notes(bin_ver=2, bin_by='price_upper'):
    ### Tripadvisor_date_hotelname_price
    tripad_df_path = "tripadvisor/tripadvisor_db/sentences_depparsed_predicted_english_only_filtered_ctrip_db2_date_hotel-name_price.csv"
    tripad_df = get_Tripadvisor_depparsed_tagged_english_sentences__ctrip_db2_filtered_date_hotel_name_price_df()
    ### Ctrip_db2_hotelname_price
    ctrip_df_path = "ctrip/ctrip_db2/sentences_depparsed_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv"
    ctrip_df = get_Ctrip_db2_depparsed_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_price_df()
    ### Hotel_db
    hotel_df = Common_Hotels_with_price_df()
    ### Number of hotels
    hotel_num = len(hotel_df)
    ### Date range
    ctrip_comments_df = get_Ctrip_db2_comments_df()
    ctrip_comments_df.Date = pandas.to_datetime(ctrip_comments_df.Date)
    ctrip_comments_filtered_df = ctrip_comments_df[ctrip_comments_df["CommentID"].isin(ctrip_df.CommentID.unique())]
    ctrip_dates = ctrip_comments_filtered_df.Date
    ctrip_earliest = ctrip_dates.min()
    ctrip_latest = ctrip_dates.max()
    tripad_df.date = pandas.to_datetime(tripad_df.date)
    tripad_dates = tripad_df.date
    tripad_earliest = tripad_dates.min() 
    tripad_latest = tripad_dates.max() 
    earliest = min(ctrip_earliest,tripad_earliest) 
    latest = max(ctrip_latest,tripad_latest)
    ### Price range
    price_lowest = hotel_df.price_lower.min()
    price_highest = hotel_df.price_upper.max()
    ### Log intros
    log_str = """Experiment After Revision: Split by price ranges
####
Bin version: {}
Bin by: {}
####
Using Ctrip_db2 and Tripadvisor_db mutually filtered by:
    date, so that it's the same time period
    hotel name, so that they're the same hotels
    price, removing any hotels without price data
####
Mutual Filter results:
    Number of Hotels: {}
Date range:
    Earliest: {}
    Latest: {}
Price range:
    Lowest: {}
    Highest: {}

    """.format(bin_ver,
                bin_by,
                hotel_num,
                earliest,
                latest,
                price_lowest,
                price_highest)
    ctrip_str = """
########################
######## Ctrip: ########
########################
Database: Ctrip_db2__mutual_filter_tripadvisor_date_hotel_name
Filepath: {}
    
    """.format(ctrip_df_path)
    tripad_str = """
########################
##### Tripadvisor: #####
########################
Database: Tripadvisor__ctrip_db2_filtered_date_hotel_name
Filepath: {}
    """.format(tripad_df_path)
    ### Load price layers
    pricedict = get_pricelayer_dict(bin_ver=bin_ver)
    price_layers = sorted(pricedict.keys())
    ### Cycle through price layers
    for price_layer in price_layers:
        tripad_df = get_Tripadvisor_depparsed_tagged_english_sentences__ctrip_db2_filtered_date_hotel_name_price_df()
        ctrip_df = get_Ctrip_db2_depparsed_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_price_df()
        price_layer_str = pricedict[price_layer]
        hotel_df = get_hotel_ids_pricelayer(bin_ver=bin_ver, bin_by=bin_by, price_layer=price_layer)
        ctrip_hotel_ids = hotel_df.Ctrip_HotelID
        ctrip_df = ctrip_df[ctrip_df.HotelID.isin(ctrip_hotel_ids)]
        tripad_hotel_ids = hotel_df.tripadvisor_hotel_id
        tripad_df = tripad_df[tripad_df.hotel_id.isin(tripad_hotel_ids)]
        #### Ctrip data
        ctrip_comments_df = get_Ctrip_db2_comments_df()
        ctrip_comments_df.Date = pandas.to_datetime(ctrip_comments_df.Date)
        ctrip_comments_filtered_df = ctrip_comments_df[ctrip_comments_df["CommentID"].isin(ctrip_df.CommentID.unique())]
        ctrip_num_hotels = len(ctrip_df.HotelID.unique())
        ctrip_comment_num = len(ctrip_df.CommentID.unique())
        ctrip_sentence_num = len(ctrip_df) 
        ctrip_sent_pos_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==1]) 
        ctrip_sent_neg_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==0]) 
        ctrip_dates = ctrip_comments_filtered_df.Date
        ctrip_earliest = ctrip_dates.min() 
        ctrip_latest = ctrip_dates.max() 
        ctrip_str += """
    ####
    ### Price Layer: {} Yen
    ##
    Number of hotels: {}
    Number of reviews: {}
    Number of sentences: {}
        Positive sentences: {}
        Negative sentences: {}
    Date range:
        Earliest: {}
        Latest: {}

        """.format(price_layer_str,
            ctrip_num_hotels,
            ctrip_comment_num,
            ctrip_sentence_num,
            ctrip_sent_pos_num,
            ctrip_sent_neg_num,
            ctrip_earliest,
            ctrip_latest)

        #### Tripadvisor data
        tripad_num_hotels = len(tripad_df.hotel_id.unique())
        tripad_comment_num = len(tripad_df.comment_id.unique())
        tripad_sentence_num = len(tripad_df) 
        tripad_sent_pos_num = len(tripad_df[tripad_df["emotion_val"]==1]) 
        tripad_sent_neg_num = len(tripad_df[tripad_df["emotion_val"]==0]) 
        tripad_df.date = pandas.to_datetime(tripad_df.date)
        tripad_dates = tripad_df.date
        tripad_earliest = tripad_dates.min()
        tripad_latest = tripad_dates.max()
        tripad_str += """
    ####
    ### Price Layer: {} Yen
    ##
    Number of hotels: {}
    Number of reviews: {}
    Number of sentences: {}
        Positive sentences: {}
        Negative sentences: {}
    Date range:
        Earliest: {}
        Latest: {}
    
        """.format(price_layer_str,
            tripad_num_hotels,
            tripad_comment_num,
            tripad_sentence_num,
            tripad_sent_pos_num,
            tripad_sent_neg_num,
            tripad_earliest,
            tripad_latest)
    log_str += ctrip_str
    log_str += tripad_str
    log_file = make_log_file("experiment_notes/Experiment_data_notes_exp_after_revision_price_ranges_bin_ver_{}_bin_by_{}.txt".format(bin_ver,bin_by))
    print_STD_log(log_str, log_file)

def main():
    for bin_by in ['price_upper','price_lower']:
        for bin_ver in [2,1]:
            Experiment_Notes(bin_ver=bin_ver, bin_by=bin_by)

if __name__ == '__main__':
    main()

