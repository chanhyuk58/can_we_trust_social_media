import pandas as pd
import numpy as np

tw115_o = pd.read_csv("../data/raw/representatives-1.csv")
# print(list(tw115.columns.values))

tw115 = tw115_o[["created_at", "hashtags", "text","user_id", "user_name", "user_screen_name"]]
tw115 = tw115.dropna(subset=["hashtags"])

tw115['created_at'] = pd.to_datetime(
        arg=tw115['created_at'],
        format='%a %b %d %H:%M:%S %z %Y',
        errors='coerce'
        )

# # All tweets ----
# tw115 = tw115[(tw115['created_at'] > '2008-01-01') & 
#         (tw115['created_at'] < '2022-12-31')
#         ]
# tw115 = tw115.sort_values(by=['created_at', 'user_id'])
# 
# tw115.to_csv("../data/tw115_all.csv", sep=",",na_rep="NaN")
# 
# # Tweets until 115th ----
# tw115 = tw115[(tw115['created_at'] > '2008-01-01') & 
#         (tw115['created_at'] < '2019-01-03')
#         ]
# tw115.to_csv("../data/tw115_until_115th.csv", sep=",",na_rep="NaN")

# Tweets during 115th ----
tw115 = tw115[(tw115['created_at'] > '2017-01-02') & 
        (tw115['created_at'] < '2019-01-03')]

tw115.to_csv("../data/tw115_during_115th.csv", sep=",",na_rep="NaN")

# Tweets during 115th & HR or Act included -----
tw115 = tw115[tw115['text'].str.contains(rf'\b(?:h|h\.|h |h\. )(?:r\.|r|r\. |r )[0-9]+\b|act', regex=True, case=False)]
tw115.to_csv("../data/tw115_during_115th_hract.csv", sep=",",na_rep="NaN")

