from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Fee, FeePaymentHistory, ExtraPayment
from apps.students.models import StudentProfile
from apps.staff.models import AdminProfile
from apps.terms.models import AcademicYear
from datetime import datetime, time, timezone
from decimal import Decimal
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from apps.settings.models import Setting


@login_required
def add_fee_view(request, pkid, matricule, *args, **kwargs):
    user = request.user
    administrator = user.admin_profile
    # get the student for which the fees needs to be paid for
    student = get_object_or_404(StudentProfile, pkid=pkid, matricule=matricule)
    setting = Setting.objects.all().first()
    current_year = AcademicYear.objects.get(is_current=True)
    if request.method == "POST":
        # Grab the fields from the form
        fee = request.POST.get("selected_fee_installment")
        fee_type = request.POST.get("selected_fee_type")
        print(fee, fee_type)
        # check if student is owning:
        if fee_type == "school_fees":
            if not student.is_owing:
                messages.warning(request, "Student Has completed Fees Already")
                return redirect(
                    reverse(
                        "students:student-detail",
                        kwargs={"pkid": student.pkid, "matricule": student.matricule},
                    )
                )
            # check if there have paid first_installment
            has_paid_first_installment = student.has_paid_only_first
            if has_paid_first_installment:
                # confirm the amount
                if student.get_amount_paid() == setting.first_installment:
                    # then student has indeed paid only first instllment
                    # pay second installment
                    # confirm that second installment was selected
                    if fee == "second_installment":
                        # studnet indeed wants to pay second installment
                        # get fee record and update
                        fee_record = Fee.objects.get(
                            student=student,
                            academic_year=current_year,
                            fee_type=fee_type,
                        )
                        fee_record.amount += setting.second_installment
                        fee_record.save()
                        # creat a new payment history record
                        payment_history = FeePaymentHistory.objects.create(
                            fee=fee_record,
                            student=student,
                            amount_paid=setting.second_installment,
                            collected_by=administrator,
                            fee_type=fee_type,
                        )
                        payment_history.save()

                        # confirm that fees has been paid in full
                        if student.get_amount_paid() == setting.get_complete_fee:
                            print("fee is complete")
                            student.is_owing = False
                            student.save()
                            fee_record.is_complete = True
                            fee_record.save()
                        messages.error(request, "Second installment paid successfully")
                        return redirect(
                            reverse(
                                "students:student-detail",
                                kwargs={
                                    "pkid": student.pkid,
                                    "matricule": student.matricule,
                                },
                            )
                        )
            else:
                # has not paid anything
                if fee == "second_installment":
                    messages.error(
                        request, "Can not pay second installment at the moment"
                    )
                    return redirect(
                        reverse(
                            "students:student-detail",
                            kwargs={
                                "pkid": student.pkid,
                                "matricule": student.matricule,
                            },
                        )
                    )
                elif fee == "first_installment":
                    fee_record = Fee.objects.create(
                        amount=setting.first_installment,
                        student=student,
                        fee_type=fee_type,
                        academic_year=current_year,
                    )
                    fee_record.save()
                    payment_history = FeePaymentHistory.objects.create(
                        fee=fee_record,
                        student=student,
                        amount_paid=setting.first_installment,
                        collected_by=administrator,
                        fee_type=fee_type,
                    )
                    payment_history.save()
                    messages.error(request, "First installment paid successfully")
                    return redirect(
                        reverse(
                            "students:student-detail",
                            kwargs={
                                "pkid": student.pkid,
                                "matricule": student.matricule,
                            },
                        )
                    )

                elif fee == "complete":
                    print("fee", fee)
                    fee_record = Fee.objects.create(
                        amount=setting.get_complete_fee,
                        student=student,
                        fee_type=fee_type,
                        academic_year=current_year,
                    )
                    fee_record.save()
                    payment_history = FeePaymentHistory.objects.create(
                        fee=fee_record,
                        student=student,
                        amount_paid=setting.get_complete_fee,
                        collected_by=administrator,
                        fee_type=fee_type,
                    )
                    payment_history.save()
                    if student.get_amount_paid() == setting.get_complete_fee:
                        print("fee is complete")
                        student.is_owing = False
                        student.save()
                        fee_record.is_complete = True
                        fee_record.save()
                    messages.error(request, "Fee completed.")
                    return redirect(
                        reverse(
                            "students:student-detail",
                            kwargs={
                                "pkid": student.pkid,
                                "matricule": student.matricule,
                            },
                        )
                    )
                else:
                    messages.error(request, "Not allowed.")
                    return redirect(
                        reverse(
                            "students:student-detail",
                            kwargs={
                                "pkid": student.pkid,
                                "matricule": student.matricule,
                            },
                        )
                    )
        elif fee_type == "pta":
            print("making pta payment")
            # perform pta payment
            fee_record = Fee.objects.create(
                amount=setting.pta,
                student=student,
                fee_type=fee_type,
                academic_year=current_year,
            )
            fee_record.save()
            payment_history = FeePaymentHistory.objects.create(
                fee=fee_record,
                student=student,
                amount_paid=setting.pta,
                collected_by=administrator,
                fee_type=fee_type,
            )
            payment_history.save()
            student.has_paid_pta = True
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
        "settings": setting,
    }

    return render(request, template_name, context)


@login_required
def add_extra_payments(request, pkid, matricule, *args, **kwargs):
    user = request.user
    admin = user.admin_profile
    student = StudentProfile.objects.get(pkid=pkid, matricule=matricule)
    if request.method == "POST":
        # get data from the form
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        remark = request.POST.get("remark")
        print(name, amount, remark)

        # create an extrapayment instance
        payment = ExtraPayment.objects.create(
            student=student,
            name=name,
            remark=remark,
            amount_paid=amount,
            collected_by=admin,
        )
        payment.save()
        messages.error(request, "Payment added successfully.")
        return redirect(
            reverse(
                "students:student-detail",
                kwargs={
                    "pkid": student.pkid,
                    "matricule": student.matricule,
                },
            )
        )

    template_name = "payments/add-extras.html"
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
