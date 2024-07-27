from django.urls import path
from . import views, controller

app_name = "reports"


urlpatterns = [
    path("", views.reports, name="reports"),
    path(
        "generate-report-card",
        controller.create_report_cards,
        name="generate_report_cards",
    ),
    path(
        "generate-report/<int:student_pkid>/",
        controller.create_one_report_card,
        name="generate_single_report_card",
    ),
    path(
        "generate-class-master-report",
        views.create_class_master_report,
        name="genereate_class_master_report",
    ),
    path(
        "download-class-master-report/<int:class_pkid>",
        views.download_class_master_report,
        name="download_class_master_report",
    ),
    path("gen", controller.generate_pdf, name="gen"),
    path("view-reports/", controller.view_reports, name="view-reports"),
    path(
        "download-report/<str:file_name>/",
        controller.download_report,
        name="download-report",
    ),
]
