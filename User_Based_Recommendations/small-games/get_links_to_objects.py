import requests
import json
from lxml import etree
from bs4 import BeautifulSoup

addr = 'https://small-games.info/'
try_addr = 'https://small-games.info/?go=game&c=13&i=15618'
headers = {
        'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Cookie' : 'log=ilil01'
}

proxies = {
        'http' : ''
}

#main_page = requests.get(addr)
#bs = BeautifulSoup(main_page.text, 'lxml')
#try_page = requests.get('https://small-games.info/?go=game&c=13&i=15618', auth = ('ilil01', 'Qkl983V1'))
#bs = BeautifulSoup(try_page.text, 'lxml')

s = requests.Session()
#s.get(try_addr)
s.post(addr, data = {'login' : 'ilil01', 'pass' : 'Qkl983V1'})

r = s.get(try_addr)
bs = BeautifulSoup(r.text, 'lxml')

print (s.__attrs__) 
print (s.cookies)
print (s.headers)
print (bs)

raise Exception ('end')

s = requests.Session()
print ('Trying to establish Session')
s.get(addr)
print ('Session established, logging in')
s.post(addr, data = {'login' : 'ilil01', 'pass' : 'Qkl983V1'})
print ('Logged in, start downloading')

# <a href = '*game*' *>

#r = s.get(addr)
#bs = BeautifulSoup(r.text, 'lxml')

num_pages = 1743
saveto = open('corrected_objects_links.txt', 'w')
print ('Output file created')

for i in range(1, num_pages + 1):
    try:
        r = s.get(addr + '?s=' + str(i))
    except:
        print ('Connection failed, trying to establish new Session')
        s = requests.Session()
        print ('Trying to establish Session')
        s.get(addr)
        print ('Session established, logging in')
        s.post(addr, data = {'login' : 'ilil01', 'pass' : 'Qkl983V1'})
        print ('Logged in, continue downloading')
    print(r.ok)
    bs = BeautifulSoup(r.text, 'lxml')
    for a in bs.find_all('a'):
        print('*', end = '')
        link = a.get('href')
        if 'go=game' in link and not '#' in link:
            saveto.write(addr + link + '\n')
    print('\n')
