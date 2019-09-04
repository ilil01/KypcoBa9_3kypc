# raise ValueError ('Not finished')

from bbac import BBAC
from math import isclose

a = BBAC(1012, 656, 102, 66)

out = open('./frequent_recommends_old.txt', 'w')
zeros = open('./clusters/users/zeros.txt', 'r').read().split(' ')
#zeros.remove('')
zeros.remove('\n')
zeros = [int(x) for x in zeros]
for i in range(1012):
    if i in zeros:
        continue
    out.write('User №' + str(i) + ':\n')
    profile = a.get_profile(i, True)
    potential = {}
    max_mark = 0
    uc = a.get_cluster(i, True)
    u_avg = a.get_average(i, True)
    uc_avg = a.get_cluster_average(uc, True)
    for j in range(656):
        if j in profile:
            continue
        obj_avg = a.get_average(j, False)
        obj_c = a.get_cluster(j, False)
        obj_cavg = a.get_cluster_average(obj_c, False)
        bic_avg = a.get_bicluster_average(uc, obj_c)
        mark = a.block_average(i, j, u_avg, obj_avg, uc_avg, obj_cavg, bic_avg)
        if isclose(mark, max_mark):
            potential[j] = mark
        elif mark > max_mark:
            potential = {j : mark}
            max_mark = mark
    out.write('\t' + str(potential) + '\n')

out.close()
print('All found!')
