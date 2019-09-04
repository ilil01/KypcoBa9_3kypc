# Bregman Block Average Co-clustering
# g — users clustering function,    g:U→G
# h — objects clustering function,  h:R→H
# ~f_ur(g,h) = $f_g(u)h(r) + ($f_u - $f_g(u)) + ($f_r - $f_h(r))
#   $f_g(u)h(r) — average by bicluster
#   $f_g(u), $f_h(r) — average by cluster
#   $f_u, $f_r — average by user, object
# Quality: sum[by D э (u,r)](~f_ur(g,h) - f_ur)^2 → min[by g,h]
# D is set of marks

# For now let us assume that number of clusters for users or objects is ⅒(1/10) of corresponding number

def get_init_clusters(num_users, num_objects, num_u_clusters = 0, num_obj_clusters = 0):
    if num_u_clusters == 0:
        num_upc = 10
        num_u_clusters = num_users // num_upc
        num_u_left = num_users - num_u_clusters * num_upc
    if num_obj_clusters == 0:
        num_opc = 10
        num_obj_clusters = num_objects // num_opc
        num_obj_left = num_objects - num_obj_clusters * num_opc
    zeros = open('./clusters/users/zeros.txt', 'r').read().split(' ')
    for i in range(num_u_clusters):
        f = open('./clusters/users/' + str(i) + '.txt', 'w')
        for j in range(num_upc):
            if zeros.count(i * num_upc + j) == 0:
                f.write(str(i * num_upc + j) + ' ')
        f.close()
    f = open('./clusters/users/' + str(num_u_clusters) + '.txt', 'w')
    tmp = num_u_clusters * num_upc
    for j in range(num_u_left):
        if zeros.count(tmp + j) == 0:
            f.write(str(tmp + j) + ' ')
    f.close()
    for i in range(num_obj_clusters):
        f = open('./clusters/objects/' + str(i) + '.txt', 'w')
        for j in range(num_opc):
            f.write(str(i * num_opc + j) + ' ')
        f.close()
    f = open('./clusters/objects/' + str(num_obj_clusters) + '.txt', 'w')
    tmp = num_obj_clusters * num_opc
    for j in range(num_obj_left):
        f.write(str(tmp + j) + ' ')
    f.close()

class BBAC:
#    def __init__ (g, h):
#        self.g = g
#        self.h = h
    def __init__ (self, u, o, uc, oc, cluster_path = './clusters/', profiles_path = './normalized_profiles/'): # (number of users, number of objects, number of users' clusters, number of objects' clusters)
        self.num_u = u
        self.num_obj = o
        self.num_uc = uc
        self.num_oc = oc
        self.cluster_path = cluster_path
        self.profiles_path = profiles_path

    def get_profile(self, num, isUser):
        error_log_file = open('./errors.log', 'a')
        if isUser:
            users = open(self.profiles_path + 'users/all.txt', 'r').read().split('\n')
            if num >= self.num_u:
                raise ValueError("Non-existing user's number")
            f = open(self.profiles_path + 'users/' + users[num] + '.txt', 'r')
#            users.close()
            profile = {}
            for line in f:
                t = line.split(':')
                try:
                    profile[int(t[0])] = int(t[1])
                except ValueError as ve:
                    error_log_file.write('user №' + str(num) + ' : object №' + t[0] + '::' + str(ve) + '\n')
            f.close()
            error_log_file.close()
            return profile
        else:
            objects = open(self.profiles_path + 'objects/all.txt', 'r').read().split('\n')
            if num >= self.num_obj:
                raise ValueError("Non-existing object's number")
            f = open(self.profiles_path + 'objects/' + objects[num] + '.txt', 'r')
#            objects.close()
            profile = {}
            for line in f:
                t = line.split(':')
                try:
                    profile[int(t[0])] = int(t[1])
                except ValueError as ve:
                    error_log_file.write('object №' + str(num) + ' : user №' + t[0] + '::' + str(ve) + '\n')
            f.close()
            error_log_file.close()
            return profile
            

    def init_characteristics(self):

#        bic = [0 for i in range(self.num_oc)]
#        oc_lens = [0 for i in range(self.num_oc)]
        u = open(self.cluster_path + 'chrs/users.txt', 'w')                 # chars of users' clusters
        b = open(self.cluster_path + 'chrs/bi.txt', 'w')                    # chars of biclusters
        ob = open(self.cluster_path + 'chrs/objects.txt', 'w')              # chars of objects' clusters

        error_log_file = open('./errors.log', 'a')

        objects = open(self.profiles_path + 'objects/all.txt', 'r').read().split('\n')
        oc_lens = [0 for i in range(self.num_oc)]
        for i in range(self.num_oc):
            f = open(self.cluster_path + 'objects/' + str(i) + '.txt', 'r')
            cluster = f.read().split(' ')
            cluster.remove('')
            oc_lens[i] = len(cluster)
            s = 0
            n = 0
            for j in cluster:
                f = open(self.profiles_path + 'objects/' + objects[int(j)] + '.txt', 'r')
                for line in f:
