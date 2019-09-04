import requests
import json
from lxml import etree
from bs4 import BeautifulSoup

addr = 'http://www.small-games.info/'
addr = 'https://small-games.info/'

src_filename = 'actual_objects_links.txt'
src = open(src_filename, 'r')

#t = src.readline()
#print (t)
#print (t[:-1]) that's the name without '\n'
#print (t[:-2])

#raise Exception(e)

users_prefix = './users/'
objects_prefix = './objects/'

users_list = []

all_users = open(users_prefix + 'all.txt', 'a')
all_objects = open(objects_prefix + 'all.txt', 'r')

print ('Skipping already done links')
tmp = 0
while all_objects.readline() != '':
#    print ('*', end = '')
    src.readline()
    tmp += 1
print ('Skipped ' + str(tmp) + ' links')

all_objects.close()
print ('Opening file for list of all objects to append')
all_objects = open(objects_prefix + 'all.txt', 'a')
print ('Success')

print ('Establishing session')
s = requests.Session()
print ('Session established, logging in')
s.post(addr, data = {'login' : 'ilil01', 'pass' : 'Qkl983V1'})
print ('Logged in, start downloading')

#r = s.get(tmp)
#bs = BeautifulSoup(r.text, 'lxml')

#t = bs.find('div', attrs = {'class' : 'sp'})
#users = [a.get('href') for a in t.find_all('a')]
#tmp = t.get_text()
#marks = tmp[tmp.find(':') + 1:].split(',')#(' - ')
#marks = tmp.split(' - ')[1:]
#for i in range(len(marks)):
#    marks[i] = marks[i].split(' ')[-1]
#    marks[i] = marks[i][:2] if marks[i][1].isdigit() else marks[i][0]

for line in src:
    print ('Getting access to ' + line)
    try:
        r = s.get(line)
    except requests.exceptions.ConnectionError:
        print ('Failure, trying another time')
        r = s.get(line)
    print ('Success')
    bs = BeautifulSoup(r.text, 'lxml')
    t = bs.find('div', attrs = {'class' : 'sp'})
    if t == None:
        continue
    if not 'Игре' in t.get('title'):
        continue
    voted = [a.get('href') for a in t.find_all('a')]
    marks = t.get_text().split(' - ')[1:]
#    print (marks)
#    print ('***')
    for i in range(len(marks)):
#        marks[i] = marks[i].split(' ')[-1]
        marks[i] = marks[i][:2] if marks[i][1].isdigit() else marks[i][0]
#    print(voted)
#    print(marks)
    obj_name = line.split('/')[-1][:-1]

#    print (obj_name)
#    print (obj_name[:-1]) actual name
#    print (obj_name[:-2])
#    raise Exception ('end')
#    obj_file = open(objects_prefix + line[:-1] + '.txt', 'w')

    obj_file = open(objects_prefix + obj_name + '.txt', 'w')
    for i in range(len(voted)):
        if not voted[i] in users_list:
            users_list.append(voted[i])
            all_users.write(voted[i] + '\n')
        user_file = open(users_prefix + voted[i] + '.txt', 'a')
        try:
            user_file.write(obj_name + ':' + marks[i] + '\n')
        except Exception as e:
            print (voted)
            print (marks)
            raise e
        user_file.close()
        obj_file.write(voted[i] + ':' + marks[i] + '\n')
    obj_file.close()
    all_objects.write(line)


