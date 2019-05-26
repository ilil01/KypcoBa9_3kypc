source = 'database_in_python_structures.txt'
f = open(source, "r")
info = eval(f.read())
f.close()

user_profiles = dict()
object_profiles = dict()
objects = []

for block in info:
    # 0 is 'name', rest {'link', 'title', 'mark'}
    # for correct saving cut block[0].split('/')[-1]
    name = block[0].split('/')[-1]
    user_profiles[name] = []
    for i in range(1, len(block)):
        if block[i]['mark'] != '–':
            user_profiles[name].append({'title' : block[i]['title'].replace('/', '_'), 'mark' : int(block[i]['mark'])})
#            objects.append(block[i]['title'])
            title = block[i]['title'].replace('/', '_')
            if not title in object_profiles:
                object_profiles[title] = []
            object_profiles[title].append({'name' : name, 'mark' : int(block[i]['mark'])})

# print (str(len(user_profiles)) + ' users and ' + str(len(object_profiles)) + 'objects')

# print ('users')
# for user in user_profiles:
#    print(user)
#    for obj in user_profiles[user]:
#        print(obj)

users_prefix = 'users/'
objects_prefix = 'objects/'

all_users = open(users_prefix + 'all.txt', 'w')

users = list(user_profiles.keys())
objects = list(object_profiles.keys())

for i in range(0, len(user_profiles)):
    all_users.write(str(users[i]) + ',' + str(i) + '\n')
#    print(str(users[i]) + ':' + str(i))
all_users.close()

all_objects = open(objects_prefix + 'all.txt', 'w')


for i in range(0, len(objects)):
    all_objects.write(str(objects[i]) + ',' + str(i) + '\n')
#    print(str(objects[i]) + ':' + str(i))
all_objects.close()

for user in users:
    f = open(users_prefix + user + '.txt', 'w')
    for info in user_profiles[user]:
        f.write(info['title'] + ',' + str(info['mark']) + '\n')
    f.close()


for obj in objects:
    f = open(objects_prefix + obj + '.txt', 'w')
    for info in object_profiles[obj]:
        f.write(info['name'] + ',' + str(info['mark']) + '\n')
    f.close()

matrix_file = open('matrix.txt', 'w')

for i in range(len(objects)):
    title = objects[i]
    for j in range(len(users)):
        tmp = user_profiles[users[j]]
        flag = False
        for info in tmp:
            if info['title'] == title:
                flag = True
                matrix_file.write(str(info['mark']))
                break
        if flag == False:
            matrix_file.write('-')
        if j != len(users) - 1:
            matrix_file.write(',')
    matrix_file.write('\n')

matrix_file.close()
