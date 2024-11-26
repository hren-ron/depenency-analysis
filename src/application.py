
from core.compute_metrics import compute_time_metrics, compare_different_thresholds


def compute_metrics(repos, nums, root_path, threshold_type):

    flags=['blocking','blocked']
    methods=['smote']
    types=['process','dependency','all']

    flags = ['blocked']
    methods = ['smote']
    types = ['process']

    for flag in flags:
        for method in methods:
            for type in types:
                compute_time_metrics(repos, nums, flag, method, type, root_path, threshold_type)

def compare_thresholds(repos, nums, root_path):
    flags = ['blocked']
    methods = ['smote']
    types = ['all']

    for flag in flags:
        for method in methods:
            for type in types:
                compare_different_thresholds(repos, nums, flag, method, type, root_path)

def main():
    root_path = 'E:/DRSpace'
    repos = ['4DIAC', 'Acceleo', 'ACTF', 'Ease', 'EclipseLink', 'EMF', 'EMFStore', 'Jubula', 'Mylyn', 'Papyrus',
             'Sirius', 'Virgo', 'JDT']

    repo_version_nums = [6, 9, 9, 3, 10, 13, 6, 8, 9, 10, 8, 7, 11]

    #compute_metrics(repos, repo_version_nums, root_path, threshold_type='medium')

    compare_thresholds(repos, repo_version_nums, root_path)



if __name__ == '__main__':
    main()