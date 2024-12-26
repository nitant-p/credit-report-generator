from rest_framework import serializers
from report_generator.models.CompanyModel import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'name', 'country_name', 'security_number', 'ticker', 'id_bb_unique',
            'id_bb_company', 'security_type', 'market_status', 'exchange_country_id',
            'domicile_id', 'industry_sector_num', 'industry_group_num',
            'industry_subgroup_num', 'revision', 'start_date', 'end_date', 'flag'
        ]