#-*- coding: utf-8 -*-

from Paper3_Methods import *
from Tripadvisor_Methods import *

def reorganize_hotel_df():
    # Load Old hotel main
    old_hotel_main_df = pandas.read_csv(make_data_path("tripadvisor/OLD/hotel_main.csv"))
    old_hotel_main_df.rename(columns={"id":"hotel_id", "name":"hotel_name","url":"hotel_url","rating":"hotel_rating"}, inplace=True)
    old_hotel_main_df.drop(columns=["incorrect_ID"], inplace=True)
    # Load Old hotel added data
    old_hotel_price_df = pandas.read_csv(make_data_path("tripadvisor/OLD/hotel_address_price_rooms.csv"))
    # Merge
    hotel_df = pandas.merge(old_hotel_main_df, old_hotel_price_df, on="hotel_id")
    hotel_df.rename(columns={"city_ID":"city_id"}, inplace=True)
    data_path = make_data_path("tripadvisor/tripadvisor_db/hotels.csv")
    hotel_df.to_csv(data_path, index=False)

def reorganize_comments_df():
    old_reviews_df = pandas.read_csv(make_data_path("tripadvisor/OLD/reviews.csv"))
    old_reviews_df.drop(columns=["incorrect_ID"], inplace=True)
    old_reviews_df.rename(columns={"id":"comment_id","hotel_ID":"hotel_id","text":"comment","rating":"score"}, inplace=True)
    comments_df = old_reviews_df[["hotel_id","username","comment_id","comment","score","date"]]
    data_path = make_data_path("tripadvisor/tripadvisor_db/comments.csv")
    comments_df.to_csv(data_path, index=False)

def reorganize_training_data():
    training_path = make_data_path("tripadvisor/SVM_training/training_sentences.csv")
    training_df = pandas.read_csv(training_path)
    training_df.drop(columns=["rowid","username","score"], inplace=True)
    training_df = training_df[['hotel_id','comment_id','sentence','emotion_val','date']]
    sentence_nums = []
    cur_comment_id = 0
    sent_num = 1
    for row in training_df.itertuples():
        if row.comment_id == cur_comment_id:
            sent_num += 1
        else:
            sent_num = 1
            cur_comment_id = row.comment_id
        sentence_nums.append(sent_num)
    training_df.insert(2, "sentence_num", sentence_nums)
    training_df.to_csv(training_path, index=False)

def remove_neutral_training_data():
    training_path = make_data_path("tripadvisor/SVM_training/training_sentences.csv")
    training_df = pandas.read_csv(training_path)
    training_df = training_df[training_df.emotion_val!=0]
    training_df["emotion_val"] = training_df["emotion_val"].map({1:1,-1:0})
    new_training_path = make_data_path("tripadvisor/SVM_training/training_sentences_posi_nega.csv")
    training_df.to_csv(new_training_path, index=False)
    
def main():
    # reorganize_hotel_df()
    # reorganize_comments_df()
    # reorganize_training_data()
    # remove_neutral_training_data()

if __name__ == '__main__':
    main()
