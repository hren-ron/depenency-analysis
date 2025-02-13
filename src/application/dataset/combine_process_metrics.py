
from globalLog import logger
from tools.process_csv_file import *


def combine_process_data(path, file_metrics):
    datas=[]
    with open(path, 'r', encoding='utf8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'file':
                continue
            key = f"{row[0]}#{row[1]}"

            temp = row[:-2]
            temp.extend(file_metrics[key])
            temp.extend(row[-2:])
            datas.append(temp)
        file.close()
    return datas

def combine_process_metrics(repos, root_path, repo_num):

    for repo in repos:

        headers=['file' ,'version' ,'CodeLine' ,'Call' ,'CallBy' ,'CallNondynamic' ,'CallNondynamicBy' ,'Couple','CoupleBy' ,'Create' ,'CreateBy' ,'DotRef' ,'DotRefBy' ,'Extend_Couple' ,'Extend_CoupleBy','Implement_Couple' ,'Implement_CoupleBy' ,'Import' ,'ImportBy',
              'Override' ,'OverrideBy' ,'Typed' ,'TypedBy' ,'Use' ,'UseBy' ,'COMM' ,'CCOMM' ,'DEV' ,'CDEV' ,'ADD','CADD' ,'DEL' ,'CDEL' ,'MOD' ,'CMOD' ,'FILE' ,'CFILE' ,'BUG' ,'CBUG' ,'REV' ,'blocking' ,'blocked']

        file_metrics = get_file_process_metrics('{}/{}/version/dataset/new_process_datasets.csv'.format(root_path, repo))

        for k in range(1, repo_num[repo] + 1):

            datas = combine_process_data('{}/{}/version/dataset/version_{}_dependency_datasets.csv'.format(root_path, repo, str(k)),file_metrics)

            save_csv_data('{}/{}/version/dataset/version_{}_combined_datasets.csv'.format(root_path, repo, str(k)), headers, datas)

            logger.info('combine_process_dependency, repo: {}, version: {}'.format(repo, k))