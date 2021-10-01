#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.StanfordCoreNLP_Chinese.StanfordCoreNLP import *

# ーーーーーーーーーーー
#>> ＊Stanford NLP Parser to Parse the grammatical dependencies of all texts, save it somewhere.
#
# ＊Identify Keywords that are adjectives, and keywords that are subjects
# ＊For each adjective keyword
# 　　＊Collect the sentences that include this keyword（extract only positive texts for positive keywords)
# 　　＊SNLPP identify the noun that the adjective refers to, and count
# 　　＊Make a list of the pairs and the counts
# 　　＊Combine with original frequency lists for "all prices" category
# ＊Split by price
# ＊For each price layer
# 　　＊Count each non-adjective subject keyword
# 　　＊For each adjective keyword
# 　　　　＊Collect the sentences that include this keyword（extract only positive texts for positive keywords)
# 　　　　＊SNLPP identify the noun that the adjective refers to, and count
# 　　　　＊Make a list of the pairs and the counts
# 　　　　＊Combine with original frequency lists for this price category
# ーーーーーーーーーーー

# just to test commit history with --ff-only

def Dependency_Ctrip():
    ctrip_db = get_Ctrip_db2_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_price_df()
    # ctrip_db.columns = ['RID', 'HotelID', 'CommentPage', 'CommentID', 'SentenceNumber', 'Sentence', 'Positive_Prediction']
    ins_path = make_data_path("ctrip/ctrip_db2/sentences_depparsed_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv")
    texts = ctrip_db.Sentence.tolist()
    deps_str = Dependency_Parse(texts, dependency_type='basicDependencies', sent_split=False, tolist=False, output_with_sentence=False, pre_tokenized=True, properties=None, timeout=15000, verbose=1, lang='zh-cn')
    ctrip_db['Dependency_Parse'] = deps_str
    ctrip_db.to_csv(ins_path, index = False)

def Dependency_Tripadvisor():
    tripad_db = get_Tripadvisor_tagged_english_sentences__ctrip_db2_filtered_date_hotel_name_price_df()
    # tripad_db.columns = ['hotel_id', 'comment_id', 'sentence_num', 'sentence', 'date', 'emotion_val']
    ins_path = make_data_path("tripadvisor/tripadvisor_db/sentences_depparsed_predicted_english_only_filtered_ctrip_db2_date_hotel-name_price.csv")
    texts = tripad_db.sentence.tolist()
    deps_str = Dependency_Parse(texts, dependency_type='basicDependencies', sent_split=False, tolist=False, output_with_sentence=False, pre_tokenized=False, properties=None, timeout=15000, verbose=1, lang='en')
    tripad_db['dependency_parse'] = deps_str
    tripad_db.to_csv(ins_path, index = False)

if __name__ == '__main__':
    Dependency_Ctrip()
    Dependency_Tripadvisor()

