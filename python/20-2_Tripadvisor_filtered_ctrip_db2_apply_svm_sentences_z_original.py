#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from EntropyBasedSVM.SVM_Methods import *
from EntropyBasedSVM.Bag_of_words import *

def Tag_Tripadvisor_sentences__ctrip_db2_filtered_date_hotel_name_df():
    # Load corpus
    sentences_df = get_Tripadvisor_english_sentences__ctrip_db2_filtered_date_hotel_name_df()
    corpus = sentences_df.sentence.tolist()
    # Load Training Data
    keyword_list = get_Tripadvisor_original_selected_keywords()
    training_sentences = get_Tripadvisor_training_data()
    x,y = Vectorize_training_data_Bag_of_Words(training_sentences, keyword_list)
    # Train selected SVM
    # From paper, C=0.5, F1 was 0.95 +- 0.01, acc was 0.92+-0.03
    clf,_,_ = SVM_Train(x, y, test_size=0, kernel ='linear', C=2)
    # Predict Corpus
    corpus_bow = Bag_of_Words(corpus, keyword_list)
    predicted = clf.predict(corpus_bow)
    # Add to sentences_df
    # hotel_id,comment_id,sentence_num,sentence,date,emotion_val
    sentences_df.insert(5,"emotion_val", predicted)
    predict_path = make_data_path("tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db2_date_hotel-name.csv")
    sentences_df.to_csv(predict_path, index=False)

def Tag_Tripadvisor_sentences__ctrip_db2_filtered_date_hotel_price_df():
    # Load corpus
    sentences_df = get_Tripadvisor_english_sentences__ctrip_db2_filtered_date_hotel_price_df()
    corpus = sentences_df.sentence.tolist()
    # Load Training Data
    keyword_list = get_Tripadvisor_original_selected_keywords()
    training_sentences = get_Tripadvisor_training_data()
    x,y = Vectorize_training_data_Bag_of_Words(training_sentences, keyword_list)
    # Train selected SVM
    # From paper, C=0.5, F1 was 0.95 +- 0.01, acc was 0.92+-0.03
    clf,_,_ = SVM_Train(x, y, test_size=0, kernel ='linear', C=2)
    # Predict Corpus
    corpus_bow = Bag_of_Words(corpus, keyword_list)
    predicted = clf.predict(corpus_bow)
    # Add to sentences_df
    # hotel_id,comment_id,sentence_num,sentence,date,emotion_val
    sentences_df.insert(5,"emotion_val", predicted)
    predict_path = make_data_path("tripadvisor/tripadvisor_db/sentences_predicted_english_only_filtered_ctrip_db2_date_hotel-price.csv")
    sentences_df.to_csv(predict_path, index=False)


if __name__ == '__main__':
    Tag_Tripadvisor_sentences__ctrip_db2_filtered_date_hotel_name_df()
    Tag_Tripadvisor_sentences__ctrip_db2_filtered_date_hotel_price_df()