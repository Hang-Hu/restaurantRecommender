from pyspark import Row
from pyspark.sql import SparkSession, functions, types
import sys
import json

def main():
    business_dict = json.loads(open('business_dict', 'r').read())
    business_dict_rdd = sc.parallelize(business_dict.items())\
        .map(lambda x: Row(business_str_id=x[0], business_id=x[1]))
    business_dict_df  = spark.createDataFrame(business_dict_rdd)
    business_df = spark.read.format("jdbc").options(
        url='jdbc:mysql://localhost/YelpRecommender',
        driver='com.mysql.jdbc.Driver',
        dbtable='Business',
        user='yelp',
        password='yelp'
    ).load().drop('business_str_id')

    business_df = business_df.join(business_dict_df, ['business_id'])

    business_df.write.parquet('output/business_with_str_id.parquet')


if __name__ == '__main__':
    assert sys.version_info >= (3, 5)
    spark = SparkSession.builder.appName('Clean business_str_id to Parquet').getOrCreate()
    assert spark.version >= '2.3'
    sc = spark.sparkContext
    main()
