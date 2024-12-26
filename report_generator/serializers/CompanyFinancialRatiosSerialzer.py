from rest_framework import serializers
from report_generator.models.CompanyFinancialRatiosModel import CompanyFinancialRatios

class CompanyFinancialRatiosSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name')

    class Meta:
        model = CompanyFinancialRatios
        fields = [
            'company_name',
            'fiscal_year',
            'latest_update_date',
            'shareholders_equity',
            'cash_and_cash_equivalents',
            'total_current_asset',
            'total_current_liab',
            'long_term_debt',
            'short_term_investment',
            'other_short_term_liab',
            'shares_outstanding',
            'current_debt',
            'total_asset',
            'total_equity',
            'total_liab',
            'net_income',
            'total_revenue',
            'inventory',
            'investment_in_assets',
            'net_debt',
        ]
