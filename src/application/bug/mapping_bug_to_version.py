import datetime

from bs4 import BeautifulSoup

from globalLog import logger
from tools.process_csv_file import *


def compare_time_on_versions(time, repo_versions, version_times):
    '''
    比较bug的时间和版本时间
    :param time: bug修复时间、报告时间
    :param repo_versions: 项目的版本
    :param version_times: 每个版本的时间
    :return:
    '''
    fixing_version_diff = {}

    for num, version in repo_versions.items():

        version_time = datetime.datetime.strptime(' '.join(version_times[version].split(' ')[:-1]),
                                                  '%Y-%m-%d %H:%M:%S')
        if time >= version_time:
            fixing_version_diff[num] = time.__sub__(version_time).days

    fixing_version_diff = sorted(fixing_version_diff.items(), key=lambda kv: (kv[1]))
    return fixing_version_diff


def mapping_bug_based_on_fixing_time(bug, bug_commits, repo_versions, commit_times, version_times):
    '''
    基于修复时间将bug映射到对应的版本上
    :param bug: bug
    :param bug_commits: bug相关的fixing commits
    :param repo_versions: bug所在项目的版本
    :param commit_times: 每个commit的报告时间
    :param version_times: 每个版本的时间
    :return:
    '''
    version_commits = {}
    for commit in bug_commits[bug]:

        if commit not in commit_times.keys():
            continue
        time = datetime.datetime.strptime(' '.join(commit_times[commit].split(' ')[:-1]), '%Y-%m-%d %H:%M:%S')

        version_diff = compare_time_on_versions(time, repo_versions, version_times)

        if len(version_diff) == 0:
            continue
        if version_diff[0][0] in version_commits.keys():
            version_commits[version_diff[0][0]].append(commit)
        else:
            version_commits[version_diff[0][0]] = [commit]
        logger.info('bug: {}, fixing commit: {}, time: {}, version: {}'.format(bug, commit, time, version_diff[0][0]))
    return version_commits


def mapping_bug_based_on_report_time(path, repo_versions, version_times):
    '''
    基于bug的报告时间将其映射到版本上
    :param path: bug的基本信息路径
    :param repo_versions: bug所在项目的版本
    :param version_times: 每个版本的时间
    :return:
    '''

    soup = BeautifulSoup(open(path, encoding='utf8').read(),
                         'html.parser')
    report_time = datetime.datetime.strptime(' '.join(soup.creation_ts.string.split(' ')[:-1]), '%Y-%m-%d %H:%M:%S')
    logger.info('bug: {}, report time: {}'.format(path.split('/')[-1].split('.')[0][1:], report_time))

    version_diff = compare_time_on_versions(report_time, repo_versions, version_times)

    if len(version_diff) == 0:
        return 0
    else:
        return version_diff[0][0]


def get_versions_from_report_to_fixed(bug_versions, report_version):
    '''
    得到每个bug的持续bug
    :param bug_versions: bug的修复版本
    :param report_version: bug的报告版本
    :return:
    '''

    ## 获得最晚修复的版本

    fixing_version = int(sorted(bug_versions.keys())[-1])
    logger.info("max fixing commit: " + str(fixing_version))
    logger.info("report version: " + str(report_version))

    # 初始化检查和类型验证
    if not isinstance(report_version, int) or not isinstance(fixing_version, int):
        raise ValueError("Both report_version and fixing_version must be integers.")

    # 处理 report_version 为 0 的情况
    if report_version == 0:
        report_version = 1

    # 边界条件处理
    if report_version > fixing_version:
        return []

    # 返回版本范围
    if report_version == fixing_version:
        return [report_version]

    return list((map(str, range(report_version, fixing_version + 1))))


def mapping_bugs(root_path, repo, bugs, bug_commits, repo_versions, commit_times, version_times):
    '''
    把项目中所有bug映射到持续版本上
    :param root_path: 项目根目录
    :param repo: 项目
    :param bugs: 所有bugs
    :param bug_commits: bug对应的fixing commits
    :param repo_versions: 项目的版本
    :param commit_times: commit的时间
    :param version_times: 版本的时间
    :return:
    '''
    count = 0
    total_count = 0
    mutli_version = 0
    bug_versions = {}
    for bug in set(bugs):
        if bug not in bug_commits.keys():
            continue

        total_count += 1
        ## 得到bug的修复版本
        fixing_version_commits = mapping_bug_based_on_fixing_time(bug, bug_commits, repo_versions[repo], commit_times,
                                                                  version_times)
        if len(fixing_version_commits) == 0:
            continue

        ## 得到bug的报告版本
        report_version = mapping_bug_based_on_report_time('{}/{}/data/b{}.xml'.format(root_path, repo, bug),
                                                          repo_versions[repo], version_times)

        ## 得到bug的持续版本
        versions = get_versions_from_report_to_fixed(fixing_version_commits, int(report_version))
        logger.info('bug: {}, continuous versions: {}'.format(bug, versions))

        if len(versions) != 0:
            count += 1
            if len(versions) > 1:
                mutli_version += 1

        bug_versions[bug] = versions
        # break
    logger.info(
        'repo: {}, total bugs: {}, fixing bugs: {}, version bugs: {}, multi version bugs:{} '.format(repo,
                                                                                                     len(set(bugs)),
                                                                                                     total_count, count,
                                                                                                     mutli_version))
    return bug_versions


def mapping_bug_to_version(root_path, repos, repo_versions):
    '''
    为所有项目的bug找到其持续时间
    :param root_path: 根目录
    :param repos: 所有项目
    :param repo_versions: 所有项目的版本
    :return:
    '''

    repo_version_time = load_csv_data('{}/4DIAC/version/main_version_information.csv'.format(root_path))

    for repo in repos:
        blocking_bugs = load_json_data('{}/{}/blocking_bugs.json'.format(root_path, repo))
        blocked_bugs = load_json_data('{}/{}/blocked_bugs.json'.format(root_path, repo))
        bug_commits = load_json_data('{}/{}/commit/bug_to_commits.json'.format(root_path, repo))

        logger.info('repo: {}, blocking bugs: {}, blocked bugs: {}'.format(repo, len(blocking_bugs), len(blocked_bugs)))

        version_times = repo_version_time[repo]

        commit_times = get_commit_time('{}/{}/commit/commit_file.csv'.format(root_path, repo), repo)
        # print(commit_times)

        # 处理blocking bugs
        bug_versions = mapping_bugs(root_path, repo, blocking_bugs, bug_commits, repo_versions, commit_times,
                                    version_times)
        save_json_data('{}/{}/version/blocking_bug_to_version.json'.format(root_path, repo), bug_versions)

        # 处理blocked bugs
        bug_versions = mapping_bugs(root_path, repo, blocked_bugs, bug_commits, repo_versions, commit_times,
                                    version_times)
        save_json_data('{}/{}/version/blocked_bug_to_version.json'.format(root_path, repo), bug_versions)
        #break
