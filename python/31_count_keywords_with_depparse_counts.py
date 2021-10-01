#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.StanfordCoreNLP_Chinese.StanfordCoreNLP import *
from collections import Counter
import string
from EntropyBasedSVM.Corpus_preprocessing import LemmatizeEnglish

# ーーーーーーーーーーー
# ＊Stanford NLP Parser to Parse the grammatical dependencies of all texts, save it somewhere.
#
# ＊Identify Keywords that are adjectives, and keywords that are subjects
# ＊Split by price
# >>>＊For each price layer
#        ＊Count each non-adjective subject keyword
#        ＊For each adjective keyword
#        　　＊Collect the sentences that include this keyword（extract only positive texts for positive keywords)
#        　　＊SNLPP identify the noun that the adjective refers to, and count
#        　　＊Make a list of the pairs and the counts
#        　　＊Combine with original frequency lists for this price category
# ーーーーーーーーーーー

def count_keywords_and_adjective_pairs_Tripadvisor(tripad_db, status='general', bin_ver=2, bin_by='price_upper', price_layer=0):
    ### Initial Database setup
    if status == 'general':
        tripad_db = tripad_db
    elif status == 'positive':
        tripad_db = tripad_db[tripad_db.emotion_val == 1]
    elif status == 'negative':
        tripad_db = tripad_db[tripad_db.emotion_val == 0]
    hotel_df = hotel_df = get_hotel_ids_pricelayer(bin_ver=bin_ver, bin_by=bin_by, price_layer=price_layer)
    hotel_ids = hotel_df.tripadvisor_hotel_id
    tripad_db = tripad_db[tripad_db.hotel_id.isin(hotel_ids)]
    ### Start counting
    total_counts = Counter()
    # First count the normal keywords.
    keywords = selected_English_subject_keywords(status=status)
    for keyword in keywords:
        sentences = tripad_db[tripad_db.seg_sents.swifter.progress_bar(False).apply(lambda sent: keyword in sent)]
        if len(sentences)>0:
            key_deps = [k for sent in sentences.seg_sents.tolist() for k in sent if k == keyword]
            for doc in sentences.depparse_list.tolist():
                for sent in doc:
                    for tup in sent:
                        if keyword in tup:
                            if 'not' in tup:
                                key_deps.append(' '.join(['not',keyword]))
            counts = Counter(key_deps)
            counts = Counter({k:counts for k,counts in counts.items() if counts>1})
            total_counts += counts
    # Then count adjective pairs
    adjective_keywords = selected_English_subject_adjective_keywords(status=status)
    for keyword in adjective_keywords:
        # # keyword = adjective_keywords[0]
        sentences = tripad_db[tripad_db.depparse_list.swifter.progress_bar(False).apply(lambda doc: any(keyword in tup for sent in doc for tup in sent))]
        if len(sentences)>0:
            ### The original adjective word dependency code is 'amod'
            # # [tup for sent in sentences.iloc[0].depparse_list for tup in sent if keyword in tup]
            ### I can also see some cases where it makes sense to include it as a link being 'nsubj'
            ### But it also links to some words like 'this' or 'that', so let's ignore those. I hope my list covers most errors.
            adj_key_deps = []
            for doc in sentences.depparse_list.tolist():
                for sent in doc:
                    for tup in sent:
                        tup = tuple([tup[0], LemmatizeEnglish(tup[1]),LemmatizeEnglish(tup[2])])
                        if keyword in tup:
                            if any(i =='fi' for i in tup):
                                tup = tuple([i if i!='fi' else 'wifi' for i in tup])
                            if 'amod' in tup:
                                adj_key_deps.append(' '.join([tup[2],tup[1]]))
                            elif 'nsubj' in tup:
                                if tup[1] == keyword:
                                    ignorelist = ['this','that','it', 'things', 'which', 'both', 'others', 'i','you','he','she','they','us','one']
                                    numbers = string.digits
                                    ignorelist += numbers
                                    if not any(i in tup for i in ignorelist):
                                        if not tup[2].isdigit():                                
                                            adj_key_deps.append(' '.join([tup[1],tup[2]]))
            counts = Counter(adj_key_deps)
            counts = Counter({k:counts for k,counts in counts.items() if counts>1})
            total_counts += counts
    return total_counts

