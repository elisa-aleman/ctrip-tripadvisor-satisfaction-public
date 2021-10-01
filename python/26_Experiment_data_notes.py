#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *

# Take note of Date range, number of hotels, number of sentences, pos,neg, price range


##########################
# Ctrip_db
##########################

##############
### Ctrip_db_hotelname__and__Tripadvisor_date_hotelname():

def Ctrip_db_hotelname__and__Tripadvisor_date_hotelname():
    # Ctrip_db_hotelname
    ctrip_df_path = "ctrip/ctrip_db/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv"
    ctrip_df = get_Ctrip_db_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_df()
    ####
    ctrip_sentence_num = len(ctrip_df)
    ctrip_sent_pos_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==1])
    ctrip_sent_neg_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==0])
    ctrip_num_hotels = len(ctrip_df.HotelID.unique())
    ctrip_comments_df = get_Ctrip_db_comments_df()
    ctrip_comments_df.Date = pandas.to_datetime(ctrip_comments_df.Date)
    ctrip_comments_filtered_df = ctrip_comments_df[ctrip_comments_df["CommentID"].isin(ctrip_df.CommentID.unique())]
    ctrip_dates = ctrip_comments_filtered_df.Date
    ctrip_earliest = ctrip_dates.min()
    ctrip_latest = ctrip_dates.max()
    # Tripadvisor_date_hotelname
    tripad_df_path = "tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db_date_hotel-name.csv"
    tripad_df = get_Tripadvisor_tagged_english_sentences__ctrip_db_filtered_date_hotel_name_df()
    ####
    tripad_sentence_num = len(tripad_df) 
    tripad_sent_pos_num = len(tripad_df[tripad_df["emotion_val"]==1]) 
    tripad_sent_neg_num = len(tripad_df[tripad_df["emotion_val"]==0]) 
    tripad_num_hotels = len(tripad_df.hotel_id.unique()) 
    tripad_df.date = pandas.to_datetime(tripad_df.date)
    tripad_dates = tripad_df.date
    tripad_earliest = tripad_dates.min() 
    tripad_latest = tripad_dates.max() 
    earliest = min(ctrip_earliest,tripad_earliest) 
    latest = max(ctrip_latest,tripad_latest) 
    #### Log
    log_str = """Experiment 1:
    Ctrip_db_hotelname__and__Tripadvisor_date_hotelname
    ###########
    ## Ctrip:
    ##
    Database: Ctrip_db__mutual_filter_tripadvisor_date_hotel_name
    Filepath: {0}
    Number of hotels: {1}
    Number of sentences: {2}
    Number of positive sentences: {3}
    Number of negative sentences: {4}
    Date range:
        Earliest: {5}
        Latest: {6}

    ###########
    ## Tripadvisor:
    ##
    Database: Tripadvisor__ctrip_db_filtered_date_hotel_name
    Filepath: {7}
    Number of hotels: {8}
    Number of sentences: {9}
    Number of positive sentences: {10}
    Number of negative sentences: {11}
    Date range:
        Earliest: {12}
        Latest: {13}
    ######
    General date range of experiment:
        Earliest: {14}
        Latest: {15}
    """.format(ctrip_df_path,
        ctrip_num_hotels,
        ctrip_sentence_num,
        ctrip_sent_pos_num,
        ctrip_sent_neg_num,
        str(ctrip_earliest).split()[0],
        str(ctrip_latest).split()[0],
        tripad_df_path,
        tripad_num_hotels,
        tripad_sentence_num,
        tripad_sent_pos_num,
        tripad_sent_neg_num,
        str(tripad_earliest).split()[0],
        str(tripad_latest).split()[0],
        str(earliest).split()[0],
        str(latest).split()[0])
    log_file = make_log_file("Experiment_data_notes_exp_1_Ctrip_db_hotelname__and__Tripadvisor_date_hotelname.txt")
    print_STD_log(log_str, log_file)

##############
### Ctrip_db__and__Tripadvisor_date_hotelprice():

