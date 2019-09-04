import os

indir_u = './users/'
outdir_u = './normalized_profiles/users/'

indir_o = './objects/'
outdir_o = './normalized_profiles/objects/'

f = open(indir_u + 'all.txt', 'r')
tmp = f.readlines()
users = dict()
for i in range(len(tmp)):
    users[tmp[i][:-1]] = i

f = open(indir_o + 'all.txt', 'r')
tmp = f.readlines()
objects = dict()
for i in range(len(tmp)):
    objects[tmp[i][:-1]] = i

for u in users:
    f1 = open(indir_u + u + '.txt', 'r')
    f2 = open(outdir_u + u + '.txt', 'w')
    for l in f1:
        tmp = l.find(':')
        obj_num = objects[l[:tmp]]
        f2.write(str(obj_num) + l[tmp:])

for obj in objects:
    f1 = open(indir_o + obj + '.txt', 'r')
    f2 = open(outdir_o + obj + '.txt', 'w')
    for l in f1:
        tmp = l.find(':')
        u_num = users[l[1:tmp]]
        f2.write(str(u_num) + l[tmp:])

