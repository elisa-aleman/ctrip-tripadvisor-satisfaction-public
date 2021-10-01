#-*- coding: utf-8 -*-

from Paper3_Methods import *
import matplotlib
import matplotlib.pyplot as plt

# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt

# ーーーーーーーーーーー
# ＊Stanford NLP Parser to Parse the grammatical dependencies of all texts, save it somewhere.
#
# ＊Identify Keywords that are adjectives, and keywords that are subjects
# >>>＊Split by price
# ＊For each price layer
#        ＊Count each non-adjective subject keyword
#        ＊For each adjective keyword
#        　　＊Collect the sentences that include this keyword（extract only positive texts for positive keywords)
#        　　＊SNLPP identify the noun that the adjective refers to, and count
#        　　＊Make a list of the pairs and the counts
#        　　＊Combine with original frequency lists for this price category
# ーーーーーーーーーーー

# >>> hotel_df.columns
# Index(['RID', 'Ctrip_HotelID', 'HotelName', 'EnglishHotelName', 'HotelScore',
#        'LocationScore', 'tripadvisor_hotel_id', 'ServicesScore',
#        'FacilitiesScore', 'HealthScore', 'HotelPrice', 'hotel_name',
#        'hotel_url', 'hotel_rating', 'city_id', 'postal_code', 'prefecture',
#        'locality', 'street', 'ext_address', 'address', 'price_lower',
#        'price_upper', 'rooms'],
#       dtype='object')

def main():
    hotel_df = Common_Hotels_with_price_df()
    hotel_df = hotel_df[['price_lower', 'price_upper']]
    hotel_df = hotel_df.rename(columns={'price_lower':'Lowest room price', 'price_upper':'Highest room price'})
    title = 'Price ranges for a single night distribution'
    max_price = hotel_df['Highest room price'].max() # 187444.0
    # bin_vers = [1,2,10,20,30,40,50]
    bin_vers = [1,2]
    for bin_ver in bin_vers:
        bins = get_price_bins(bin_ver=bin_ver)
        plt.close('all')
        fig, ax = plt.subplots()
        hotel_df.plot.hist(bins=bins, ax=ax, title=title, alpha=0.5, legend=True)
        ax.set_xlabel('Price in Yen')
        ax.set_ylabel('Hotels')
        # plt.show()
        dpi = 900
        if bin_ver in [1,2]:
            filepath = make_log_file("price_range_histograms/price_range_distribution_bins_ver_{}.png".format(bin_ver))
        else:
            filepath = make_log_file("price_range_histograms/price_range_distribution_{}_even_bins.png".format(bin_ver))
        fig.savefig(filepath, dpi=dpi)

if __name__ == '__main__':
    main()

