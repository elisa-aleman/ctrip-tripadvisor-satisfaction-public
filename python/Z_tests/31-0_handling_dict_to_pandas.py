#-*- coding: utf-8 -*-

import pandas
from collections import Counter

a_list = ['banana','banana','banana','terracota','pie']
b_list = ['terracota','pie','terracota','pie','feet']
c_list = ['banana','feet','golden']
a = Counter(a_list)
b = Counter(b_list)
c = Counter(c_list)
db_counts = [('a',a),('b',b),('c',c)]

for price_layer_str,x in db_counts:
    for price_layer_str,y in db_counts:
        x.update({k:0 for k in y.keys() if x[k]==0})


key_counts_separate_df = pandas.DataFrame()
key_counts_separate_df['keyword'] = list({k for price_layer,counts in db_counts for k in counts.keys()})
key_counts_separate_df.sort_values(by='keyword',ascending=True,inplace=True, ignore_index=True)
for price_layer,x in db_counts:
    key_counts_separate_df[price_layer] = key_counts_separate_df['keyword'].map(x)

key_counts_sorted_df = pandas.DataFrame()
for price_layer_str,x in db_counts:
    ins_col = ['{} : {}'.format(k,v) for k,v in x.most_common()]
    key_counts_sorted_df[price_layer_str] = ins_col