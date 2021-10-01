#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *

###############################
########### Chinese ###########
###############################

def get_Chinese_frequencies_positive_df(freq_df):
    # freq_df.columns = 
    # Keyword, Emotion List, Positive Absolute Frequency,
    #    Positive Relative Frequency, Positive Probability per sentence,
    #    Negative Absolute Frequency, Negative Relative Frequency,
    #    Negative Probability per sentence
    # Insert translations to english
    translation_df = get_Ctrip_original_selected_keywords_translations_values_df()
    # Keyword,Translation,KeywordList,WordValue
    translation_dict = dict(zip(translation_df.Keyword,translation_df.Translation))
    freq_df["Translation"] = [translation_dict[key] for key in freq_df.Keyword]
    # Filter to keep positives
    freqs_positive = freq_df[freq_df["Emotion List"]=="Positive"]
    # Filter out grammatical words, keep subject words
    freqs_positive = freqs_positive[freqs_positive["Keyword"].isin(translation_df[translation_df["WordValue"]=="subject"]["Keyword"])]
    # Keep only relevant columns
    freqs_positive = freqs_positive[["Keyword","Translation","Positive Absolute Frequency","Positive Relative Frequency", "Positive Probability per sentence"]]
    # Sort by relevant column
    freqs_positive.sort_values(by=["Positive Absolute Frequency"], ascending=False,inplace=True)
    return freqs_positive

    
def get_Chinese_frequencies_negative_df(freq_df):
    # freq_df.columns = 
    # Keyword, Emotion List, Positive Absolute Frequency,
    #    Positive Relative Frequency, Positive Probability per sentence,
    #    Negative Absolute Frequency, Negative Relative Frequency,
    #    Negative Probability per sentence
    # Insert translations to english
    translation_df = get_Ctrip_original_selected_keywords_translations_values_df()
    # Keyword,Translation,KeywordList,WordValue
    translation_dict = dict(zip(translation_df.Keyword,translation_df.Translation))
    freq_df["Translation"] = [translation_dict[key] for key in freq_df.Keyword]
    # Filter to keep negatives
    freqs_negative = freq_df[freq_df["Emotion List"]=="Negative"]
    # Filter out grammatical words, keep subject words
    freqs_negative = freqs_negative[freqs_negative["Keyword"].isin(translation_df[translation_df["WordValue"]=="subject"]["Keyword"])]
    # Keep only translation and frequency
    freqs_negative = freqs_negative[["Keyword","Translation","Negative Absolute Frequency", "Negative Relative Frequency", "Negative Probability per sentence"]]
    # Sort by relevant column
    freqs_negative.sort_values(by=["Negative Absolute Frequency"], ascending=False,inplace=True)
    return freqs_negative

###############################
########### English ###########
###############################

def get_English_frequencies_positive_df(freq_df):
    # freq_df.columns = 
    # Keyword, Emotion List, Positive Absolute Frequency,
    #    Positive Relative Frequency, Positive Probability per sentence,
    #    Negative Absolute Frequency, Negative Relative Frequency,
    #    Negative Probability per sentence
    # Check for word value
    values_df = get_Tripadvisor_original_selected_keywords_values_df()
    # Keyword,KeywordList,WordValue
    # Filter to keep positives
    freqs_positive = freq_df[freq_df["Emotion List"]=="Positive"]
    # Filter out grammatical words, keep subject words
    freqs_positive = freqs_positive[freqs_positive["Keyword"].isin(values_df[values_df["WordValue"]=="subject"]["Keyword"])]
    # Keep only keyword and frequency
    freqs_positive = freqs_positive[["Keyword","Positive Absolute Frequency","Positive Relative Frequency", "Positive Probability per sentence"]]
    # Sort by relevant column
    freqs_positive.sort_values(by=["Positive Absolute Frequency"], ascending=False,inplace=True)
    return freqs_positive


