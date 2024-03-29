from django.shortcuts import render


def reports(request, *args, **kwargs):

    template_name = "reports/reports.html"
    context = {
        "section": "reports",
    }

    return render(request, template_name, context)
