import json
import pandas as pd
import os
import csv

# column_names = [
#     'Timestamp', 'DPC Rate', '% Idle Time', '% C3 Time', '% Interrupt Time',
#     '% C2 Time', '% User Time', '% C1 Time', '% Processor Time', 'C1 Transitions/sec',
#     '% DPC Time', 'C2 Transitions/sec', '% Privileged Time', 'C3 Transitions/sec',
#     'DPCs Queued/sec', 'Interrupts/sec', 'Pool Paged Bytes', 'IO Read Operations/sec',
#     'Working Set - Private', 'Working Set Peak', 'IO Write Operations/sec', 'Page File Bytes',
#     '% User Time (Process _Total)', 'Virtual Bytes Peak', 'Page File Bytes Peak',
#     'IO Other Bytes/sec', 'Private Bytes', 'IO Write Bytes/sec', 'Elapsed Time',
#     'Virtual Bytes', '% Processor Time (Process _Total)', 'Creating Process ID',
#     'Pool Nonpaged Bytes', 'Working Set (Process _Total)', 'Page Faults/sec',
#     'ID Process', 'IO Other Operations/sec', 'IO Data Operations/sec', 'Thread Count',
#     '% Privileged Time (Process _Total)', 'IO Data Bytes/sec', 'IO Read Bytes/sec',
#     'Priority Base', 'Handle Count', 'TCP RSC Average Packet Size (Teredo Tunneling Pseudo-Interface)',
#     'TCP RSC Average Packet Size (isatap.{E14F6981-3B33-403B-8A47-88F61C9C453E})',
#     'TCP RSC Average Packet Size (Intel[R] 82574L Gigabit Network Connection)',
#     'TCP RSC Average Packet Size (isatap.localdomain)', 'Packets Received Unknown (Teredo Tunneling Pseudo-Interface)',
#     'Packets Received Unknown (isatap.{E14F6981-3B33-403B-8A47-88F61C9C453E})',
#     'Packets Received Unknown (Intel[R] 82574L Gigabit Network Connection)',
#     'Packets Received Unknown (isatap.localdomain)', 'Bytes Received/sec (Teredo Tunneling Pseudo-Interface)',
#     'Bytes Received/sec (isatap.{E14F6981-3B33-403B-8A47-88F61C9C453E})',
#     'Bytes Received/sec (Intel[R] 82574L Gigabit Network Connection)',
#     'Bytes Received/sec (isatap.localdomain)', 'Bytes Sent/sec (Teredo Tunneling Pseudo-Interface)',
#     'Bytes Sent/sec (isatap.{E14F6981-3B33-403B-8A47-88F61C9C453E})',
#     'Bytes Sent/sec (Intel[R] 82574L Gigabit Network Connection)',
#     'Bytes Sent/sec (isatap.localdomain)', 'Packets Outbound Errors (Teredo Tunneling Pseudo-Interface)',
#     'Packets Outbound Errors (isatap.{E14F6981-3B33-403B-8A47-88F61C9C453E})',
#     'Packets Outbound Errors (Intel[R] 82574L Gigabit Network Connection)',
#     'Packets Outbound Errors (isatap.localdomain)', 'Packets Received Discarded (Teredo Tunneling Pseudo-Interface)',
#     'Packets Received Discarded (isatap.{E14F6981-3B33-403B-8A47-88F61C9C453E})',
#     'Packets Received Discarded (Intel[R] 82574L Gigabit Network Connection)',
#     'Packets Received Discarded (isatap.localdomain)', 'Bytes Total/sec (Teredo Tunneling Pseudo-Interface)',
#     'Bytes Total/sec (isatap.{E14F6981-3B33-403B-8A47-88F61C9C453E})',
#     'Bytes Total/sec (Intel[R] 82574L Gigabit Network Connection)',
#     'Bytes Total/sec (isatap.localdomain)', 'Packets Outbound Discarded (Teredo Tunneling Pseudo-Interface)',
#     'Packets Outbound Discarded (isatap.{E14F6981-3B33-403B-8A47-88F61C9C453E})',
#     'Packets Outbound Discarded (Intel[R] 82574L Gigabit Network Connection)',
#     'Packets Outbound Discarded (isatap.localdomain)', 'TCP RSC Exceptions/sec (Teredo Tunneling Pseudo-Interface)',
#     'TCP RSC Exceptions/sec (isatap.{E14F6981-3B33-403B-8A47-88F61C9C453E})',
#     'TCP RSC Exceptions/sec (Intel[R] 82574L Gigabit Network Connection)',
#     'TCP RSC Exceptions/sec (isatap.localdomain)', 'Packets Sent Unicast/sec (Teredo Tunneling Pseudo-Interface)'
# ]


def open_csv_file(file_name, label):
    with open(file_name, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        header = next(reader)
        lines = list(reader)
    data = pd.DataFrame(lines, columns=header)
    data.columns = ([data.columns[0]] +
                    [column.split('\\')[-2] +
                     '|' + column.split('\\')[-1].replace('% ', '') for column in data.columns[1:]])
    data[label] = label
    return data


def combine_normal():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    normal = [('Dataset_Iot/Normal/win7_normal_2.csv', 'normal'),
              ('Dataset_Iot/Normal/win7_normal_3.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_1.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_2.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_3.csv', 'normal'),
              ('Dataset_Iot/Normal/win10_normal_4.csv', 'normal')]
    df = [open_csv_file(os.path.join(current_directory, file), _) for file, _ in normal]
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
    # for base in [backdoor, ddos, dos, infection, mitm, password, runsomware, scanning, xss]:
    df = [open_csv_file(os.path.join(current_directory, file), label)
          for base in [backdoor, ddos, dos, infection, mitm, password, runsomware, scanning, xss] for file, label in base]

    return pd.concat(df, ignore_index=True)

