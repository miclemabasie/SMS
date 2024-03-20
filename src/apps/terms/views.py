from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import AcademicYear, ExaminationSession, Term
from django.contrib import messages
from django.utils import timezone as tz
from datetime import datetime, timezone, time
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def create_academic_year(request):

    if request.method == "POST":
        # Extract the infomation from the forms
        session_name = request.POST.get("academic_session_name")
        session_start_date = request.POST.get("academic_session_start_date")

        print( session_start_date, session_name)

        if not session_start_date:
            session_start_date = tz.now()
        else:
            # Convert the date to an appropriate date and recalculate
            date_string_from_form = session_start_date

            dob = datetime.strptime(date_string_from_form, '%Y-%m-%d').date()
            # Create a specific time
            specific_time = time(8, 51, 2)

            session_start_date = datetime.combine(dob, specific_time, tzinfo=timezone.utc)


        # Crete the session
        session = AcademicYear.objects.create(
            name = session_name,
            start_date = session_start_date
        )

        session.save()

        messages.success(request, "Session Successfully Created")

        return redirect(reverse("settings:setting-sessions"))


@login_required
def edit_academic_year(request, pkid):
    session = get_object_or_404(AcademicYear, pkid=pkid)
    if request.method == "POST":
        # Extract the infomation from the forms
        session_name = request.POST.get("academic_session_name")
        session_start_date = request.POST.get("academic_session_start_date")

        print( session_start_date, session_name)
        # Crete the session
        session.name = session_name

        if session_start_date:
            # Convert the date to an appropriate date and recalculate
            date_string_from_form = session_start_date

            dob = datetime.strptime(date_string_from_form, '%Y-%m-%d').date()
            # Create a specific time
            specific_time = time(8, 51, 2)

            session_start_date = datetime.combine(dob, specific_time, tzinfo=timezone.utc)

            session.start_date = session_start_date
        session.save()

        messages.success(request, "Session Successfully Updated")

        return redirect(reverse("settings:setting-sessions"))


@login_required
def mark_session_as_active(request, pkid):
    session = get_object_or_404(AcademicYear, pkid=pkid)

    # Get all other session and mark them as inactive for the mean time
    sessions = AcademicYear.objects.filter(is_current=True)
    print("These are the sessions: ", sessions)
    for ses in sessions:
        print(ses)
        ses.is_current = False
        ses.save()

    session.is_current = True
    session.save()

    messages.success(request, "Session Successfully Marked as Active")
    return redirect(reverse("settings:setting-sessions"))


@login_required
def create_term_view(request):
    if request.method == "POST":

        # extract the fields
        term_name = request.POST.get("selected_term")
        year_name = request.POST.get("selected_year")

        # Get the year
        years = AcademicYear.objects.filter(name=year_name)
        if years.exists:
            year = year.first()
        else:
            messages.warning(request, "Given year not found")
            return redirect(reverse("settings:setting-terms"))
        # Create a new term
        # make sure not term is current create with the same for the given year
        test_term = Term.objects.filter(academic_year=year, term=term_name)
        if test_term.exists():
            messages.error(request, "Term with same name already exist for the given year.")
            return redirect(reverse("settings:setting-terms"))
        
        # proceed to create the term

        term = Term.objects.create(
            term=term_name,
            academic_year = year
        )

        term.save()
        messages.success(request, "Term has successfully been created")
        return redirect(reverse("settings:setting-terms"))
    
    return redirect(reverse("settings:setting-terms"))


@login_required
def edit_term_view(request, pkid):
    if request.method == "POST":
        # extract the fields
        term_name = request.POST.get("selected_term")
        year_name = request.POST.get("selected_year")
        # Get the year
        print("form info", term_name, year_name)
        year = AcademicYear.objects.filter(name=year_name)
        if year.exists():
            year = year.first()
        else:
            messages.warning(request, "Given year not found")
            return redirect(reverse("settings:setting-terms"))
        # get and update the given term
        print("This is the year", year)
        terms = Term.objects.filter(academic_year=year, term=term_name)

        if terms.exists():
            term = terms.first()
            term.term = term_name
            term.academic_year = year

            term.save()
            messages.success(request, "Term updated successfully.")
            return redirect(reverse("settings:setting-terms"))
        else:
            messages.error(request, "Term not found")
            return redirect(reverse("settings:setting-terms"))

        
    return redirect(reverse("settings:setting-terms"))


@login_required
def mark_term_as_active(request, pkid):
    term = get_object_or_404(Term, pkid=pkid)

    # Get all other term and mark them as inactive for the mean time
    terms = Term.objects.filter(is_current=True)

    print(terms)
    for t in terms:
        print(t)
        t.is_current = False
        t.save()

    term.is_current = True
    term.save()

    messages.success(request, "Term Successfully Marked as Active")
    return redirect(reverse("settings:setting-terms"))