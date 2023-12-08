def open_csv_file(file_name, label):
    """
    Opens a CSV file, adjusts column names, adds a 'Label' column, and returns a DataFrame.
    :param file_name: Path to the CSV file locally
    :param label: Label to be assigned to the 'Label' column.
    :return: pd.DataFrame: DataFrame containing data from the CSV file.
    """
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        lines = list(reader)
    data = pd.DataFrame(lines, columns=header)
    data.columns = ([data.columns[0]] +
                    [column.split('\\')[-2] +
                     '|' + column.split('\\')[-1].replace('% ', '') for column in data.columns[1:]])
    data['Label'] = label

    return data

def combine_data_from_files(file_label_tuples):
    """
    Combines data from a list of file label tuples..
    :param file_label_tuples: List of tuples containing file paths and labels.
    :return: Combined DataFrame containing data from files.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    data_frames = [open_csv_file(os.path.join(current_directory, file), label) for file, label in file_label_tuples]
    combined_df = pd.concat(data_frames, ignore_index=True)
    return combined_df


def combine_normal():
    """
    Combine normal dataset
    :return: Combined DataFrame containing normal data.
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    normal_files = [('Dataset_Iot/Normal/win7_normal_2.csv', 'normal'),
              ('Dataset_Iot/Normal/win7_normal_3.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_1.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_2.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_3.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_4.csv', 'normal')]
    return combine_data_from_files(normal_files)


def combine_attack():
    """
    Combine dataset with attacks
    :return: Combined DataFrame containing attacks data.
    """
    attack_files = [('Dataset_Iot/Backdoor/win7_backdoor_normal_1.csv', 'backdoor'),
                    ('Dataset_Iot/Backdoor/win7_backdoor_normal_2.csv', 'backdoor'),
                    ('Dataset_Iot/DDos/win7_DDoS_normal_1.csv', 'DDoS'),
                    ('Dataset_Iot/DDos/win10_DDoS_normal_1.csv', 'DDoS'),
                    ('Dataset_Iot/Dos/win7_DoS_normal_1.csv', 'dos'),
                    ('Dataset_Iot/Dos/win10_DoS_normal_1.csv', 'dos'),
                    ('Dataset_Iot/Infection/win7_injection_normal_1.csv', 'infection'),
                    ('Dataset_Iot/Infection/win10_injection_normal_1.csv', 'infection'),
                    ('Dataset_Iot/MITM/win7_MIMT_normal_1.csv', 'mitm'),
                    ('Dataset_Iot/MITM/win10_MITM_normal_1.csv', 'mitm'),
                    ('Dataset_Iot/Password/win7_password_normal_1.csv', 'password'),
                    ('Dataset_Iot/Password/win10_password_normal_1.csv', 'password'),
                    ('Dataset_Iot/Runsomware/win7_runsomware_normal_1.csv', 'runsomware'),
                    ('Dataset_Iot/Runsomware/win7_runsomware_normal_2.csv', 'runsomware'),
                    ('Dataset_Iot/Runsomware/win7_runsomware_normal_3.csv', 'runsomware'),
                    ('Dataset_Iot/Scanning/win7_scanning_normal_1.csv', 'scanning'),
                    ('Dataset_Iot/Scanning/win10_scanning_normal_1.csv', 'scanning'),
                    ('Dataset_Iot/Scanning/win10_scanning_normal_2.csv', 'scanning'),
                    ('Dataset_Iot/Scanning/win10_scanning_normal_3.csv', 'scanning'),
                    ('Dataset_Iot/XSS/win7_XSS_normal_1.csv', 'xss'),
                    ('Dataset_Iot/XSS/win10_XSS_normal_1.csv', 'xss')
                    ]
    return combine_data_from_files(attack_files)


def clean_null_rows(df):
    """
    Cleans rows with null values in a DataFrame.
    :param df: Input DataFrame.
    :return: Cleaned DataFrame without rows where sum of null values is lower than average.
    """
    df = df.drop(df.columns[0], axis=1)
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
    """
    Replace NA values in a DataFrame.
    :param df: Input DataFrame.
    :return: DataFrame with cleaned NA values.
    """
    df.replace('', pd.NA, inplace=True)
    df.fillna(0, inplace=True)
    df.replace(' ', pd.NA, inplace=True)
    df.fillna(0, inplace=True)
    return df


def common_type(df):
    """
    Converts each column to a common data type in the column and change '', ' ' to 0.
    :param df: Input DataFrame.
    :return: DataFrame.
    """
    for i in df.columns:
        main_data_type = df[i].apply(type).mode().iloc[0]
        if main_data_type == int or main_data_type == float:
            df[i] = df[i].astype(float)
        else:
            df.replace('', pd.NA, inplace=True)
            df.fillna(0, inplace=True)
            df.replace(' ', pd.NA, inplace=True)
            df.fillna(0, inplace=True)
            df[i] = df[i].astype(main_data_type)

    return df