def get_English_frequencies_negative_df(freq_df):
    # freq_df.columns = 
    # Keyword, Emotion List, Positive Absolute Frequency,
    #    Positive Relative Frequency, Positive Probability per sentence,
    #    Negative Absolute Frequency, Negative Relative Frequency,
    #    Negative Probability per sentence
    # Check for word value
    values_df = get_Tripadvisor_original_selected_keywords_values_df()
    # Keyword,KeywordList,WordValue
    # Filter to keep negatives
    freqs_negative = freq_df[freq_df["Emotion List"]=="Negative"]
    # Filter out grammatical words, keep subject words
    freqs_negative = freqs_negative[freqs_negative["Keyword"].isin(values_df[values_df["WordValue"]=="subject"]["Keyword"])]
    # Keep only keyword and frequency
    freqs_negative = freqs_negative[["Keyword","Negative Absolute Frequency", "Negative Relative Frequency", "Negative Probability per sentence"]]
    # Sort by relevant column
    freqs_negative.sort_values(by=["Negative Absolute Frequency"], ascending=False,inplace=True)
    return freqs_negative

############################
########### Main ###########
############################

##########################
# Ctrip_db
##########################

##############
### Ctrip_db_hotelname__and__Tripadvisor_date_hotelname

def Ctrip_db_hotelname__and__Tripadvisor_date_hotelname():
    # Chinese
    ctrip_freq_df = get_Ctrip_db_keyword_frequencies_z_original__mutual_filter_tripadvisor_date_hotel_name_df()
    ctrip_pos_freq_df = get_Chinese_frequencies_positive_df(ctrip_freq_df)
    ctrip_pos_freq_path = make_data_path("ctrip/ctrip_db/keyword_subject_positive_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv")
    ctrip_pos_freq_df.to_csv(ctrip_pos_freq_path,index=False)
    ctrip_neg_freq_df = get_Chinese_frequencies_negative_df(ctrip_freq_df)
    ctrip_neg_freq_path = make_data_path("ctrip/ctrip_db/keyword_subject_negative_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv")
    ctrip_neg_freq_df.to_csv(ctrip_neg_freq_path,index=False)
    # English    
    tripad_freq_df = get_Tripadvisor_keyword_frequencies_z_original__ctrip_db_filtered_date_hotel_name_df()
    tripad_pos_freq_df = get_English_frequencies_positive_df(tripad_freq_df)
    tripad_pos_freq_path = make_data_path("tripadvisor/tripadvisor_db/keyword_subject_positive_frequencies_Combined_Keywords_z_original_p1.5_n4.25_english_only_filtered_ctrip_db_date_hotel-name.csv")
    tripad_pos_freq_df.to_csv(tripad_pos_freq_path,index=False)
    tripad_neg_freq_df = get_English_frequencies_negative_df(tripad_freq_df)
    tripad_neg_freq_path = make_data_path("tripadvisor/tripadvisor_db/keyword_subject_negative_frequencies_Combined_Keywords_z_original_p1.5_n4.25_english_only_filtered_ctrip_db_date_hotel-name.csv")
    tripad_neg_freq_df.to_csv(tripad_neg_freq_path,index=False)


##############
### Ctrip_db__and__Tripadvisor_date_hotelprice

def Ctrip_db__and__Tripadvisor_date_hotelprice():
    # Chinese
    ctrip_freq_df = get_Ctrip_db_keyword_frequencies_z_original_df()
    ctrip_pos_freq_df = get_Chinese_frequencies_positive_df(ctrip_freq_df)
    ctrip_pos_freq_path = make_data_path("ctrip/ctrip_db/keyword_subject_positive_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only.csv")
    ctrip_pos_freq_df.to_csv(ctrip_pos_freq_path,index=False)
    ctrip_neg_freq_df = get_Chinese_frequencies_negative_df(ctrip_freq_df)
    ctrip_neg_freq_path = make_data_path("ctrip/ctrip_db/keyword_subject_negative_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only.csv")
    ctrip_neg_freq_df.to_csv(ctrip_neg_freq_path,index=False)
    # English
    tripad_freq_df = get_Tripadvisor_keyword_frequencies_z_original__ctrip_db_filtered_date_hotel_price_df()
    tripad_pos_freq_df = get_English_frequencies_positive_df(tripad_freq_df)
    tripad_pos_freq_path = make_data_path("tripadvisor/tripadvisor_db/keyword_subject_positive_frequencies_Combined_Keywords_z_original_p1.5_n4.25_english_only_filtered_ctrip_db_date_hotel-price.csv")
    tripad_pos_freq_df.to_csv(tripad_pos_freq_path,index=False)
    tripad_neg_freq_df = get_English_frequencies_negative_df(tripad_freq_df)
    tripad_neg_freq_path = make_data_path("tripadvisor/tripadvisor_db/keyword_subject_negative_frequencies_Combined_Keywords_z_original_p1.5_n4.25_english_only_filtered_ctrip_db_date_hotel-price.csv")
    tripad_neg_freq_df.to_csv(tripad_neg_freq_path,index=False)

