from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedUUIDModel
# Create your models here.


class TermChoices(models.TextChoices):
    FIRST_TERM = 'first_term', _('First Term')
    SECOND_TERM = 'second_term', _('Second Term')
    THIRD_TERM = 'third_term', _('Third Term')


class ExamSequenceChoices(models.TextChoices):
    FIRST_SEQUENCE = 'first_sequence', _('First Sequence')
    SECOND_SEQUENCE = 'second_sequence', _('Second Sequence')
    THIRD_SEQUENCE = 'third_sequence', _('Third Sequence')
    FOURTH_SEQUENCE = 'fourth_sequence', _('Fourth Sequence')
    FIFTH_SEQUENCE = 'fifth_sequence', _('Fifth Sequence')
    SIXTH_SEQUENCE = 'sixth_sequence', _('Sixth Sequence')
    SEVENTH_SEQUENCE = 'seventh_sequence', _('Seventh Sequence')

class Term(TimeStampedUUIDModel):
    term = models.CharField(
        verbose_name=_('Session'),
        max_length=20,
        choices=TermChoices.choices,
        default=TermChoices.FIRST_TERM,
    )

class ExaminationSession(TimeStampedUUIDModel):
    term = models.ForeignKey(Term, related_name='examination_sessions', on_delete=models.CASCADE)
    exam_session = models.CharField(
        verbose_name=_('Exam Sequence'),
        max_length=20,
        choices=ExamSequenceChoices.choices,
        default=ExamSequenceChoices.FIRST_SEQUENCE,
    )