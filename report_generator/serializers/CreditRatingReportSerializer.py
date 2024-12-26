from rest_framework import serializers
from report_generator.models.CreditRatingReportModel import CreditRatingReport
from report_generator.serializers.CompanySerializer import CompanySerializer
from report_generator.serializers.UserSerializer import UserSerializer

class CreditRatingReportSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = CreditRatingReport
        fields = ['id', 'company', 'report_content', 'created_at', 'user']
