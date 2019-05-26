import numpy as np
import pandas as pd

from scipy.spatial import distance

from sklearn.metrics.pairwise import cosine_similarity

class processing:
    def __init__ (self, users_prefix = 'users/', objects_prefix = 'objects/'):
        self.users = dict()
        self.objects = dict()
        self.user_profiles = dict()
        self.user_sims = dict()
        self.users_prefix = users_prefix
        self.objects_prefix = objects_prefix

        all_users = open(users_prefix + 'all.txt', 'r').read().split('\n')
        all_users.remove('')
        for i in range(len(all_users)):
            tmp = all_users[i].split(',')
            self.users[int(tmp[1])] = tmp[0]

        all_objects = open(objects_prefix + 'all.txt', 'r').read().split('\n')
        all_objects.remove('')
        for i in range(len(all_objects)):
            title = all_objects[i][:all_objects[i].find(',', -5)]
            id_ = all_objects[i].split(',')[-1]
            self.objects[int(id_)] = title

    def init_user_profile (self, user):
        if not user in self.user_profiles:
            self.update_user_profile(user)
#        else:
#            print ('???')

    def update_user_profile (self, user):
        f = open(self.users_prefix + self.users[user] + '.txt', 'r')
#        self.user_profiles[user] = set()
        self.user_profiles[user] = dict()
        d = dict()
        for line in f:
#            d = dict()
#            d['title'] = line[:line.find(',', -3)]
#            d['mark'] = int(line.split(',')[-1])
#            self.user_profiles[user].add(d)
            d[line[:line.find(',', -3)]] = int(line.split(',')[-1])
        self.user_profiles[user] = d

    def similarity (self, user1, user2):
        if not (user1 in self.user_profiles and user2 in self.user_profiles):
            raise ValueError ("you must first initialize users' profiles")
        commons = set(self.user_profiles[user1].keys()).intersection(self.user_profiles[user2].keys())
        norm_mul = len(set(self.user_profiles[user1].keys()).union(self.user_profiles[user2].keys()))
        if len(commons) == 0:
            return 0.
        marks1 = []
        marks2 = []
        for title in commons:
            marks1.append(self.user_profiles[user1][title])
            marks2.append(self.user_profiles[user2][title])
        return cosine_similarity([marks1], [marks2])[0][0] * len(commons) / norm_mul

    def init_all_user_profiles (self):
        for user in self.users:
            self.init_user_profile(user)

    def update_all_user_profiles (self):
        for user in self.users:
            self.update_user_profile(user)

    def init_user_sims (self, user):
        if not user in self.user_sims:
            self.update_user_sims(user)

    def update_user_sims (self, user):
        if not user in self.users:
            raise ValueError ('user id must be < ' + str(len(self.users)))
        self.user_sims[user] = dict()
        for another_user in self.users:
            self.user_sims[user][another_user] = self.similarity(user, another_user)

    def predict(self, user, obj, threshold = 0.001):
        if not user in self.users:
            raise ValueError ('user id must be < ' + str(len(self.users)))
        if not obj in self.objects:
            raise ValueError ('object id must be < ' + str(len(self.objects)))
        if not user in self.user_diffs:
            self.init_user_sims(user)
        sim_users = []
        for u in self.user_sims:
            if self.user_sims[u] > threshold and self.user_profiles[u][self.objects[obj]] >= 0.001:
                sim_users.append(u)
        if len(sim_users) == 0:
            raise ValueError ('not enough information for user number ' + str(user) + ' and object number ' + str(obj))
        :


use = processing()

test_user1 = 3
test_user2 = 10

use.init_user_profile(test_user1)
use.init_user_profile(test_user2)

print(use.user_profiles[test_user1])
print(use.user_profiles[test_user2])
print(use.similarity(test_user1, test_user2))

max_similarity = -500

for i in range(len(use.users)):
    for j in range(i + 1, len(use.users)):
        use.init_user_profile(i)
        use.init_user_profile(j)
        tmp = use.similarity(i, j)
        if tmp > max_similarity:
            max_similarity = tmp
            test_user1 = i
            test_user2 = j

print(max_similarity)
print(use.user_profiles[test_user1])
print(use.user_profiles[test_user2])
print(use.similarity(test_user1, test_user2))
