from Paper3_Methods import *

bin_ver = 2
pricedict = get_comma_yen_pricelayer_dict(bin_ver=bin_ver)
price_layer_strs = sorted(pricedict.values())

###########################
########## Ctrip ##########
###########################

####### 'general'
db = 'ctrip'
view='most_common'
filtered=True
status='general'
log_df = selected_keyword_count_logs_no_doubles(db=db, status=status, view=view, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10).to_clipboard(index=False)

####### 'positive'
db = 'ctrip'
view='most_common'
filtered=True
status='positive'
log_df = selected_keyword_count_logs_no_doubles(db=db, status=status, view=view, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10).to_clipboard(index=False)

####### 'negative'
db = 'ctrip'
view='most_common'
filtered=True
status='negative'
log_df = selected_keyword_count_logs_no_doubles(db=db, status=status, view=view, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10).to_clipboard(index=False)

####
# Test each adjective

status='positive'
db = 'ctrip'
filtered=True
adj = '不错'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = '大'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = '干净'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = '近'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = '新'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = '棒'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = '远'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)



####
status='negative'
db = 'ctrip'
filtered=True

adj = '一般'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = '陈旧'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = '老'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)



# ## Ctrip Raw count look
# db = 'ctrip'
# view='raw_counts'
# filtered=True
# status='general'
# # status = 'positive'
# # status = 'negative'
# log_df = selected_keyword_count_logs_no_doubles(db=db, status=status, view=view, filtered=filtered)
# adj = '大'
# log_df[log_df['keyword'].str.contains(adj)].sort_values(by='0: All Prices',ascending=False).head(10)
# log_df[log_df['keyword'].str.contains(adj)].sort_values(by='0: All Prices',ascending=False).head(10).to_clipboard(index=False)


###########################
####### Tripadvisor #######
###########################

####### 'general'
db = 'tripadvisor'
view='most_common'
filtered=True
status='general'
log_df = selected_keyword_count_logs(db=db, status=status, view=view, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10).to_clipboard(index=False)

###### 'positive'
db = 'tripadvisor'
view='most_common'
filtered=True
status='positive'
log_df = selected_keyword_count_logs(db=db, status=status, view=view, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10).to_clipboard(index=False)

###### 'negative'
db = 'tripadvisor'
view='most_common'
filtered=True
status='negative'
log_df = selected_keyword_count_logs(db=db, status=status, view=view, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10).to_clipboard(index=False)

####
# Test each adjective

db = 'tripadvisor'
filtered=True
status='positive'

adj = 'good'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'great'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'nice'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'excellent'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'clean'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'comfortable'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'friendly'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = 'helpful'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(7)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(7).to_clipboard(index=False)

adj = 'free'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = 'large'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(7)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(7).to_clipboard(index=False)

adj = 'beautiful'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'wonderful'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)


###

db = 'tripadvisor'
filtered=True
status='negative'

adj = 'poor'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'dated'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(7)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(7).to_clipboard(index=False)

adj = 'worst'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(6).to_clipboard(index=False)

adj = 'disappointing'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'disappointment'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'dirty'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(7)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(7).to_clipboard(index=False)

adj = 'minor'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'funny'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'annoying'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'uncomfortable'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'unable'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'worse'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'rude'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'smallest'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'mixed'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)

adj = 'paper'
log_df = select_adjective_logs_most_common(adj=adj, db=db, status=status, filtered=filtered)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5)
log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(5).to_clipboard(index=False)


if __name__ == '__main__':
    pass
