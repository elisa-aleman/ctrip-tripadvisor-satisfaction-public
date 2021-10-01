#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.SVM_Methods import *
from EntropyBasedSVM.Bag_of_words import 

def Tag_Ctrip_db2_sentences():
    # Load corpus
    data_path = make_data_path("ctrip/ctrip_db2/sentences_zh-cn_chinese_only.csv")
    sentences_df = pandas.read_csv(data_path)
    corpus = sentences_df.Sentence.tolist()
    # Load Training Data
    keyword_list = get_original_selected_keywords()
    training_sentences = get_Ctrip_training_data()
    x,y = Vectorize_training_data_Bag_of_Words(training_sentences, keyword_list)
    # Train selected SVM
    # From paper, C=0.5, F1 was 0.95 +- 0.01, acc was 0.92+-0.03
    clf,_,_ = SVM_Train(x, y, test_size=0, kernel ='linear', C=0.5)
    # Predict Corpus
    corpus_bow = Bag_of_Words(corpus, keyword_list)
    predicted = clf.predict(corpus_bow)
    # Add to sentences_df
    # RID,HotelID,CommentPage,CommentID,SentenceNumber,Sentence,Positive_Prediction
    sentences_df.insert(5,"Positive_Prediction", predicted)
    predict_path = make_data_path("ctrip/ctrip_db2/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only.csv")
    sentences_df.to_csv(predict_path, index=False)

if __name__ == '__main__':
    Tag_Ctrip_db2_sentences()