# Report

You will submit a report of at most 5 pages giving an overview of your project. (A little more is okay for groups of 3; a little less is probably appropriate for groups of 1 or 2.)

3-4 pages for me.

## Problem definition

What is the problem that you are trying to solve? What are the challenges of this problem?

People with different tastes like different restaurants. Websites like Yelp and Google do have recommendations to users, but they prefer more to use Content-Based Filtering. Content-Based Filtering does the recommendation based on the similarity of restaurants, it will recommend restaurants similiar to those the user highly rated or favorited, or even viewed.

There are three benefits for these websites to prefer the Content-Based Filtering.

To begin with, point-based reviews from target user are not necessary for this algorithm. It can utilize users' recently viewed restaurants or searched restaurants or favoriated restaurants to make recommendations instead. 

Besides, it only have to do computation again when there are new restaurants instead of new reviews, which increase much more faster. And the computation based on restaurants takes less effort compared to that based on reviews, since the data size of restaurants are much smaller.

Finally, it can do recommendations quickly even to new users. When new user creates the profile, these websites usually prompt some recommended restaurants for user to favoriate or follow, so that the system collect enough information. And since it's based on content and number of restaurants won't increase significantly, it can recommend similiar restaurants to this new user using previouly trained model. This way Content-Based Filtering solves new user problem.

However, Content-Based Filtering does have limitations, it can only recommend restaurants in categories the user favoriated/viewed/rated. Collaborative Filtering can solve this problem since it's based on group of users with similiar interest, which makes it possible to recommend restaurants in unrelated categories. Besides, it makes sense to recommend based on users with similiar interest rather than content similarity, because the content similarity only draw a portion of user interest. In addition, Collaborative Filtering doesn't have know about restaurants attributes, the review data is all required.

Therefore I used Collaborative Filtering to do recommendations for restaurants using Yelp's 7.35 gigabytes uncompressed data.

challenges

Collaborative filtering is commonly used for recommender systems. These techniques aim to fill in the missing entries of a user-item association matrix. spark.ml currently supports model-based collaborative filtering, in which users and products are described by a small set of latent factors that can be used to predict missing entries. spark.ml uses the alternating least squares (ALS) algorithm to learn these latent factors. The implementation in spark.ml has the following parameters:



## Methodology

What is the problem that you are trying to solve? Briefly explain which tool(s)/technique(s) were used for which task and why you chose to implement that way.




## Problems

What problems did you encounter while attacking the problem? How did you solve them?

### Getting the data

I downloaded Yelp Dataset from https://www.yelp.com/dataset/download.

### ETL

Since Spark's DataFrame based ml library I used only supports numeric types for the user and item id columns, but all the id in Yelp Dataset are string like 'wKlH90YB5RYFvJ8N3pstVw', so I mapped business_id, user_id, and review_id to int values using `zipWithIndex()`.

I only need business which has review_count, is open and is a restaurant, so I first cleaned it. I need reviews which are commented on this business I just generated. I need users which have reviews on restaurants. This was done in `clean_data_to_parquet.py`.

In `write_parquet_to_mysql.py` I encountered a critical problem, `Duplicate entry '94157' for key 'PRIMARY'`. The reason is when business_id is 0, since MySQL treats 0 specially as Null, it will insert as a random business_id like 94157, which conflicts the row with business_id 94157. And `zipWithIndex()` will index from 0. My solution is to make business_id start from 1 by `.zipWithIndex().map(lambda x: (x[0], x[1]+1))`.

After writing business, user and tip to MySQL, I found I need the original string based business_id to query Yelp Fusion API to get the photos of restaurants so that I can display them in Web Front End. Then I used `clean_str_business_id_to_parquet.py` and `write_business_with_str_id_to_mysql.py` to add the column `business_str_id` to Business Table in MySQL.

### Technologies

I learned Django, Celery, and Redis in developing the project, and encountered some traps, especially when integrating tools together.

#### Django with MySQL

Django requires only one primary key, but for Recommend table, since one will only have one predicted rating on one restaurant, I use user_id and business_id as primary key, this is common in Java Spring Framework and MySQL, but Django is different. So I have to add recommend_id as primary key, add constraint of unique on `user_id` and `business_id by` `alter table Recommend add constraint unique_recommend unique (user_id, business_id);`. 

### Spark with MySQL

When writing DataFrame to MySQL, if `mode` is `overwrite`, the Spark will drop table of MySQL and create this table. This makes my `bigint` magically turned into `int`, `Not Null` constraint disappear after Spark writing data to MySQL. I found that behavior by setting up a new user of MySQL with only `SELECT, INSERT, DELETE` permissions on YelpRecommender database. Then Spark complained for no permission of dropping table.

I switched to `append` mode then it worked without droping and re-creating that table.

```
tip_df.write.format('jdbc').options(
      url='jdbc:mysql://localhost/YelpRecommender',
      driver='com.mysql.jdbc.Driver',
      dbtable='Tip',
      user='yelp',
      password='yelp').mode('append').save()
```

#### Celery, Spark with MySQL

