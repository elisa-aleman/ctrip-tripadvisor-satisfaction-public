#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *

def keyword_frequencies__ctrip_db2_mutual_filter_date_hotel_name_filter():
    tagged_df = get_Ctrip_db2_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_df()
    keyword_list = get_Ctrip_original_selected_keywords()
    pos_list = get_Ctrip_original_selected_positive_keywords()
    # neg_list = get_Ctrip_original_selected_negative_keywords()
    pos_count_dict = dict.fromkeys(keyword_list,0)
    neg_count_dict = dict.fromkeys(keyword_list,0)
    pos_tagged_corpus = tagged_df[tagged_df.Positive_Prediction==1].Sentence.tolist()
    pos_total = len(list(flatten([word for word in [sentence.split() for sentence in pos_tagged_corpus]])))
    neg_tagged_corpus = tagged_df[tagged_df.Positive_Prediction==0].Sentence.tolist()
    neg_total = len(list(flatten([word for word in [sentence.split() for sentence in neg_tagged_corpus]])))
    for tagged_sentence in tagged_df.itertuples():
        text = tagged_sentence.Sentence.split()
        emotion_val = tagged_sentence.Positive_Prediction
        for word in text:
            if word in keyword_list:
                if emotion_val == 1:
                    pos_count_dict[word] += 1
                elif emotion_val == 0:
                    neg_count_dict[word] += 1
    ins_table = []
    for keyword in keyword_list:
        val = "Positive" if keyword in pos_list else "Negative"
        pos_abs = pos_count_dict[keyword]
        pos_rel = pos_count_dict[keyword]/pos_total
        pos_prob = pos_count_dict[keyword]/len(tagged_df)
        neg_abs = neg_count_dict[keyword]
        neg_rel = neg_count_dict[keyword]/neg_total
        neg_prob = neg_count_dict[keyword]/len(tagged_df)
        ins_row = (keyword,val,pos_abs,pos_rel,pos_prob,neg_abs,neg_rel,neg_prob)
        ins_table.append(ins_row)
    ins_df = pandas.DataFrame(ins_table, columns=["Keyword","Emotion List","Positive Absolute Frequency","Positive Relative Frequency","Positive Probability per sentence","Negative Absolute Frequency","Negative Relative Frequency", "Negative Probability per sentence"])
    ins_path = make_data_path("ctrip/ctrip_db2/keyword_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv")
    ins_df.sort_values(by=["Positive Absolute Frequency"], ascending=False,inplace=True)
    ins_df.to_csv(ins_path, index=False)

def keyword_frequencies_refiltered():
    tagged_df = get_Ctrip_db2_tagged_z_original_chinese_sentences_df()
    keyword_list = get_Ctrip_original_selected_keywords()
    pos_list = get_Ctrip_original_selected_positive_keywords()
    # neg_list = get_Ctrip_original_selected_negative_keywords()
    pos_count_dict = dict.fromkeys(keyword_list,0)
    neg_count_dict = dict.fromkeys(keyword_list,0)
    pos_tagged_corpus = tagged_df[tagged_df.Positive_Prediction==1].Sentence.tolist()
    pos_total = len(list(flatten([word for word in [sentence.split() for sentence in pos_tagged_corpus]])))
    neg_tagged_corpus = tagged_df[tagged_df.Positive_Prediction==0].Sentence.tolist()
    neg_total = len(list(flatten([word for word in [sentence.split() for sentence in neg_tagged_corpus]])))
    for tagged_sentence in tagged_df.itertuples():
        text = tagged_sentence.Sentence.split()
        emotion_val = tagged_sentence.Positive_Prediction
        for word in text:
            if word in keyword_list:
                if emotion_val == 1:
                    pos_count_dict[word] += 1
                elif emotion_val == 0:
                    neg_count_dict[word] += 1
    ins_table = []
    for keyword in keyword_list:
        val = "Positive" if keyword in pos_list else "Negative"
        pos_abs = pos_count_dict[keyword]
        pos_rel = pos_count_dict[keyword]/pos_total
        pos_prob = pos_count_dict[keyword]/len(tagged_df)
        neg_abs = neg_count_dict[keyword]
        neg_rel = neg_count_dict[keyword]/neg_total
        neg_prob = neg_count_dict[keyword]/len(tagged_df)
        ins_row = (keyword,val,pos_abs,pos_rel,pos_prob,neg_abs,neg_rel,neg_prob)
        ins_table.append(ins_row)
    ins_df = pandas.DataFrame(ins_table, columns=["Keyword","Emotion List","Positive Absolute Frequency","Positive Relative Frequency","Positive Probability per sentence","Negative Absolute Frequency","Negative Relative Frequency", "Negative Probability per sentence"])
    ins_path = make_data_path("ctrip/ctrip_db2/keyword_frequencies_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only.csv")
    ins_df.sort_values(by=["Positive Absolute Frequency"], ascending=False,inplace=True)
    ins_df.to_csv(ins_path, index=False)

if __name__ == '__main__':
    keyword_frequencies__ctrip_db2_mutual_filter_date_hotel_name_filter()
    keyword_frequencies_refiltered()