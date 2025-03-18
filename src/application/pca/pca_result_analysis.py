import os.path

from tools.file_operation import read_file


def get_pc_depends(path):
    pc_depends = {}
    for line in read_file(path):
        lines = line.strip().split(',')
        pc = lines[2].replace('"', '')
        depend = lines[1].replace('"', '')
        if pc in pc_depends.keys():
            pc_depends[pc].append(depend)
        else:
            pc_depends[pc] = [depend]
    return pc_depends

def get_pc_metrics(path):
    datas = []
    for line in read_file(path):
        # 去除行首尾空白并按逗号分割
        stripped_line = line.strip()
        if not stripped_line:  # 忽略空行
            continue

        split_lines = stripped_line.split(',')
        # 移除每个字段中的双引号
        cleaned_lines = [field.replace('"', '') for field in split_lines]
        datas.append(cleaned_lines)
    return datas

def transfer_table(root_path, repo_version, flag, depends, process, bug_type):
    '''
    将pca结果转换成latex表格
    :param root_path: 根路径
    :param repo_version:
    :param flag: 是否过滤版本
    :param depends: 依赖关系
    :param bug_type: blocking / blocked
    :return:
    '''

    for repo, versions in repo_version.items():
        for version in versions:
            print(repo, version)
            pc_path = '{}/{}/new_pca/{}_{}_{}_pca_depend_pc.csv'.format(root_path, repo, flag, version, bug_type)
            if not os.path.exists(pc_path):
                continue
            pc_depends = get_pc_depends(pc_path)

            summary_path = '{}/{}/new_pca/{}_{}_{}_pca_summary.csv'.format(root_path, repo, flag, version, bug_type)
            pc_metrics = get_pc_metrics(summary_path)
            print(pc_metrics)

            break
        break
