#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Ctrip_Methods import *
import langdetect

def detect_languages_ctrip_db():
    data_path = make_data_path("ctrip/ctrip_db/comments.csv")
    comments_df = pandas.read_csv(data_path)
    langs = []
    for row in comments_df.itertuples():
        text = row.Comment
        if text!='':
            try:
                lang = langdetect.detect(text)
            except langdetect.lang_detect_exception.LangDetectException:
                lang = "undetermined"
            langs.append(lang)
    comments_df.insert(3,"Language", langs)
    comments_df.to_csv(comment_path, index=False)

def make_chinese_comments_only():
    data_path = make_data_path("ctrip/ctrip_db/comments.csv")
    comments_df = pandas.read_csv(data_path)
    new_comments_df = comments_df[comments_df["Language"]=="zh-cn"]
    new_comment_path = make_data_path("ctrip/ctrip_db/comments_zh-cn_chinese_only.csv")
    new_comments_df.to_csv(new_comment_path, index=False)

def make_chinese_words_only():
    data_path = make_data_path("ctrip/ctrip_db/comments_zh-cn_chinese_only.csv")
    comments_df = pandas.read_csv(data_path)
    word_path = make_data_path("ctrip/ctrip_db/words.csv")
    word_df = pandas.read_csv(word_path)
    new_word_df = word_df[word_df.CommentID.isin(comments_df.CommentID)]
    new_word_path = make_data_path("ctrip/ctrip_db/words_zh-cn_chinese_only.csv")
    new_word_df.to_csv(new_word_path,index=False)


def main():
    detect_languages_ctrip_db()
    make_chinese_comments_only()
    make_chinese_words_only()
    
if __name__ == '__main__':
    main()