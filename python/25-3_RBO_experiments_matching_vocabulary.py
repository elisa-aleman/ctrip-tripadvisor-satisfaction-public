#-*- coding: utf-8 -*-
# https://github.com/dlukes/rbo/blob/master/rbo.py

from rbo.rbo import rbo, rbo_dict
from Paper3_Methods import *
from Tripadvisor_Methods import *
from Ctrip_Methods import *

###############################
########### Chinese ###########
###############################

def get_Chinese_frequencies_positive(freq_df, cutoff=None):
    freq_df.sort_values(by=["Positive Absolute Frequency"], ascending=False,inplace=True)
    if cutoff:
        freq_df = freq_df[:cutoff]
    freqs_dict = dict(zip(freq_df["Translation"],freq_df["Positive Absolute Frequency"]))
    return freqs_dict
    
def get_Chinese_frequencies_negative(freq_df, cutoff=None):
    freq_df.sort_values(by=["Negative Absolute Frequency"], ascending=False,inplace=True)
    if cutoff:
        freq_df = freq_df[:cutoff]
    freqs_dict = dict(zip(freq_df["Translation"],freq_df["Negative Absolute Frequency"]))
    return freqs_dict

###############################
########### English ###########
###############################

def get_English_frequencies_positive(freq_df, cutoff=None):
    freq_df.sort_values(by=["Positive Absolute Frequency"], ascending=False,inplace=True)
    if cutoff:
        freq_df = freq_df[:cutoff]
    freqs_dict = dict(zip(freq_df["Keyword"],freq_df["Positive Absolute Frequency"]))
    return freqs_dict

def get_English_frequencies_negative(freq_df, cutoff=None):
    freq_df.sort_values(by=["Negative Absolute Frequency"], ascending=False,inplace=True)
    freq_df.loc[freq_df.Keyword == 'pricey', 'Keyword'] = 'price'
    if cutoff:
        freq_df = freq_df[:cutoff]
    freqs_dict = dict(zip(freq_df["Keyword"],freq_df["Negative Absolute Frequency"]))
    return freqs_dict

def filter_match_dict_keys(a,b):
    a = dict([(i,a[i]) for i in a if i in b])
    b = dict([(i,b[i]) for i in b if i in a])
    return a,b

#######################################
########### RBO experiments ###########
#######################################

def RBO_Experiment_matching_vocabulary(ctrip_pos_df, ctrip_neg_df, tripad_pos_df, tripad_neg_df, p=0.9, cutoff=None):
    pos_zh = get_Chinese_frequencies_positive(ctrip_pos_df, cutoff=cutoff)
    neg_zh = get_Chinese_frequencies_negative(ctrip_neg_df, cutoff=cutoff)
    pos_en = get_English_frequencies_positive(tripad_pos_df, cutoff=cutoff)
    neg_en = get_English_frequencies_negative(tripad_neg_df, cutoff=cutoff)
    pos_zh, pos_en = filter_match_dict_keys(pos_zh, pos_en)
    neg_zh, neg_en = filter_match_dict_keys(neg_zh, neg_en)
    pos_rbo = rbo_dict(pos_zh,pos_en, p = p)
    neg_rbo = rbo_dict(neg_zh,neg_en, p = p)
    return pos_rbo,neg_rbo

def RBO_Experiments_matching_vocabulary(ctrip_pos_df, ctrip_neg_df, tripad_pos_df, tripad_neg_df, ps=[0.9,0.75,0.5,0.25], cutoffs=[None, 20, 10, 7, 5]):
    ins_table = []
    for p in ps:
        for cutoff in cutoffs:
            cutoff_str = str(cutoff)
            pos_rbo,neg_rbo = RBO_Experiment_matching_vocabulary(ctrip_pos_df, ctrip_neg_df, tripad_pos_df, tripad_neg_df, p=p,cutoff=cutoff)
            ins_table.append((p,cutoff_str,"Satisfaction",pos_rbo['ext'],pos_rbo['min'],pos_rbo['res']))
            ins_table.append((p,cutoff_str,"Dissatisfaction",neg_rbo['ext'],neg_rbo['min'],neg_rbo['res']))
    ins_df = pandas.DataFrame(ins_table, columns=["p_val", "List cutoff", "Emotion", "RBO_EXT", "RBO_MIN", "RBO_RES"])
    return ins_df

############################
########### Main ###########
############################

##########################
# Ctrip_db2
##########################

##############
### Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname___RBO_Experiments

def Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname___RBO_Experiments(ps=[0.9,0.75,0.5,0.25], cutoffs=[None, 20, 10, 7, 5]):
    ctrip_pos_df = get_Ctrip_db2_keyword_subject_positive_frequencies_z_original__mutual_filter_tripadvisor_date_hotel_name_df()
    ctrip_neg_df = get_Ctrip_db2_keyword_subject_negative_frequencies_z_original__mutual_filter_tripadvisor_date_hotel_name_df()
    tripad_pos_df = get_Tripadvisor_keyword_subject_positive_frequencies_z_original__ctrip_db2_filtered_date_hotel_name_df()
    tripad_neg_df = get_Tripadvisor_keyword_subject_negative_frequencies_z_original__ctrip_db2_filtered_date_hotel_name_df()
    ins_df = RBO_Experiments_matching_vocabulary(ctrip_pos_df, ctrip_neg_df, tripad_pos_df, tripad_neg_df, ps=ps, cutoffs=cutoffs)
    ins_path = make_log_file("RBO_experiments_matching_vocabulary_only/Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname___RBO_Experiments.csv")
    ins_df.to_csv(ins_path, index=False)


def main():
    ps=[0.9,0.75,0.5,0.25]
    cutoffs=[None, 20, 10, 7, 5]
    ### Ctrip_db2
    Ctrip_db2_hotelname__and__Tripadvisor_date_hotelname___RBO_Experiments(ps, cutoffs)

if __name__ == '__main__':
    main()


