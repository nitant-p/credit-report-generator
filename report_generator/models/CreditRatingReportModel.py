from django.db import models
from django.utils import timezone

from report_generator.models.CompanyModel import Company
from report_generator.models.UserModel import User

class CreditRatingReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reports')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_reports')
    report_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.company.name}. Created at: {self.created_at}"

