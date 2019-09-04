# hi

user_files = './normalized_profiles/users/'
object_files = './normalized_profiles/objects/'

num_users = 1012
num_objects = 656

users = open(user_files + 'all.txt').read().split('\n')
objects = open(object_files + 'all.txt').read().split('\n')

users_marks = 0
objects_marks = 0

for i in range(num_users):
    f = open(user_files + users[i] + '.txt', 'r')
    users_marks += len(f.readlines())

for i in range(num_objects):
    f = open(object_files + objects[i] + '.txt', 'r')
    objects_marks += len(f.readlines())

print('users_marks == ' + str(users_marks))
print('objects_marks == ' + str(objects_marks))
