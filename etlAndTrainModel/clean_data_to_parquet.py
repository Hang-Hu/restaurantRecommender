from pyspark import Row
from pyspark.sql import SparkSession, functions, types
import sys
import json

def main():
    business_rdd = sc.textFile('dataset/yelp_academic_dataset_business.json')\
        .map(json.loads)\
        .map(lambda x: (x['business_id'],x['name'], x['city'], int(x['stars']), int(x['review_count']),
                        int(x['is_open']), x['categories']))\
        .filter(lambda x: x[4] > 0)\
        .filter(lambda x: x[5] == 1)\
        .filter(lambda x: x[6] and len(x[6])>0 and 'Restaurants' in x[6]).cache()
    business_dict = business_rdd.map(lambda x: x[0]).distinct().zipWithIndex().map(lambda x: (x[0], x[1]+1)).collectAsMap()
    with open('business_dict', 'w') as f:
        f.write(json.dumps(business_dict))

    business_rdd = business_rdd\
        .map(lambda x: (business_dict[x[0]], x[1], x[2], x[3], x[4], x[5], x[6]))\
        .map(lambda x: Row(business_id=x[0], name=x[1], city=x[2], stars=x[3], review_count=x[4], categories=x[6]))

    business_df = spark.createDataFrame(business_rdd)
    business_df.write.parquet('output/business.parquet')

    review_rdd = sc.textFile('dataset/yelp_academic_dataset_review.json')\
        .map(json.loads)\
        .map(lambda x: (x['review_id'],x['user_id'], x['business_id'], int(x['stars'])))\
        .filter(lambda x: x[2] in business_dict.keys()).cache()
    user_list_in_reviews = review_rdd.map(lambda x: x[1]).distinct().collect()
    user_rdd = sc.textFile('dataset/yelp_academic_dataset_user.json') \
        .map(json.loads) \
        .map(lambda x: (x['user_id'], x['name'], int(x['review_count']))) \
        .filter(lambda x: x[2] > 0)\
        .filter(lambda x: x[0] in user_list_in_reviews).cache()
    user_dict = user_rdd.map(lambda x: x[0]).distinct().zipWithIndex().map(lambda x: (x[0], x[1] + 1)).collectAsMap()
    with open('user_dict', 'w') as f:
        f.write(json.dumps(user_dict))
    user_rdd = user_rdd \
        .map(lambda x: (user_dict[x[0]], x[1], x[2])) \
        .map(lambda x: Row(user_id=x[0], name=x[1], review_count=x[2]))
    user_df = spark.createDataFrame(user_rdd)
    user_df.write.parquet('output/user.parquet')
    review_dict = review_rdd.map(lambda x: x[0]).distinct().zipWithIndex().map(lambda x: (x[0], x[1]+1)).collectAsMap()
    with open('review_dict', 'w') as f:
        f.write(json.dumps(review_dict))
    review_rdd = review_rdd\
        .map(lambda x: (review_dict[x[0]] if x[0] in review_dict else 0,
                        user_dict[x[1]] if x[1] in user_dict else 0,
                        business_dict[x[2]] if x[2] in business_dict else 0,
                        x[3]))\
        .filter(lambda x: x[0] is not 0 and x[1] is not 0 and x[2] is not 0)\
        .map(lambda x: Row(review_id=x[0], user_id=x[1], business_id=x[2], stars=x[3]))
    review_df = spark.createDataFrame(review_rdd)

    review_df.write.parquet('output/review.parquet')


if __name__ == '__main__':
    assert sys.version_info >= (3, 5)
    spark = SparkSession.builder.appName('Write Yelp Data to Parquet').getOrCreate()
    assert spark.version >= '2.3'
    sc = spark.sparkContext
    main()
