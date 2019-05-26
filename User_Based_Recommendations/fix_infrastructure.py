import os

users_prefix = 'users/'
objects_prefix = 'objects/'

all_users = open(users_prefix + 'all.txt', 'r').read().split('\n')
#for user in all_users:
#    if user == '':
#        all_users.remove(user)
#    else:
#        user = user.split(',')[0]
all_users.remove('')
for i in range(len(all_users)):
    all_users[i] = all_users[i].split(',')[0]
#print((all_users))


all_objects = open(objects_prefix + 'all.txt', 'r').read().split('\n')
all_objects.remove('')
for i in range(len(all_objects)):
#    all_objects[i] = all_objects[i].split(',')[0]
    all_objects[i] = all_objects[i][:all_objects[i].find(',', -5)]

#print (str(len(all_users)), str(len(all_objects)))
#print (all_objects)

for obj in all_objects:
    os.system('mv -t objects/ \"' + users_prefix + obj + '.txt\"')
