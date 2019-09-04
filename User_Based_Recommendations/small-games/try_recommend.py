from recommend import recommend
a = recommend()
zeros = [52, 77, 149, 791, 977]
for i in range(1012):
    if i not in zeros:
        print(a.recommend(i))
