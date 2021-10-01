#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.StanfordCoreNLP_Chinese.StanfordCoreNLP import *

# ーーーーーーーーーーー
# ＊Stanford NLP Parser to Parse the grammatical dependencies of all texts, save it somewhere.
#
#>> ＊Identify Keywords that are adjectives, and keywords that are subjects
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

###################
###### Ctrip ######
###################

# For details on how I determined which ones to use:
# ./Z_tests/29-0_confirm_hand_selected_subject_keywords.py
# Checking previously hand selected keywords to see what my judgment was
## 'NN', 'VA', 'VV','JJ'
# Basically nouns, verbs and adjectives



def POS_Tag_keywords_Ctrip():
    manual_keyword_df = pandas.read_csv(make_data_path("ctrip/SVM_training/Combined_Keywords_Z_original_p2.75_n3.75_translations__manually_selected_values.csv"))
    keywords = manual_keyword_df.Keyword.tolist()
    res = POS_Tag(keywords,sent_split=False,tolist=True,pre_tokenized=True, lang='zh-cn')
    pos = [[tup[1] for tup in kw] for kw in res]
    pos = ['+'.join(kw) for kw in pos]
    manual_keyword_df['POS_Tag'] = pos
    subjects = manual_keyword_df[manual_keyword_df['WordValue']=='subject']
    print(subjects.POS_Tag.unique())
    # ['NN', 'VA', 'VV', 'NR', 'DT+M', 'JJ', 'VE+M']
    # ignore-->>>'VE+M', 'DT+M'
    # ['NN', 'VA', 'VV','JJ', 'NR']
    manual_keyword_df.to_csv(make_data_path("ctrip/SVM_training/Combined_Keywords_Z_original_p2.75_n3.75_translations__manually_selected_values.csv"), index=False)

# Added to Ctrip_Methods.py
def selected_Chinese_subject_keywords(status='general'):
    '''
    # 'NN', 'VA', 'VV','JJ'  
    ignore-->>>'VE+M', 'DT+M', 'NR'
    Basically nouns, verbs and adjectives
    '''
    sel_list = ['NN', 'VA', 'VV','JJ', 'NR']
    manual_keyword_df = get_Ctrip_original_selected_keywords_translations_values_df()
    selected = manual_keyword_df[manual_keyword_df['POS_Tag'].isin(sel_list)]
    if status == 'general':
        selected = selected
    elif status == 'positive':
        selected = selected[selected.KeywordList=='positive']
    elif status == 'negative':
        selected = selected[selected.KeywordList=='negative']
    keywords = selected.Keyword.tolist()
    return keywords

# Added to Ctrip_Methods.py
def selected_Chinese_subject_adjective_keywords(status='general'):
    '''
    # 'VA', 'JJ'
    Basically adjectives in Chinese can be verbs too.
    '''
    sel_list = ['VA','JJ']
    manual_keyword_df = get_Ctrip_original_selected_keywords_translations_values_df()
    selected = manual_keyword_df[manual_keyword_df['POS_Tag'].isin(sel_list)]
    if status == 'general':
        selected = selected
    elif status == 'positive':
        selected = selected[selected.KeywordList=='positive']
    elif status == 'negative':
        selected = selected[selected.KeywordList=='negative']
    keywords = selected.Keyword.tolist()
    return keywords

#########################
###### Tripadvisor ######
#########################

def POS_Tag_keywords_Tripadvisor():
    manual_keyword_df = pandas.read_csv(make_data_path("tripadvisor/SVM_training/Combined_Keywords_z_original_p1.5_n4.25_values.csv"))
    keywords = manual_keyword_df.Keyword.tolist()
    res = POS_Tag(keywords,sent_split=False,tolist=True,pre_tokenized=True, lang='en')
    pos = [[tup[1] for tup in kw] for kw in res]
    pos = ['+'.join(kw) for kw in pos]
    manual_keyword_df['POS_Tag'] = pos
    subjects = manual_keyword_df[manual_keyword_df['WordValue']=='subject']
    print(subjects.POS_Tag.unique())
    # ['JJ', 'VB', 'NN', 'RB', 'VBP', 'NNS', 'VBN', 'JJR', 'UH', 'NNP', 'JJS', 'VBG', 'PRP', 'CC', 'CD']
    # ignore-->>> 'RB', 'UH', 'PRP', 'CC','CD'
    # ['JJ', 'VB', 'NN', 'VBP', 'NNS', 'VBN', 'JJR', 'NNP', 'JJS', 'VBG']
    manual_keyword_df.to_csv(make_data_path("tripadvisor/SVM_training/Combined_Keywords_z_original_p1.5_n4.25_values.csv"), index=False)

# Added to Tripadvisor_Methods.py
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

# Added to Tripadvisor_Methods.py
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
    # POS_Tag_keywords_Ctrip()
    # POS_Tag_keywords_Tripadvisor()

