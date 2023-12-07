import json
import pandas as pd
import os
import csv


def open_csv_file(file_name, label):
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        lines = list(reader)
    data = pd.DataFrame(lines, columns=header)
    data.columns = ([data.columns[0]] +
                    [column.split('\\')[-2] +
                     '|' + column.split('\\')[-1].replace('% ', '') for column in data.columns[1:]])
    data['Label'] = label
    if 'Label' in data.columns:
        print(label)
    return data


def combine_normal():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    normal = [('Dataset_Iot/Normal/win7_normal_2.csv', 'normal'),
              ('Dataset_Iot/Normal/win7_normal_3.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_1.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_2.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_3.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_4.csv', 'normal')]
    df = [open_csv_file(os.path.join(current_directory, file), label) for file, label in normal]
    normal = pd.concat(df, ignore_index=True)
    return normal


def combine_attack():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    backdoor = [('Dataset_Iot/Backdoor/win7_backdoor_normal_1.csv', 'backdoor'),
                ('Dataset_Iot/Backdoor/win7_backdoor_normal_2.csv', 'backdoor')]
    ddos = [('Dataset_Iot/DDos/win7_DDoS_normal_1.csv', 'DDoS'),
            ('Dataset_Iot/DDos/win10_DDoS_normal_1.csv', 'DDoS')]
    dos = [('Dataset_Iot/Dos/win7_DoS_normal_1.csv', 'dos'),
           ('Dataset_Iot/Dos/win10_DoS_normal_1.csv', 'dos')]
    infection = [('Dataset_Iot/Infection/win7_injection_normal_1.csv', 'infection'),
                 ('Dataset_Iot/Infection/win10_injection_normal_1.csv', 'infection')]
    mitm = [('Dataset_Iot/MITM/win7_MIMT_normal_1.csv', 'mitm'),
            ('Dataset_Iot/MITM/win10_MITM_normal_1.csv', 'mitm')]
    password = [('Dataset_Iot/Password/win7_password_normal_1.csv', 'password'),
                ('Dataset_Iot/Password/win10_password_normal_1.csv', 'password')]
    runsomware = [('Dataset_Iot/Runsomware/win7_runsomware_normal_1.csv', 'runsomware'),
                  ('Dataset_Iot/Runsomware/win7_runsomware_normal_2.csv', 'runsomware'),
                  ('Dataset_Iot/Runsomware/win7_runsomware_normal_3.csv', 'runsomware')]
    scanning = [('Dataset_Iot/Scanning/win7_scanning_normal_1.csv', 'scanning'),
                ('Dataset_Iot/Scanning/win10_scanning_normal_1.csv', 'scanning'),
                ('Dataset_Iot/Scanning/win10_scanning_normal_2.csv', 'scanning'),
                ('Dataset_Iot/Scanning/win10_scanning_normal_3.csv', 'scanning')]
    xss = [('Dataset_Iot/XSS/win7_XSS_normal_1.csv', 'xss'),
           ('Dataset_Iot/XSS/win10_XSS_normal_1.csv', 'xss')]
    df = [open_csv_file(os.path.join(current_directory, file), label)
          for base in [backdoor, ddos, dos, infection, mitm, password, runsomware, scanning, xss]
          for file, label in base]

    return pd.concat(df, ignore_index=True)


def clean_null_rows(df):
    count_null_values = df.isnull().sum(axis=1)
    df = pd.concat([df, count_null_values.rename('sum of null')], axis=1)
    # df['sum of null'] = count_null_values
    print("Max null in row:", df['sum of null'].max())
    print("Min null in row:", df['sum of null'].min())
    print("Average null in row:", df['sum of null'].mean())
    print('Rows with sum of null values more then {} was cleaned'.format(df['sum of null'].mean()))
    df = df[(df['sum of null'] < df['sum of null'].mean())]
    df = df.drop(columns=['sum of null'])
    return df


def clean_na(df):
    df.replace('', pd.NA, inplace=True)
    df.fillna(0, inplace=True)
    df.replace(' ', pd.NA, inplace=True)
    df.fillna(0, inplace=True)
    return df


def common_type(df):
    for i in df.columns:
        main_data_type = df[i].apply(type).mode().iloc[0]
        if main_data_type == int or main_data_type == float:
            df[i] = df[i].astype(float)
        else:
            df[i] = df[i].astype(main_data_type)
            df.replace('', pd.NA, inplace=True)
            df.fillna(0, inplace=True)
            df.replace(' ', pd.NA, inplace=True)
            df.fillna(0, inplace=True)
    return df
