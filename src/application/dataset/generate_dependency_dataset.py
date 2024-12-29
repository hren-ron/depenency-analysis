import os

from globalLog import logger
from tools.process_csv_file import load_json_data, save_csv_data


def get_features(depend_data, java_files, i, k, data, flag):
    # 使用字典映射来简化条件判断
    offset_map = {
        'depend': 2 * i + 3,
        'dependby': 2 * i + 4
    }

    for file, num in depend_data.items():
        file = file + '#' + str(k)
        if file not in java_files:
            continue
        index = java_files.index(file)
        if flag in offset_map:
            data[index][offset_map[flag]] = num
        else:
            raise ValueError("Invalid flag")
    return data


def get_labels(path, java_files, k, data, flag):
    if os.path.exists(path):
        blocking_file_nums = load_json_data(path)
        for file, num in blocking_file_nums.items():
            file = file + '#' + str(k)
            if file not in java_files:
                continue
            index = java_files.index(file)
            if flag == 'depend':
                data[index][-2] = num
            if flag == 'dependby':
                data[index][-1] = num
    return data


def generate_version_datasets(root_path, repos, repo_num, depends):
    # repos=['EclipseLink']
    for repo in repos:

        for k in range(1, repo_num[repo] + 1):

            total_files = load_json_data('{}/{}/version-{}/dependency/total_files.json'.format(root_path, repo, str(k)))
            # 每个文件上的代码行
            file_code_num = load_json_data(
                '{}/{}/version-{}/dependency/file_code_num.json'.format(root_path, repo, str(k)))

            java_files = []
            data_num_num = []
            for file in total_files:
                if file.split('.')[-1] != 'java':
                    continue
                java_files.append(file + '#' + str(k))
                code_num = file_code_num[file]
                temp = [file, k, code_num]
                temp.extend([0] * 24)
                data_num_num.append(temp)

            logger.info(
                "repo: {}, version: {}, files: {}, datas: {}".format(repo, k, len(java_files), len(data_num_num)))

            for i in range(len(depends)):
                depend_data = load_json_data(
                    '{}/{}/version-{}/dependency/filter_{}_depend_file_nums.json'.format(root_path, repo, str(k),
                                                                                         depends[i]))

                dependby_data = load_json_data(
                    '{}/{}/version-{}/dependency/filter_{}_dependby_file_nums.json'.format(root_path, repo, str(k),
                                                                                           depends[i]))

                data_num_num = get_features(depend_data, java_files, i, k, data_num_num, 'depend')

                data_num_num = get_features(dependby_data, java_files, i, k, data_num_num, 'dependby')

            data_num_num = get_labels(
                '{}/{}/version/version_{}_blocking_buggy_file.json'.format(root_path, repo, str(k)), java_files, k,
                data_num_num, 'depend')
            data_num_num = get_labels(
                '{}/{}/version/version_{}_blocked_buggy_file.json'.format(root_path, repo, str(k)), java_files, k,
                data_num_num, 'dependby')

            headers = ['file', 'version', 'CodeLine', 'Call', 'CallBy', 'CallNondynamic', 'CallNondynamicBy', 'Couple',
                       'CoupleBy', 'Create', 'CreateBy', 'DotRef', 'DotRefBy', 'Extend_Couple', 'Extend_CoupleBy',
                       'Implement_Couple', 'Implement_CoupleBy', 'Import', 'ImportBy',
                       'Override', 'OverrideBy', 'Typed', 'TypedBy', 'Use', 'UseBy', 'blocking', 'blocked']
            save_csv_data('{}/{}/version/dataset/version_{}_dependency_datasets.csv'.format(root_path, repo, k),
                          headers, data_num_num)
        # break