##########################
# Ctrip_db2
##########################

##############
### Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname

def Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname():
    # Chinese
    ctrip_freq_df = get_Ctrip_db2_keyword_frequencies_z_original__mutual_filter_tripadvisor_date_hotel_name_df()
    ctrip_pos_freq_df = get_Chinese_frequencies_positive_df(ctrip_freq_df)
    ctrip_pos_freq_path = make_data_path("ctrip/ctrip_db2/keyword_subject_positive_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv")
    ctrip_pos_freq_df.to_csv(ctrip_pos_freq_path,index=False)
    ctrip_neg_freq_df = get_Chinese_frequencies_negative_df(ctrip_freq_df)
    ctrip_neg_freq_path = make_data_path("ctrip/ctrip_db2/keyword_subject_negative_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv")
    ctrip_neg_freq_df.to_csv(ctrip_neg_freq_path,index=False)
    # English
    tripad_freq_df = get_Tripadvisor_keyword_frequencies_z_original__ctrip_db2_filtered_date_hotel_name_df()
    tripad_pos_freq_df = get_English_frequencies_positive_df(tripad_freq_df)
    tripad_pos_freq_path = make_data_path("tripadvisor/tripadvisor_db/keyword_subject_positive_frequencies_Combined_Keywords_z_original_p1.5_n4.25_english_only_filtered_ctrip_db2_date_hotel-name.csv")
    tripad_pos_freq_df.to_csv(tripad_pos_freq_path,index=False)
    tripad_neg_freq_df = get_English_frequencies_negative_df(tripad_freq_df)
    tripad_neg_freq_path = make_data_path("tripadvisor/tripadvisor_db/keyword_subject_negative_frequencies_Combined_Keywords_z_original_p1.5_n4.25_english_only_filtered_ctrip_db2_date_hotel-name.csv")
    tripad_neg_freq_df.to_csv(tripad_neg_freq_path,index=False)
    

##############
### Ctrip_db2__and__Tripadvisor_date_hotelprice

def Ctrip_db2__and__Tripadvisor_date_hotelprice():
    # Chinese
    ctrip_freq_df = get_Ctrip_db2_keyword_frequencies_z_original_df()
    ctrip_pos_freq_df = get_Chinese_frequencies_positive_df(ctrip_freq_df)
    ctrip_pos_freq_path = make_data_path("ctrip/ctrip_db2/keyword_subject_positive_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only.csv")
    ctrip_pos_freq_df.to_csv(ctrip_pos_freq_path,index=False)
    ctrip_neg_freq_df = get_Chinese_frequencies_negative_df(ctrip_freq_df)
    ctrip_neg_freq_path = make_data_path("ctrip/ctrip_db2/keyword_subject_negative_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only.csv")
    ctrip_neg_freq_df.to_csv(ctrip_neg_freq_path,index=False)
    # English
    tripad_freq_df = get_Tripadvisor_keyword_frequencies_z_original__ctrip_db2_filtered_date_hotel_price_df()
    tripad_pos_freq_df = get_English_frequencies_positive_df(tripad_freq_df)
    tripad_pos_freq_path = make_data_path("tripadvisor/tripadvisor_db/keyword_subject_positive_frequencies_Combined_Keywords_z_original_p1.5_n4.25_english_only_filtered_ctrip_db2_date_hotel-price.csv")
    tripad_pos_freq_df.to_csv(tripad_pos_freq_path,index=False)
    tripad_neg_freq_df = get_English_frequencies_negative_df(tripad_freq_df)
    tripad_neg_freq_path = make_data_path("tripadvisor/tripadvisor_db/keyword_subject_negative_frequencies_Combined_Keywords_z_original_p1.5_n4.25_english_only_filtered_ctrip_db2_date_hotel-price.csv")
    tripad_neg_freq_df.to_csv(tripad_neg_freq_path,index=False)
    
def main():
    Ctrip_db_hotelname__and__Tripadvisor_date_hotelname()
    Ctrip_db__and__Tripadvisor_date_hotelprice()
    Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname()
    Ctrip_db2__and__Tripadvisor_date_hotelprice()

if __name__ == '__main__':
    main()