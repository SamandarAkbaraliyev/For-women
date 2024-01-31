from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from users.views import user_detail_view, user_redirect_view, user_update_view

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),

    path('api/allauth/', include('allauth.urls')),
]
