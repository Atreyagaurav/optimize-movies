# Optimize movies

This program optimizes the movies for a fixed hour (right now 10 hours, you can change that in code). 

## Objective 
The objective was to maximize the total rating of all the movies watched in the fixed hour.
Suppose you have 10 hours to watch a movie, watching a movie which has 10 ratings but 9.5 hours time would be considered suboptimum compared to watching 10 movies with 2 ratings, which may not sound realistic but it is made so to increase the complexity of the problem.

Here, increasing the number of movies would increase your total ratings, but you also have to consider the ratings of the movies you are going to watch. it'd be better to watch a movie with 9 rating and 2 hour over 9 rating and 2.1 hour. while it might be better to watch a movie with 8 rating and 1.5 hour, if the additional gap allows another movie to fit inside the criteria.

## Algorithms

### Bruteforce
The general way is to find all the combinations of movies possible, then filter the combination of movies which lie inside the time limit, then extract the one with the maximum total ratings.

This way of solving works for very small number of movies, as the algorithm is O(n*n!), a movie list of more than 10 movies will start to show serious time problem.

### weighted sort
Instead of using time and rating as two seperate paramters, a simple weight parameter can be calculated from those two,

Our objective for the weight are, 
* higher the rating, heigher the weight
* higher the time, lower the weight

these will make sure that we make the list of movies with high rating and low time, latter making it fit more movies.

After the weights are calculated, we can just sort the list and take movies with higher weights.

**Problem** with this approach is, it may give good movies, but it doesn't exactly give the optimum solution, if the limit is 10 hours, it may end up giving a solution with 9.1 hours while removing one movie from here would make two movies with greater sum of ratings than that one.

### Filtering from Bruteforce
This is the algorithm I came up with. I had seen a sort called [Stalin Sort](https://github.com/gustavo-depaula/stalin-sort) from a meme. Although it may have been made as a joke, it is a sort with O(n) time complexity, and I found a perfect way to use that here.

What I did is the followings:
1. First I sort the movies with their time in ascending order.
2. The use stalin sort with their ratings. what it does it removes any movies which'll take more time to watch but have fewer ratings.
(This step ensures that if we are spending more time then we are definitely watching movies with more ratings.)
3. Now, the remaining movies are used to make a combination of 2 movies from the original movie list. 
4. again, step 1 and 2 are applied. so there won't be any movie list which has more time but less total ratings. and if there are any movie group with more total ratins than the constrains they are removed. 
5. These steps are repeated, each time adding one extra movie till no more movies can be added (when all the new combinations exceeds limit). 
6. The last member of the array of movie list is the most optimum solution.


So this algorithm makes an array with the movies, only keeps them in increasing order of both time and ratings, and keeps adding movie group of lower total time than the limit while only adding new if the total rating is more than the last member of the array, hence resulting in the optimum group of movies.


## Testing
I have made the movies_test.py module to test the system, you can test any function with the test_fun() module of the movies_test module, just pass your function, which sould take movies.MovieList object and time_limit in hours. 