def count_keywords_and_adjective_pairs_Ctrip(ctrip_db, status='general', bin_ver=2, bin_by='price_upper', price_layer=0):
    ### Initial Database setup
    if status == 'general':
        ctrip_db = ctrip_db
    elif status == 'positive':
        ctrip_db = ctrip_db[ctrip_db.Positive_Prediction == 1]
    elif status == 'negative':
        ctrip_db = ctrip_db[ctrip_db.Positive_Prediction == 0]
    hotel_df = get_hotel_ids_pricelayer(bin_ver=bin_ver, bin_by=bin_by, price_layer=price_layer)
    hotel_ids = hotel_df.Ctrip_HotelID
    ctrip_db = ctrip_db[ctrip_db.HotelID.isin(hotel_ids)]
    ### Start counting
    total_counts = Counter()
    # First count the normal keywords.
    keywords = selected_Chinese_subject_keywords(status=status)
    for keyword in keywords:
        # keyword = keywords[0]
        sentences = ctrip_db[ctrip_db.seg_sents.swifter.progress_bar(False).apply(lambda sent: keyword in sent)]
        if len(sentences)>0:
            key_deps = [k for sent in sentences.seg_sents.tolist() for k in sent if k == keyword]
            for doc in sentences.depparse_list.tolist():
                for sent in doc:
                    for tup in sent:
                        if keyword in tup:
                            if '不' in tup:
                                key_deps.append(' '.join(['不',keyword]))
                            if '没有' in tup:
                                key_deps.append(' '.join(['没有',keyword]))
            counts = Counter(key_deps)
            counts = Counter({k:counts for k,counts in counts.items() if counts>1})
            total_counts += counts
    # Then count adjective pairs
    adjective_keywords = selected_Chinese_subject_adjective_keywords(status=status)
    for keyword in adjective_keywords:
        # # keyword = adjective_keywords[0]
        sentences = ctrip_db[ctrip_db.depparse_list.swifter.progress_bar(False).apply(lambda doc: any(keyword in tup for sent in doc for tup in sent))]
        if len(sentences)>0:
            ### The original adjective word dependency code is 'amod'
            # # [tup for sent in sentences.iloc[0].depparse_list for tup in sent if keyword in tup]
            ### I can guess this would also have other cases. Let's ask a Chinese lab mate.
            ### nsubj sometimes has other adjectives, but let's count and remove later post process.
            adj_key_deps = []
            for doc in sentences.depparse_list.tolist():
                for sent in doc:
                    for tup in sent:
                        if keyword in tup:
                            if 'amod' in tup:
                                adj_key_deps.append(' '.join([tup[2],tup[1]]))
                            elif 'nsubj' in tup:
                                if tup[1] == keyword:
                                    ignorelist = ['这']
                                    numbers = ['一','二','三','四','五','六','七','八','九','十']
                                    numbers += string.digits
                                    romaji = ["亅", "ω", "é", "è", "à", "ó"]
                                    romaji += string.ascii_letters
                                    ignorelist += romaji
                                    if not any(i in tup for i in ignorelist):
                                        if not tup[2].isdigit():
                                            adj_key_deps.append(' '.join([tup[1],tup[2]]))
            counts = Counter(adj_key_deps)
            counts = Counter({k:counts for k,counts in counts.items() if counts>1})
            total_counts += counts
    return total_counts

