user_files = './normalized_profiles/users/'
object_files = './normalized_profiles/objects/'

num_users = 1012
num_objects = 656

users = open(user_files + 'all.txt').read().split('\n')
objects = open(object_files + 'all.txt').read().split('\n')

err = open('database_errors.log', 'w')

for i in range(num_users):
    f = open(user_files + users[i] + '.txt', 'r')
    profile = {}
    for line in f:
        t = line.split(':') # remember that line has '\n' as its last char
        try:
            profile[int(t[0])] = int(t[1])
        except ValueError as ve:
            if not 'invalid literal for int() with base 10' in str(ve):     # to avoid saving non-decimal marks (errors from crawler)
                raise ve
#    if len(profile) == 0:
#        users.remove(users[i])                                              # to delete profiles consisted of only non-decimal marks
#        continue
    for obj in profile:
        f = open(object_files + objects[obj] + '.txt', 'r')
        flag = False
        for line in f:
            t = line.split(':')
            if int(t[0]) == i:
                flag = True
                if int(t[1]) != profile[obj]:
#                    flag = True
#                else:
#                    flag = 2
                    err.write('profile of user №' + str(i) + ' contrs profile of object №' + str(obj) + ', marks are ' + str(profile[obj]) + ' vs ' + t[1] + '\n') # maybe i will fix it manually
                break
        f.close()
        if flag == False:
            err.write('profile of user №' + str(i) + ' had mark not saved in profile of object №' + str(obj) + ':' + str(profile[obj]) + '\n')
            f = open(object_files + objects[obj] + '.txt', 'a')
            f.write(str(i) + ':' + str(profile[obj]))
            f.close()
    f = open(user_files + users[i] + '.txt', 'w')
    for obj in profile:
        f.write(str(obj) + ':' + str(profile[obj]) + '\n')                       # to delete duplicates


for i in range(num_objects):
    f = open(object_files + objects[i] + '.txt', 'r')
    profile = {}
    for line in f:
        t = line.split(':') # remember that line has '\n' as its last char
        try:
            profile[int(t[0])] = int(t[1])
        except ValueError as ve:
            if not 'invalid literal for int() with base 10' in str(ve):     # to avoid saving non-decimal marks (errors from crawler)
                raise ve
#    if len(profile) == 0:
#        objects.remove(objects[i])
#        continue
    for u in profile:
        f = open(user_files + users[u] + '.txt', 'r')
        flag = False
        for line in f:
            t = line.split(':')
            if int(t[0]) == i:
                flag = True
                if int(t[1]) != profile[u]:
#                    flag = True
#                else:
#                    flag = 2
                    err.write('profile of object №' + str(i) + ' contrs profile of user №' + str(u) + ', marks are ' + str(profile[u]) + ' vs ' + t[1] + '\n') # maybe i will fix it manually
                break
        f.close()
        if flag == False:
            err.write('profile of object №' + str(i) + ' had mark not saved in profile of user №' + str(u) + ':' + str(profile[u]) + '\n')
            f = open(user_files + users[obj] + '.txt', 'a')
            f.write(str(i) + ':' + str(profile[u]))
            f.close()
    f = open(object_files + objects[i] + '.txt', 'w')
    for u in profile:
        f.write(str(u) + ':' + str(profile[u]) + '\n')                       # to delete duplicates
