import numpy as np
from scipy.spatial import distance
from sklearn.metrics.pairwise import cosine_similarity

class matrix_based_predicting:
    def __init__ (self, users, objects, user_based = True, matrix_filename = 'matrix.txt'):
        self.matrix = np.ndarray((users, objects))
        f = open(matrix_filename, 'r')
        j = 0
        for line in f:
            column = line[:-1].split(',')
#            print (column)
            for i in range(len(column)):
                if column[i] == '-':
                    self.matrix[i][j] = 0
                elif column[i] == '':
                    raise Exception ('i == ' + str(i) + ', j == ' + str(j) + ', line is "' + line + '"')
                else:
                    self.matrix[i][j] = float(column[i])
            j += 1
        if user_based == False:
            self.matrix = self.matrix.T
        self.distances = cosine_similarity(self.matrix)
        self.user_based = user_based

    def predict (self, user, obj, threshold = 0.9):
        indices = []
        s = 0.
        mark = 0.
        if self.user_based:
            for i in range(self.matrix.shape[0]):
                if i != user and self.distances[user][i] >= threshold and self.matrix[i][obj] > 0.001:
                    indices.append(i)
                    s += self.distances[user][i]
        else:
            for i in range(self.matrix.shape[0]):
                if i != obj and self.distances[obj][i] >= threshold and self.matrix[i][user] > 0.001:
                    indices.append(i)
                    s += self.distances[obj][i]        
        if len(indices) == 0:
#            raise ValueError ('too big threshold' + str(threshold))
            return 0.
        if self.user_based:
            for i in indices:
                mark += self.matrix[i][obj] * self.distances[user][i]
        else:
            for i in indices:
                mark += self.matrix[i][user] * self.distances[obj][i]
        mark /= s
        return mark

class profiles_based_predicting:
    def __init__ (self, user_based = True users_prefix = 'users/', objects_prefix = 'objects/'):
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
            if user_based:
                self.users[int(tmp[1])] = tmp[0]
            else:
                self.users[tmp[0]] = int(tmp[1])

        all_objects = open(objects_prefix + 'all.txt', 'r').read().split('\n')
        all_objects.remove('')
        for i in range(len(all_objects)):
            title = all_objects[i][:all_objects[i].find(',', -5)]
            id_ = all_objects[i].split(',')[-1]
            if user_based:
                self.objects[title] = int(id_)
            else:
                self.objects[int(id_)] = title
        self.user_based = user_based

    def init_user_profile (self, user):
        if not user in self.profiles:
            self.update_user_profile(user)

    def update_user_profile (self, user):
        f = open(self.users_prefix + self.users[user] + '.txt', 'r')
        self.profiles[user] = dict()
        d = dict()
        for line in f:
            title = line[:line.find(',', -4)]
            d[self.objects[title]] = int(line.split(',')[-1])
        self.profiles[user] = d

    def init_object_profile (self, obj):
        if not obj in self.profiles:
            self.update_object_profile(obj)

    def update_object_profile (self, obj):
        f = open(self.objects_prefix + self.objects[obj] + '.txt', 'r')
        d = dict()
        for line in f:
            tmp = line.split(',')
            d[self.users[tmp[0]]] = int(tmp[1])
        self.profiles[obj] = d

    def similarity (self, user1, user2):
        if self.user_based == True:
            if not (user1 in self.profiles and user2 in self.profiles):
                raise ValueError ("you must first initialize users' profiles")
        else:
            if not (user1 in self.profiles and user2 in self.profiles):
                raise ValueError ("you must first initialize users' profiles")
        commons = set(self.profiles[user1].keys()).intersection(self.profiles[user2].keys())
        norm_mul = len(set(self.profiles[user1].keys()).union(self.profiles[user2].keys()))
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

    def init_all_object_profiles (self):
        for obj in self.objects:
            self.init_object_profile(obj)

    def update_all_object_profiles (self):
        for obj in self.objects:
            self.update_object_profile(obj)

    def init_user_sims (self, user):
        if not user in self.sims:
            self.update_user_sims(user)

    def update_user_sims (self, user):
        if not user in self.users:
            raise ValueError ('user id must be < ' + str(len(self.users)))
        self.sims[user] = dict()
        for another_user in self.users:
            self.user_sims[user][another_user] = self.similarity(user, another_user)

    def init_object_sims (self, obj):
        if not obj in self.sims:
            self.update_sims(obj)

    def update_object_sims (self, obj):
        if not obj in self.objects:
            raise ValueError ('object id must be < ' + str(len(self.objects)))
        self.sims[obj] = dict()
        for another_obj in self.objects:
            self.sims[obj][another_obj] = self.similarity(obj, another_obj)

    def predict(self, user, obj, threshold = 0.001):
        if self.user_based == True:
            if not user in self.users:
                raise ValueError ('user id must be < ' + str(len(self.users)))
            if not obj in self.objects.values():
                raise ValueError ('object id must be < ' + str(len(self.objects)))
            if not user in self.user_sims:
                self.init_user_sims(user)
        else:
            if not user in self.users.values():
                raise ValueError ('user id must be < ' + str(len(self.users)))
            if not obj in self.objects:
                raise ValueError ('object id must be < ' + str(len(self.objects)))
            if not obj in self.sims:
                self.init_sims(obj)
        sim_users = []
        s = 0.
        mark = 0.
        if self.user_based == True:
            for u in self.sims[user]:
                if u != user and self.user_sims[user][u] > threshold and obj in self.user_profiles[u]:
                    sim_users.append(u)
                    s += self.user_sims[user][u]
        else:
            for u in self.sims[obj]:
                if u != obj and self.sims[obj][u] > threshold and user in self.profiles[u]:
                    sim_users.append(u)
                    s += self.sims[obj][u]
        if len(sim_users) == 0:
            return 0.
        if self.user_based == True:
            for u in sim_users:
                mark += self.user_profiles[u][obj] * self.user_sims[user][u]
        else:
            for u in sim_objects:
                mark += self.profiles[u][user] * self.sims[obj][u]
        mark /= s
        return mark

