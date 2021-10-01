#-*- coding: utf-8 -*-

from Paper3_Methods import *

##########################################
######## Tripadvisor Pandas Paths ########
##########################################

##########################
######## Raw data ########
##########################

###### Hotels
def get_Tripadvisor_hotels_df():
    data_path = make_data_path("tripadvisor/tripadvisor_db/hotels.csv")
    hotels_df = pandas.read_csv(data_path)
    return hotels_df

###### Comments Raw
def get_Tripadvisor_comments_df():
    data_path = make_data_path("tripadvisor/tripadvisor_db/comments.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

###### Comments English Only
def get_Tripadvisor_english_comments_df():
    data_path = make_data_path("tripadvisor/tripadvisor_db/comments_english_only.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

###### Sentences English Only
def get_Tripadvisor_english_sentences_df():
    data_path = make_data_path("tripadvisor/tripadvisor_db/sentences_english_only.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

###### Sentences English Only Ctrip_db2 Filtered Date and Hotel Name with Price data
def get_Tripadvisor_english_sentences__ctrip_db2_filtered_date_hotel_name_price_df():
    data_path = make_data_path("tripadvisor/tripadvisor_db/sentences_english_only_filtered_ctrip_db2_date_hotel-name_price.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

###################################
########### Predictions ###########
###################################

###### Tagged Sentences English Only Ctrip_db2 Filtered Date and Hotel Name with Price Data
def get_Tripadvisor_tagged_english_sentences__ctrip_db2_filtered_date_hotel_name_price_df():
    data_path = make_data_path("tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db2_date_hotel-name_price.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df

##########################################
########### Dependency_parsing ###########
##########################################

def get_Tripadvisor_depparsed_tagged_english_sentences__ctrip_db2_filtered_date_hotel_name_price_df():
    data_path = make_data_path("tripadvisor/tripadvisor_db/sentences_depparsed_predicted_english_only_filtered_ctrip_db2_date_hotel-name_price.csv")
    comments_df = pandas.read_csv(data_path)
    return comments_df


########################################
######## Tripadvisor SVM Pandas ########
########################################

def get_Tripadvisor_training_df():
    data_path = make_data_path("tripadvisor/SVM_training/training_sentences_posi_nega.csv")
    training_df = pandas.read_csv(data_path)
    return training_df

def get_Tripadvisor_training_data():
    data_path = make_data_path("tripadvisor/SVM_training/training_sentences_posi_nega.csv")
    training_df = pandas.read_csv(data_path)
    training_data = list(zip(training_df.sentence, training_df.emotion_val))
    return training_data

def get_Tripadvisor_entropies_df():
    data_path = make_data_path("tripadvisor/SVM_training/entropies.csv")
    entropies_df = pandas.read_csv(data_path)
    return entropies_df

# Personal keyword list loading method
def get_Tripadvisor_original_selected_keywords(status='general'):
    if status=='general':
        com_dictionary = read_dict(make_keyword_path("tripadvisor/Combined_Keywords_z_original_p1.5_n4.25.txt"))
    elif status == 'positive':
        com_dictionary = read_dict(make_keyword_path("tripadvisor/Z_original_Positive_Keywords_alpha_1.5.txt"))
    elif status == 'negative':
        com_dictionary = read_dict(make_keyword_path("tripadvisor/Z_original_Negative_Keywords_alpha_4.25.txt"))
    return com_dictionary

def get_Tripadvisor_original_selected_keywords_values_df():
    data_path = make_data_path("tripadvisor/SVM_training/Combined_Keywords_z_original_p1.5_n4.25_values.csv")
    com_dict_df =pandas.read_csv(data_path)
    return com_dict_df

# Added from 29_subject_keywords.py
def selected_English_subject_keywords(status='general'):
    '''
    ['JJ', 'VB', 'NN', 'RB', 'VBP', 'NNS', 'VBN', 'JJR', 'UH', 'NNP', 'JJS', 'VBG', 'PRP', 'CC', 'CD']
    ignore-->>> ['RB', 'UH', 'PRP', 'CC','CD']
    ['JJ', 'VB', 'NN', 'VBP', 'NNS', 'VBN', 'JJR', 'NNP', 'JJS', 'VBG']
    Basically nouns, verbs and adjectives
    '''
    sel_list = ['JJ', 'VB', 'NN', 'VBP', 'NNS', 'VBN', 'JJR', 'NNP', 'JJS', 'VBG']
    manual_keyword_df = get_Tripadvisor_original_selected_keywords_values_df()
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
def selected_English_subject_adjective_keywords(status='general'):
    '''
    ['JJ', 'JJR', 'JJS']
    Basically adjectives only.
    '''
    sel_list = ['JJ', 'JJR', 'JJS']
    manual_keyword_df = get_Tripadvisor_original_selected_keywords_values_df()
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