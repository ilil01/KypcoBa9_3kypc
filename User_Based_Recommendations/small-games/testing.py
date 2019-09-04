import math

class Test:
    def __init__ (self, test_obj, **kwargs): # name = 'generated_matrix.txt'):
        self.test_object = test_obj
        if 'name' in kwargs:
            self.matrix_filename = kwargs[name]
        else:
            self.matrix_filename = 'generated_matrix.txt'
        if 'threshold' in kwargs:
            self.threshold = kwargs['threshold']
        else:
            self.threshold = 0.

    def test_on_all(self):
        f = open(self.matrix_filename, 'r')
        obj = 0
        s = 0.
        num = 0
        for line in f:
            marks = line.replace('\n', '').split(',')
            for user in range(len(marks)):
                if marks[user] != '-':
                    tmp = self.test_object.predict(user, obj, self.threshold)
                    if tmp != 0.:
                        num += 1
                        try:
                            s += math.fabs(float(marks[user]) - tmp)
                        except ValueError as ve:
#                            if not 'ValueError: could not convert string to float:' in str(ve):
#                                raise ve
                            print(str(ve))
            obj += 1
        print ('sum == ' + str(s) + ', number == ' + str(num))
        return s / num
