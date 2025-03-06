import pandas as pd

from settings import Settings
from tools.process_csv_file import *

def compute_blocking_bug_num_each_project(root_path, repo_num):

    datas = []
    for repo in repos:
        for num in range(1, repo_num[repo] + 1):
            #print("repo = {}, num = {}".format(repo, num))

            path = "{}/{}/version/dataset/version_{}_combined_datasets.csv".format(root_path, repo, num)

            data = pd.read_csv(path)

            datas.append([repo, num, len(data), (data['blocking']>0).sum(), (data['blocked']>0).sum()])
            #break
        #break
    print(datas)
    headers = ['repo', 'version', 'total_bugs', 'blocking_bugs', 'blocked_bugs']
    save_csv_data('{}/4DIAC/version/dataset/blocking_bug_num_each_project.csv'.format(root_path), headers, datas)

if __name__ == "__main__":
    settings = Settings('../config/config.ini')
    repos = settings.get_config('basic', 'repos').split(',')
    root_path = settings.get_config('basic', 'root_path')

    repo_version_nums = list(map(int, settings.get_config('basic', 'repo_version_nums').split(',')))
    repo_num = dict(zip(repos, repo_version_nums))

    compute_blocking_bug_num_each_project(root_path, repo_num)
