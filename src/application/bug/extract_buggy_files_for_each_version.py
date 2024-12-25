import json
from collections import Counter

from globalLog import logger
from tools.process_csv_file import load_json_data, save_json_data


def get_buggy_files(bug_versions, bug_commits, commit_files):
    '''
    获取每个版本上的bug files
    :param bug_versions: bug versions信息
    :param bug_commits: bug commits信息
    :param commit_files: commit到files的映射
    :return: version files
    '''
    version_files={}
    for bug, versions in bug_versions.items():
        if bug not in bug_commits.keys():
            continue
        commits = bug_commits[bug]

        files = [
            file for commit in commits
            if commit in commit_files and commit_files[commit]
            for file in commit_files[commit]
        ]

        logger.info('bug: {}, commits: {}, files: {}'.format(bug, len(commits), len(files)))

        for version in versions:
            if files and isinstance(files, list):
                version_files.setdefault(version, []).extend(files)
            else:
                if files is None or not isinstance(files, list):
                    print(f"Warning: 'files' for version {version} is not a valid list.")
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
        bug_commits = load_json_data('{}/{}/commit/bug_to_commits.json'.format(root_path, repo))

        # 获取bug files
        blocking_version_files = get_buggy_files(blocking_bug_versions, bug_commits, commit_files)
        blocked_version_files = get_buggy_files(blocked_bug_versions, bug_commits, commit_files)

        # 保存bug files
        save_buggy_files(root_path, repo, blocking_version_files, 'blocking')
        save_buggy_files(root_path, repo, blocked_version_files, 'blocked')

        #break


