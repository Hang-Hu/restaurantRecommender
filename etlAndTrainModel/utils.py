import os

def path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def get_businessid_count_average(businessid_ratings):
    business_id, ratings = businessid_ratings
    rating_count = len(ratings)
    rating_average = sum(n for n in ratings)/rating_count
    return business_id, (rating_count, rating_average)

def gen(x, output_index_list, output_func_list):
    for i in range(len(output_index_list)):
        yield output_func_list[i](x[output_index_list[i]])

