from process_profiles import processing
from math import isclose

out = open('./frequent_recommends_sample.txt', 'w')
zeros = open('./clusters/users/zeros.txt', 'r').read().split(' ')
#zeros.remove('')
zeros.remove('\n')
zeros = [int(x) for x in zeros]

use = processing()
use.init_all_user_profiles()

for i in range(1012):
    if i in zeros:
        continue
    out.write('User №' + str(i) + ':\n')
    max_mark = 0
    potential = {}
    for j in range(656):
        if j in use.user_profiles[i]:
            continue
        mark = use.predict(i, j)
        if isclose(mark, max_mark):
            potential[j] = mark
        elif mark > max_mark:
            potential = {j : mark}
            max_mark = mark
    out.write('\t' + str(potential) + '\n')

out.close()
print('All found!')
