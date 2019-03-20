In your repository's README.md, you may include other notes about things we should look for, or be aware of when marking. If you created some kind of web frontend, please include a URL in the README.md as well.

## Web Frontend

http://localhost:3000/

## Project Description

This project is a real-time restaurants recommendation system using Collaborative Filtering. It makes recommendations based on user reviews, to find out those with similar interest and recommend based on that.

When a user login, Django will call Spark through Celery to make recommendations for this user based on trained model loaded in Spark application. Once done, it will cache the result into MySQL and return the result to Django. Next time the user login, Django will get cached recommendations from MySQL.

## Technology

PySpark DataFrame, PySpark RDD, PySpark ML, Redis, Celery, MySQL, Django, Yelp Fusion API, React, Material-UI.

<img src="./images/architecture.jpg" alt="">

## Database Design

<img src="./images/database.png" alt="">

## Screenshots

<img src="./images/front-end-1.png" alt="">
<img src="./images/front-end-2.png" alt="">
<img src="./images/front-end-3.png" alt="">
<img src="./images/front-end-4.png" alt="">
<img src="./images/front-end-5.png" alt="">


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