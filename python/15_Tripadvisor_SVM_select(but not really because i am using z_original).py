#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from EntropyBasedSVM.Best_SVM_selection import *
from EntropyBasedSVM.Corpus_preprocessing import general_dictionary

def get_Tripadvisor_general_dict():
    training_df = get_Tripadvisor_training_df()
    corpus = training_df.sentence.tolist()
    general_dict = general_dictionary(corpus)
    return general_dict

def make_Tripadvisor_entropies_table():
    training_df = get_Tripadvisor_training_df()
    corpus = training_df.sentence.tolist()
    positive_documents = training_df[training_df.emotion_val == 1].sentence.tolist()
    negative_documents = training_df[training_df.emotion_val == 0].sentence.tolist()
    general_dict = general_dictionary(corpus)
    file_prefix = "tripadvisor/SVM_training/"
    print("Making Entropies Table")
    make_entropies_table(corpus, positive_documents, negative_documents, general_dict, file_prefix)

def main():
    make_Tripadvisor_entropies_table()
    entropies_df = get_Tripadvisor_entropies_df()
    training_sentences = get_Tripadvisor_training_data()
    general_dict = get_Tripadvisor_general_dict()
    ##
    alphas = list(numpy.arange(1.25,6.25,0.25))
    Cs = list(numpy.arange(1.0,3.5,0.25))
    k = 10
    Make_Keyword_Lists(alphas, general_dict, entropies_df, file_prefix='tripadvisor/')
    SVMResults(training_sentences,alphas, k, Cs, kernel='linear', file_prefix='tripadvisor/')
    SelectBestSVM(file_prefix='tripadvisor/')
    

if __name__ == '__main__':
    main()