#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.StanfordCoreNLP_Chinese.StanfordCoreNLP import *

ctrip_db = pandas.read_csv(make_data_path("ctrip/ctrip_db2/sentences_predicted_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv"))
zh_texts = ctrip_db.Sentence.tolist()

# Checking previously hand selected keywords to see what my judgment was
# adjectives, nouns, verbs

# 下次 ? what is it?
# Determiner + Measure word
# Maybe let's ignore it in the long run
a = "下次"
texts = [text for text in zh_texts if a in text]
texts = texts[:10]
res = POS_Tag(texts,sent_split=False,tolist=True,pre_tokenized=True)

b = '欣赏'
texts = [text for text in zh_texts if b in text]
texts = texts[:10]
res = POS_Tag(texts,sent_split=False,tolist=True,pre_tokenized=True)
# VV : other verb

c = '推荐'
texts = [text for text in zh_texts if c in text]
texts = texts[:10]
res = POS_Tag(texts,sent_split=False,tolist=True,pre_tokenized=True)
# NN: noun

# Checking previously hand selected keywords to see what my judgment was
# adjectives, nouns, verbs
