from django.urls import path

from . import views

urlpatterns = [
    path('recommend/<int:user_id>/', views.recommend, name='recommend'),
    path('business_info/<int:business_id>/', views.business_info, name='business_info'),
    path('business_detailed_info/<int:business_id>/', views.business_detailed_info, name='business_detailed_info'),
    path('tips/<int:business_id>/', views.tips, name='tips'),
    path('user_id_list/', views.user_id_list, name='user_id_list'),

]