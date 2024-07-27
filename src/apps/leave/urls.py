from django.urls import path

from . import views

app_name = "leave"

urlpatterns = [
    path("", views.list_leave, name="list-leave"),
    path("add-leave", views.add_leave, name="add-leave"),
    path(
        "approve-leave/<int:leave_pkid>/<str:leave_type>",
        views.approve_leave,
        name="approve-leave",
    ),
    path(
        "reject-leave/<int:leave_pkid>/<str:leave_type>",
        views.reject_leave,
        name="reject-leave",
    ),
    path("see-leave/<int:pkid>/", views.see_leave, name="see-leave"),
    path("list-per-person", views.get_user_leaves, name="leave-per-person"),
]
