#from process import main_class
import process_profiles
import process_profiles_item_based

testing_user = 58

#use1 = process.main_class()
use1 = process_profiles.processing()
use2 = process_profiles_item_based.processing()

test_indices = []

#use1.init_user_profile(testing_user)
use1.init_all_user_profiles()
use2.init_all_profiles()

print (use1.user_profiles[testing_user])
#print (use2
test_indices = list(use1.user_profiles[testing_user].keys())

for indice in test_indices:
    print (str(indice) + ', ' + str(use1.user_profiles[testing_user][indice]) + ' : ' + str(use1.predict(testing_user, indice, 0.)) + ', ' + str(use2.predict(testing_user, indice, 0.)))
