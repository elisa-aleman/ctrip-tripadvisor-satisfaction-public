#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *
import langdetect

def detect_languages_ctrip_db():
    comment_path = make_data_path("ctrip/ctrip_db2/comments.csv")
    comments_df = pandas.read_csv(comment_path)
    langs = []
    for row in comments_df.itertuples():
        text = row.Comment
        if text!='':
            try:
                lang = langdetect.detect(text)
            except langdetect.lang_detect_exception.LangDetectException:
                lang = "undetermined"
            langs.append(lang)
    comments_df.insert(4,"Language", langs)
    rename_filepath = make_data_path("ctrip/ctrip_db2/OLD_comments.csv")
    os.rename(comment_path, rename_filepath)
    comments_df.to_csv(comment_path, index=False)

def make_chinese_comments_only():
    data_path = make_data_path("ctrip/ctrip_db2/comments.csv")
    comments_df = pandas.read_csv(data_path)
    new_comments_df = comments_df[comments_df["Language"]=="zh-cn"]
    new_comment_path = make_data_path("ctrip/ctrip_db2/comments_zh-cn_chinese_only.csv")
    new_comments_df.to_csv(new_comment_path, index=False)

def make_chinese_segmented_comments_only():
    data_path = make_data_path("ctrip/ctrip_db2/comments_zh-cn_chinese_only.csv")
    comments_df = pandas.read_csv(data_path)
    seg_path = make_data_path("ctrip/ctrip_db2/comments_segmented.csv")
    seg_df = pandas.read_csv(seg_path)
    new_seg_df = seg_df[seg_df.CommentID.isin(comments_df.CommentID)]
    new_seg_path = make_data_path("ctrip/ctrip_db2/comments_segmented_zh-cn_chinese_only.csv")
    new_seg_df.to_csv(new_seg_path,index=False)

def make_chinese_segmented_kaotag_comments_only():
    data_path = make_data_path("ctrip/ctrip_db2/comments_zh-cn_chinese_only.csv")
    comments_df = pandas.read_csv(data_path)
    seg_kao_path = make_data_path("ctrip/ctrip_db2/comments_segmented_kaotag.csv")
    seg_kao_df = pandas.read_csv(seg_kao_path)
    new_seg_kao_df = seg_kao_df[seg_kao_df.CommentID.isin(comments_df.CommentID)]
    new_seg_kao_path = make_data_path("ctrip/ctrip_db2/comments_segmented_kaotag_zh-cn_chinese_only.csv")
    new_seg_kao_df.to_csv(new_seg_kao_path,index=False)


def main():
    detect_languages_ctrip_db()
    make_chinese_comments_only()
    make_chinese_segmented_comments_only()
    make_chinese_segmented_kaotag_comments_only()

if __name__ == '__main__':
    main()