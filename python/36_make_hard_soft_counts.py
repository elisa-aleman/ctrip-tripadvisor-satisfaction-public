from Paper3_Methods import *
from collections import Counter

bin_ver = 2
pricedict = get_comma_yen_pricelayer_dict(bin_ver=bin_ver)
price_layer_strs = sorted(pricedict.values())

##### CTRIP POSITIVE

db = 'ctrip'
view='most_common'
filtered=True
status='positive'
log_df = selected_keyword_count_logs_no_doubles(db=db, status=status, view=view, filtered=filtered)

for column in log_df: 
    log_df[column] = log_df[column].str.split(' \(').str[0]

log_df = log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
hard_soft_dict = get_hard_soft_df(db=db)[get_hard_soft_df(db=db).emotion == status][['keyword','hard','soft','undefined']].set_index('keyword').to_dict(orient='index')

hs_counts = []
for column in log_df:
    words = log_df[column].tolist()
    counts = Counter({'hard':0,'soft':0,'undefined':0})
    for word in words:
        counts.update(hard_soft_dict.get(word))
    counts = dict(counts)
    row = (column,counts['hard'],counts['soft'],counts['undefined'])
    hs_counts.append(row)

hs_counts = pandas.DataFrame(hs_counts, columns=['Price range', 'Hard attributes', 'Soft attributes', 'Undefined'])
hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']] = hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']].div(hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']].sum(axis=1),axis=0)
hs_counts
hs_counts.to_clipboard(index=False)

##### CTRIP NEGATIVE

db = 'ctrip'
view='most_common'
filtered=True
status='negative'
log_df = selected_keyword_count_logs_no_doubles(db=db, status=status, view=view, filtered=filtered)

for column in log_df: 
    log_df[column] = log_df[column].str.split(' \(').str[0]

log_df = log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
hard_soft_dict = get_hard_soft_df(db=db)[get_hard_soft_df(db=db).emotion == status][['keyword','hard','soft','undefined']].set_index('keyword').to_dict(orient='index')

hs_counts = []
for column in log_df:
    words = log_df[column].tolist()
    counts = Counter({'hard':0,'soft':0,'undefined':0})
    for word in words:
        counts.update(hard_soft_dict.get(word))
    counts = dict(counts)
    row = (column,counts['hard'],counts['soft'],counts['undefined'])
    hs_counts.append(row)

hs_counts = pandas.DataFrame(hs_counts, columns=['Price range', 'Hard attributes', 'Soft attributes', 'Undefined'])
hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']] = hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']].div(hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']].sum(axis=1),axis=0)
hs_counts
hs_counts.to_clipboard(index=False)


#####################
#####################
#####################


##### TRIPADVISOR POSITIVE

db = 'tripadvisor'
view='most_common'
filtered=True
status='positive'
log_df = selected_keyword_count_logs(db=db, status=status, view=view, filtered=filtered)

for column in log_df: 
    log_df[column] = log_df[column].str.split(' : ').str[0]

log_df = log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
hard_soft_dict = get_hard_soft_df(db=db)[get_hard_soft_df(db=db).emotion == status][['keyword','hard','soft','undefined']].set_index('keyword').to_dict(orient='index')

hs_counts = []
for column in log_df:
    words = log_df[column].tolist()
    counts = Counter({'hard':0,'soft':0,'undefined':0})
    for word in words:
        counts.update(hard_soft_dict.get(word))
    counts = dict(counts)
    row = (column,counts['hard'],counts['soft'],counts['undefined'])
    hs_counts.append(row)

hs_counts = pandas.DataFrame(hs_counts, columns=['Price range', 'Hard attributes', 'Soft attributes', 'Undefined'])
hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']] = hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']].div(hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']].sum(axis=1),axis=0)
hs_counts
hs_counts.to_clipboard(index=False)

##### TRIPADVISOR NEGATIVE

db = 'tripadvisor'
view='most_common'
filtered=True
status='negative'
log_df = selected_keyword_count_logs(db=db, status=status, view=view, filtered=filtered)

for column in log_df: 
    log_df[column] = log_df[column].str.split(' : ').str[0]

log_df = log_df[[price_layer_strs[0]]+price_layer_strs[3:]].head(10)
hard_soft_dict = get_hard_soft_df(db=db)[get_hard_soft_df(db=db).emotion == status][['keyword','hard','soft','undefined']].set_index('keyword').to_dict(orient='index')

hs_counts = []
for column in log_df:
    words = log_df[column].tolist()
    counts = Counter({'hard':0,'soft':0,'undefined':0})
    for word in words:
        counts.update(hard_soft_dict.get(word))
    counts = dict(counts)
    row = (column,counts['hard'],counts['soft'],counts['undefined'])
    hs_counts.append(row)

hs_counts = pandas.DataFrame(hs_counts, columns=['Price range', 'Hard attributes', 'Soft attributes', 'Undefined'])
hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']] = hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']].div(hs_counts[['Hard attributes', 'Soft attributes', 'Undefined']].sum(axis=1),axis=0)
hs_counts
hs_counts.to_clipboard(index=False)

