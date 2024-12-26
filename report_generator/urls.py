from django.urls import path

from report_generator.views.ReportView import ReportView
from report_generator.views.GenerateReportView import GenerateReportView
from report_generator.views.UserManagementView import RegisterView, LoginView, LogoutView

urlpatterns = [
    path('generate/', GenerateReportView.as_view(), name='generate_report'),
    path('get-report/', ReportView.as_view(), name='view_report'),
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
