users_prefix = 'users/'
objects_prefix = 'objects/'

users = dict()
objects = dict()

all_users = open(users_prefix + 'all.txt', 'r').read().split('\n')
all_users.remove('')
for i in range(len(all_users)):
#    all_users[i] = all_users[i].split(',')[0]
    users[i] = '/' + all_users[i]
#print((all_users))


all_objects = open(objects_prefix + 'all.txt', 'r').read().split('\n')
all_objects.remove('')
for i in range(len(all_objects)):
    title = all_objects[i]
    id_ = i
    objects[int(id_)] = title

#for i in users:
#    print(str(i) + ' : ' + users[i])

#print ('*'*100)


#for i in objects:
#    print(str(i) + ' : ' + objects[i])

result_filename = 'generated_matrix.txt'
result = open(result_filename, 'w')

#print(users)
#print(objects)

for obj in objects:
    info_file = open(objects_prefix + objects[obj] + '.txt', 'r')
    # line :: user,mark
    info = dict()
    for line in info_file:
        tmp = line.split(':')
        info[tmp[0]] = tmp[1][:-1]
#    print (info)
    for i in range(len(users)):
        if i != 0:
            result.write(',')
        if users[i] in info:
            result.write(info[users[i]])
        else: 
            result.write('-')
    result.write('\n')
