## Input files

Download Yelp Dataset from https://www.yelp.com/dataset/download, uncompress and put them in `etlAndTrainModel/dataset`.


## How to import MySQL database

```
mysql -u username -p YelpRecommender < YelpRecommender.sql
```

In MySQL:

```
CREATE USER 'yelp'@'localhost' IDENTIFIED BY 'yelp';
GRANT SELECT, INSERT, DELETE ON YelpRecommender.* TO yelp@'localhost';
```


## How to run ETL code

```
spark-submit clean_data_to_parquet.py

spark-submit clean_tip_to_parquet.py

spark-submit --packages mysql:mysql-connector-java:5.1.39 write_parquet_to_mysql.py

spark-submit --packages mysql:mysql-connector-java:5.1.39 clean_str_business_id_to_parquet.py
```

In MYSQL: 

```
use YelpRecommender
delete from Business;
```

```
spark-submit --packages mysql:mysql-connector-java:5.1.39 write_business_with_str_id_to_mysql.py
```

## How to run model training code

```
spark-submit train_model_all_data.py
```

The RMSE is 3.313339901807028.

## How to use trained model to make recommendations for test

```
spark-submit --packages mysql:mysql-connector-java:5.1.39 use_model.py
```

## How to run the web application with real-time recommendation spark

Run backend:

```
cd backendWithCelery/
source venv/bin/activate
python yelp_recommender/manage.py runserver
```

Run redis as broker for celery:

```
./redis-server
```

Run celery worker:

```
cd backendWithCelery/yelp_recommender/business/ml/
python3.6 -m celery -A tasks worker --loglevel=info --hostname=worker1@%h
```

Run front end:

```
cd frontEnd/
npm start
```

