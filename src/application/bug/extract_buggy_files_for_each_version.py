
from collections import Counter

from globalLog import logger
from tools.process_csv_file import load_json_data, save_json_data


def get_buggy_files(bug_version_commits, bug_versions, commit_files):
    """
    获取每个版本上的bug files
    :param bug_version_commits:
    :param bug_versions: bug versions信息
    :param commit_files: commit到files的映射
    :return: version files
    """
    version_files={}
    bug_fixing_versions={}
    bug_fixing_files={}
    for bug, item in bug_version_commits.items():


        # bug修复时commit上的文件
        all_files=[]
        fixing_versions=[]
        for version, commits in item.items():
            version=int(version)
            fixing_versions.append(version)
            files = []
            for commit in commits:
                if commit not in commit_files:
                    continue
                files.extend(commit_files[commit])
            all_files.extend(files)
            if version in version_files:
                version_files[version].extend(files)
            else:
                version_files[version] = files
        logger.info("bug: {}, versions:{}, files:{}".format(bug, len(item), len(all_files)))
        bug_fixing_files[bug]=all_files
        bug_fixing_versions[bug]=fixing_versions

    # 使用报告时间来增强数据
    for bug,versions in bug_versions.items():
        for version in versions:
            version=int(version)
            if version not in bug_fixing_versions[bug]:

                if version in version_files:
                    version_files[version].extend(bug_fixing_files[bug])
                else:
                    version_files[version] = bug_fixing_files[bug]
    return version_files

def save_buggy_files(root_path, repo, version_files, flag):
    '''
    保持buggy files
    :param root_path: 根目录
    :param repo: 项目
    :param version_files: version files信息
    :param flag: blocking or blocked
    :return:
    '''
    for version, files in version_files.items():
        file_num = Counter(files)
        save_json_data('{}/{}/version/version_{}_{}_buggy_file.json'.format(root_path, repo, version, flag), file_num)
def get_version_buggy_files(root_path, repos):
    # repos=['EclipseLink']

    '''
    将项目中的blocking bug映射到每个版本的文件上
    :param root_path: 根目录
    :param repos: 项目
    :return:
    '''
    for repo in repos:

        logger.info('Extract buggy files for each version of {}'.format(repo))

        commit_files = load_json_data('{}/{}/commit/commit_file.json'.format(root_path, repo))

        blocking_bug_versions = load_json_data('{}/{}/version/blocking_bug_to_version.json'.format(root_path, repo))
        blocked_bug_versions = load_json_data('{}/{}/version/blocked_bug_to_version.json'.format(root_path, repo))
        blocking_bug_version_commits=load_json_data('{}/{}/version/blocking_bug_to_version_commits.json'.format(root_path, repo))
        blocked_bug_version_commits=load_json_data('{}/{}/version/blocked_bug_to_version_commits.json'.format(root_path, repo))

        # 获取bug files
        blocking_version_files = get_buggy_files(blocking_bug_version_commits, blocking_bug_versions, commit_files)
        blocked_version_files = get_buggy_files(blocked_bug_version_commits, blocked_bug_versions, commit_files)

        # 保存bug files
        save_buggy_files(root_path, repo, blocking_version_files, 'blocking')
        save_buggy_files(root_path, repo, blocked_version_files, 'blocked')

        #break


