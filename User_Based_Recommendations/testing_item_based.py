from testing import Test
from process_item_based import main_class
from process_profiles_item_based import processing

users_prefix = 'users/'
objects_prefix = 'objects/'

tmp = open(users_prefix + 'all.txt', 'r').read().split('\n')
tmp.remove('')
num_users = len(tmp)
tmp = open(objects_prefix + 'all.txt', 'r').read().split('\n')
tmp.remove('')
num_objects = len(tmp)
#use = Test(main_class(num_users, num_objects, 'generated_matrix.txt'))
use = Test(processing())
use.test_object.init_all_profiles()
for obj in use.test_object.objects:
    use.test_object.init_sims(obj)
max_sim = -500.
for i in use.test_object.sims:
    for j in use.test_object.sims[i]:
        if j > max_sim:
            max_sim = j
print(use.test_on_all())
