#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *
from EntropyBasedSVM.Kaomoji_parsing.Kaomoji import *
from EntropyBasedSVM.StanfordCoreNLP_Chinese.StanfordCoreNLP import *

def PreliminarySegmentation():
    data_path = make_data_path("ctrip/ctrip_db2/comments.csv")
    comments_df = pandas.read_csv(data_path)
    k_dict = getKaomojiDict()
    print("Preparing Comments for segmentation (kaomoji tag)")
    ins_kao = []
    limit = comments_df.shape[0]
    for ind,row in enumerate(comments_df.itertuples()):
        print("Segmenting comment {} of {}".format(ind+1,limit))
        text = row.Comment
        if text:
            text_tagged = Kaomoji_totag(text, k_dict)
            #
            seg_text = Segment(text_tagged, sent_split=False, tolist=False, chinese_only=True)
            seg_text_tagged = Segmented_tagged(seg_text)
        else:
            seg_text_tagged = text
        # HotelID,CommentPage,CommentID,Segmented_Comment
        ins_kao_row = (row.HotelID,row.CommentPage,CommentID,seg_text_tagged)
        ins_kao.append(ins_kao_row)
        up()
    down()
    print("Insert segmented with tags for kaomoji")
    ins_kao_df = pandas.DataFrame(ins_kao,columns=['HotelID','CommentPage','CommentID','Segmented_Comment'])
    ins_kao_df.index += 1
    ins_kao_df.index.name = 'RID'
    ins_path = make_data_path("ctrip/ctrip_db2/comments_segmented_kaotag.csv")
    ins_kao_df.to_csv(ins_path, index=True)
    ############
    print("Preparing Comments for Kaomoji replacement and SQL insertion")
    ins = []
    for item in ins_kao:
        seg_text_tagged = item[3]
        segmented = KaoTag_toKaomoji(seg_text_tagged, k_dict)
        ins_row = (item[0],item[1],item[2],segmented)
        ins.append(ins_row)
    ins_df = pandas.DataFrame(ins,columns=['HotelID','CommentPage','CommentID','Segmented_Comment'])
    ins_df.index += 1
    ins_df.index.name = 'RID'
    ins_path = make_data_path("ctrip/ctrip_db2/comments_segmented.csv")
    ins_df.to_csv(ins_path, index=True)
    ############
    print("Done")

if __name__ == "__main__":
    PreliminarySegmentation()