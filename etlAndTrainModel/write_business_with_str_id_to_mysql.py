from pyspark import Row
from pyspark.sql import SparkSession, functions, types
import sys
import json

def main():
    business_with_str_id_df = spark.read.parquet('output/business_with_str_id.parquet')
    business_with_str_id_df.show()
    business_with_str_id_df.write.format('jdbc').options(
          url='jdbc:mysql://localhost/YelpRecommender',
          driver='com.mysql.jdbc.Driver',
          dbtable='Business',
          user='yelp',
          password='yelp').mode('append').save()

if __name__ == '__main__':
    assert sys.version_info >= (3, 5)
    spark = SparkSession.builder.appName('Write business_str_id to MySQL').getOrCreate()
    assert spark.version >= '2.3'
    sc = spark.sparkContext
    main()
