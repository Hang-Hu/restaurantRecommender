from pyspark.sql import SparkSession
import sys
import utils
from time import time
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS


def main():
    ratings = spark.read.parquet('output/review.parquet')
    ratings = ratings.select(ratings['user_id'], ratings['business_id'], ratings['stars'])
    train, test = ratings.randomSplit([0.8, 0.2])
    t0 = time()
    als = ALS(maxIter=5, regParam=0.01, userCol="user_id", itemCol="business_id", ratingCol="stars",
              coldStartStrategy="drop")
    ratings_model = als.fit(train)
    time_len = time() - t0
    print("New model trained in {} seconds".format(time_len))

    predictions = ratings_model.transform(test)
    evaluator = RegressionEvaluator(metricName="rmse", labelCol="stars",
                                    predictionCol="prediction")
    rmse = evaluator.evaluate(predictions)
    with open('rmse.txt', 'w') as f:
        f.write(str(rmse))
    print("Root-mean-square error = " + str(rmse))
    # After test, train with all data and save this model
    ratings_model = als.fit(ratings)
    ratings_model.save(utils.path('ratings_model'))

if __name__ == '__main__':
    assert sys.version_info >= (3, 5)
    spark = SparkSession.builder.appName('Use all Yelp data to train model').getOrCreate()
    assert spark.version >= '2.3'
    sc = spark.sparkContext
    main()