# Report

## Problem definition

What is the problem that you are trying to solve? What are the challenges of this problem?

People with different tastes like different restaurants. Websites like Yelp and Google do have recommendations to users, but they prefer more to use Content-Based Filtering. Content-Based Filtering does the recommendation based on the similarity of restaurants, it will recommend restaurants similiar to those the user highly rated or favorited, or even viewed.

There are three benefits for these websites to prefer the Content-Based Filtering.

To begin with, point-based reviews from target user are not necessary for this algorithm. It can utilize users' recently viewed restaurants or searched restaurants or favoriated restaurants to make recommendations instead. 

Besides, it only have to do computation again when there are new restaurants instead of new reviews, which increase much more faster. And the computation based on restaurants takes less effort compared to that based on reviews, since the data size of restaurants are much smaller.

Finally, it can do recommendations quickly even to new users. When new user creates the profile, these websites usually prompt some recommended restaurants for user to favoriate or follow, so that the system collect enough information. And since it's based on content and number of restaurants won't increase significantly, it can recommend similiar restaurants to this new user using previouly trained model. This way Content-Based Filtering solves new user problem.

However, Content-Based Filtering does have limitations, it can only recommend restaurants in categories the user favoriated/viewed/rated. Collaborative Filtering can solve this problem since it's based on group of users with similiar interest, which makes it possible to recommend restaurants in unrelated categories. Besides, it makes sense to recommend based on users with similiar interest rather than content similarity, because the content similarity only draw a portion of user interest. In addition, Collaborative Filtering doesn't have know about restaurants attributes, the review data is all required.

Therefore I used Collaborative Filtering to do recommendations for restaurants using Yelp's 7.35 gigabytes uncompressed data.

Challenges: how to implement ML with recommendation app, how to reply to user request quickly.



## Methodology

What is the problem that you are trying to solve? Briefly explain which tool(s)/technique(s) were used for which task and why you chose to implement that way.

To prepare reviews data for Machine Learning model training, I have to clean data to meet my requirement. I only need business which has review_count, is open and is a restaurant, so I first cleaned it. I need reviews which are commented on this business I just generated. I need users which have reviews on restaurants. This was done in `clean_data_to_parquet.py`. I used PySpark DataFrame and RDD, and save cleaned data in Parquet. I used PySpark because spark cluster works well with big data, I did it in ts.sfucloud.ca. I used Parquet because it's fast to save and load parquet, and parquet uses less space.

To do recommendations, I chose Spark ML due to the scalability it has.

To save user, business, tip data and cache recommendation, I used MySQL since it's fast and it's relational database, which is easy for query.

To have a back end, I chose Django because it has good support for MySQL and Django Model provides object mapping, which is convenient for data query.

To make Django communicate with Spark Cluster, I used Celery, with Redis as the broker.

For front-end, I used React because it's a library encouraging reusable UI components, where I can reuse my UI code and develop complex interactions with user. Material-UI is a UI Component library, I used together with React to implement good user interface quickly.

To get the images for restaurants, I used the Fusion API to query with business_id.


## Problems

What problems did you encounter while attacking the problem? How did you solve them?

### ETL

Since Spark's DataFrame based ml library I used only supports numeric types for the user and item id columns, but all the id in Yelp Dataset are string like 'wKlH90YB5RYFvJ8N3pstVw', so I mapped business_id, user_id, and review_id to int values using `zipWithIndex()`.


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