def Ctrip_db__and__Tripadvisor_date_hotelprice():
    # Ctrip_db
    ctrip_df_path = "ctrip/ctrip_db/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only.csv"
    ctrip_df = get_Ctrip_db_tagged_z_original_chinese_sentences_df()
    ####
    ctrip_sentence_num = len(ctrip_df) 
    ctrip_sent_pos_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==1]) 
    ctrip_sent_neg_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==0])

    ctrip_num_hotels = len(ctrip_df.HotelID.unique()) 
    ctrip_comments_df = get_Ctrip_db_comments_df()
    ctrip_comments_df.Date = pandas.to_datetime(ctrip_comments_df.Date)
    ctrip_comments_filtered_df = ctrip_comments_df[ctrip_comments_df["CommentID"].isin(ctrip_df.CommentID.unique())]
    ctrip_dates = ctrip_comments_filtered_df.Date
    ctrip_earliest = ctrip_dates.min() 
    ctrip_latest = ctrip_dates.max() 
    # Tripadvisor_date_hotelprice
    tripad_df_path = "tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db_date_hotel-price.csv"
    tripad_df = get_Tripadvisor_tagged_english_sentences__ctrip_db_filtered_date_hotel_price_df()
    ####
    tripad_sentence_num = len(tripad_df) 
    tripad_sent_pos_num = len(tripad_df[tripad_df["emotion_val"]==1]) 
    tripad_sent_neg_num = len(tripad_df[tripad_df["emotion_val"]==0]) 
    tripad_num_hotels = len(tripad_df.hotel_id.unique()) 
    tripad_df.date = pandas.to_datetime(tripad_df.date)
    tripad_dates = tripad_df.date
    tripad_earliest = tripad_dates.min() 
    tripad_latest = tripad_dates.max() 
    earliest = min(ctrip_earliest,tripad_earliest) 
    latest = max(ctrip_latest,tripad_latest) 
    #### Log
    log_str = """Experiment 2:
    Ctrip_db__and__Tripadvisor_date_hotelprice
    ###########
    ## Ctrip:
    ##
    Database: Ctrip_db
    Filepath: {0}
    Number of hotels: {1}
    Number of sentences: {2}
    Number of positive sentences: {3}
    Number of negative sentences: {4}
    Date range:
        Earliest: {5}
        Latest: {6}

    ###########
    ## Tripadvisor:
    ##
    Database: Tripadvisor__ctrip_db_filtered_date_hotel_price
    Filepath: {7}
    Number of hotels: {8}
    Number of sentences: {9}
    Number of positive sentences: {10}
    Number of negative sentences: {11}
    Date range:
        Earliest: {12}
        Latest: {13}
    ######
    General date range of experiment:
        Earliest: {14}
        Latest: {15}
    """.format(ctrip_df_path,
        ctrip_num_hotels,
        ctrip_sentence_num,
        ctrip_sent_pos_num,
        ctrip_sent_neg_num,
        str(ctrip_earliest).split()[0],
        str(ctrip_latest).split()[0],
        tripad_df_path,
        tripad_num_hotels,
        tripad_sentence_num,
        tripad_sent_pos_num,
        tripad_sent_neg_num,
        str(tripad_earliest).split()[0],
        str(tripad_latest).split()[0],
        str(earliest).split()[0],
        str(latest).split()[0])
    log_file = make_log_file("Experiment_data_notes_exp_2_Ctrip_db__and__Tripadvisor_date_hotelprice.txt")
    print_STD_log(log_str, log_file)


##########################
# Ctrip_db2
##########################

##############
### Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname():

def Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname():
    # Ctrip_db2_hotelname
    ctrip_df_path = "ctrip/ctrip_db2/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv"
    ctrip_df = get_Ctrip_db2_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_df()
    ####
    ctrip_sentence_num = len(ctrip_df) 
    ctrip_sent_pos_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==1]) 
    ctrip_sent_neg_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==0]) 
    ctrip_num_hotels = len(ctrip_df.HotelID.unique()) 
    ctrip_comments_df = get_Ctrip_db2_comments_df()
    ctrip_comments_df.Date = pandas.to_datetime(ctrip_comments_df.Date)
    ctrip_comments_filtered_df = ctrip_comments_df[ctrip_comments_df["CommentID"].isin(ctrip_df.CommentID.unique())]
    ctrip_dates = ctrip_comments_filtered_df.Date
    ctrip_earliest = ctrip_dates.min() 
    ctrip_latest = ctrip_dates.max() 
    # Tripadvisor_date_hotelname
    tripad_df_path = "tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db2_date_hotel-name.csv"
    tripad_df = get_Tripadvisor_tagged_english_sentences__ctrip_db2_filtered_date_hotel_name_df()
    ####
    tripad_sentence_num = len(tripad_df) 
    tripad_sent_pos_num = len(tripad_df[tripad_df["emotion_val"]==1]) 
    tripad_sent_neg_num = len(tripad_df[tripad_df["emotion_val"]==0]) 
    tripad_num_hotels = len(tripad_df.hotel_id.unique()) 
    tripad_df.date = pandas.to_datetime(tripad_df.date)
    tripad_dates = tripad_df.date
    tripad_earliest = tripad_dates.min() 
    tripad_latest = tripad_dates.max() 
    earliest = min(ctrip_earliest,tripad_earliest) 
    latest = max(ctrip_latest,tripad_latest) 
    #### Log
    log_str = """Experiment 3:
    Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname
    ###########
    ## Ctrip:
    ##
    Database: Ctrip_db2__mutual_filter_tripadvisor_date_hotel_name
    Filepath: {0}
    Number of hotels: {1}
    Number of sentences: {2}
    Number of positive sentences: {3}
    Number of negative sentences: {4}
    Date range:
        Earliest: {5}
        Latest: {6}

    ###########
    ## Tripadvisor:
    ##
    Database: Tripadvisor__ctrip_db2_filtered_date_hotel_name
    Filepath: {7}
    Number of hotels: {8}
    Number of sentences: {9}
    Number of positive sentences: {10}
    Number of negative sentences: {11}
    Date range:
        Earliest: {12}
        Latest: {13}
    ######
    General date range of experiment:
        Earliest: {14}
        Latest: {15}
    """.format(ctrip_df_path,
        ctrip_num_hotels,
        ctrip_sentence_num,
        ctrip_sent_pos_num,
        ctrip_sent_neg_num,
        str(ctrip_earliest).split()[0],
        str(ctrip_latest).split()[0],
        tripad_df_path,
        tripad_num_hotels,
        tripad_sentence_num,
        tripad_sent_pos_num,
        tripad_sent_neg_num,
        str(tripad_earliest).split()[0],
        str(tripad_latest).split()[0],
        str(earliest).split()[0],
        str(latest).split()[0])
    log_file = make_log_file("Experiment_data_notes_exp_3_Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname.txt")
    print_STD_log(log_str, log_file)

