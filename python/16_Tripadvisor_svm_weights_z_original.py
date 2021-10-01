#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from EntropyBasedSVM.SVM_Methods import *
from EntropyBasedSVM.Bag_of_words import *

def Tripadvisor_SVM_weights():
    # Load Training Data
    keyword_list = get_Tripadvisor_original_selected_keywords()
    training_sentences = get_Tripadvisor_training_data()
    x,y = Vectorize_training_data_Bag_of_Words(training_sentences, keyword_list)
    # Train selected SVM
    # From paper, C=0.5, F1 was 0.95 +- 0.01, acc was 0.92+-0.03
    clf,_,_ = SVM_Train(x, y, test_size=0, kernel ='linear', C=2)
    influences = SVM_weights_trained(clf,keyword_list)
    ins_path = make_data_path("tripadvisor/SVM_training/SVM_Influences_Combined_Keywords_z_original_p1.5_n4.25.csv")
    influences_df = pandas.DataFrame(influences, columns = ["Word","Weight"])
    influences_df.to_csv(ins_path, index=False)

if __name__ == '__main__':
    Tripadvisor_SVM_weights()