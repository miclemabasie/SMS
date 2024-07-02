from django.urls import path
from . import views

app_name = "reports"


urlpatterns = [
    path("", views.reports, name="reports"),
    path(
        "generate-report-card",
        views.create_report_cards,
        name="generate_report_cards",
    ),
    path(
        "generate-report",
        views.create_one_report_card,
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
]
