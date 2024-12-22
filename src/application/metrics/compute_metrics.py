from tools.compute_metrics import compute_time_metrics, compare_different_thresholds

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