Celery complained on `java.lang.ClassNotFoundException: com.mysql.jdbc.Driver`. But `spark-submit --packages mysql:mysql-connector-java:5.1.39 --master=local[*] tasks.py` just not work for me, I have to use `python3.6 -m celery -A tasks worker --loglevel=info --hostname=worker1@%h` to have celery worker running. I checked `http://localhost:4040/environment/` and found jars listed like /usr/local/spark-2.3.1-bin-hadoop2.7/jars/aopalliance-1.0.jar, therefore I thought `/usr/local/spark-2.3.1-bin-hadoop2.7/jars/` is the right directory to put mysql connector jar. As for `~/.ivy2/jars/mysql_mysql-connector-java-5.1.39.jar`, `spark-submit --packages mysql:mysql-connector-java:5.1.39` will check if `~/.ivy2` has this dependency or not. If not, it will download from central repository to `~/.ivy2/jars`. So I copied the mysql jar from ivy2 to spark jars using `sudo cp ~/.ivy2/jars/mysql_mysql-connector-java-5.1.39.jar  /usr/local/spark-2.3.1-bin-hadoop2.7/jars/`.


#### Celery with Redis

Redis setup is different from rabbitmq, it doesn't require username and password setup. The problem is that celery is not widely used with redis and hard for me to search a guide, so I have to read the official document and find out the answer.

```
app = Celery('tasks', backend='rpc://', broker='redis://localhost:6379/0')
```


#### Spark, Celery with Django

Another difficult problem is to have Celery work with Django. It works differently from the ipython one.

Here follows one error.


Can't decode message body: ContentDisallowed('Refusing to deserialize untrusted content of type pickle (application/x-python-serialize)',) [type:'application/x-python-serialize' encoding:'binary' headers:{}]


This is because since celery4, the default serializer and accepted content is `json` instead of `pickle`, and celery just rejected other formats. I changed the config as followed.

```
app.conf.update(
    task_serializer='pickle',
    accept_content=['pickle'],  # Ignore other content
)
```

Another problem is that django send the task name as `business.tasks.recommend_business` even my code `in views.py` is `from .ml.tasks import recommend_business`. But the celery shows it to be `tasks.recommend_business`, only ipython works. My trick is to specify the task name by `@app.task(name='business.tasks.recommend_business')`. This time django works well, but ipython doesn't match anymore.


## Results: What are the outcomes of the project? What did you learn from the data analysis? What did you learn from the implementation?


## Project Summary: A summary of what you did to guide our marking.


UI: User interface to the results, possibly including web or data exploration frontends.
Technologies: New technologies learned as part of doing the project.
Total: 20


Bigness/parallelization: Efficiency of the analysis on a cluster, and scalability to larger data sets.



Project Summary
At the end of your project report, please provide a summary of the emphasis/priorities in your project. Give yourself a total of 20 point in these categories:

Getting the data: Acquiring/gathering/downloading.
ETL: Extract-Transform-Load work and cleaning the data set.
Problem: Work on defining problem itself and motivation for the analysis.
Algorithmic work: Work on the algorithms needed to work with the data, including integrating data mining and machine learning techniques.
Bigness/parallelization: Efficiency of the analysis on a cluster, and scalability to larger data sets.
UI: User interface to the results, possibly including web or data exploration frontends.
Visualization: Visualization of analysis results.
Technologies: New technologies learned as part of doing the project.
Total: 20

Don't think of this as giving yourself a mark. (That's our job.) This is intended to be a guide for our marking, so we don't miss significant work you did. (e.g. if you give yourself 6 points on “new technologies” and we haven't noticed any, we know to keep looking; if you gave yourself 0 then we can move on and look at other aspects.)

Since this will be guiding our marking, you may want to address these areas in your report as well.

You will likely be giving yourself 0 in some of these categories: that's perfectly reasonable. You aren't expected to do all of these, but should (of course) have done some subset of them (including “bigness” which we expect you to think about).

[If there are other categories you think should be here, ask us.]



This is also due Friday December 07 2018 and submitted to Project as a PDF or a URL to HTML (only one of those is necessary).

<!-- ## Screenshots -->

<!-- <img src="/home/joanna/Pictures/CodePic/big-data-proj/1.png" alt="">
<img src="/home/joanna/Pictures/CodePic/big-data-proj/2.png" alt="">
<img src="/home/joanna/Pictures/CodePic/big-data-proj/6.png" alt="">
<img src="/home/joanna/Pictures/CodePic/big-data-proj/4.png" alt="">
<img src="/home/joanna/Pictures/CodePic/big-data-proj/5.png" alt="">
 -->

## Reference

https://www.codementor.io/jadianes/building-a-recommender-with-apache-spark-python-example-app-part1-du1083qbw
https://www.codementor.io/jadianes/building-a-web-service-with-apache-spark-flask-example-app-part2-du1083854

https://spark.apache.org/docs/latest/ml-collaborative-filtering.html

https://www.djangoproject.com/start/

http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
http://docs.celeryproject.org/en/latest/userguide/security.html
http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
http://docs.celeryproject.org/en/latest/getting-started/brokers/redis.html

https://bugra.github.io/work/notes/2014-04-19/alternating-least-squares-method-for-collaborative-filtering/#Intuition
https://www.quora.com/What-is-the-difference-between-content-based-filtering-and-collaborative-filtering