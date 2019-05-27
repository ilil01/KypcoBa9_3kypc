import numpy as np
import pandas as pd

from scipy.spatial import distance

from sklearn.metrics.pairwise import cosine_similarity

class processing:
    def __init__ (self, users_prefix = 'users/', objects_prefix = 'objects/'):
# We are able to not store all profiles and similarities in main memory
        self.users = dict()
        self.objects = dict()
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
            self.objects[title] = int(id_)

    def init_user_profile (self, user):
        return self.update_user_profile(user)

    def update_user_profile (self, user):
        if not user in self.users:
            raise ValueError ('user id must be < ' + str(len(self.users)))
        f = open(self.users_prefix + self.users[user] + '.txt', 'r')
        d = dict()
        for line in f:
            title = line[:line.find(',', -4)]
            d[self.objects[title]] = int(line.split(',')[-1])
        return d

    def similarity (self, user1_profile, user2_profile):
        commons = set(user1_profile.keys()).intersection(user2_profile.keys())
        norm_mul = len(set(user1_profile.keys()).union(user2_profile.keys()))
        if len(commons) == 0:
            return 0.
        marks1 = []
        marks2 = []
        for title in commons:
            marks1.append(user1_profile[title])
            marks2.append(user2_profile[title])
        return cosine_similarity([marks1], [marks2])[0][0] * len(commons) / norm_mul

    def init_user_sims (self, user):
        return self.update_user_sims(user)

    def update_user_sims (self, user):
        if not user in self.users:
            raise ValueError ('user id must be < ' + str(len(self.users)))
        user_sims = dict()
        user_profile = self.init_user_profile(user)
        for another_user in self.users:
            user_sims[another_user] = self.similarity(user_profile, self.init_user_profile(another_user))
        return user_sims

    def predict(self, user, obj, threshold = 0.001):
        if not user in self.users:
            raise ValueError ('user id must be < ' + str(len(self.users)))
        if not obj in self.objects.values():
            raise ValueError ('object id must be < ' + str(len(self.objects)))
#        sims = self.init_user_sims(user)
        s = 0.
        mark = 0.
        user_profile = self.init_user_profile(user)
 #       for u in sims:
        for u in self.users:
            if u == user:
                continue
            u_p = self.init_user_profile(u)
            sim = self.similarity(user_profile, u_p)
            if sim > threshold and obj in u_p:
                s += sim
                mark += u_p[obj] * sim
        if s <= 0.0001:
            return 0.
        mark /= s
#        print ('*', end = '')
        return mark
