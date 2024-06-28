from django.urls import path
from . import views

app_name = "leave"

urlpatterns = [
    path("", views.list_leave, name="list-leave"),
    path("add-leave", views.add_leave, name="add-leave"),
    path("approve-leave", views.approve_leave, name="approve-leave"),
    path("reject-leave", views.reject_leave, name="reject-leave"),
    path("see-leave/<int:pkid>/", views.see_leave, name="see-leave"),
]