def Count_Keywords(comments_db, db='tripadvisor', bin_ver=2, bin_by='price_upper'):
    statuses = ['general','positive','negative']
    pricedict = get_comma_pricelayer_dict(bin_ver=bin_ver)
    price_layers = sorted(pricedict.keys())
    for status in statuses:
        db_counts = []
        for price_layer in price_layers:
            price_layer_str = pricedict[price_layer]
            print("Counting for {} status: {}, bin_ver_{}, bin_by_{}, price_layer:{}".format(db,status,bin_ver,bin_by,price_layer_str))
            if db=='tripadvisor':
                counts = count_keywords_and_adjective_pairs_Tripadvisor(tripad_db=comments_db, status=status, bin_ver=bin_ver, bin_by=bin_by, price_layer=price_layer)
            elif db == 'ctrip':
                counts = count_keywords_and_adjective_pairs_Ctrip(ctrip_db=comments_db, status=status, bin_ver=bin_ver, bin_by=bin_by, price_layer=price_layer)
            db_counts.append((price_layer_str, counts))
        ###### Insert zeros for counts not in each other
        for price_layer_str,x in db_counts:
            for price_layer_str,y in db_counts:
                x.update({k:0 for k in y.keys() if x[k]==0})
        ###### Print to CSV raw counts
        key_counts_separate_df = pandas.DataFrame()
        key_counts_separate_df['keyword'] = list({k for price_layer,counts in db_counts for k in counts.keys()})
        key_counts_separate_df.sort_values(by='keyword',ascending=True,inplace=True)
        for price_layer_str,x in db_counts:
            key_counts_separate_df[price_layer_str] = key_counts_separate_df['keyword'].map(x)
        if db=='tripadvisor':
            ins_path = make_log_file('tripadvisor/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
        elif db == 'ctrip':
            ins_path = make_log_file('ctrip/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by))
        key_counts_separate_df.to_csv(ins_path,index=False)
        print("Made Separate CSV for {} status: {}, bin_ver_{}, bin_by_{}".format(db,status,bin_ver,bin_by))
        ###### Print to CSV in order of most used
        key_counts_sorted_df = pandas.DataFrame()
        for price_layer_str,x in db_counts:
            ins_col = ['{} : {}'.format(k,v) for k,v in x.most_common()]
            key_counts_sorted_df[price_layer_str] = ins_col
        if db=='tripadvisor':
            ins_path = make_log_file('tripadvisor/keyword_counts/most_common/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
        elif db == 'ctrip':
            ins_path = make_log_file('ctrip/keyword_counts/most_common/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by))
        key_counts_sorted_df.to_csv(ins_path,index=False)
        print("Made Most Common CSV for {} status: {}, bin_ver_{}, bin_by_{}".format(db,status,bin_ver,bin_by))

# def parse_most_used_to_raw_csv():
#     for db in ['tripadvisor','ctrip']:
#         for bin_by in ['price_upper','price_lower']:
#             for bin_ver in [2,1]:
#                 for status in ['general','positive','negative']:
#                     if db=='tripadvisor':
#                         file_path = make_log_file('tripadvisor/keyword_counts/most_common/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
#                     elif db == 'ctrip':
#                         file_path = make_log_file('ctrip/keyword_counts/most_common/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by))
#                     log_df = pandas.read_csv(file_path)
#                     db_counts = [(column,dict([entry.split(' : ') for entry in log_df[column].tolist()])) for column in log_df]
#                     key_counts_separate_df = pandas.DataFrame()
#                     key_counts_separate_df['keyword'] = list({k for price_layer,counts in db_counts for k in counts.keys()})
#                     key_counts_separate_df.sort_values(by='keyword',ascending=True,inplace=True)
#                     for price_layer_str,x in db_counts:
#                         key_counts_separate_df[price_layer_str] = key_counts_separate_df['keyword'].map(x)
#                     if db=='tripadvisor':
#                         ins_path = make_log_file('tripadvisor/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
#                     elif db == 'ctrip':
#                         ins_path = make_log_file('ctrip/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by))
#                     key_counts_separate_df.to_csv(ins_path,index=False)
#                     print("Made Separate CSV for {} status: {}, bin_ver_{}, bin_by_{}".format(db,status,bin_ver,bin_by))
        
def count_main():
    # ### Load Tripadvisor DB
    print('Load Tripadvisor DB')
    tripad_db = get_Tripadvisor_depparsed_tagged_english_sentences__ctrip_db2_filtered_date_hotel_name_price_df()
    tripad_db = tripad_db[tripad_db.dependency_parse.notnull()]
    deps = Dependency_Parse(tripad_db.sentence.tolist(), sent_split=False, pre_tokenized=False, tolist=True, output_with_sentence=False, lang='en')
    segs = [sent.lower().split() for sent in tripad_db.sentence]
    tripad_db['depparse_list'] = deps
    tripad_db['seg_sents'] = segs
    ### Load Ctrip DB
    # print('Load Ctrip DB')
    # ctrip_db = get_Ctrip_db2_depparsed_tagged_z_original_chinese_sentences__mutual_filter_tripadvisor_date_hotel_name_price_df()
    # ctrip_db = ctrip_db[ctrip_db.Dependency_Parse.notnull()]
    # deps = [Dependency_Parse_str_tolist(dep_parse_str.lower(), output_with_sentence=False) for dep_parse_str in ctrip_db.Dependency_Parse]
    # segs = [sent.lower().split() for sent in ctrip_db.Sentence]
    # ctrip_db['depparse_list'] = deps
    # ctrip_db['seg_sents'] = segs
    #### Start Counts
    print('Start Counts')
    for bin_by in ['price_upper','price_lower']:
        for bin_ver in [2,1]:
            Count_Keywords(comments_db=tripad_db, db='tripadvisor', bin_ver=bin_ver, bin_by=bin_by)
            # Count_Keywords(comments_db=ctrip_db, db='ctrip', bin_ver=bin_ver, bin_by=bin_by)

def main():
    count_main()
    # parse_most_used_to_raw_csv()

if __name__ == '__main__':
    main()