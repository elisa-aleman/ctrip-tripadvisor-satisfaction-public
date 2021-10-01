#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
from gensim.summarization.textcleaner import split_sentences

def Make_sentence_only_reviews():
    comments_df = get_Tripadvisor_english_comments_df()
    # hotel_id,username,language,comment_id,comment,score,date
    ins_table = []
    # columns = ["hotel_id","comment_id","sentence_num","sentence","date"]
    limit = comments_df.shape[0]
    for ind,row in enumerate(comments_df.itertuples()):
        print("Segmenting comment {} of {}".format(ind+1,limit))
        text = row.comment
        sentences = split_sentences(text)
        for num, sentence in enumerate(sentences):
            ins = (row.hotel_id,row.comment_id,num+1,sentence,row.date)
            ins_table.append(ins)
        up()
    down()
    print("Insert segmented sentences")
    ins_table_df = pandas.DataFrame(ins_table,columns=["hotel_id","comment_id","sentence_num","sentence","date"])
    ins_path = make_data_path("tripadvisor/tripadvisor_db/sentences_english_only.csv")
    ins_table_df.to_csv(ins_path, index=False)

if __name__ == '__main__':
    Make_sentence_only_reviews()