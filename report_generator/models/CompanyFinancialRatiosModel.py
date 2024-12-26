from django.db import models
from django.utils import timezone

from report_generator.models.CompanyModel import Company

class CompanyFinancialRatios(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='financial_ratios')
    fiscal_year = models.IntegerField()
    latest_update_date = models.DateField(default=timezone.now)
    shareholders_equity = models.FloatField(null=True, blank=True)
    cash_and_cash_equivalents = models.FloatField(null=True, blank=True)
    total_current_asset = models.FloatField(null=True, blank=True)
    total_current_liab = models.FloatField(null=True, blank=True)
    long_term_debt = models.FloatField(null=True, blank=True)
    short_term_investment = models.FloatField(null=True, blank=True)
    other_short_term_liab = models.FloatField(null=True, blank=True)
    shares_outstanding = models.FloatField(null=True, blank=True)
    current_debt = models.FloatField(null=True, blank=True)
    total_asset = models.FloatField(null=True, blank=True)
    total_equity = models.FloatField(null=True, blank=True)
    total_liab = models.FloatField(null=True, blank=True)
    net_income = models.FloatField(null=True, blank=True)
    total_revenue = models.FloatField(null=True, blank=True)
    inventory = models.FloatField(null=True, blank=True)
    investment_in_assets = models.FloatField(null=True, blank=True)
    net_debt = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Financial Ratios for {self.company.name} | Fiscal Year {self.fiscal_year}"

