

def compute_confusion_matrix(true_labels, pre_labels):
    tn = 0
    tp = 0
    fp = 0
    fn = 0
    for i in range(len(true_labels)):
        if true_labels[i] == 1 and pre_labels[i] == 1:
            tp += 1
        if true_labels[i] == 1 and pre_labels[i] == 0:
            fn += 1
        if true_labels[i] == 0 and pre_labels[i] == 1:
            fp += 1
        if true_labels[i] == 0 and pre_labels[i] == 0:
            tn += 1
    return tn, fp, fn, tp
