from settings import Settings
from tools.process_csv_file import load_json_data


def compare_files(repo, path1, path2):

    source_datas = load_json_data(path1)
    target_datas = load_json_data(path2)

    print("repo: {}, source datas - target datas: {}".format(repo, len(set(source_datas.keys())-set(target_datas.keys()))))

    print("repo: {}, target datas - source datas: {}".format(repo, len(set(target_datas.keys())-set(source_datas.keys()))))


def compare_all_repo_files(repos):

    for repo in repos:
        compare_files(repo, "E:/DRSpace/{}/version/blocking_bug_versions.json".format(repo), "E:/DRSpace/{}/version/blocking_bug_to_version_commits.json".format(repo))
        compare_files(repo, "E:/DRSpace/{}/version/blocked_bug_versions.json".format(repo), "E:/DRSpace/{}/version/blocked_bug_to_version_commits.json".format(repo))

if __name__ == '__main__':
    settings = Settings('../config/config.ini')
    repos = settings.get_config('basic', 'repos').split(',')
    compare_all_repo_files(repos)
