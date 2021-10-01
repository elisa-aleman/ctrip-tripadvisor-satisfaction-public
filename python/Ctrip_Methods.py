#-*- coding: utf-8 -*-

from Paper3_Methods import *

#######################################
######## Ctrip_db Pandas Paths ########
#######################################

##########################
######## Raw data ########
##########################

###### Hotels
def get_Ctrip_db2_hotels_df():
    data_path = make_data_path("ctrip/ctrip_db2/hotels.csv")
    hotels_df = pandas.read_csv(data_path)
    return hotels_df

###### Comments Raw
def get_Ctrip_db2_comments_df():
    data_path = make_data_path("ctrip/ctrip_db2/comments.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

###### Comments Chinese Only
def get_Ctrip_db2_chinese_comments_df():
    data_path = make_data_path("ctrip/ctrip_db2/comments_zh-cn_chinese_only.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

###### Segmented Comments Chinese Only
def get_Ctrip_db2_chinese_segmented_comments_df():
    data_path = make_data_path("ctrip/ctrip_db2/comments_segmented_zh-cn_chinese_only.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

###### Segmented Sentences Chinese Only
def get_Ctrip_db2_chinese_sentences_df():
    data_path = make_data_path("ctrip/ctrip_db2/sentences_zh-cn_chinese_only.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

###### Segmented Sentences Chinese Only Filtered to match Tripadvisor filter date hotel name, with price data
def get_Ctrip_db2_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_price_df():
    data_path = make_data_path("ctrip/ctrip_db2/sentences_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df


###################################
########### Predictions ###########
###################################

## Z Original experiments with filter and price
## Tagged Filtered Sentences Chinese Only Filtered to match Tripadvisor's filter: date, hotel_name, price

def get_Ctrip_db2_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_price_df():
    data_path = make_data_path("ctrip/ctrip_db2/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

##########################################
########### Dependency_parsing ###########
##########################################

def get_Ctrip_db2_depparsed_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_price_df():
    data_path = make_data_path("ctrip/ctrip_db2/sentences_depparsed_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df


##################################
######## Ctrip SVM Pandas ########
##################################

def get_Ctrip_training_df():
    data_path = make_data_path("ctrip/SVM_training/training_sentences.csv")
    training_df = pandas.read_csv(data_path)
    return training_df

def get_Ctrip_training_data():
    data_path = make_data_path("ctrip/SVM_training/training_sentences.csv")
    training_df = pandas.read_csv(data_path)
    training_data = list(zip(training_df.Sentence, training_df.Positive))
    return training_data

def get_Ctrip_entropies_df():
    data_path = make_data_path("ctrip/SVM_training/entropies.csv")
    entropies_df = pandas.read_csv(data_path)
    return entropies_df

# Personal keyword list loading method
def get_Ctrip_original_selected_keywords():
    com_dictionary = read_dict(make_keyword_path("ctrip/Combined_Keywords_Z_original_p2.75_n3.75.txt"))
    return com_dictionary

# Personal positive keyword list loading method
def get_Ctrip_original_selected_positive_keywords():
    com_dictionary = read_dict(make_keyword_path("ctrip/Z_original_Positive_Keywords_alpha_2.75.txt"))
    return com_dictionary

# Personal negative keyword list loading method
def get_Ctrip_original_selected_negative_keywords():
    com_dictionary = read_dict(make_keyword_path("ctrip/Z_original_Negative_Keywords_alpha_3.75.txt"))
    return com_dictionary

# Personal keyword list translations and values
def get_Ctrip_original_selected_keywords_translations_values_df():
    data_path = make_data_path("ctrip/SVM_training/Combined_Keywords_Z_original_p2.75_n3.75_translations__manually_selected_values.csv")
    com_dict_df =pandas.read_csv(data_path)
    return com_dict_df
    
# Added from 29_subject_keywords.py
def selected_Chinese_subject_keywords(status='general'):
    '''
    # 'NN', 'VA', 'VV','JJ'  
    ignore-->>>'VE+M', 'DT+M', 'NR'
    Basically nouns, verbs and adjectives
    '''
    sel_list = ['NN', 'VA', 'VV','JJ', 'NR']
    manual_keyword_df = get_Ctrip_original_selected_keywords_translations_values_df()
    selected = manual_keyword_df[manual_keyword_df['POS_Tag'].isin(sel_list)]
    if status == 'general':
        selected = selected
    elif status == 'positive':
        selected = selected[selected.KeywordList=='positive']
    elif status == 'negative':
        selected = selected[selected.KeywordList=='negative']
    keywords = selected.Keyword.tolist()
    return keywords

# Added from 29_subject_keywords.py
def selected_Chinese_subject_adjective_keywords(status='general'):
    '''
    # 'VA', 'JJ'
    Basically adjectives in Chinese can be verbs too.
    '''
    sel_list = ['VA','JJ']
    manual_keyword_df = get_Ctrip_original_selected_keywords_translations_values_df()
    selected = manual_keyword_df[manual_keyword_df['POS_Tag'].isin(sel_list)]
    if status == 'general':
        selected = selected
    elif status == 'positive':
        selected = selected[selected.KeywordList=='positive']
    elif status == 'negative':
        selected = selected[selected.KeywordList=='negative']
    keywords = selected.Keyword.tolist()
    return keywords

if __name__ == '__main__':
    pass