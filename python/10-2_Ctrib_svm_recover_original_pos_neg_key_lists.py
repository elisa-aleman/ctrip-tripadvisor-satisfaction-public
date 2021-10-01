#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *

def select_original_positive_negative_keywords():
    old_svm_influences_path = make_data_path("ctrip/SVM_training/SVM_Influences.csv")
    old_svm_df = pandas.read_csv(old_svm_influences_path)
    neg_list = old_svm_df[old_svm_df.DictionaryName=='Negative Classification: "NegativeKeywordsList_alpha_3.75.txt"'].Word.tolist()
    pos_list_combined = old_svm_df[old_svm_df.DictionaryName=='Positive Classification: "CombinedKeywordsList.txt"'].Word.tolist()
    pos_list = [i for i in pos_list_combined if i not in neg_list]
    pos_path = make_keyword_path("ctrip/Z_original_Positive_Keywords_alpha_2.75.txt")
    neg_path = make_keyword_path("ctrip/Z_original_Negative_Keywords_alpha_3.75.txt")
    for pos_word in pos_list: print_log(pos_word,pos_path)
    for neg_word in neg_list: print_log(neg_word,neg_path)

def main():
    select_original_positive_negative_keywords()

if __name__ == '__main__':
    main()