# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Plurlanalysis(models.Model):
    id = models.BigAutoField(primary_key=True)
    expect = models.ForeignKey('SfcDetail', models.DO_NOTHING, db_column='expect',to_field="expect", blank=True, null=True)
    peiname = models.CharField(max_length=255, blank=True, null=True)
    peivalue = models.TextField(blank=True, null=True)
    updatetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plurlanalysis'


class Sfc(models.Model):
    id = models.BigAutoField(primary_key=True)
    expect = models.CharField(max_length=255, blank=True, null=True,unique=True)
    updatetime = models.DateTimeField(blank=True, null=True)
    fsendtime = models.DateTimeField(blank=True, null=True)
    j141 = models.IntegerField(blank=True, null=True)
    j142 = models.IntegerField(blank=True, null=True)
    j14t = models.IntegerField(blank=True, null=True)
    j91 = models.IntegerField(blank=True, null=True)
    j9t = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sfc'


class SfcDetail(models.Model):
    id = models.BigAutoField(primary_key=True)
    expect = models.ForeignKey(Sfc, models.DO_NOTHING, db_column='expect', to_field="expect",blank=True,unique=True,null=True)
    ordernum = models.IntegerField(blank=True, null=True)
    hometeam = models.CharField(max_length=255, blank=True, null=True)
    guestteam = models.CharField(max_length=255, blank=True, null=True)
    homescore = models.IntegerField(blank=True, null=True)
    guestscore = models.IntegerField(blank=True, null=True)
    result = models.IntegerField(blank=True, null=True)
    plurl_3 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plurl_1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plurl_0 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    homestanding = models.IntegerField(blank=True, null=True)
    gueststanding = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sfc_detail'
