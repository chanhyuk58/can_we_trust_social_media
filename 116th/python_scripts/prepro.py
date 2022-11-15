import pandas as pd
import numpy as np

tw116_o = pd.read_csv("../data/raw/representatives-1.csv")
# print(list(tw116.columns.values))

tw116 = tw116_o[["created_at", "hashtags", "text","user_id", "user_name", "user_screen_name"]]
tw116 = tw116.dropna(subset=["hashtags"])

tw116['created_at'] = pd.to_datetime(
        arg=tw116['created_at'],
        format='%a %b %d %H:%M:%S %z %Y',
        errors='coerce'
        )

# All tweets ----
#tw116 = tw116[(tw116['created_at'] > '2008-01-01') & 
#        (tw116['created_at'] < '2022-12-31')
#        ]
#tw116 = tw116.sort_values(by=['created_at', 'user_id'])
#
#tw116.to_csv("../data/tw116_all.csv", sep=",",na_rep="NaN")

# Tweets during 116th ----
tw116 = tw116[(tw116['created_at'] > '2019-01-02') & 
        (tw116['created_at'] < '2021-01-03')]

tw116.to_csv("../data/tw116_during_116th.csv", sep=",",na_rep="NaN")

# Tweets during 115th & HR or Act included -----
tw116 = tw116[tw116['text'].str.contains(rf'\b(?:h|h\.|h |h\. )(?:r\.|r|r\. |r )[0-9]+\b|act', regex=True, case=False)]
tw116.to_csv("../data/tw116_during_116th_hract.csv", sep=",",na_rep="NaN")

