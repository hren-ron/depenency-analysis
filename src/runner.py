import json

from settings import Settings
from application.bug.mapping_bug_to_version import mapping_bug_to_version
from tools.load_dataset import load_json_data


def main():
    settings = Settings('config.ini')
    root_path = settings.get_config('basic', 'root_path')
    repos = settings.get_config('basic', 'repos').split(',')
    repo_version_nums = list(map(int,settings.get_config('basic', 'repo_version_nums').split(',')))
    repo_versions=load_json_data('repo_version_config.json')

    mapping_bug_to_version(root_path, repos, repo_versions)

    #compute_metrics(repos, repo_version_nums, root_path, threshold_type='medium')
    #compare_thresholds(repos, repo_version_nums, root_path)


if __name__ == '__main__':
    main()
