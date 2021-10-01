#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.SVM_Methods import *
from EntropyBasedSVM.Bag_of_words import *

def Tag_Ctrip_db_sentences__mutual_filter_tripadvisor_date_hotel_name():
    # Load corpus
    sentences_df = get_Ctrip_db_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_df()
    corpus = sentences_df.Sentence.tolist()
    # Load Training Data
    keyword_list = get_Ctrip_original_selected_keywords()
    training_sentences = get_Ctrip_training_data()
    x,y = Vectorize_training_data_Bag_of_Words(training_sentences, keyword_list)
    # Train selected SVM
    # From paper, C=0.5, F1 was 0.95 +- 0.01, acc was 0.92+-0.03
    clf,_,_ = SVM_Train(x, y, test_size=0, kernel ='linear', C=0.5)
    # Predict Corpus
    corpus_bow = Bag_of_Words(corpus, keyword_list)
    predicted = clf.predict(corpus_bow)
    # Add to sentences_df
    # RID,HotelID,CommentID,SentenceNumber,Sentence,Positive_Prediction
    sentences_df.insert(5,"Positive_Prediction", predicted)
    predict_path = make_data_path("ctrip/ctrip_db/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name.csv")
    sentences_df.to_csv(predict_path, index=False)

if __name__ == '__main__':
    Tag_Ctrip_db_sentences__mutual_filter_tripadvisor_date_hotel_name()