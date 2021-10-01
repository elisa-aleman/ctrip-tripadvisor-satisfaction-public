#-*- coding: utf-8 -*-

from Paper3_Methods import *
import os


def clean_comment_repeats():
    comment_path = make_data_path("ctrip/ctrip_db/comments.csv")
    comments_df = pandas.read_csv(comment_path)
    new_comments_df = comments_df.drop_duplicates(subset="CommentID", keep="last")
    rename_filepath = make_data_path("ctrip/ctrip_db/OLD_comments.csv")
    os.rename(comment_path, rename_filepath)
    new_comments_df.to_csv(comment_path, index=False)

def clean_hotel_repeats():
    hotel_path = make_data_path("ctrip/ctrip_db/hotels.csv")
    hotels_df = pandas.read_csv(hotel_path)
    new_hotels_df = hotels_df.drop_duplicates(subset="HotelName", keep="last")
    rename_filepath = make_data_path("ctrip/ctrip_db/OLD_hotels.csv")
    os.rename(hotel_path, rename_filepath)
    new_hotels_df.to_csv(hotel_path, index=False)

# def clean_words_repeats():
#     word_path = make_data_path("ctrip/ctrip_db/words.csv")
#     word_df = pandas.read_csv(word_path)
#     new_word_df = word_df.drop_duplicates(subset=['CommentID', 'WordNumber', 'Word'], keep="last")
#     rename_filepath = make_data_path("ctrip/ctrip_db/OLD_words.csv")
#     os.rename(word_path, rename_filepath)
#     new_word_df.to_csv(word_path, index=False)

# def clean_sentences_repeats():
#     sentence_path = make_data_path("ctrip/ctrip_db/sentences.csv")
#     sentence_df = pandas.read_csv(sentence_path)
#     new_sentence_df = sentence_df.drop_duplicates(subset=['CommentID','SentenceNumber','Sentence'], keep="last")
#     rename_filepath = make_data_path("ctrip/ctrip_db/OLD_sentences.csv")
#     os.rename(sentence_path, rename_filepath)
#     new_sentence_df.to_csv(sentence_path, index=False)

def main():
    clean_comment_repeats()
    clean_hotel_repeats()
    # clean_words_repeats()
    # clean_sentences_repeats()
    
if __name__ == '__main__':
    main()