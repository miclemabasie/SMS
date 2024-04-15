from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Fee, FeePaymentHistory
from apps.students.models import StudentProfile
from apps.staff.models import AdminProfile
from apps.terms.models import AcademicYear
from datetime import datetime, time, timezone
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def add_fee_view(request, pkid, matricule, *args, **kwargs):

    # get the student for which the fees needs to be paid for
    student = get_object_or_404(StudentProfile, pkid=pkid, matricule=matricule)

    if request.method == "POST":
        # Grab the fields from the form
        fees_amount = request.POST.get("fees_amount")
        target_amount = request.POST.get("target_amount")
        selected_fee_type = request.POST.get("selected_fee_type")
        pay_date = request.POST.get("pay_date")

        # Create the user instance
        # construct a valid date out of the html date

        if fees_amount > target_amount:
            messages.warning(request, "Fees amount is greater than the target amount.")
            return redirect(
                reverse("fees:add-fee", kwargs={"pkid": pkid, "matricule": matricule})
            )
        pay_date_with_time = None
        if pay_date:
            date_string_from_form = pay_date

            pay_date = datetime.strptime(date_string_from_form, "%Y-%m-%d").date()
            # Create a specific time
            specific_time = time(8, 51, 2)

            pay_date_with_time = datetime.combine(
                pay_date, specific_time, tzinfo=timezone.utc
            )

        print(fees_amount, target_amount, selected_fee_type, pay_date)
        admin = AdminProfile.objects.filter(user=request.user).first()

        # Get the current Academic year

        current_year = AcademicYear.objects.get(is_current=True)
        fees = Fee.objects.create(
            student=student,
            amount=Decimal(fees_amount),
            fee_type=selected_fee_type,
            target=Decimal(target_amount),
            recieved_by=admin,
            academic_year=current_year,
        )
        if pay_date_with_time:
            fees.date_of_payment = pay_date_with_time
        fees.save()

        # Create a history record for the fee collection

        history = FeePaymentHistory.objects.create(
            fee=fees,
            student=student,
            amount_paid=fees_amount,
            collected_by=admin,
            pay_date=fees.date_of_payment,
            fee_type=fees.fee_type,
        )

        history.save()

        if fees.is_complete:
            student.is_owing = False
        else:
            student.is_owing = True
        student.save()

        return redirect(
            reverse(
                "students:student-detail",
                kwargs={"pkid": student.pkid, "matricule": student.matricule},
            )
        )

    template_name = "payments/add-fee.html"
    context = {
        "section": "fees",
        "student": student,
    }

    return render(request, template_name, context)


@login_required
def edit_fee_view(request, pkid, matricule, *args, **kwargs):

    # get the student for which the fees needs to be paid for
    student = get_object_or_404(StudentProfile, pkid=pkid, matricule=matricule)
    fee = Fee.objects.filter(student=student).first()

    if request.method == "POST":
        # Grab the fields from the form
        fees_amount = request.POST.get("fees_amount")
        target_amount = request.POST.get("target_amount")
        selected_fee_type = request.POST.get("selected_fee_type")
        pay_date = request.POST.get("pay_date")

        if fees_amount > target_amount:
            messages.warning(request, "Fees amount is greater than the target amount.")
            return redirect(
                reverse("fees:edit-fee", kwargs={"pkid": pkid, "matricule": matricule})
            )

        # Create the user instance
        # construct a valid date out of the html date
        pay_date_with_time = None
        if pay_date:
            date_string_from_form = pay_date

            pay_date = datetime.strptime(date_string_from_form, "%Y-%m-%d").date()
            # Create a specific time
            specific_time = time(8, 51, 2)

            pay_date_with_time = datetime.combine(
                pay_date, specific_time, tzinfo=timezone.utc
            )

        print(fees_amount, target_amount, selected_fee_type, pay_date)
        admin = AdminProfile.objects.filter(user=request.user).first()

        # Get the fee object associated with the student.
        fee = Fee.objects.filter(student=student).first()

        fee.student = student
        fee.fee_type = selected_fee_type
        fee.target = Decimal(target_amount)
        # fee.recieved_by = admin

        fee.amount = fee.amount + Decimal(fees_amount)

        if pay_date_with_time:
            fee.date_of_payment = pay_date_with_time
        fee.save()

        # Create a history record for the fee collection
        history = FeePaymentHistory.objects.create(
            fee=fee,
            student=student,
            amount_paid=Decimal(fees_amount),
            collected_by=admin,
            pay_date=fee.date_of_payment,
            fee_type=fee.fee_type,
        )

        history.save()

        if fee.is_complete:
            student.is_owing = False
        else:
            student.is_owing = True
        student.save()

        return redirect(
            reverse(
                "students:student-detail",
                kwargs={"pkid": student.pkid, "matricule": student.matricule},
            )
        )

    template_name = "payments/edit-fee.html"
    context = {"section": "fees", "student": student, "fee": fee}

    return render(request, template_name, context)
