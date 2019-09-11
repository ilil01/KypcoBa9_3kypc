from math import isclose

sample = open('./frequent_recommends_sample.txt', 'r')
my = open('./frequent_recommends.txt', 'r')
old = open('./frequent_recommends_old.txt', 'r')
alt = open('./frequent_recommends_alt.txt', 'r')

my_quality = 0
old_quality = 0
alt_quality = 0

n_my = 0
n_old = 0
n_alt = 0
n_sample = 0

for i in range(1007):
    sample.readline()
    my.readline()
    old.readline()
    alt.readline()
    s = eval(sample.readline())
    m = my.readline()
    try:
        m = eval(m)
    except:
        m = -1
    o = eval(old.readline())
    
    a = alt.readline()
    try:
        a = eval(a)
    except:
        a = -1

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

    a_isInt = False
    try:
        len(a)
    except:
        a_isInt = True

    if s_isInt:
        n_sample += 1
        if m_isInt:
            n_my += 1
            if isclose(s, m):
                my_quality += 1
        else:
            n_my += len(m)
            if s in m:
                my_quality += 1
        if o_isInt:
            n_old += 1
            if isclose(s, o):
                old_quality += 1
        else:
            n_old += len(o)
            if s in o:
                old_quality += 1
        if a_isInt:
            n_alt += 1
            if isclose(s, a):
                alt_quality += 1
        else:
            n_alt += len(a)
            if s in a:
                alt_quality += 1
    else:
        n_sample += len(s)
        if m_isInt:
            n_my += 1
            if m in s:
                my_quality += 1
        else:
            n_my += len(m)
            for j in m:
                if j in s:
                    my_quality += 1
        if o_isInt:
            n_old += 1
            if o in s:
                old_quality += 1
        else:
            n_old += len(o)
            for j in o:
                if j in s:
                    old_quality += 1
        if a_isInt:
            n_alt += 1
            if a in s:
                alt_quality += 1
        else:
            n_alt += len(a)
            for j in a:
                if j in s:
                    alt_quality += 1

print('My quality == ' + str(my_quality) + ', in %:' + str(my_quality / n_my * 100))
print('Old quality == ' + str(old_quality) + ', in %:' + str(old_quality / n_old * 100))
print('Alt quality == ' + str(alt_quality) + ', in %:' + str(alt_quality / n_alt * 100))
