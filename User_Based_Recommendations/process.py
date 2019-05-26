import numpy as np
import pandas as pd

from scipy.spatial import distance

from sklearn.metrics.pairwise import cosine_similarity

class main_class:
    def __init__ (self, users, objects, matrix_filename = 'matrix.txt'):
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
        self.distances = cosine_similarity(self.matrix)

    def predict (self, user, obj, threshold = 0.9):
        indices = []
        s = 0.
        for i in range(self.matrix.shape[0]):
            if i != user and self.distances[user][i] >= threshold and self.matrix[i][obj] > 0.001:
                indices.append(i)
                s += self.distances[user][i]
        if len(indices) == 0:
#            raise ValueError ('too big threshold' + str(threshold))
            return 0.
        mark = 0.
        for i in indices:
            mark += self.matrix[i][obj] * self.distances[user][i]
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
#use = main_class(num_users, 1466)
print(use.matrix)

#distances = cosine_similarity(use.matrix)
print(use.distances)

#for i in range(num_users):
#    print (str(distances[i][i]), end = ', ')
#    if abs(distances[i][i]) < 0.001:
#        if not all( [a < 0.001 for a in use.matrix[i]] ):
#            print ('!!!')

print (use.matrix[4][105])

print (use.predict(4, 105, 0))

test_user = 0
test_object = 7
test_threshold = 0.
print ("actual mark of " + str(test_user) + "th user for " + str(test_object) + "th object is " + str(use.matrix[test_user][test_object]))
print ("and predict equals to " + str(use.predict(test_user, test_object, test_threshold)) + " with threshold for similarity " + str(test_threshold))
