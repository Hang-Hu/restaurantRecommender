from django.http import JsonResponse
from .models import Recommend, Business, Tip, User
from .ml.tasks import recommend_business

import requests
# Create your views here.


def recommend(request, user_id):
    if request.method == 'GET':
        print('---------------\n', user_id, '\n-------------')
        qs = Recommend.objects.raw('SELECT * FROM Recommend WHERE user_id={} ORDER BY rating DESC'.format(user_id))
        l = []
        if len(qs) == 0:
            print('Recommendations with user id {} is not in database.'.format(user_id))
            # l = recommend_business(100, user_id)
            l = recommend_business.delay(100, user_id)
            l = l.get(timeout=10000)
        else:
            for recommend in qs:
                l.append(recommend.business_id)

        return JsonResponse({
            'result': 'success',
            'business_id_list': l
        })
    else:
        return JsonResponse({
            'result': 'fail',
            'error': 'Request method must be GET'
        })


def business_info(request, business_id):
    if request.method == 'GET':
        rqs = Business.objects.raw('SELECT * FROM Business WHERE business_id={}'.format(business_id))
        business = rqs[0]
        dict = {
            'name': business.name,
            'city': business.city,
            'stars': business.stars,
            'review_count': business.review_count,
            'categories': business.categories
        }
        return JsonResponse({
            'result': 'success',
            'business_info': dict
        })
    else:
        return JsonResponse({
            'result': 'fail',
            'error': 'Request method must be GET'
        })

def business_detailed_info(request, business_id):
    if request.method == 'GET':
        rqs = Business.objects.raw('SELECT * FROM Business WHERE business_id={}'.format(business_id))
        r = requests.get(url='https://api.yelp.com/v3/businesses/{}'.format(rqs[0].business_str_id),
                     headers={'Authorization': 'Bearer 80dOa-z4cmO_W8wGIDOSV581XOwqMSHCW3GbN4201kdzzZywxGCgW1jbhxvl_XZOKExHzTC2a0zAh3mQ1aNCC_LJYYxThsYaTFm2rfMj14R700VsGiYM51QHAYAIXHYx'})
        business_info = r.json()
        return JsonResponse({
            'result': 'success',
            'business_info': business_info
        })
    else:
        return JsonResponse({
            'result': 'fail',
            'error': 'Request method must be GET'
        })

def tips(request, business_id):
    if request.method == 'GET':
        rqs = Tip.objects.raw('SELECT * FROM Tip WHERE business_id={}'.format(business_id))
        l = []
        for tip in rqs:
            l.append({
                'date': tip.date,
                'text': tip.text,
                'user_id': tip.user.user_id
            })
        return JsonResponse({
            'result': 'success',
            'tips': l
        })
    else:
        return JsonResponse({
            'result': 'fail',
            'error': 'Request method must be GET'
        })

def user_id_list(request):
    if request.method == 'GET':
        rqs = User.objects.raw('SELECT * FROM User ORDER BY user_id DESC LIMIT 0, 1')
        return JsonResponse({
            'result': 'success',
            'user_id_list': [1, rqs[0].user_id]
        })
    else:
        return JsonResponse({
            'result': 'fail',
            'error': 'Request method must be GET'
        })