# We have in clusters/[users/, objects/] for every cluster list of who belongs to it
# Algorithm for recommendation:
#   0) Initiate for-use profiles: for every user generate list consisting of its cluster and its average marks in every object cluster and save it into './use/users'
#       Also in same file write user's average 'popularity' of objects' clusters to make recommendation more fair
#   1) For user u:
#       1.1) Initiate list of pre-possibilities whether user will choose object from that cluster, using its' popularity if above average. For non-marked: calculate sum of those under average but above 0 and divide fairly. For others use half of non-marked
#       1.2) Initiate list of possibilities by normalizing pre-possibilities (sum must equals to 1.0)
#       1.3) Choose cluster randomly with calculated possibilities
#       1.4) For every object in chosen cluster, non-marked by u, 'popularity' is average mark by users from u's cluster except u itself. If every equals to 0, every will be 1.0
#       1.5) Normalization as for clusters, choice also

from bbac import BBAC   #   because a lot useful already is there
from random import random

class recommend:
    def __init__(self, num_u = 1012, num_o = 656, num_uc = 102, num_oc = 66, cluster_path = './clusters/', profiles_path = './normalized_profiles/'):
        self.funcs = BBAC(num_u, num_o, num_uc, num_oc, cluster_path, profiles_path)

    def init_popularities(self, u, isUser):
        if u >= self.funcs.num_u:
            raise ValueError ('non-existing user; if new, rerun bbac or wait for next rerun')
        profile = self.funcs.get_profile(u, isUser)
        popularities = [0 for x in range(self.funcs.num_oc if isUser else self.funcs.num_uc)]
        zeros = []
        path1 = 'aa'
        path2 = 'bb'
        if isUser:
            path1 = self.funcs.cluster_path + 'objects/'
            path2 = './use/users/'
        else:
            path1 = self.funcs.cluster_path + 'users/'
            path2 = './use/objects/'
            pass
        for i in range(self.funcs.num_oc):
#            f = open(self.funcs.cluster_path + 'objects/' + str(i) + '.txt', 'r')
            f = open(path1 + str(i) + '.txt', 'r')
            objects = f.readline().split(' ')
            for line in f:
                objects += line.split(' ')
            f.close()
            while '' in objects:
                objects.remove('')
            while '\n' in objects:
                objects.remove('\n')
            objects = [int(x) for x in objects]
            n = 0
            for obj in objects:
                if obj in profile:
                    popularities[i] += profile[obj]
                    n += 1
            if n != 0:
                popularities[i] /= n
            else:
                zeros.append(i)
#        if not isUser:
#            f = open(path2 + str(u) + '.txt', 'w')
#            f.write(str(popularities))
#            f.close
#            return 
#        if len(zeros) != 0:
#            average = sum(popularities) / len(popularities)
#            below_avg = []
#            for i in range(len(popularities)):
#                if 0 < popularities[i] < average:
#                    below_avg.append(i)
#            tmp = sum([popularities[x] for x in below_avg]) / len(zeros)
#            for i in zeros:
#                popularities[i] = tmp
#            for i in below_avg:
#                popularities[i] = tmp / 2.0
#            tmp = sum(popularities)
#            popularities = [x / tmp for x in popularities]
#        f = open('./use/users/' + str(u) + '.txt', 'w')
        f = open(path2 + str(u) + '.txt', 'w')
        f.write(str(popularities))
        f.close()

    def init_all_popularities(self):
        zeros = open(self.funcs.cluster_path + 'users/zeros.txt', 'r').read().split(' ')
        while '' in zeros:
            zeros.remove('')
        while '\n' in zeros:
            zeros.remove('\n')
        zeros = [int(x) for x in zeros]
        for i in range(self.funcs.num_u):
            if i not in zeros:
                self.init_popularities(i, True)
        for i in range(self.funcs.num_obj):
            self.init_popularities(i, False)

    def choose(possibilities_list):
        tmp = random()
        i = 0
        while possibilities_list[i] <= tmp:
            tmp -= possibilities_list[i]
            i += 1
        return i

    def recommend(self, u):
        if u >= self.funcs.num_u:
            raise ValueError ('non-existing or new user')
        f = open('./use/users/' + str(u) + '.txt', 'r')
        ps = eval(f.read())
        f.close()
#        tmp = random()
#        i = 0
#        while ps[i] <= tmp:
#            tmp -= ps[i]
#            i += 1
        uc = self.funcs.get_cluster(u, True)
        if uc == -1:
            return -1
#            raise ValueError ('non-clustered user')
        potential = {}
        profile = self.funcs.get_profile(u, True)

        while len(potential) == 0:
            i = recommend.choose(ps)
#            print(i)
            # i is cluster
            f = open(self.funcs.cluster_path + 'objects/' + str(i) + '.txt', 'r')
            cluster = f.readline().split(' ')
            for line in f:
                cluster += line.split(' ')
            f.close()
            while '' in cluster:
                cluster.remove('')
#            while '\n' in potential:
            while '\n' in cluster:
                cluster.remove('\n')
            cluster = [int(x) for x in cluster]
#            print(cluster)
            for obj in cluster:
                if obj not in profile:
                    f = open('./use/objects/' + str(obj) + '.txt', 'r')
                    tmp = eval(f.read())
                    potential[obj] = tmp[uc]
#            print(potential)
#            print(profile)
            if len(potential) == 0:
                ps[i] = 0
#                ps.remove(0)
                tmp = sum(ps)
                try:
                    ps = [x / tmp for x in ps]
                except ZeroDivisionError as zde:
                    return -2   # cannot choose object, only by absolute random
#        avg = sum([potential[x] for x in potential]) / len(potential)
#        below_avg = []
#        zeros = []
#        for obj in potential:
#            if potential[obj] == 0:
#                zeros.append(obj)
#            elif potential[obj] < avg:
#                below_avg.append(obj)
#        if len(zeros) == len(potential):
#            for obj in potential:
#                potential[obj] = 1.0
#        elif len(zeros) != 0:
#            tmp = sum([potential[x] for x in below_avg]) / len(zeros)
#            for obj in zeros:
#                potential[obj] = tmp
#            for obj in below_avg:
#                potential[obj] = tmp / 2
        tmp = sum([potential[x] for x in potential])
        for obj in potential:
            potential[obj] /= tmp
        tmp = random()
        for obj in potential:
            if potential[obj] <= tmp:
                tmp -= potential[obj]
            else:
                return obj

