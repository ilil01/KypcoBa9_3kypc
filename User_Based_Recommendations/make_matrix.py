users_prefix = 'users/'
objects_prefix = 'objects/'

users = dict()
objects = dict()

all_users = open(users_prefix + 'all.txt', 'r').read().split('\n')
all_users.remove('')
for i in range(len(all_users)):
#    all_users[i] = all_users[i].split(',')[0]
    tmp = all_users[i].split(',')
    if len(tmp) != 2:
        raise Exception(all_users[i])
    users[int(tmp[1])] = tmp[0]
#print((all_users))


all_objects = open(objects_prefix + 'all.txt', 'r').read().split('\n')
all_objects.remove('')
for i in range(len(all_objects)):
    #all_objects[i] = all_objects[i].split(',')[0]
#    all_objects[i] = all_objects[i][:all_objects[i].find(',', -5)]
    title = all_objects[i][:all_objects[i].find(',', -5)]
    id_ = all_objects[i].split(',')[-1]
    objects[int(id_)] = title

#for i in users:
#    print(str(i) + ' : ' + users[i])

#print ('*'*100)


#for i in objects:
#    print(str(i) + ' : ' + objects[i])

result_filename = 'generated_matrix.txt'
result = open(result_filename, 'w')

for obj in objects:
    info_file = open(objects_prefix + objects[obj] + '.txt', 'r')
    # line :: user,mark
    info = dict()
    for line in info_file:
        tmp = line.split(',')
        info[tmp[0]] = tmp[1][:-1]
    for i in range(len(users)):
        if i != 0:
            result.write(',')
        if users[i] in info:
            result.write(info[users[i]])
        else: 
            result.write('-')
    result.write('\n')
