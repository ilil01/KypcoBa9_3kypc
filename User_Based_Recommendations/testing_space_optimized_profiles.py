from testing import Test
from space_optimized_process_profiles import processing

users_prefix = 'users/'
objects_prefix = 'objects/'

use = Test(processing())

print (use.test_object.predict(0, 7, 0.))

print(use.test_on_all())
