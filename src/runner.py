from application.bug.extract_buggy_files_for_each_version import get_version_buggy_files
from application.bug.mapping_bug_to_version import mapping_bug_to_version
from application.dataset.generate_dependency_dataset import generate_version_datasets
from application.dataset.combine_process_metrics import combine_process_metrics
from application.pca.pca_result_analysis import transfer_table
from application.ulr.ula_result_analysis import analysis_ulr_result
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
    depends=settings.get_config('metric', 'depends').split(',')

    # generate_version_datasets(root_path, repos, repo_num, depends)

    # combine_process_metrics(repos, root_path, repo_num)

    # 计算PCA, 将PCA结果转换成latex表格
    dependbys = settings.get_config('metric', 'dependbys').split(',')
    processes = settings.get_config('metric', 'process').split(',')
    # transfer_table(root_path, repo_versions, 'all_version', depends, processes,'blocked')
    # transfer_table(root_path, repo_versions, 'all_version', dependbys, processes, 'blocking')
    # transfer_table(root_path, repo_versions, 'part_version', dependbys, processes, 'blocking')
    # transfer_table(root_path, repo_versions, 'part_version', depends, processes, 'blocked')

    # 处理单因素逻辑回归的实验结果
    # analysis_ulr_result(root_path, repo_versions, 'all_version', dependbys, processes, 'blocking')
    # analysis_ulr_result(root_path, repo_versions, 'all_version', depends, processes, 'blocked')

    filtered_repo_versions = load_json_data('config/filtered_repo_version_config.json')
    # analysis_ulr_result(root_path, filtered_repo_versions, 'part_version', dependbys, processes, 'blocking')
    analysis_ulr_result(root_path, filtered_repo_versions, 'part_version', depends, processes, 'blocked')

    # compute_metrics(repos, repo_version_nums, root_path, threshold_type='medium')
    # compare_thresholds(repos, repo_version_nums, root_path)


if __name__ == '__main__':
    main()
