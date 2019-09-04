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
            self.users[i] = all_users[i]

        all_objects = open(objects_prefix + 'all.txt', 'r').read().split('\n')
        all_objects.remove('')
        for i in range(len(all_objects)):
            title = all_objects[i]
            id_ = i
#            self.objects[int(id_)] = title
            self.objects[title] = int(id_)

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
            title = line[:line.find(':', -4)]
            try:
                d[self.objects[title]] = int(line.split(':')[-1])
            except ValueError as ve:
                if not 'invalid literal for int() with base 10:' in str(ve):
                    raise ve
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
        if not obj in self.objects.values():
            raise ValueError ('object id must be < ' + str(len(self.objects)))
        if not user in self.user_sims:
            self.init_user_sims(user)
        sim_users = []
        s = 0.
#        obj_name = self.objects[obj]
        for u in self.user_sims[user]:
#            if u != user and self.user_sims[user][u] > threshold and obj_name in self.user_profiles[u]:
            if u != user and self.user_sims[user][u] > threshold and obj in self.user_profiles[u]:
                sim_users.append(u)
                s += self.user_sims[user][u]
        if len(sim_users) == 0:
#            raise ValueError ('not enough information for user number ' + str(user) + ' and object number ' + str(obj))
            return 0.
        mark = 0.
        for u in sim_users:
#            mark += self.matrix[i][obj] * self.distances[user][i]
            mark += self.user_profiles[u][obj] * self.user_sims[user][u]
        mark /= s
        return mark

