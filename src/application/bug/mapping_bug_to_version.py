import datetime

from bs4 import BeautifulSoup

from tools.load_dataset import *


def compare_time_on_versions(time, repo_versions, version_times):
    fixing_version_diff = {}
    report_version_diff = {}

    for num, version in repo_versions.items():

        version_time = datetime.datetime.strptime(' '.join(version_times[version].split(' ')[:-1]),
                                                  '%Y-%m-%d %H:%M:%S')
        print('version time ',version_time)
        print("time: ", time)
        print("version num: ", num)

        if time >= version_time:
            fixing_version_diff[num] = time.__sub__(version_time).days
        if time <= version_time:
            report_version_diff[num] = version_time.__sub__(time).days
    fixing_version_diff = sorted(fixing_version_diff.items(), key=lambda kv: (kv[1]))
    report_version_diff = sorted(report_version_diff.items(), key=lambda kv: (kv[1]))
    return fixing_version_diff, report_version_diff


def mapping_bug_based_on_fixing_time(bug, bug_commits, repo_versions, commit_times, version_times):
    version_commits = {}
    for commit in bug_commits[bug]:
        time = datetime.datetime.strptime(' '.join(commit_times[commit].split(' ')[:-1]), '%Y-%m-%d %H:%M:%S')
        print('fixing time ',time)
        version_diff = compare_time_on_versions(time, repo_versions, version_times)[0]

        if len(version_diff) == 0:
            continue
        if version_diff[0][0] in version_commits.keys():
            version_commits[version_diff[0][0]].append(commit)
        else:
            version_commits[version_diff[0][0]] = [commit]
    return version_commits


def mapping_bug_based_on_report_time(report_time, repo_versions, version_times):
    version_diff = compare_time_on_versions(report_time, repo_versions, version_times)[1]
    print("report time: ", report_time)
    #print(version_times)
    if len(version_diff) == 0:
        return len(version_diff) + 1
    else:
        return version_diff[0][0]


def mapping_bugs(root_path, repo, bugs, bug_commits, repo_versions, commit_times, version_times):
    count = 0
    total_count = 0
    bug_versions = {}
    for bug in set(bugs):
        if bug not in bug_commits.keys():
            continue

        total_count += 1
        fixing_version_commits = mapping_bug_based_on_fixing_time(bug, bug_commits, repo_versions[repo], commit_times,
                                                                  version_times)
        if len(fixing_version_commits) != 0:
            count += 1
        bug_versions[bug] = fixing_version_commits

        soup = BeautifulSoup(open('{}/{}/data/b{}.xml'.format(root_path, repo, bug), encoding='utf8').read(),
                             'html.parser')
        report_time = datetime.datetime.strptime(' '.join(soup.creation_ts.string.split(' ')[:-1]), '%Y-%m-%d %H:%M:%S')
        report_version = mapping_bug_based_on_report_time(report_time, repo_versions[repo], version_times)

        print(bug_versions, report_version)
        break

    print(len(set(bugs)), total_count, total_count / len(set(bugs)), count,
          count / len(set(bugs)))

    return bug_versions


def mapping_bug_to_version(root_path, repos, repo_versions):
    repo_version_time = load_csv_data('{}/4DIAC/version/main_version_information.csv'.format(root_path))

    for repo in repos:
        print(repo)
        blocking_bugs = load_json_data('{}/{}/blocking_bugs.json'.format(root_path, repo))
        blocked_bugs = load_json_data('{}/{}/blocked_bugs.json'.format(root_path, repo))
        bug_commits = load_json_data('{}/{}/commit/bug_to_commits.json'.format(root_path, repo))

        print(len(blocking_bugs))

        version_times = repo_version_time[repo]

        commit_times = get_commit_time('{}/{}/commit/commit_file.csv'.format(root_path, repo), repo)
        # print(commit_times)
        mapping_bugs(root_path, repo, blocking_bugs, bug_commits, repo_versions, commit_times, version_times)
        break
