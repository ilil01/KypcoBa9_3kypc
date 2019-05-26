from testing import Test
from process import main_class

users_prefix = 'users/'
objects_prefix = 'objects/'

tmp = open(users_prefix + 'all.txt', 'r').read().split('\n')
tmp.remove('')
num_users = len(tmp)
#print (num_users)
tmp = open(objects_prefix + 'all.txt', 'r').read().split('\n')
tmp.remove('')
num_objects = len(tmp)
#print (num_objects)
#use = main_class(num_users, num_objects, 'generated_matrix.txt')
use = Test(main_class(num_users, num_objects, 'generated_matrix.txt'))
print(use.test_on_all())
