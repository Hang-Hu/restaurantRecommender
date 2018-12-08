from pyspark.sql import SparkSession, functions, types
import sys
import json

def main():
    business_df = spark.read.parquet('output/business.parquet')
    business_df.write.format('jdbc').options(
          url='jdbc:mysql://localhost/YelpRecommender',
          driver='com.mysql.jdbc.Driver',
          dbtable='Business',
          user='yelp',
          password='yelp').mode('append').save()
    user_df = spark.read.parquet('output/user.parquet')
    user_df.write.format('jdbc').options(
        url='jdbc:mysql://localhost/YelpRecommender',
        driver='com.mysql.jdbc.Driver',
        dbtable='User',
        user='yelp',
        password='yelp').mode('append').save()
    tip_df = spark.read.parquet('output/tip.parquet')
    # tip_df.printSchema()
    # tip_df.show()
    tip_df.write.format('jdbc').options(
          url='jdbc:mysql://localhost/YelpRecommender',
          driver='com.mysql.jdbc.Driver',
          dbtable='Tip',
          user='yelp',
          password='yelp').mode('append').save()

if __name__ == '__main__':
    assert sys.version_info >= (3, 5)
    spark = SparkSession.builder.appName('Write Parquet to MySQL').getOrCreate()
    assert spark.version >= '2.3'
    sc = spark.sparkContext
    main()
