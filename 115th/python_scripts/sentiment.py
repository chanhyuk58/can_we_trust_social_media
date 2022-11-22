from transformers import AutoModelForSequenceClassification
# from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
import pandas as pd 
from scipy.special import softmax
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score


# from transformers import pipeline
import time

st = time.time()
# Preprocess text (username and link placeholders)
def preprocess(text):
    new_text = []
    for t in text.split(' '):
        t = '@user' if t.startswith('@') and len(t) > 1 else t
        t = 'http' if t.startswith('http') else t
        new_text.append(t)
    return ' '.join(new_text)

MODEL = f'cardiffnlp/twitter-roberta-base-sentiment-latest'
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)

model = AutoModelForSequenceClassification.from_pretrained(MODEL)

def sentiment(target):
    text = preprocess(target)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    conditions = [
            (scores[0] > scores[2]) & 
            (scores[0] > scores[1]),
            (scores[2] > scores[0]) &
            (scores[2] > scores[1]),
            (scores[1] >= scores[0]) &
            (scores[1] >= scores[2]),
           ]
    values = [-1, 1, 0]
    score1 = np.select(conditions, values)
    return score1

### Load test data ###
df_test = pd.read_csv('../data/twt_test.csv')
X = df_test['text']
y = df_test['score1']
y_hat = X.apply(sentiment)
accu = accuracy_score(y, y_hat)
f1 = f1_score(y, y_hat, average=None)
score = [accu, f1]
score = pd.DataFrame(score)
score.to_csv('../data/test_scores.csv', sep=',', index=False, na_rep='')


### Load data ###
df = pd.read_csv('../data/twt.csv')
print(df.shape)

senti = df['text'].apply(sentiment)
df['score1'] = ''

for i in range(0,len(df)):
    df.loc[i,'score1'] = senti[i]

df = pd.concat([df,df_test], axis=0)
df.to_csv('../data/senti.csv', sep=',', index=False, na_rep='')

elapsed_time = time.time() - st
print(time.strftime('%H:%M:%S', time.gmtime(elapsed_time)))

# account_list_115 = df['user_screen_name'].unique()
# account_list_115 = pd.DataFrame(account_list_115, columns=['user_screen_name'])
# account_list_115.to_csv('../R/data/account_list_115.csv', sep=',', index=False, na_rep='')


