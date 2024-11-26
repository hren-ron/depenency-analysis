
import csv,os
import pandas as pd
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,roc_auc_score,matthews_corrcoef

from tools.compute_confusion_matrix import compute_confusion_matrix

'''
compute metrics when perform 10 times prediction model
'''
def compute_time_metrics(repos, nums, flag, method, type, root_path, threshold_type="normal"):

    file = open('{}/{}/version/new_prediction/{}_{}_{}_{}_time_combined_datasets.csv'.format(root_path, repos[0], flag, method, type, threshold_type), 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(file)
    csv_writer.writerow(['repo', 'version', 'time', 'classifier', 'metric', 'value'])

    THRESHOLD = 0.5

    for i in range(len(repos)):

        for j in range(1, nums[i]):

            for k in range(10):
                path = '{}/{}/version/new_prediction/time_result/version_{}_time_{}_{}_{}_{}_scale_train_result.csv'.format(root_path,
                    repos[i], str(j), str(k), flag, method, type)

                if not os.path.exists(path):
                    continue
                pre_data = pd.read_csv(path)

                path = '{}/{}/version/dataset/version_dataset/{}_remove_confound_new_combined_test_datasets_{}.csv'.format(root_path,
                    repos[i], flag, str(j))
                true_data = pd.read_csv(path)

                true_labels = true_data[flag]

                for cla in ['rf', 'lr', 'ada', 'xgb']:

                    print(repos[i], j, k, flag, method, cla)
                    #print(true_labels[true_labels == 1].shape)
                    #print(true_labels[true_labels == 0].shape)

                    if threshold_type== 'medium':
                        THRESHOLD=pre_data[cla].median()
                    print(THRESHOLD)
                    pre_data[cla][pre_data[cla] >= THRESHOLD] = 1
                    pre_data[cla][pre_data[cla] < THRESHOLD] = 0
                    pre_labels = pre_data[cla]
                    # print(pre_data[cla][pre_data[cla]==0].shape)

                    print(pre_labels[pre_labels == 1].shape)
                    print(pre_labels[pre_labels == 0].shape)

                    acc = accuracy_score(true_labels, pre_labels)
                    f1 = f1_score(true_labels, pre_labels)
                    pre = precision_score(true_labels, pre_labels)
                    rec = recall_score(true_labels, pre_labels)

                    tn, fp, fn, tp = compute_confusion_matrix(true_labels, pre_labels)
                    if tp + fn == 0:
                        sen = float('nan')
                    else:
                        sen = tp / float(tp + fn)
                    if tn + fp == 0:
                        spe = float('nan')
                        fpr = float('nan')
                    else:
                        spe = tn / float(tn + fp)
                        fpr = fp / float(tn + fp)
                    mcc = matthews_corrcoef(true_labels, pre_labels)

                    if true_labels[true_labels == 1].shape[0] == 0 or true_labels[true_labels == 0].shape[0] == 0:
                        auc = float('nan')
                    else:
                        auc = roc_auc_score(true_labels, pre_labels)

                    print(acc, f1, pre, rec)
                    # print(sen,spe)
                    print(mcc, auc, fpr)

                    csv_writer.writerow([repos[i], j, k, cla, 'Accuracy', acc])
                    csv_writer.writerow([repos[i], j, k, cla, 'F1', f1])
                    csv_writer.writerow([repos[i], j, k, cla, 'Precision', pre])
                    csv_writer.writerow([repos[i], j, k, cla, 'Recall', rec])
                    csv_writer.writerow([repos[i], j, k, cla, 'Sensitivity', sen])
                    csv_writer.writerow([repos[i], j, k, cla, 'Specificity', spe])
                    csv_writer.writerow([repos[i], j, k, cla, 'MCC', mcc])
                    csv_writer.writerow([repos[i], j, k, cla, 'AUC', auc])
                    csv_writer.writerow([repos[i], j, k, cla, 'FPR', fpr])

def compare_different_thresholds(repos, nums, flag, method, type, root_path):

    file = open('{}/{}/version/new_prediction/{}_{}_{}_different_threshold_time_combined_datasets.csv'.format(root_path, repos[0], flag, method, type), 'w', encoding='utf-8', newline='')
    csv_writer = csv.writer(file)
    csv_writer.writerow(['repo', 'version','threshold', 'time', 'classifier', 'metric', 'value'])

    thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    for i in range(len(repos)):

        for j in range(1, nums[i]):

            for k in range(10):
                path = '{}/{}/version/new_prediction/time_result/version_{}_time_{}_{}_{}_{}_scale_train_result.csv'.format(root_path,
                    repos[i], str(j), str(k), flag, method, type)

                if not os.path.exists(path):
                    continue
                pre_data = pd.read_csv(path)

                path = '{}/{}/version/dataset/version_dataset/{}_remove_confound_new_combined_test_datasets_{}.csv'.format(root_path,
                    repos[i], flag, str(j))
                true_data = pd.read_csv(path)
                #print(len(true_data[flag]))

                true_labels = true_data[flag]

                for cla in ['rf', 'lr', 'ada', 'xgb']:

                    print(repos[i], j, k, flag, method, cla)

                    for THRESHOLD in thresholds:
                        new_pre_data = pre_data.copy()
                        #print(THRESHOLD)

                        new_pre_data[cla][pre_data[cla] >= THRESHOLD] = 1
                        new_pre_data[cla][pre_data[cla] < THRESHOLD] = 0
                        pre_labels = new_pre_data[cla]
                        # print(pre_data[cla][pre_data[cla]==0].shape)

                        print(pre_labels[pre_labels == 1].shape)
                        print(pre_labels[pre_labels == 0].shape)

                        acc = accuracy_score(true_labels, pre_labels)
                        f1 = f1_score(true_labels, pre_labels)
                        pre = precision_score(true_labels, pre_labels)
                        rec = recall_score(true_labels, pre_labels)

                        tn, fp, fn, tp = compute_confusion_matrix(true_labels, pre_labels)
                        if tp + fn == 0:
                            sen = float('nan')
                        else:
                            sen = tp / float(tp + fn)
                        if tn + fp == 0:
                            spe = float('nan')
                            fpr = float('nan')
                        else:
                            spe = tn / float(tn + fp)
                            fpr = fp / float(tn + fp)
                        mcc = matthews_corrcoef(true_labels, pre_labels)

                        if true_labels[true_labels == 1].shape[0] == 0 or true_labels[true_labels == 0].shape[0] == 0:
                            auc = float('nan')
                        else:
                            auc = roc_auc_score(true_labels, pre_labels)

                        print(acc, f1, pre, rec)

                        print(mcc, auc, fpr)

                        csv_writer.writerow([repos[i], j, THRESHOLD, k, cla, 'Accuracy', acc])
                        csv_writer.writerow([repos[i], j, THRESHOLD, k, cla, 'F1', f1])
                        csv_writer.writerow([repos[i], j, THRESHOLD, k, cla, 'Precision', pre])
                        csv_writer.writerow([repos[i], j, THRESHOLD, k, cla, 'Recall', rec])
                        csv_writer.writerow([repos[i], j, THRESHOLD, k, cla, 'Sensitivity', sen])
                        csv_writer.writerow([repos[i], j, THRESHOLD, k, cla, 'Specificity', spe])
                        csv_writer.writerow([repos[i], j, THRESHOLD, k, cla, 'MCC', mcc])
                        csv_writer.writerow([repos[i], j, THRESHOLD, k, cla, 'AUC', auc])
                        csv_writer.writerow([repos[i], j, THRESHOLD, k, cla, 'FPR', fpr])