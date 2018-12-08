from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession, functions, types
import sys
import utils
from pyspark.sql import Row


def recommend(num, user_id, spark, ratings_model):
    user_df = spark.createDataFrame([user_id], types.LongType())
    user_df = user_df.select(user_df['value'].alias('user_id'))
    rec_df_raw = ratings_model.recommendForUserSubset(user_df, num).select('recommendations')
    rec_rdd = rec_df_raw.rdd\
        .flatMap(lambda x: x['recommendations'])\
        .map(lambda x: (x['business_id'], x['rating']))\
        .map(lambda x: Row(business_id=x[0], rating=x[1]))
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
    rec_df.show()
    l = list(rec_df.select('business_id').rdd.map(lambda x: (x['business_id'])).collect())
    return l


if __name__ == '__main__':
    assert sys.version_info >= (3, 5)
    spark = SparkSession.builder.appName('Use Model').getOrCreate()
    assert spark.version >= '2.3'
    sc = spark.sparkContext
    ratings_model = ALSModel.load(utils.path('ratings_model'))
    num = 20
    user_id = 1
    l = recommend(num, user_id, spark, ratings_model)
    print('Finished')
    print(l)

