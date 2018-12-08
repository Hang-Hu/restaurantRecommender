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

