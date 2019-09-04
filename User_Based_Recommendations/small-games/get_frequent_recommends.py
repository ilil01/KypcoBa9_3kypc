out = open('./frequent_recommends.txt', 'w')
zeros = open('./clusters/users/zeros.txt', 'r').read().split(' ')
#zeros.remove('')
zeros.remove('\n')
zeros = [int(x) for x in zeros]
for i in range(1012):
    if i in zeros:
        continue
    out.write('User №' + str(i) + ':\n')
    f = open('./use/users/' + str(i) + '.txt', 'r')
    ps = eval(f.read())
    f.close()
    profile = {}
    users = open('./normalized_profiles/users/all.txt', 'r').read().split('\n')
    f = open('./normalized_profiles/users/' + users[i] + '.txt', 'r')
    for line in f:
        tmp = line.split(':')
        profile[int(tmp[0])] = int(tmp[1])
    f.close()
    potential = {}
    s = str(i)
    uc = -1
    for k in range(102):
        f = open('./clusters/users/' + str(k) + '.txt', 'r')
        if f.read().split(' ').count(s) != 0:
            uc = k
            f.close()
            break
        f.close()
    if uc == -1:
        out.write('\tUser №' + i + ': cannot find in clusters\n')
    while len(potential) == 0:
        j = -1
        tmp = 0
        for k in range(len(ps)):
            if ps[k] > tmp:
                tmp = ps[k]
                j = k
        if j == -1:
            break
        f = open('./clusters/objects/' + str(j) + '.txt', 'r')
        cluster = f.readline().split(' ')
        for line in f:
            cluster += line.split(' ')
        f.close()
        while '' in cluster:
            cluster.remove('')
        while '\n' in cluster:
            cluster.remove('\n')
        cluster = [int(x) for x in cluster]
        for obj in cluster:
            if obj not in profile:
                f = open('./use/objects/' + str(obj) + '.txt', 'r')
                tmp = eval(f.read())
                potential[obj] = tmp[uc]
        if len(potential) == 0:
            ps[j] = 0
    if len(potential) == 0:
        out.write('\tUser №' + str(i) + ' cannot be recommended by that method\n')
        continue
    tmp = 0
    j = -1
    for obj in potential:
        if potential[obj] > tmp:
            tmp = potential[obj]
            j = obj
    if j == -1:
        out.write('\t' + str(potential) + '\n')
    else:
        out.write('\t' + str(j) + '\n')

out.close()
print('All found!')
