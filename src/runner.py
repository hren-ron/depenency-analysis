from application.bug.extract_buggy_files_for_each_version import get_version_buggy_files
from application.bug.mapping_bug_to_version import mapping_bug_to_version
from application.dataset.generate_dependency_dataset import generate_version_datasets
from settings import Settings
from tools.process_csv_file import load_json_data


def main():
    settings = Settings('config/config.ini')
    root_path = settings.get_config('basic', 'root_path')
    repos = settings.get_config('basic', 'repos').split(',')

    repo_versions = load_json_data('config/repo_version_config.json')

    # 将bug映射到对应的版本上
    # mapping_bug_to_version(root_path, repos, repo_versions)

    # 将bug映射到项目每个版本的源文件上
    # get_version_buggy_files(root_path, repos)

    repo_version_nums = list(map(int, settings.get_config('basic', 'repo_version_nums').split(',')))
    repo_num = dict(zip(repos, repo_version_nums))
    depends=settings.get_config('basic', 'depends').split(',')

    generate_version_datasets(root_path, repos, repo_num, depends)

    # compute_metrics(repos, repo_version_nums, root_path, threshold_type='medium')
    # compare_thresholds(repos, repo_version_nums, root_path)


if __name__ == '__main__':
    main()
