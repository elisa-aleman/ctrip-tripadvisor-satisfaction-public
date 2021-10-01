#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *

def segmented_words_to_comments():
    word_path = make_data_path("ctrip/ctrip_db/words_zh-cn_chinese_only.csv")
    word_df = pandas.read_csv(word_path)
    data_path = make_data_path("ctrip/ctrip_db/comments_zh-cn_chinese_only.csv")
    comments_df = pandas.read_csv(data_path)
    ###
    seg_group = word_df.groupby('CommentID')
    commentids = comments_df.CommentID.tolist()
    comment_to_hotel_dict = dict(zip(comments_df.CommentID,comments_df.HotelID))
    ins_table = []
    for cid in commentids:
        comment = seg_group.get_group(cid).Word.fillna('').tolist()
        seg_comment = " ".join(comment)
        hotelid = comment_to_hotel_dict[cid]
        ins_row = (hotelid,cid,seg_comment)
        ins_table.append(ins_row)
    com_seg_df = pandas.DataFrame(ins_table,columns=['HotelID', 'CommentID', 'Segmented_Comment'])
    com_seg_df.index += 1
    com_seg_df.index.name = 'RID'
    com_seg_path = make_data_path("ctrip/ctrip_db/comments_segmented_zh-cn_chinese_only.csv")
    com_seg_df.to_csv(com_seg_path, index=True)


def main():
    segmented_words_to_comments()
    
    
if __name__ == '__main__':
    main()