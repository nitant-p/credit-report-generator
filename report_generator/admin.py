from django.contrib import admin

from report_generator.models import User
from report_generator.models.CompanyFinancialRatiosModel import CompanyFinancialRatios
from report_generator.models.CompanyModel import Company
from report_generator.models.CreditRatingReportModel import CreditRatingReport

admin.site.register(Company)
admin.site.register(CreditRatingReport)
admin.site.register(CompanyFinancialRatios)
admin.site.register(User)
