from django.urls import path
from . import views

app_name = "reports"


urlpatterns = [
    path("reports", views.reports, name="reports"),
    path(
        "generate-report-card",
        views.generate_report_card_pdf,
        name="generate_report_cards",
    ),
    path(
        "generate-report",
        views.create_one_report_card,
        name="generate_single_report_card",
    ),
]
