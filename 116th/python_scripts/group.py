import pandas as pd

votes = pd.read_csv('../data/voteview/H116_votes.csv')
df = pd.read_csv('../data/senti.csv')
final = (df
         .groupby(['name', 'party', 'state', 'gender', 'born', 'bill_number'], as_index=False)
         .agg({'score1':'mean', 
               'tweet_id':'count',
               'rollnumber':'mean', 
               'clerk_rollnumber':'mean', 
               'icpsr':'mean'
               }
              )
         )

final['rollnumber'] = final['rollnumber'].astype(int)
final = pd.merge(final, votes, how='left', on=['rollnumber', 'icpsr'])

final.to_csv('../data/final.csv',sep=',', index=False, na_rep='')


