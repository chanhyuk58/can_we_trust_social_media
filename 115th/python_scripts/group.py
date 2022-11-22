import pandas as pd

votes = pd.read_csv('../data/voteview/H115_votes.csv')
df = pd.read_csv('../data/senti.csv')
df['introduced_at2'] = pd.to_datetime(df['introduced_at']).astype(int)
df['voted_at2'] = pd.to_datetime(df['voted_at']).astype(int)
df['created_at2'] = pd.to_datetime(df['created_at']).astype(int)
final = (df
         .groupby(['name', 'party', 'state', 'gender', 'born', 'bill_number'], 
                  as_index=False)
         .agg({'score1':'mean', 
               'tweet_id':'count',
               'rollnumber':'mean', 
               'clerk_rollnumber':'mean', 
               'icpsr':'mean',
               'created_at2':'min',
               'introduced_at2':'mean'
               }
              )
         )
final['created_at'] = pd.to_datetime(final['created_at2'])
final['introduced_at'] = pd.to_datetime(final['introduced_at2'])

final['rollnumber'] = final['rollnumber'].astype(int)
final = pd.merge(final, votes, how='left', on=['rollnumber', 'icpsr'])

final.to_csv('../data/final.csv',sep=',', index=False, na_rep='')




