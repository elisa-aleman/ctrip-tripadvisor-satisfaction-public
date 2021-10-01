#-*- coding: utf-8 -*-

from Paper3_Methods import *
from collections import Counter
from EntropyBasedSVM.StanfordCoreNLP_Chinese.StanfordCoreNLP import *
import string
import os

# Then by identifying adj + noun, remove the ones that don't make sense, list here:
def make_tripadvisor_remove_list():
    all_keywords = set()
    for bin_by in ['price_upper','price_lower']:
        for bin_ver in [2,1]:
            for status in ['general','positive','negative']:
                file_path = make_log_file('tripadvisor/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
                log_df = pandas.read_csv(file_path)
                keywords = log_df.keyword
                all_keywords.update(keywords)
    all_keywords = list(all_keywords)
    pos = POS_Tag(all_keywords, sent_split=False,pre_tokenized=True,tolist=True, lang='en')
    remove_these = []
    for i,keyword in enumerate(pos):
        tags = [tup[1] for tup in keyword]
        words = [tup[0] for tup in keyword]
        adjs = ['VA','JJ','AD']
        if len(keyword)>1:
            num_ads = len([item for item in tags if item in adjs])
            if num_ads>1:
                remove_these.append(all_keywords[i])
        removable_tags = ['DT','PN','CD','DEV','PU','IJ','SP','M', 'NR', 'PRP$', 'WP']
        removable_texts = ['hilton','shinjuku','downside','working','bother','what','aware', 'negative', 'drawback', 'thing', 'kyoto']
        removable_texts += string.ascii_letters
        removable_texts += string.digits
        if any(item in removable_tags for item in tags):
            remove_these.append(all_keywords[i].strip())
        elif any(item in removable_texts for item in words):
            remove_these.append(all_keywords[i].strip())
    log_file = make_log_file('tripadvisor/keyword_counts/remove_keywords_list.txt')
    if os.path.exists(log_file):
        os.remove(log_file)
    print_list_to_log(remove_these, log_file)
    return remove_these

def logs_sum_duplicates():
    for bin_by in ['price_upper','price_lower']:
        for bin_ver in [2,1]:
            for status in ['general','positive','negative']:
                file_path = make_log_file('tripadvisor/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
                log_df = pandas.read_csv(file_path)
                log_df.keyword = log_df.keyword.str.strip()
                log_df = log_df.groupby(['keyword'], as_index=False).agg('sum')
                log_df.to_csv(file_path, index=False)

def sum_dups_most_common():
    for bin_by in ['price_upper','price_lower']:
        for bin_ver in [2,1]:
            pricedict = get_comma_pricelayer_dict(bin_ver=bin_ver)
            price_layer_strs = sorted(pricedict.values())
            for status in ['general','positive','negative']:
                file_path = make_log_file('tripadvisor/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
                log_df = pandas.read_csv(file_path)
                db_counts = [(column,dict(list(zip(log_df['keyword'],log_df[column])))) for column in log_df[price_layer_strs]]
                key_counts_sorted_df = pandas.DataFrame()
                for price_layer_str,x in db_counts:
                    x = Counter(x)
                    ins_col = ['{} : {}'.format(k,v) for k,v in x.most_common()]
                    key_counts_sorted_df[price_layer_str] = ins_col
                ins_path = make_log_file('tripadvisor/keyword_counts/most_common/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
                key_counts_sorted_df.to_csv(ins_path,index=False)
                print("Made Most Common CSV for Ctrip status: {}, bin_ver_{}, bin_by_{}".format(status,bin_ver,bin_by))


# Filter the keyword counts      
def logs_filtered_raw():
    # remove_these = make_tripadvisor_remove_list()
    remove_these = get_tripadvisor_remove_list()
    for bin_by in ['price_upper','price_lower']:
        for bin_ver in [2,1]:
            for status in ['general','positive','negative']:
                file_path = make_log_file('tripadvisor/keyword_counts/raw_counts/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
                log_df = pandas.read_csv(file_path)
                log_df.keyword = log_df.keyword.str.strip()
                log_df = log_df[~log_df.keyword.isin(remove_these)]
                ins_path = make_log_file('tripadvisor/keyword_counts/raw_counts_filtered/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
                log_df.to_csv(ins_path, index=False)

def filtered_most_common():
    for bin_by in ['price_upper','price_lower']:
        for bin_ver in [2,1]:
            pricedict = get_comma_pricelayer_dict(bin_ver=bin_ver)
            price_layer_strs = sorted(pricedict.values())
            for status in ['general','positive','negative']:
                file_path = make_log_file('tripadvisor/keyword_counts/raw_counts_filtered/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_raw_counts_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
                log_df = pandas.read_csv(file_path)
                db_counts = [(column,dict(list(zip(log_df['keyword'],log_df[column])))) for column in log_df[price_layer_strs]]
                key_counts_sorted_df = pandas.DataFrame()
                for price_layer_str,x in db_counts:
                    x = Counter(x)
                    ins_col = ['{} : {}'.format(k,v) for k,v in x.most_common()]
                    key_counts_sorted_df[price_layer_str] = ins_col
                ins_path = make_log_file('tripadvisor/keyword_counts/most_common_filtered/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_most_common_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by))
                key_counts_sorted_df.to_csv(ins_path,index=False)
                print("Made Most Common CSV for Ctrip status: {}, bin_ver_{}, bin_by_{}".format(status,bin_ver,bin_by))

def Change_Tripadvisor_and_ctrip_yen():
    for db in ['ctrip','tripadvisor']:
        for filtered in ['','_filtered']:
            for mode in ['raw_counts','most_common']:
                for bin_by in ['price_upper','price_lower']:
                    for bin_ver in [2,1]:
                        for status in ['general','positive','negative']:
                            if db == 'tripadvisor':
                                file_path = make_log_file('tripadvisor/keyword_counts/{3}{4}/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_{3}_bin_ver_{1}_bin_by_{2}_Combined_Keywords_z_original_p1.5_n4.25_en_english_only_mutual_filter_ctrip_db2_date_hotel-name_price.csv'.format(status, bin_ver, bin_by, mode, filtered))
                            if db == 'ctrip':
                                file_path = make_log_file('ctrip/keyword_counts/{3}{4}/bin_by_{2}/bin_ver_{1}/keyword_counts_bin_by_{2}_keyword_subject_{0}_frequencies_{3}_bin_ver_{1}_bin_by_{2}_Combined_Keywords_Z_original_p2.75_n3.75_zh-cn_chinese_only_mutual_filter_tripadvisor_date_hotel_name_price.csv'.format(status, bin_ver, bin_by, mode, filtered))
                            log_df = pandas.read_csv(file_path)
                            old_pricestrs = sorted(get_comma_pricelayer_dict(bin_ver=bin_ver).values())
                            new_pricestrs = sorted(get_comma_yen_pricelayer_dict(bin_ver=bin_ver).values())
                            rename_dict = dict(list(zip(old_pricestrs,new_pricestrs)))
                            log_df = log_df.rename(columns=rename_dict)
                            log_df.to_csv(file_path, index=False)

def main():
    print("Removing duplicates")
    logs_sum_duplicates()
    sum_dups_most_common()
    print("Filter Raw")
    logs_filtered_raw()
    print("Filter translate")
    filtered_most_common()
    print("Done")
    # Change_Tripadvisor_and_ctrip_yen()


if __name__ == '__main__':
    main()
