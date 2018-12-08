# from http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html
# start with: celery -A tasks worker --loglevel=info
# then: from tasks import add; add.delay(4, 4)
# from spark_celery import SparkCeleryApp, SparkCeleryTask, cache, main
from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession, functions, types
import sys
from pyspark.sql import Row
from celery import Celery
import os
assert sys.version_info >= (3, 5)

def path(filename):
    return os.path.join(os.path.dirname(__file__), filename)


def recommend(num, user_id, spark, ratings_model):
    user_df = spark.createDataFrame([user_id], types.LongType())
    user_df = user_df.select(user_df['value'].alias('user_id'))
    rec_df_raw = ratings_model.recommendForUserSubset(user_df, num).select('recommendations')
    rec_rdd = rec_df_raw.rdd\
        .flatMap(lambda x: x['recommendations'])\
        .map(lambda x: (x['business_id'], x['rating']))\
        .map(lambda x: Row(business_id=x[0], rating=x[1]))
    if rec_rdd.isEmpty():
        return []
    rec_df = spark.createDataFrame(rec_rdd)\
        .withColumn('user_id', functions.lit(user_id))\
        .withColumn('timestamp', functions.current_timestamp())
    try:
        rec_df.write.format('jdbc').options(
          url='jdbc:mysql://localhost/YelpRecommender',
          driver='com.mysql.jdbc.Driver',
          dbtable='Recommend',
          user='yelp',
          password='yelp').mode('append').save()
    except Exception as e:
        print('recommend() function in use_model.py\n', str(e))
    # rec_df.show()
    l = list(rec_df.select('business_id').rdd.map(lambda x: (x['business_id'])).collect())
    return l

spark = SparkSession.builder.appName('Yelp Recommender').getOrCreate()
assert spark.version >= '2.3'
sc = spark.sparkContext
ratings_model = ALSModel.load(path('ratings_model'))

app = Celery('tasks', backend='rpc://', broker='redis://localhost:6379/0')
app.conf.update(
    task_serializer='pickle',
    accept_content=['pickle'],  # Ignore other content
)

@app.task(name='business.tasks.recommend_business')
def recommend_business(num, user_id):
    return recommend(num, user_id, spark, ratings_model)
