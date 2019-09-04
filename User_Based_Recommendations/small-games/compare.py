from math import isclose

sample = open('./frequent_recommends_sample.txt', 'r')
my = open('./frequent_recommends.txt', 'r')
old = open('./frequent_recommends_old.txt', 'r')

my_quality = 0
old_quality = 0

for i in range(1007):
    sample.readline()
    my.readline()
    old.readline()
    s = eval(sample.readline())
    m = my.readline()
    try:
        m = eval(m)
    except:
        m = -1
    o = eval(old.readline())

    s_isInt = False
    try:
        len(s)
    except:
        s_isInt = True

    m_isInt = False
    try:
        len(m)
    except:
        m_isInt = True

    o_isInt = False
    try:
        len(o)
    except:
        o_isInt = True

    if s_isInt:
        if m_isInt:
            if isclose(s, m):
                my_quality += 1
        else:
            if s in m:
                my_quality += 1
        if o_isInt:
            if isclose(s, o):
                old_quality += 1
        else:
            if s in o:
                old_quality += 1
    else:
        if m_isInt:
            if m in s:
                my_quality += 1
        else:
            for j in m:
                if j in s:
                    my_quality += 1
        if o_isInt:
            if o in s:
                old_quality += 1
        else:
            for j in o:
                if j in s:
                    old_quality += 1

print('My quality == ' + str(my_quality))
print('Old quality == ' + str(old_quality))
