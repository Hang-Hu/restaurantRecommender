# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Business(models.Model):
    business_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    stars = models.CharField(max_length=255, blank=True, null=True)
    review_count = models.CharField(max_length=255, blank=True, null=True)
    categories = models.CharField(max_length=2550, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Business'


class Recommend(models.Model):
    recommend_id = models.BigAutoField(primary_key=True)
    business = models.ForeignKey(Business, models.DO_NOTHING)
    rating = models.FloatField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Recommend'
        unique_together = (('user', 'business'),)


class Tip(models.Model):
    tip_id = models.BigAutoField(primary_key=True)
    business = models.ForeignKey(Business, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    text = models.TextField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tip'


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    review_count = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'

