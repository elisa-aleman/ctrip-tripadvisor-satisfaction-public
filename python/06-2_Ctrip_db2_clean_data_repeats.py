#-*- coding: utf-8 -*-

from Paper3_Methods import *
import pandas
import os

def clean_hotel_repeats():
    hotel_path = make_data_path("ctrip/ctrip_db2/hotels.csv")
    hotels_df = pandas.read_csv(hotel_path)
    new_hotels_df = hotels_df.drop_duplicates(subset="HotelName", keep="last")
    rename_filepath = make_data_path("ctrip/ctrip_db2/OLD_hotels.csv")
    os.rename(hotel_path, rename_filepath)
    new_hotels_df.to_csv(hotel_path, index=False)

def clean_comment_repeats():
    comment_path = make_data_path("ctrip/ctrip_db2/comments.csv")
    comments_df = pandas.read_csv(comment_path)
    new_comments_df = comments_df.drop_duplicates(subset="CommentID", keep="last")
    rename_filepath = make_data_path("ctrip/ctrip_db2/OLD_comments.csv")
    os.rename(comment_path, rename_filepath)
    new_comments_df.to_csv(comment_path, index=False)

def clean_comment_segmented_kaotag():
    comment_path = make_data_path("ctrip/ctrip_db2/comments_segmented_kaotag.csv")
    comments_df = pandas.read_csv(comment_path)
    new_comments_df = comments_df.drop_duplicates(subset="CommentID", keep="last")
    rename_filepath = make_data_path("ctrip/ctrip_db2/OLD_comments_segmented_kaotag.csv")
    os.rename(comment_path, rename_filepath)
    new_comments_df.to_csv(comment_path, index=False)

def clean_comment_segmented():
    comment_path = make_data_path("ctrip/ctrip_db2/comments_segmented.csv")
    comments_df = pandas.read_csv(comment_path)
    new_comments_df = comments_df.drop_duplicates(subset="CommentID", keep="last")
    rename_filepath = make_data_path("ctrip/ctrip_db2/OLD_comments_segmented.csv")
    os.rename(comment_path, rename_filepath)
    new_comments_df.to_csv(comment_path, index=False)

def main():
    clean_hotel_repeats()
    clean_comment_repeats()
    clean_comment_segmented_kaotag()
    clean_comment_segmented()
    
if __name__ == '__main__':
    main()