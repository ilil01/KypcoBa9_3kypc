import numpy as np
import pandas as pd

from scipy.spatial import distance

from sklearn.metrics.pairwise import cosine_similarity

class processing:
    def __init__ (self, users_prefix = 'users/', objects_prefix = 'objects/'):
        self.users = dict()
        self.objects = dict()
        self.profiles = dict()
        self.sims = dict()
        self.users_prefix = users_prefix
        self.objects_prefix = objects_prefix

        all_users = open(users_prefix + 'all.txt', 'r').read().split('\n')
        all_users.remove('')
        for i in range(len(all_users)):
            tmp = all_users[i].split(',')
#            self.users[int(tmp[1])] = tmp[0]
            self.users[tmp[0]] = int(tmp[1])

        all_objects = open(objects_prefix + 'all.txt', 'r').read().split('\n')
        all_objects.remove('')
        for i in range(len(all_objects)):
            title = all_objects[i][:all_objects[i].find(',', -5)]
            id_ = all_objects[i].split(',')[-1]
            self.objects[int(id_)] = title
#            self.objects[title] = int(id_)

    def init_object_profile (self, obj):
        if not obj in self.profiles:
            self.update_object_profile(obj)

    def update_object_profile (self, obj):
        f = open(self.objects_prefix + self.objects[obj] + '.txt', 'r')
        d = dict()
        for line in f:
#            title = line[:line.find(',', -4)]
#            d[self.users[title]] = int(line.split(',')[-1])
            tmp = line.split(',')
            d[self.users[tmp[0]]] = int(tmp[1])
        self.profiles[obj] = d

    def similarity (self, obj1, obj2):
        if not (obj1 in self.profiles and obj2 in self.profiles):
            raise ValueError ("you must first initialize objects' profiles")
        commons = set(self.profiles[obj1].keys()).intersection(self.profiles[obj2].keys())
        norm_mul = len(set(self.profiles[obj1].keys()).union(self.profiles[obj2].keys()))
        if len(commons) == 0:
            return 0.
        marks1 = []
        marks2 = []
        for title in commons:
            marks1.append(self.profiles[obj1][title])
            marks2.append(self.profiles[obj2][title])
        return cosine_similarity([marks1], [marks2])[0][0] * len(commons) / norm_mul

    def init_all_profiles (self):
        for obj in self.objects:
            self.init_object_profile(obj)

    def update_all_profiles (self):
        for obj in self.objects:
            self.update_object_profile(obj)

    def init_sims (self, obj):
        if not obj in self.sims:
            self.update_sims(obj)

    def update_sims (self, obj):
        if not obj in self.objects:
            raise ValueError ('object id must be < ' + str(len(self.objects)))
        self.sims[obj] = dict()
        for another_obj in self.objects:
            self.sims[obj][another_obj] = self.similarity(obj, another_obj)

    def predict(self, user, obj, threshold = 0.001):
        if not user in self.users.values():
            raise ValueError ('user id must be < ' + str(len(self.users)))
        if not obj in self.objects:
            raise ValueError ('object id must be < ' + str(len(self.objects)))
        if not obj in self.sims:
            self.init_sims(obj)
        sim_objects = []
        s = 0.
        for u in self.sims[obj]:
            if u != obj and self.sims[obj][u] > threshold and user in self.profiles[u]:
                sim_objects.append(u)
                s += self.sims[obj][u]
        if len(sim_objects) == 0:
            return 0.
        mark = 0.
        for u in sim_objects:
            mark += self.profiles[u][user] * self.sims[obj][u]
        mark /= s
        return mark

