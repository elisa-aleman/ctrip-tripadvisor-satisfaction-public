#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.StanfordCoreNLP_Chinese.StanfordCoreNLP import *

# ctrip_db = pandas.read_csv(make_data_path("ctrip/ctrip_db2/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv"))
# zh_text = ctrip_db.iloc[0].Sentence
# '日本 的 酒店 就 是 如果 ， 不过 这里 出行 便利 ， 周围 环境 非常 不错 ， 晚上 睡觉 非常 安静'

ctrip_db = pandas.read_csv(make_data_path("ctrip/ctrip_db2/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv"))
zh_texts = [ctrip_db.iloc[i].Sentence for i in range(100)]

results = Dependency_Parse_many(zh_texts,tolist=False,output_with_sentence=False,be_quiet=True,lang='zh-cn')
results = Dependency_Parse_many(zh_texts,tolist=True,output_with_sentence=False,be_quiet=True,lang='zh-cn')

en_text = 'This is a nice sentence for the server to handle. I wonder what it will do.'

#.replace(' ','') 
# even split, the pos tagging takes place well, so it's not necessary


# ctrip_comments_db = pandas.read_csv(make_data_path("ctrip/ctrip_db2/comments_zh-cn_chinese_only.csv"))
# comment = ctrip_comments_db.iloc[0].Comment
# Segment(comment,sent_split=False,tolist=True)

annotators=['depparse']
properties={
        'tokenize_pretokenized': True, # Assume the text is tokenized by white space and sentence split by newline. Do not run a model.
        'tokenize_no_ssplit':True # Assume the sentences are split by two continuous newlines (\n\n). Only run tokenization and disable sentence segmentation.
        }
properties = get_StanfordCoreNLP_chinese_properties(properties=properties)

# with CoreNLPClient(annotators=annotators, properties=properties, timeout=15000) as client:
#     ann = client.annotate(en_text)

# Attempt to wake client once for many sentences
with CoreNLPClient(annotators=annotators, properties=properties, timeout=15000) as client:
    anns = [client.annotate(text) for text in zh_texts]


# https://stanfordnlp.github.io/stanza/client_usage.html

sentence = ann.sentence[0]

print(sentence.basicDependencies)

sentence.basicDependencies.node # list of nodes
sentence.basicDependencies.edge # list of edges
sentence.basicDependencies.root # main subject node

# res:
    # node {
    #   sentenceIndex: 0
    #   index: 1
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 2
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 3
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 4
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 5
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 6
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 7
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 8
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 9
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 10
    # }
    # node {
    #   sentenceIndex: 0
    #   index: 11
    # }
    # edge {
    #   source: 5
    #   target: 1
    #   dep: "nsubj"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # edge {
    #   source: 5
    #   target: 2
    #   dep: "cop"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # edge {
    #   source: 5
    #   target: 3
    #   dep: "det"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # edge {
    #   source: 5
    #   target: 4
    #   dep: "amod"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # edge {
    #   source: 5
    #   target: 10
    #   dep: "acl"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # edge {
    #   source: 5
    #   target: 11
    #   dep: "punct"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # edge {
    #   source: 8
    #   target: 7
    #   dep: "det"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # edge {
    #   source: 10
    #   target: 6
    #   dep: "mark"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # edge {
    #   source: 10
    #   target: 8
    #   dep: "nsubj"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # edge {
    #   source: 10
    #   target: 9
    #   dep: "mark"
    #   isExtra: false
    #   sourceCopy: 0
    #   targetCopy: 0
    #   language: UniversalEnglish
    # }
    # root: 5

########################
'''
Now let's explain the result. Each node is a word, the index is its number in the sentence.
Each edge is a connection between the words. Let's look at the edge between 5 and 4:

# edge {
#   source: 5       # which is 'sentence'
#   target: 4       # which is 'nice'
#   dep: "amod"     # "amod" means adjective modifier
#   isExtra: False  # 
#   sourceCopy: 0
#   targetCopy: 0
#   language: UniversalEnglish
# }

dependency list in: https://nlp.stanford.edu/software/dependencies_manual.pdf

##########################

'''

