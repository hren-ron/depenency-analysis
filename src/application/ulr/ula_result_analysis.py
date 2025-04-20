
import pandas as pd

def analysis_ulr_result(root_path, repo_version, flag, depends, process, bug_type):
    '''
    将单因素逻辑回归的结果转换成latex表格
    :param root_path:
    :param repo_version:
    :param flag:
    :param depends:
    :param process:
    :param bug_type:
    :return:
    '''
    depends.extend(process)
    depends.remove("CodeLine")

    for repo, versions in repo_version.items():
        file_path = '{}/{}/version/RQ2/{}_num_to_01_ulr_coefficients.csv'.format(root_path, repo, bug_type)
        file_data = pd.read_csv(file_path)

        file_versions= list(set(file_data['versions']))

        nums = ['0'] * len(depends)
        counts = ['0'] * len(depends)
        for version in file_versions:
            if str(version) not in versions.keys():
                continue

            data = file_data[file_data['versions'] == version]

            depend_coef = data.set_index("new_depends")["OR"].to_dict()
            depend_p = data.set_index("new_depends")["Pr(>|z|)"].to_dict()
            #print(depend_coef)
            #print(depend_p)
            s = ''
            s += repo + '&' + str(version)
            for depend in depends:
                if depend in depend_coef.keys():
                    p = float(depend_p[depend])
                    coef = depend_coef[depend]

                    if p < 0.0001:
                        s += '&' + '\cellcolor{mygray}' + ' \\tabincell{c}{\\textbf{' + str(
                            format(coef, '.4f')) + '}\\\\($<$0.0001)}'
                        if coef >= 1:
                            nums[depends.index(depend)] = str(int(nums[depends.index(depend)]) + 1)
                        else:
                            counts[depends.index(depend)] = str(int(counts[depends.index(depend)]) + 1)
                    elif p < 0.001:
                        s += '&' + '\cellcolor{mygray}' + ' \\tabincell{c}{\\textbf{' + str(
                            format(coef, '.4f')) + '}\\\\($<$0.001)}'
                        if coef >= 1:
                            nums[depends.index(depend)] = str(int(nums[depends.index(depend)]) + 1)
                        else:
                            counts[depends.index(depend)] = str(int(counts[depends.index(depend)]) + 1)
                    elif p < 0.01:
                        s += '&' + '\cellcolor{mygray}' + ' \\tabincell{c}{\\textbf{' + str(
                            format(coef, '.4f')) + '}\\\\($<$0.01)}'
                        if coef >= 1:
                            nums[depends.index(depend)] = str(int(nums[depends.index(depend)]) + 1)
                        else:
                            counts[depends.index(depend)] = str(int(counts[depends.index(depend)]) + 1)
                    elif p < 0.05:
                        s += '&' + '\cellcolor{mygray}' + ' \\tabincell{c}{\\textbf{' + str(
                            format(coef, '.4f')) + '}\\\\(' + str(format(p, '.4f')) + ')}'
                        if coef >= 1:
                            nums[depends.index(depend)] = str(int(nums[depends.index(depend)]) + 1)
                        else:
                            counts[depends.index(depend)] = str(int(counts[depends.index(depend)]) + 1)
                    else:
                        s += '&' + ' \\tabincell{c}{' + str(format(coef, '.4f')) + '\\\\(' + str(
                            format(p, '.4f')) + ')}'
                else:
                    s += '&-'
                # s+='\n'
            s += '\\\\'
            print(s)
            # break
        s = ''
        s += '\\hline\n'
        s += 'Significance&-'

        for i in range(len(depends)):
            s += '&' + str(int(nums[i]) + int(counts[i])) + '(' + nums[i] + '/' + counts[i] + ')'
        s += '\\\\' + '\n'
        s += '\\hline\n'
        s += '\\hline\n'
        print(s)
        #break

