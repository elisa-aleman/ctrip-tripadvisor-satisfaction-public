#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.Best_SVM_selection import *
from EntropyBasedSVM.Corpus_preprocessing import general_dictionary

def get_Ctrip_general_dict():
    training_df = get_Ctrip_training_df()
    corpus = training_df.Sentence.tolist()
    general_dict = general_dictionary(corpus)
    return general_dict

def make_Ctrip_entropies_table():
    training_df = get_Ctrip_training_df()
    corpus = training_df.Sentence.tolist()
    positive_documents = training_df[training_df.Positive == 1].Sentence.tolist()
    negative_documents = training_df[training_df.Positive == 0].Sentence.tolist()
    general_dict = general_dictionary(corpus)
    file_prefix = "ctrip/SVM_training/"
    print("Making Entropies Table")
    make_entropies_table(corpus, positive_documents, negative_documents, general_dict, file_prefix)

def main():
    make_Ctrip_entropies_table()
    entropies_df = get_Ctrip_entropies_df()
    training_sentences = get_Ctrip_training_data()
    general_dict = get_Ctrip_general_dict()
    ##
    alphas = list(numpy.arange(1.25,6.25,0.25))
    Cs = list(numpy.arange(1.0,3.5,0.25))
    k = 10
    Make_Keyword_Lists(alphas, general_dict, entropies_df, file_prefix='ctrip/')
    SVMResults(training_sentences,alphas, k, Cs, kernel='linear', file_prefix='ctrip/')
    SelectBestSVM(file_prefix='ctrip/')
    ##
    alphas = list(numpy.arange(1.25,4,0.25))
    Cs = list(numpy.arange(0.5,3.5,0.25))
    k = 5
    Make_Keyword_Lists(alphas, general_dict, entropies_df, file_prefix='ctrip/Z_Original_alphas_')
    SVMResults(training_sentences,alphas, k, Cs, kernel='linear', file_prefix='ctrip/Z_Original_alphas_')
    SelectBestSVM(file_prefix='ctrip/Z_Original_alphas_')
    ###

if __name__ == '__main__':
    main()