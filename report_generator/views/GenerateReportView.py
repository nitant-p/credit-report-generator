import json
import os
import logging
from datetime import datetime
from rest_framework import status, views
from rest_framework.response import Response
from report_generator.groqllm import GroqClient
from report_generator.models.CompanyFinancialRatiosModel import CompanyFinancialRatios
from report_generator.models.CompanyModel import Company
from report_generator.models.CreditRatingReportModel import CreditRatingReport
from report_generator.mongodb import MongoDBConnection
from report_generator.serializers.CompanyFinancialRatiosSerialzer import CompanyFinancialRatiosSerializer
from report_generator.serializers.CompanySerializer import CompanySerializer
from report_generator.utils import get_case_insensitive_closest_names, convert_datetimes

logger = logging.getLogger(__name__)


class GenerateReportView(views.APIView):

    def post(self, request):
        user = request.user
        company_name = request.data.get('company_name', None)
        company_id = request.data.get('company_id', None)

        if company_id is not None:
            try:
                company_id = int(company_id)
            except ValueError:
                return Response({"error": "Company ID must be a number."}, status=status.HTTP_400_BAD_REQUEST)

        if company_name is not None and not isinstance(company_name, str):
            return Response({"error": "company_name must be a string."}, status=status.HTTP_400_BAD_REQUEST)

        # name and id cannot both be present
        if bool(company_name) == bool(company_id):
            return Response({"error": "Please provide either company_name or company_id, but not both."},
                            status=status.HTTP_400_BAD_REQUEST)

        use_llm = request.data.get('use_llm', None)

        # check if company exists
        try:
            if company_name:
                company = Company.objects.get(name=company_name)
            else:
                company = Company.objects.get(id=company_id)
            company_data = CompanySerializer(company).data
        except Company.DoesNotExist:
            return Response({"error": "Company not found!"}, status=status.HTTP_404_NOT_FOUND)

        company_name = company.name

        if use_llm:
            # get transcript data
            earning_calls_transcript = self.get_earning_calls_transcript(company_name)
            # get financial ratio data
            financial_ratios = self.get_financial_ratios(company)
            # get ten k report
            ten_k_report = self.get_ten_k_report(company_name)

            print(f"Earning calls transcript found: \n{earning_calls_transcript}")
            print(f"Financial ratios found: \n {financial_ratios}")
            print(f"Ten K reports found: \n{ten_k_report}")

            try:
                company_data_string = json.dumps(company_data)
                groq = GroqClient.get_instance()
                generated_report = groq.generate_report_text(
                    company_name=company_name,
                    data=company_data_string
                    # financial_ratios=financial_ratios,
                    # earning_calls_transcript=earning_calls_transcript,
                    # ten_k_report=ten_k_report
                )

                # save report
                report_instance = CreditRatingReport.objects.create(
                    user=user,
                    company=company,
                    report_content=generated_report,
                    created_at=datetime.now()
                )

                response_data = {
                    "report_id": report_instance.id,
                    "company_name": company_name,
                    "report_content": generated_report,
                    "created_at": report_instance.created_at
                }

                return Response(response_data, status=status.HTTP_201_CREATED)
            except Exception as exc:
                print(exc)
                return Response({"error": "There was an error while using the LLM. Please try without it."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            file_path = os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'dummy_report.txt')
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    dummy_report = file.read()
                    report_instance = CreditRatingReport.objects.create(
                        user=user,
                        company=company,
                        report_content=dummy_report,
                        created_at=datetime.now()
                    )

                    response_data = {
                        "report_id": report_instance.id,
                        "company_name": company_name,
                        "report_content": dummy_report,
                        "created_at": report_instance.created_at
                    }

                    return Response(response_data, status=status.HTTP_201_CREATED)

    def get_earning_calls_transcript(self, company_name):
        try:
            db = MongoDBConnection.get_instance()
            transcripts_collection = db.earnings_call_transcripts
            company_names_from_transcript = transcripts_collection.distinct('company_name')
            close_matches = get_case_insensitive_closest_names(company_name, company_names_from_transcript, n=5)
            earnings_transcripts = []
            if close_matches:
                transcripts = transcripts_collection.find({"company_name": {"$in": close_matches}})

                for transcript in transcripts:
                    transcript['_id'] = str(transcript['_id'])
                    earnings_transcripts.append(transcript)

                # handle datetime objects
                earnings_transcripts = convert_datetimes(earnings_transcripts)
                earnings_transcripts = json.dumps(earnings_transcripts, indent=4)
            return earnings_transcripts
        except Exception as exc:
            print(exc)
            return []

    def get_financial_ratios(self, company):
        financial_ratios = CompanyFinancialRatios.objects.filter(company=company)
        if financial_ratios.exists():
            financial_ratios_serializer = CompanyFinancialRatiosSerializer(financial_ratios, many=True)
            return financial_ratios_serializer.data
        else:
            return []

    def get_ten_k_report(self, company_name):
        try:
            db = MongoDBConnection.get_instance()
            reports_collection = db.ten_k
            company_names_from_report = reports_collection.distinct('conm')
            close_matches = get_case_insensitive_closest_names(company_name, company_names_from_report, n=5)

            ten_k_reports = []
            if close_matches:
                transcripts = reports_collection.find({"conm": {"$in": close_matches}})
                for transcript in transcripts:
                    transcript['_id'] = str(transcript['_id'])
                    ten_k_reports.append(transcript)

                ten_k_reports = convert_datetimes(ten_k_reports)
                ten_k_reports = json.dumps(ten_k_reports, indent=4)

            return ten_k_reports
        except Exception:
            return []
