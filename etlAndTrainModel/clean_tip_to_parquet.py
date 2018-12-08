from pyspark import Row
from pyspark.sql import SparkSession, functions, types
import sys
import json

def main():
    business_dict = json.loads(open('business_dict', 'r').read())
    user_dict = json.loads(open('user_dict', 'r').read())
    # business in retaurant
    tip_rdd = sc.textFile('dataset/yelp_academic_dataset_tip.json')\
        .map(json.loads)\
        .map(lambda x: (x['business_id'],x['user_id'], x['text'], int(x['likes']), x['date']))\
        .filter(lambda x: x[2] is not '')\
        .filter(lambda x: x[0] in business_dict.keys())\
        .map(lambda x: (business_dict[x[0]], user_dict[x[1]] if x[1] in user_dict else 0, x[2], x[3], x[4]))\
        .filter(lambda x: x[1] is not 0) \
        .map(lambda x: Row(business_id=x[0], user_id=x[1], text=x[2], likes=x[3], date=x[4]))
    tip_df = spark.createDataFrame(tip_rdd)
    print('---------------------------------------------')
    tip_df.show()
    print('---------------------------------------------')

    tip_df.write.parquet('output/tip.parquet')


if __name__ == '__main__':
    assert sys.version_info >= (3, 5)
    spark = SparkSession.builder.appName('Clean Tip to Parquet').getOrCreate()
    assert spark.version >= '2.3'
    sc = spark.sparkContext
    main()
