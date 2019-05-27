import numpy as np
import pandas as pd

from scipy.spatial import distance

from sklearn.metrics.pairwise import cosine_similarity

class main_class:
    def __init__ (self, users, objects, matrix_filename = 'matrix.txt'):
        self.matrix = np.ndarray((objects, users))
        f = open(matrix_filename, 'r')
        j = 0
        for line in f:
            column = line[:-1].split(',')
#            print (column)
            for i in range(len(column)):
                if column[i] == '-':
                    self.matrix[j][i] = 0
                elif column[i] == '':
                    raise Exception ('i == ' + str(i) + ', j == ' + str(j) + ', line is "' + line + '"')
                else:
                    self.matrix[j][i] = float(column[i])
            j += 1
        self.distances = cosine_similarity(self.matrix)

    def predict (self, user, obj, threshold = 0.9):
        indices = []
        s = 0.
        for i in range(self.matrix.shape[0]):
            if i != obj and self.distances[obj][i] >= threshold and self.matrix[i][user] > 0.001:
                indices.append(i)
                s += self.distances[obj][i]
        if len(indices) == 0:
#            raise ValueError ('too big threshold' + str(threshold))
            return 0.
        mark = 0.
        for i in indices:
            mark += self.matrix[i][user] * self.distances[obj][i]
        mark /= s
        return mark


users_prefix = 'users/'
objects_prefix = 'objects/'

tmp = open(users_prefix + 'all.txt', 'r').read().split('\n')
tmp.remove('')
num_users = len(tmp)
print (num_users)
tmp = open(objects_prefix + 'all.txt', 'r').read().split('\n')
tmp.remove('')
num_objects = len(tmp)
print (num_objects)
use = main_class(num_users, num_objects, 'generated_matrix.txt')

#print (use.matrix[4][105])
print (use.matrix[105][4])
print (use.predict(4, 105, 0))

test_user = 0
test_object = 7
test_threshold = 0.
print ("actual mark of " + str(test_user) + "th user for " + str(test_object) + "th object is " + str(use.matrix[test_object][test_user]))
print ("and predict equals to " + str(use.predict(test_user, test_object, test_threshold)) + " with threshold for similarity " + str(test_threshold))
