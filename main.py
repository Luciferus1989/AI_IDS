import os
from CNN import CNN
from openread import combine_normal, combine_attack, clean_null_rows, common_type
import pandas as pd

if os.path.isfile('df.csv'):
    df = pd.read_csv('df.csv', low_memory=False)
else:
    if os.path.isfile('normal.csv'):
        print('Fail {} is founded in dir.'.format('normal.csv'))
        df_normal = pd.read_csv('normal.csv', low_memory=False)
    else:
        df_normal = combine_normal()
        df_normal.to_csv('normal.csv', index=False)

    if os.path.isfile('attack.csv'):
        print('Fail {} is founded in dir.'.format('attack.csv'))
        df_attack = pd.read_csv('attack.csv', low_memory=False)
    else:
        df_attack = combine_attack()
        df_attack.to_csv('attack.csv', index=False)
    df = pd.concat([df_normal, df_attack], ignore_index=True)
    print(df.shape)
    df = clean_null_rows(df)
    df = common_type(df)
    print(df.shape)
    df.to_csv('df.csv', index=False)
df = df.drop(df.columns[0], axis=1)
cnn = CNN(df)
cnn.train(10, 24)

