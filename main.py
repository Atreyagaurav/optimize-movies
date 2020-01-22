import random
import pandas as pd
import movies
import time

def extract_data(filein="data/movies2019.csv",fileout="data/extracted.csv",rows=10):
    with open(filein) as reader:
        lines=reader.readlines()
    headers = lines[0]
    lines = lines[1:]
    random.shuffle(lines)
    new_data = [headers]+lines[:rows]
    with open(fileout,"w") as writer:
        writer.write(''.join(new_data))
    
def random_data(n):
    fileout= "data/rand/rand{index}.csv"
    for i in range(n):
        extract_data(fileout=fileout.format(index=i),rows=10)
    for i in range(n,2*n):
        extract_data(fileout=fileout.format(index=i),rows=20)
    for i in range(2*n,3*n):
        extract_data(fileout=fileout.format(index=i),rows=100)
    for i in range(3*n,3*n+10):
        extract_data(fileout=fileout.format(index=i),rows=1000)


def read_movies(filename="data/movies2019.csv"):
    df = pd.read_csv(filename)
    movie_list= []
    for index,row in df.iterrows():
        m = movies.Movie(row.Name,row.rating,row.time_min)
        movie_list.append(m)
    return movie_list

if __name__ == '__main__':
    print("reading files")
    # random_data(100)
    t1 = time.time()
    # mlist= movies.MovieList(read_movies())
    hours = 10
    if False:
        for i in range(10):
            fn="data/rand/rand{index}.csv".format(index=i)
            print(fn)
            mlist= movies.MovieList(read_movies(fn))
            recomm= movies.filtered_combinations(mlist,hours)
            # recomm2= movies.bruteforce(mlist,hours)
            print(recomm)
            # print("A:%.2f, B:%.2f\t\t%s"%(recomm.total_rating,recomm2.total_rating,"" if (recomm.total_rating<=recomm2.total_rating) else '**'))
        
    mlist= movies.MovieList(read_movies("data/rand/rand0.csv"))
    # mlist= movies.MovieList(read_movies())
    print("total movies: ",mlist.total_count)
    # print(mlist)
    if True:
        print("time",time.time()-t1)
        print("recommendations: weighted")
        t1=time.time()
        recomm= movies.weighted_recommendations(mlist,hours)
        print("time",time.time()-t1)
        print(recomm)
    if True:
        print("time",time.time()-t1)
        print("recommendations: filtered")
        t1=time.time()
        recomm1= movies.filtered_combinations(mlist,hours)
        print("time",time.time()-t1)
        print(recomm1)
    if True:
        print("recommendations: bruteforce")
        t1=time.time()
        recomm2= movies.bruteforce(mlist,hours,verbose=True)
        print("time",time.time()-t1)
        print(recomm2)