#                    n += 1
                    try:
                        s += int(line.split(':')[1])
                        n += 1
                    except ValueError as ve:
                        error_log_file.write('object №' + j + ':user №' + line.split(':')[0] + '\n')
            if len(cluster) != 0:
                s /= len(cluster) * self.num_u # there we have $f_h(r) ## nope, we shall not process non-markes
#            if n != 0:
#                s /= n
            ob.write(str(s) + ' ')

        ob.close()

        users = open(self.profiles_path + 'users/all.txt', 'r').read().split('\n')
        for i in range(self.num_uc):
            f = open(self.cluster_path + 'users/' + str(i) + '.txt', 'r')
            cluster = f.read().split(' ')
            cluster.remove('')
            s = 0
            n = 0
            bic = [0 for i in range(self.num_oc)]
#            oc_lens = [0 for i in range(self.num_oc)]
            for j in cluster:
                profile = {}
                f = open(self.profiles_path + 'users/' + users[int(j)] + '.txt', 'r')
                for line in f:
#                    s += int(line.split(':')[1])
                    t = line.split(':')
#                    tmp.append((int(t[0]), int(t[1])))
                    try:
                        profile[int(t[0])] = int(t[1])
                        s += int(t[1])
                        n += 1
                    except ValueError as ve:
                        error_log_file.write('user №' + j + ':object №' + t[0] + '\n')
                for k in range(self.num_oc):
                    f = open(self.cluster_path + 'objects/' + str(k) + '.txt', 'r')
#                    t = [int(x) for x in f.read().split(' ')]
                    t = f.read().split(' ')
                    t.remove('')
                    t = [int(x) for x in t]
                    for l in t:
                        if l in profile:
                            bic[k] += profile[l]
#                            oc_lens[k] += 1
            for j in range(self.num_oc):
                if oc_lens[j] != 0 and len(cluster) != 0:
                    bic[j] /= oc_lens[j] * len(cluster)         # there we have a line of $f_g(u)h(r)
                b.write(str(bic[j]) + ' ')
            b.write('\n')
            if len(cluster) != 0:
                s /= len(cluster) * self.num_obj # there we have $f_g(u)
#            if n != 0:
#                s /= n
            u.write(str(s) + ' ')
        b.close()
        u.close()
        error_log_file.close()
    
    # So we have files './clusters/chrs/[users, objects].txt' with average marks by [users', objects'] clusters
    # And file './clusters/chrs/bi.txt' with matrix of average marks by biclusters [column is the number of objects' cluster and row — users']

    def generate_average(self, num, isUser):
#        if isUser:
#            if num >= self.num_u:
#                raise ValueError('Non-existing user number')
#            f = open(self.profiles_path + 'users/' + str(num) + '.txt', 'r')
        profile = self.get_profile(num, isUser)
        if len(profile) == 0:
#            print(profile, num, 'isUser == ' + str(isUser))
            return 0
#            return (0, 0)
        tmp = 0
        if isUser:
            tmp = self.num_obj
        else:
            tmp = self.num_u
        return sum([profile[x] for x in profile]) / tmp # len(profile)
#        s = sum([profile[x] for x in profile]) / len(profile)
#        ss = 0
#        for i in profile:
#            ss += profile[i]
#        ss /= len(profile)
#        return (s, ss)

    def generate_all_averages(self):
        users = open('./avgs/users.txt', 'w')
        for i in range(self.num_u):
            users.write(str(self.generate_average(i, True)) + '\n')
        users.close()
        objects = open('./avgs/objects.txt', 'w')
        for i in range(self.num_obj):
            objects.write(str(self.generate_average(i, False)) + '\n')
        objects.close()

    def get_average(self, num, isUser):
        f = 'something to initiate'
        if isUser:
            if num >= self.num_u:
                raise ValueError('That user does not exist')
            f = open('./avgs/users.txt', 'r')
        else:
            if num >= self.num_obj:
                raise ValueError('That object does not exist')
            f = open('./avgs/objects.txt', 'r')
        avg = f.readline()
        for i in range(num):
            avg = f.readline()
        f.close()
        return float(avg)

    def get_cluster_average(self, num, isUser):
        f = 'qqq'
        if isUser:
            if num >= self.num_uc:
                raise ValueError('Non-existing user cluster')
            f = open(self.cluster_path + 'chrs/users.txt', 'r')
        else:
            if num >= self.num_oc:
                raise ValueError('Non-existing object cluster')
            f = open(self.cluster_path + 'chrs/objects.txt', 'r')
        chars = f.read().split(' ')
        f.close()
        try:
            return float(chars[num])
        except ValueError as ve:
            print(chars, num, chars[num])
            raise ve

    def get_bicluster_average(self, num_uc, num_oc):
        if num_uc >= self.num_uc:
            raise ValueError('That user cluster does not exist')
        if num_oc >= self.num_oc:
            raise ValueError('That object cluster does not exist')
        f = open(self.cluster_path + 'chrs/bi.txt', 'r')
        return float(f.read().split('\n')[num_uc].split(' ')[num_oc])
        tmp = f.read().split('\n')[num_uc].split(' ')[num_oc]
        try:
            tmp = float(tmp)
        except ValueError as ve:
            print(tmp, num_uc, num_oc)
            raise ve
        return tmp

    def get_cluster(self, num, isUser):
        path = self.cluster_path
        limit = 0
        if isUser:
            if num >= self.num_u:
                raise ValueError('Non-clustered user')
            path += 'users/'
            limit = self.num_uc
        else:
            if num >= self.num_obj:
                raise ValueError('Non-clustered object')
            path += 'objects/'
            limit = self.num_oc
        s = str(num)
        for i in range(limit):
            f = open(path + str(i) + '.txt', 'r')
            if f.read().split(' ').count(s) != 0:
                return i
            f.close()
        print('Not found cluster, ' + s + ' ' + str(isUser) + ' ' + path + ' ' + str(limit))
        return -1

