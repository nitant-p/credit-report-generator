from django.db import models
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    country_name = models.CharField(max_length=255)
    security_number = models.IntegerField()
    ticker = models.CharField(max_length=50)
    id_bb_unique = models.CharField(max_length=255)
    id_bb_company = models.CharField(max_length=50)
    security_type = models.CharField(max_length=50)
    market_status = models.CharField(max_length=50)
    exchange_country_id = models.IntegerField()
    domicile_id = models.IntegerField()
    industry_sector_num = models.IntegerField()
    industry_group_num = models.IntegerField()
    industry_subgroup_num = models.IntegerField()
    revision = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    flag = models.IntegerField()

    def __str__(self):
        return self.name
