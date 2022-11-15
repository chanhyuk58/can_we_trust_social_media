import pandas as pd
import json

hr_list = ['hr' + str(i) for i in range(1, 7500)]

df = pd.DataFrame(columns=['bill_number', 'title', 
                           'introduced_at', 'sponsor', 
                           'status', 'passed_at'
                           , 'subject', 
                           'top_term'
                           ]
                  )
for hr in hr_list:
    try:
        with open(f'../data/propublica_bills/hr/{hr}/data.json') as f:
            temp = json.load(f)

        if 'house_passage_result_at' in temp['history']:
            dic1 = {'bill_number':temp['number'],
                    'title':temp['short_title'],
                    'introduced_at':temp['introduced_at'],
                    'status':temp['status'],
                    'passed_at':temp['history']['house_passage_result_at'],
                    'sponsor':temp['sponsor']['name'],
                    'subject':temp['subjects'],
                    'top_term':temp['subjects_top_term']
                    }

            df = df.append(dic1, ignore_index=True)
        else:
            # pass
            dic1 = {'bill_number':temp['number'],
                    'title':temp['short_title'],
                    'introduced_at':temp['introduced_at'],
                    'status':temp['status'],
                    'passed_at':'',
                    'sponsor':temp['sponsor']['name'],
                    'subject':temp['subjects'],
                    'top_term':temp['subjects_top_term']
                    }

            df = df.append(dic1, ignore_index=True)
    except:
        pass

# df['date'] = pd.to_datetime(arg=df['date'])
# df['date'] = df['date'].apply(lambda x: x.date())
# # df['date'] = pd.to_datetime(arg=df['date'])
# df['date'] = df['date'].astype(str)
# print(df['bill_number'])
df['bill_number'] = df['bill_number'].astype(int)

# df.to_csv('../data/bills(2).csv', sep=',', na_rep='', index=False)
rollcalls = pd.read_csv('../data/voteview/rollcalls2.csv')
# rollcalls['date'] = pd.to_datetime(arg=rollcalls['date'])
# rollcalls['date'] = rollcalls['date'].astype(str)
rollcalls['bill_number'] = rollcalls['bill_number'].astype(int)
# print(rollcalls['date'])
# print(rollcalls['bill_number'])

df = pd.merge(df, rollcalls, how='left', on=['bill_number'])
df = df[df['rollnumber'].notnull()]

df.to_csv('../data/bills.csv', sep=',', na_rep='', index=False)
              
