import csv
import json


def load_json_data(path):
    '''
    获取json文件
    :param path:
    :return:
    '''
    with open(path, 'r') as f:
        data = json.load(f)
        f.close()
    return data

def save_json_data(path, data):
    '''
    保存json文件
    :param path:
    :param data:
    :return:
    '''
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)
        f.close()

def load_csv_data(path):
    '''
    获取repo version time
    :param path:
    :return:
    '''
    repo_version_time = {}
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['repo'] in repo_version_time.keys():
                repo_version_time[row['repo']][row['version']] = row['time']
            else:
                version_time = {row['version']: row['time']}
                repo_version_time[row['repo']] = version_time
        f.close()
    return repo_version_time

def save_csv_data(path, headers, data):
    '''
    保存csv文件
    :param path:
    :param headers:
    :param data:
    :return:
    '''
    file=open(path, 'w', encoding='utf-8', newline='')
    writer=csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)

def get_commit_time(path, repo):
    '''
    获取 commit time
    :param repo:
    :param path:
    :return:
    '''

    commit_time = {}
    months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
              'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
    with open(path, 'r', encoding='utf8', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            times = row['ad'].strip().split(' ')
            # print(times)
            if repo == 'JDT':
                if '/' in row['ad']:
                    commit_time[row['commit']] = row['ad'].replace('/', '-').strip() + ':00 +0000'
                else:
                    commit_time[row['commit']] = row['ad'].strip()
            else:
                commit_time[row['commit']] = times[-2] + '-' + months[times[1]] + '-' + times[2] + ' ' + times[
                    3] + ' ' + times[5]
        file.close()
    return commit_time


def get_file_process_metrics(path):
    '''
    获取文件过程度量
    :param path:
    :return:
    '''

    file_metrics = {}

    with open(path, 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        for row in reader:
            # print(row)
            if row[0] == 'file':
                continue
            key = f"{row[0]}#{row[1]}"
            file_metrics[key] = row[2:]
        file.close()
    return file_metrics