#    def calculate_cluster
    def block_average(self, num_u, num_obj, u_avg, obj_avg, uc_avg, objc_avg, bic_avg):
        return bic_avg + (u_avg - uc_avg) + (obj_avg - objc_avg)

    def quality(self, num, isUser, numc = -1):
        a_avg = self.get_average(num, isUser)
        if numc == -1:
            numc = self.get_cluster(num, isUser)
        ac_avg = self.get_cluster_average(numc, isUser)
        profile = self.get_profile(num, isUser)
        s = 0
        for i in profile:
            b_avg = self.get_average(i, not isUser)
            bc = self.get_cluster(i, not isUser)
            bc_avg = self.get_cluster_average(bc, not isUser)
            bic_avg = -1
            if isUser:
                bic_avg = self.get_bicluster_average(numc, bc)
            else:
                bic_avg = self.get_bicluster_average(bc, numc)
            s += (self.block_average(num, i, a_avg, b_avg, ac_avg, bc_avg, bic_avg) - profile[i]) ** 2
        return s

    def run(self):
        flag = False
#        error_log_file = open('./reclustering.log', 'a')
        for i in range(self.num_uc):
#            error_log_file.write('Started processing users cluster ' + str(i) + '\n')
            replaced = []
            f = open(self.cluster_path + 'users/' + str(i) + '.txt', 'r')
#            users = f.read().split(' ')
            users = f.readline().split(' ')
            for line in f:
#                users.append(line)
                users += line.split(' ')
            f.close()
            while '' in users:
                users.remove('')
            while '\n' in users:
                users.remove('\n')
            users = [int(x) for x in users]
            for u in users:
#                error_log_file.write('\tProcessing user №' + str(u) + '\n')
                mq = self.quality(u, True, i)
#                error_log_file.write('\t\tNow quality == ' + str(mq) + '\n')
                mj = i
                for j in range(self.num_uc):
                    tmp = self.quality(u, True, j)
                    if tmp < mq:
                        mq = tmp
                        mj = j
#                error_log_file.write('\t\tMinimum quality == ' + str(mq) + ' in cluster №' + str(mj) + '\n')
                if mj != i:
                    flag = True
                    replaced.append(u)
                    f = open(self.cluster_path + 'users/' + str(mj) + '.txt', 'a')
                    f.write(str(u) + ' ')
                    f.close()
            if len(replaced) != 0:
                for x in replaced:
                    users.remove(x)
                f = open(self.cluster_path + 'users/' + str(i) + '.txt', 'w')
                for u in users:
                    f.write(str(u) + ' ')
                f.close()                                                               # Here we have reclustered users

        for i in range(self.num_oc):
#            error_log_file.write('Started processing objects cluster ' + str(i) + '\n')
            replaced = []
            f = open(self.cluster_path + 'objects/' + str(i) + '.txt', 'r')
            objects = f.readline().split(' ')
            for line in f:
#                objects.append(line)
                objects += line.split(' ')
            f.close()
            while '' in objects:
                objects.remove('')
            while '\n' in objects:
                objects.remove('\n')
            objects = [int(x) for x in objects]
            for obj in objects:
#                error_log_file.write('\tProcessing object №' + str(obj) + '\n')
                mq = self.quality(obj, False, i)
#                error_log_file.write('\t\tNow quality == ' + str(mq) + '\n')
                mj = i
                for j in range(self.num_oc):
                    tmp = self.quality(obj, False, j)
                    if tmp < mq:
                        mq = tmp
                        mj = j
#                error_log_file.write('\t\tMinimum quality == ' + str(mq) + ' in cluster №' + str(mj) + '\n')
                if mj != i:
                    flag = True
                    replaced.append(obj)
                    f = open(self.cluster_path + 'objects/' + str(mj) + '.txt', 'a')
                    f.write(str(obj) + ' ')
                    f.close()
            if len(replaced) != 0:
                for x in replaced:
                    objects.remove(x)
                f = open(self.cluster_path + 'objects/' + str(i) + '.txt', 'w')
                for obj in objects:
                    f.write(str(obj) + ' ')
                f.close()                                                               # Here we have reclustered objects
        return flag

    def algorithm(self, times = None):
        while self.run():
            self.init_characteristics()
            if times is not None:
                if times == 0:
                    break
                times -= 1

    def rrr():
        pass
