# stop was on 49th users cluster

clustered_users = []
clustered_objects = []

for i in range(102):
    f = open('./users/' + str(i) + '.txt', 'r')
    clustered_users += f.readline().split(' ')
    for line in f:
        clustered_users += line.split(' ')
    f.close()
    while '' in clustered_users:
        clustered_users.remove('')
    while '\n' in clustered_users:
        clustered_users.remove('\n')

for i in range(66):
    f = open('./objects/' + str(i) + '.txt', 'r')
    clustered_objects += f.readline().split(' ')
    for line in f:
        clustered_objects += line.split(' ')
    f.close()
    while '' in clustered_objects:
        clustered_objects.remove('')
    while '\n' in clustered_objects:
        clustered_objects.remove('\n')

#print(clustered_users)
#print(clustered_objects)

clustered_users = [int(x) for x in clustered_users]
clustered_objects = [int(x) for x in clustered_objects]

clustered_users = sorted(clustered_users)
clustered_objects = sorted(clustered_objects)

print(len(clustered_users))
print(len(clustered_objects))

# objects are without problems, but nevertheless

for i in range(1, len(clustered_users)):
    if clustered_users[i] - clustered_users[i - 1] != 1:
        print('\t' + str(clustered_users[i - 1]) + ', ' + str(clustered_users[i]))

for i in range(1, len(clustered_objects)):
    if clustered_objects[i] - clustered_objects[i - 1] != 1:
        print('\t\t' + str(clustered_objects[i - 1]) + ', ' + str(clustered_objects[i]))
