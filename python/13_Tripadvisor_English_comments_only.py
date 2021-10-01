#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *
import langdetect

def detect_languages_ctrip_db():
    comment_path = make_data_path("tripadvisor/tripadvisor_db/comments.csv")
    comments_df = pandas.read_csv(comment_path)
    langs = []
    for row in comments_df.itertuples():
        text = row.comment
        if text!='':
            try:
                lang = langdetect.detect(text)
            except langdetect.lang_detect_exception.LangDetectException:
                lang = "undetermined"
            langs.append(lang)
    comments_df.insert(2,"language", langs)
    comments_df.to_csv(comment_path, index=False)

def make_english_comments_only():
    comments_df = get_Tripadvisor_comments_df()
    new_comments_df = comments_df[comments_df["language"]=="en"]
    new_comment_path = make_data_path("tripadvisor/tripadvisor_db/comments_english_only.csv")
    new_comments_df.to_csv(new_comment_path, index=False)

def main():
    detect_languages_ctrip_db()
    make_english_comments_only()
    
if __name__ == '__main__':
    main()