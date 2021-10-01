#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *
import string
import itertools

def split_sentences():
    data_path = make_data_path("ctrip/ctrip_db/comments_segmented_zh-cn_chinese_only.csv")
    comments_df = pandas.read_csv(data_path)
    # RID,HotelID,CommentID,Segmented_Comment
    splitchars=["。","！","？",".","!","?"]
    ins_table = []
    # RID,CommentID,SentenceNumber,Sentence
    limit = comments_df.shape[0]
    for ind,row in enumerate(comments_df.itertuples()):
        print("Segmenting comment {} of {}".format(ind+1,limit))
        text = row.Segmented_Comment
        # group by sentences using punctuation in splitchars as a border (leaves border as part of the list)
        split_text = [list(g) for k, g in itertools.groupby(text.split(), lambda x: x not in splitchars)]
        # remove border characters (splitchars)
        sentences = [i for i in split_text if i[0] not in splitchars]
        for sent_num,sentence in enumerate(sentences):
            sent_text = " ".join(sentence)
            ins_row = (row.HotelID,row.CommentID,sent_num+1,sent_text)
            ins_table.append(ins_row)
        up()
    down()
    print("Insert segmented sentences")
    ins_table_df = pandas.DataFrame(ins_table,columns=["HotelID","CommentID","SentenceNumber","Sentence"])
    ins_table_df.index += 1
    ins_table_df.index.name = 'RID'
    ins_path = make_data_path("ctrip/ctrip_db/sentences_zh-cn_chinese_only.csv")
    ins_table_df.to_csv(ins_path, index=True)

if __name__ == '__main__':
    split_sentences()