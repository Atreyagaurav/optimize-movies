import json
import main as md
import movies
import math

DATA_FILE = "data/test.json"


def test_1():
    with open(DATA_FILE) as reader:
        js=json.load(reader)
    for filename,answer in js.items():
        ml = md.read_movies(filename)
        recom = movies.filtered_combinations(ml,answer['hours'])
        assert ([m.name for m in recom.movies.values()] == answer['movies'])

def make_data():
    hours =10
    data={}
    for i in range(310):
        filename="data/rand/rand{index}.csv".format(index=i)
        mlist= movies.MovieList(md.read_movies(filename))
        recom= movies.filtered_combinations(mlist,hours)
        print(filename)
        data[filename]= {'rating':recom.total_rating,
                         'time':recom.time,
                         'movies':[m.name for m in recom.movies.values()],
                         'hours':hours,
        }
        with open(DATA_FILE,'w') as writer:
            json.dump(data,writer)
            
def test_fun(func):
    with open(DATA_FILE) as reader:
        js=json.load(reader)
    i,j=0,0
    for filename,ans in js.items():
        ml = movies.MovieList(md.read_movies(filename))
        recom=func(ml,ans['hours'])
        if (recom.total_rating-ans['rating'])>-0.1:
            print(i,' passed ',j,'failed','\r',end="")
            i+=1
        else:
            j+=1
            print(filename,'\t',recom.total_rating,ans['rating'])
            print(recom)
            print(ans['movies'])
    print(i," of ",len(js)," passed, (",j," failed)")


if __name__ == '__main__':
    # make_data()
    test_fun(movies.filtered_combinations)