##############
### Ctrip_db2__and__Tripadvisor_date_hotelprice():

def Ctrip_db2__and__Tripadvisor_date_hotelprice():
    # Ctrip_db2
    ctrip_df_path = "ctrip/ctrip_db2/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only.csv"
    ctrip_df = get_Ctrip_db2_tagged_z_original_chinese_sentences_df()
    ####
    ctrip_sentence_num = len(ctrip_df) 
    ctrip_sent_pos_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==1]) 
    ctrip_sent_neg_num = len(ctrip_df[ctrip_df["Positive_Prediction"]==0]) 
    ctrip_num_hotels = len(ctrip_df.HotelID.unique()) 
    ctrip_comments_df = get_Ctrip_db2_comments_df()
    ctrip_comments_df.Date = pandas.to_datetime(ctrip_comments_df.Date)
    ctrip_comments_filtered_df = ctrip_comments_df[ctrip_comments_df["CommentID"].isin(ctrip_df.CommentID.unique())]
    ctrip_dates = ctrip_comments_filtered_df.Date
    ctrip_earliest = ctrip_dates.min() 
    ctrip_latest = ctrip_dates.max() 
    # Tripadvisor_date_hotelprice
    tripad_df_path = "tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db2_date_hotel-price.csv"
    tripad_df = get_Tripadvisor_tagged_english_sentences__ctrip_db2_filtered_date_hotel_price_df()
    ####
    tripad_sentence_num = len(tripad_df) 
    tripad_sent_pos_num = len(tripad_df[tripad_df["emotion_val"]==1]) 
    tripad_sent_neg_num = len(tripad_df[tripad_df["emotion_val"]==0]) 
    tripad_num_hotels = len(tripad_df.hotel_id.unique()) 
    tripad_df.date = pandas.to_datetime(tripad_df.date)
    tripad_dates = tripad_df.date
    tripad_earliest = tripad_dates.min() 
    tripad_latest = tripad_dates.max() 
    earliest = min(ctrip_earliest,tripad_earliest) 
    latest = max(ctrip_latest,tripad_latest) 
    #### Log
    log_str = """Experiment 4:
    Ctrip_db2__and__Tripadvisor_date_hotelprice
    ###########
    ## Ctrip:
    ##
    Database: Ctrip_db2
    Filepath: {0}
    Number of hotels: {1}
    Number of sentences: {2}
    Number of positive sentences: {3}
    Number of negative sentences: {4}
    Date range:
        Earliest: {5}
        Latest: {6}

    ###########
    ## Tripadvisor:
    ##
    Database: Tripadvisor__ctrip_db2_filtered_date_hotel_price
    Filepath: {7}
    Number of hotels: {8}
    Number of sentences: {9}
    Number of positive sentences: {10}
    Number of negative sentences: {11}
    Date range:
        Earliest: {12}
        Latest: {13}
    ######
    General date range of experiment:
        Earliest: {14}
        Latest: {15}
    """.format(ctrip_df_path,
        ctrip_num_hotels,
        ctrip_sentence_num,
        ctrip_sent_pos_num,
        ctrip_sent_neg_num,
        str(ctrip_earliest).split()[0],
        str(ctrip_latest).split()[0],
        tripad_df_path,
        tripad_num_hotels,
        tripad_sentence_num,
        tripad_sent_pos_num,
        tripad_sent_neg_num,
        str(tripad_earliest).split()[0],
        str(tripad_latest).split()[0],
        str(earliest).split()[0],
        str(latest).split()[0])
    log_file = make_log_file("Experiment_data_notes_exp_4_Ctrip_db2__and__Tripadvisor_date_hotelprice.txt")
    print_STD_log(log_str, log_file)

def main():
    Ctrip_db_hotelname__and__Tripadvisor_date_hotelname()
    Ctrip_db__and__Tripadvisor_date_hotelprice()
    Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname()
    Ctrip_db2__and__Tripadvisor_date_hotelprice()

if __name__ == '__main__':
    main()
    