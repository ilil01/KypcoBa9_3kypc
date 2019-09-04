#!/usr/bin/python3

import os

expected_profiles = open('./users/all.txt', 'r').readlines()
for i in range(len(expected_profiles)):
    expected_profiles[i] = expected_profiles[i][1:-1]
#    print (i[28:-1])

existing_profiles = os.listdir('./users/')
for i in range(len(existing_profiles)):
    existing_profiles[i] = existing_profiles[i][:-4]
#    print(i[:-4])

existing_profiles.remove('all')
f = open('./all_users_profiles.txt', 'w')
for i in existing_profiles:
    f.write(i + '\n')

raise Exception('end of the program')

print(str(expected_profiles[0]) + '|' + str(existing_profiles[0]))

for i in existing_profiles:
    try:
        expected_profiles.remove(i)
    except:
        print(i)

print ('+'*100)

for i in expected_profiles:
    print(i)
