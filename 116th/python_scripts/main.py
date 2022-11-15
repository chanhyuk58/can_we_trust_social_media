###### This is the Python Script Execution file ######

#### (1) Subset Relavent Tweets from Raw ####
# input = tweets raw file
# output = tweets_during_115_hract.csv
import prepro

#### (2-1) Construct Bills data ####
# input = ProPublica bills file
#         VoteView bills - roll call dataset
# output = bills2
import bills

#### (2-2-1) Execute Sentiment Score Analysis ####
# input = tweets data from (1) + roBERTa model
# output = senti.csv (tweets data with sentiment score)
#          account_list.csv (account list in tweets)
import sentiment

#### (2-2-2) Account list -> R + Manual ####

#### (3) Split tweets by Bills ####
# input = senti.csv from (2-2)
#         bills2.csv from (2-1)
#         account_list2.csv
# output = tweets splitted by hr_id (ex. hr1.csv)
import tweets_by_bills

#### (4) Sentiment Score By Reps and Bills + Roll call vote records ####
# input = tweets splitted by hr_id (3)
#         VoteView roll call vote records
# output = aggregated data by bills (ex. hr1.csv)
#          final.csv
