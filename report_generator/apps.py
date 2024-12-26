import os
import json

from django.apps import AppConfig

class ReportGeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'report_generator'

    def ready(self):
        self.populate_companies()
        self.populate_financial_ratios()

    def populate_companies(self):
        from report_generator.models.CompanyModel import Company

        file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'company_metadata.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                company_data = json.load(file)
                company_id_set = set(Company.objects.values_list('id', flat=True))
                for company in company_data:
                    company_id = company['company_id']
                    if company_id not in company_id_set:
                        Company.objects.create(
                            id=company_id,
                            name=company['company_name'],
                            country_name=company['country_name'],
                            security_number=company['security_number'],
                            ticker=company['ticker'],
                            id_bb_unique=company['id_bb_unique'],
                            id_bb_company=company['id_bb_company'],
                            security_type=company['security_type'],
                            market_status=company['market_status'],
                            exchange_country_id=company['exchange_country_id'],
                            domicile_id=company['domicile_id'],
                            industry_sector_num=company['industry_sector_num'],
                            industry_group_num=company['industry_group_num'],
                            industry_subgroup_num=company['industry_subgroup_num'],
                            revision=company['revision'],
                            start_date=company['start_date'],
                            end_date=company['end_date'],
                            flag=company['flag'],
                        )

    def populate_financial_ratios(self):
        from report_generator.models.CompanyModel import Company
        from report_generator.models.CompanyFinancialRatiosModel import CompanyFinancialRatios

        file_path = os.path.join(os.path.dirname(__file__), 'fixtures', 'company_financial_ratios.json')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                for ratio in data:
                    company_id = ratio['company_id']
                    fiscal_year = ratio['fiscal_year']
                    if not CompanyFinancialRatios.objects.filter(company_id=company_id,
                                                                 fiscal_year=fiscal_year).exists():

                        company = Company.objects.get(id=company_id)
                        CompanyFinancialRatios.objects.create(
                            company=company,
                            fiscal_year=fiscal_year,
                            latest_update_date=ratio['latest_update_date'],
                            shareholders_equity=ratio['shareholders_equity'],
                            cash_and_cash_equivalents=ratio['cash_and_cash_equivalents'],
                            total_current_asset=ratio['total_current_asset'],
                            total_current_liab=ratio['total_current_liab'],
                            long_term_debt=ratio['long_term_debt'],
                            short_term_investment=ratio['short_term_investment'],
                            other_short_term_liab=ratio['other_short_term_liab'],
                            shares_outstanding=ratio['shares_outstanding'],
                            current_debt=ratio['current_debt'],
                            total_asset=ratio['total_asset'],
                            total_equity=ratio['total_equity'],
                            total_liab=ratio['total_liab'],
                            net_income=ratio['net_income'],
                            total_revenue=ratio['total_revenue'],
                            inventory=ratio['inventory'],
                            investment_in_assets=ratio['investment_in_assets'],
                            net_debt=ratio['net_debt']
                        )
