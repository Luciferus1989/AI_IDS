import pandas as pd
import os
from bow import bow_svm, bow_lr
from glove import glove_svm, glove_lr
from openread import open_csv_twitter, get_review_tabel, open_csv_big
from twit_prepare import preprocess_text, info


sts_gt_db = open_csv_twitter('lib/sts_gold_tweet.csv')
sts_gt_db['text'] = sts_gt_db['text'].apply(preprocess_text)
sts_gt_db.name = 'sts_gold_tweet'

if os.path.exists('amazon_data.csv'):
    review_db = pd.read_csv('amazon_data.csv')
    review_db.name = 'review_amazon'
else:
    review_db, review_db_unl = get_review_tabel()
    review_db['text'] = review_db['text'].apply(preprocess_text)
    review_db_unl['text'] = review_db_unl['text'].apply(preprocess_text)
    review_db.name = 'review_amazon'
    review_db_unl.name = 'review_amazon_unlabaled'
    review_db.to_csv('amazon_data.csv', index=False)


cln_data_db = open_csv_twitter('lib/twitter-2013train-A.csv')
cln_data_db['text'] = cln_data_db['text'].apply(preprocess_text)
cln_data_db.name = 'twitter-2013train-A'


db_list = [sts_gt_db, review_db, cln_data_db]
# db_list = [sts_gt_db, cln_data_db]
table_info = pd.DataFrame(columns=['Name', 'Row count', 'Positive', 'Negative'])
for i, df in enumerate(db_list):
    pos, neg = info(df)
    table_info.loc[i] = {'Name': df.name, 'Row count': len(df), 'Positive': pos, 'Negative': neg}


print(table_info)
db_name_list = ['sts_gold_tweet', 'review_amazon', 'twitter-2013train-A']
model_list = ['bowSVM', 'bowLR', 'gloveSVM', 'gloveLR']
model_f_list = [bow_svm, bow_lr, glove_svm, glove_lr]
model_table_info = pd.DataFrame(columns=['Name of model', 'sts_gold_tweet', 'review_amazon', 'twitter-2013train-A'])
for i, model in enumerate(model_f_list):
    row = {'Name of model': model_list[i]}
    for j, db in enumerate(db_list):
        trained_model, accuracy = model(db)
        row[db_name_list[j]] = f'{accuracy*100:.2f}%'
    model_table_info.loc[i] = row

print(model_table_info)




