import math
import itertools
import copy

class Movie:
    COUNT=0
    def __init__(self,name,rating,time):
        self.id = Movie.COUNT
        Movie.COUNT+=1
        self.name=name
        self.rating=rating
        self.time=time
        self.weight = 0


    def set_weight(self,available_time):
        self.weight = self.rating /self.time #+available_time/self.time*5
        return self.weight

    def fits(self,movie_group):
        return  movie_group.vacancy>self.time
    
    def __str__(self):
        return "Name: {name}\nRating:{rating}\ttime:{time}".format(name=self.name,rating=self.rating,time=self.time)

class MovieGroup:
    def __init__(self,available_time):
        self.limit = available_time
        self.time = 0
        self.movies ={}
        self.vacancy = self.limit-self.time
        self.total_rating= 0
        self.full = False

    def add_movie(self,movie):
        # print(movie.time,self.vacancy,movie.id,self.movies)
        if movie.time <= self.vacancy and movie.id not in self.movies:
            self.movies[movie.id]=movie
            self.time += movie.time
            self.total_rating+=movie.rating
            self.check_vacancy()
            return True
        else:
            # print(movie.time, self.vacancy,movie.id,list(self.movies.keys()))
            return False
    def check_vacancy(self):
        self.vacancy = self.limit - self.time
        if self.vacancy < 100:
            self.full = True
        else:
            self.full = False

    def __str__(self):
        s='Movie Group:\n{count} movies with total {rating} rating and {time} min(~{hour}hr) time.\n'.format(count=len(self.movies),rating=self.total_rating,time=self.time,hour="%.2f"%(self.time/60,))
        for m in self.movies.values():
            s+= "\t*{name} (r:{rating}) {time} min\n".format(name=m.name,rating=m.rating,time=m.time)
        return s

class MovieList:
    def __init__(self,movie_list):
        self.movies = {m.id:m for m in movie_list}
        self.total_count= len(self.movies)
        
    def get_movie(self,index):
        return self.movies[index]

    def remove_movie(self,index):
        del self.movies[index]
        self.total_count= len(self.movies)
    
    def __str__(self):
        s= "List of {count} movies".format(count=self.total_count)
        for m in self.movies.values():
            s+='\n\t*'+m.name+'(%.1f) %d'%(m.rating,m.time)
        return s

    def sort_by_weight(self,available_time):
        weightages ={m.id:m.set_weight(available_time) for m in self.movies.values()}
        return [self.get_movie(k) for k, v in sorted(weightages.items(), key=lambda item: item[1],reverse=True)]

def weighted_recommendations(movies_list,available_hour):
    recom_list = MovieGroup(available_hour*60)
    mlist = movies_list.sort_by_weight(available_hour*60)
    for movie in mlist:
        recom_list.add_movie(movie)
    return recom_list


def add_movie_in_movie_group(grp,lst):
    for mv in lst.movies.values():
        m= MovieGroup(grp.limit)
        [m.add_movie(_) for _ in grp.movies.values()]
        m.add_movie(mv)
        yield m



def bruteforce(movies_list,available_hour,verbose=False):
    comb= itertools.permutations(movies_list.movies.values(),len(movies_list.movies))
    rating = 0
    final=None
    n=math.factorial(movies_list.total_count)
    i=0
    for c in comb:
        i+=1
        if verbose:
            print("%f percentage\r"%(i*100.0/n),end="")
        recom_list = MovieGroup(available_hour*60)
        for mov in c:
            if not recom_list.add_movie(mov):
                break
        if recom_list.total_rating>rating :
            rating = recom_list.total_rating
            final=recom_list
    return final
    
def filtered_combinations(movies_list,available_hour):
    mov_dict = {}
    movies = movies_list.movies.values()
    limit= available_hour*60
    _=[update_dict(mov_dict,[m]) for m in movies]
    movies_sorted=[m for m in sorted(mov_dict.values(), key=lambda item: total_time(item))]
    movies_rat=movies_stalinsort_rating(movies_sorted,limit)
    new_movie_list= []
    while True:
        new_movie_list=[]#movies_rat[:]
        for rated_movies in movies_rat:
            for movie_from_list in movies:
                if movie_from_list not in rated_movies:
                    new_movie_list.append(rated_movies+[movie_from_list])
        old_len=len(movies_rat)
        s1=set([tuple(m) for m in movies_rat])
        movies_rat += new_movie_list
        # movies_rat += sorted(sorted(movies_rat,key=lambda item:total_time(item)),key=lambda item: ratings(item))
        # l=[[m.time for m in m_] for m_ in movies_rat]
        # t={total_time(m):ratings(m) for m in movies_rat}
        # _=0
        movies_rat=movies_stalinsort_rating(sorted(movies_rat, key=lambda item: total_time(item)),limit)
        # l=[[m.time for m in m_] for m_ in movies_rat]
        # t={total_time(m):ratings(m) for m in movies_rat}
        s2=set([tuple(m) for m in movies_rat])
        if len(s2.difference(s1))==0:
            mg= MovieGroup(limit)
            _=[mg.add_movie(m) for m in movies_rat[-1]]
            return mg

            
    
def get_min(mov_list,time_limit):
    for i in range(1,len(mov_list)):
        if total_time(mov_list[i])>time_limit:
            return mov_list[i-1]
    return None

def update_dict(movie_dict,movies):
    time = total_time(movies)
    if time in movie_dict:
        if ratings(movies)<=ratings(movie_dict[time]):
            return
    movie_dict[time]=movies

def movies_stalinsort_rating(movies,limit):
    m=[movies[0]]
    for i in range(1,len(movies)):
        if total_time(movies[i])>limit:
            continue
        if ratings(movies[i])>ratings(m[-1]):
            m.append(movies[i])
    return m

def get_min(mov_list,time_limit):
    for i in range(1,len(mov_list)):
        if total_time(mov_list[i])>time_limit:
            return mov_list[i-1]
    return None

def ratings(movies):
    return sum([m.rating for m in movies])

def total_time(movies):
    return sum([m.time for m in movies])

def pr(ml):
    for m in ml:
        print("%.2f|%d"%(ratings(m),total_time(m)))
