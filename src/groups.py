from apps.fees.models import Fee, FeePaymentHistory
from apps.profiles.models import ParentProfile
from apps.reports.models import AcademicRecord, ReportCard
from apps.settings.models import Setting
from apps.staff.models import AdminProfile
from apps.students.models import (
    Attendance,
    Class,
    Mark,
    StudentProfile,
    StudentTempCreateProfile,
    Subject,
    TeacherProfile,
    TeacherTempCreateProfile,
)
from apps.terms.models import AcademicYear, ExaminationSession, Term
from apps.users.models import User
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

# Shell Plus Django Imports
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Avg, Case, Count, F, Max, Min, Prefetch, Q, Sum, When
from django.utils import timezone
from django.urls import reverse
from django.db.models import Exists, OuterRef, Subquery
