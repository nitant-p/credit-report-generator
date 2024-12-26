from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from report_generator.models.CreditRatingReportModel import CreditRatingReport
from report_generator.serializers.CreditRatingReportSerializer import CreditRatingReportSerializer


class ReportView(APIView):
    def get(self, request):
        user = request.user
        company_name = request.query_params.get('company_name', None)
        company_id = request.query_params.get('company_id', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        user_only = request.query_params.get('user_only', 'false').lower() == 'true'

        # name and id cannot both be present
        if company_name and company_id:
            return Response({"error": "Please provide either company_name or company_id, but not both."},
                            status=status.HTTP_400_BAD_REQUEST)

        if company_id is not None:
            try:
                company_id = int(company_id)
            except ValueError:
                return Response({"error": "Company ID must be a number."}, status=status.HTTP_400_BAD_REQUEST)

        if company_name is not None and not isinstance(company_name, str):
            return Response({"error": "company_name must be a string."}, status=status.HTTP_400_BAD_REQUEST)

        reports = CreditRatingReport.objects.all()

        if user_only:
            reports = reports.filter(user=user)

        if company_name:
            reports = reports.filter(company__name__icontains=company_name)

        if company_id:
            reports = reports.filter(company__id=company_id)

        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                reports = reports.filter(created_at__gte=start_date)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
                reports = reports.filter(created_at__lte=end_date)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if not reports.exists():
            return Response({"message": "No reports match the given criteria."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CreditRatingReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)