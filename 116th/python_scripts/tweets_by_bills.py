import pandas as pd
# import numpy as np
import re

df = pd.read_csv('../data/tw116_during_116th_hract.csv')
account_list = pd.read_csv('../R/accountlist2.csv')
bills = pd.read_csv('../data/bills.csv')

# bills['bill_number'].nunique

df = pd.merge(df, account_list, how='left', on='user_screen_name')

bills['introduced_at'] = pd.to_datetime(bills['introduced_at'])
bills['date'] = pd.to_datetime(arg=bills['date'])
bills['bill_number'] = bills['bill_number'].astype(int)

num_list = list(bills.bill_number)
# num_list = [1, 2, 3, 4, 5]

size = []
twt = []

for num in num_list:

    ### Set for search parameters: hr numbering and title ----
    hr = '\\b(?:h|h\.|h |h\. )(?:r\.|r|r\. |r )' + str(num) + '\\b'

    title = bills[bills.bill_number==num].title


    title = pd.DataFrame(title)
    title = title.iloc[0,0]
    title = re.sub(r'Act .+', 'Act', str(title))
    title_list = title.split()
    act = '(?:\s|)'.join(title_list)
    act = '#' + act 

    intro = bills[bills.bill_number==num].introduced_at
    intro = pd.DataFrame(intro).iloc[0,0]
    intro = str(intro)

    voted = bills[bills.bill_number==num].date
    voted = pd.DataFrame(voted).iloc[0,0]
    voted = str(voted)

    ### now subset tweets ----
    if title == 'nan':
        tw_hract = df[df.text.str.contains(rf'{hr}', regex=True, case=False)]
    else:
        tw_hract = df[df.text.str.contains(rf'{hr}|{act}', regex=True, case=False)]

    if voted == 'nan':
         tw_hract = tw_hract[(tw_hract.created_at >= intro)] 
    else:
        tw_hract = tw_hract[(tw_hract.created_at < voted) & 
            (tw_hract.created_at >= intro)]

    tw_hract['bill_number'] = ''
    tw_hract['bill_number'] = num
    rollnumber = bills.loc[bills['bill_number']==num, 'clerk_rollnumber']
    rollnumber = pd.DataFrame(rollnumber).iloc[0,0]
    tw_hract['clerk_rollnumber'] = ''
    tw_hract['clerk_rollnumber'] = rollnumber
    rollnumber2 = bills.loc[bills['bill_number']==num, 'rollnumber']
    rollnumber2 = pd.DataFrame(rollnumber2).iloc[0,0]
    tw_hract['rollnumber'] = ''
    tw_hract['rollnumber'] = rollnumber2
    
    if tw_hract.empty:
        pass
    else:
        tw_hract2 = tw_hract.values.tolist()
        twt = twt + tw_hract2
    ### collect data size ----
    data_size = str(tw_hract.shape[0])
    size = size + [[num, data_size]]


size = pd.DataFrame(size, columns=['bill_number', 'size'])
twt = pd.DataFrame(twt, columns=['tweet_id', 'created_at', 'hashtags', 'text', 
                                 'user_id', 'user_name', 'user_screen_name', 
                                 'state', 'party', 'last_name', 'name', 
                                 'gender', 'state_abbrev', 'icpsr', 'born', 
                                 'bill_number', 'clerk_rollnumber', 'rollnumber']
                   )
#### Split data into test and normal ####
twt = twt.sample(frac=1, random_state=1066).reset_index(drop=True)
print(len(twt))
twt_test = twt[int((len(twt)+1)*.80):]
print(len(twt_test))
twt = twt[:int((len(twt)+1)*.80)]
print(len(twt))

size.to_csv('../data/tweet_by_bills.csv',sep=',', na_rep='', index=False)
twt.to_csv('../data/twt.csv',sep=',', na_rep='', index=False)
twt_test.to_csv('../data/twt_test.csv',sep=',', na_rep='', index=False)




