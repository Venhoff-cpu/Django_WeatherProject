from django.contrib import admin
from django.urls import path
from .views import (
    About,
    Index,
    WeatherCurrent,
    WeatherDetail,
    WeatherForcast,
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    ChangeProfileView,
    ChangePasswordView,
    AddToFavorite,
    ProfileDetailView,
    DeleteFromFav,
    DeleteAccountView,
)


urlpatterns = [
    path("weather/", WeatherCurrent.as_view(), name="index"),
    path("weather/register/", RegisterView.as_view(), name="register"),
    path("weeather/login/", LoginView.as_view(), name="login"),
    path("weether/logout/", LogoutView.as_view(), name="logout"),
    path("weather/profile/hub", ProfileView.as_view(), name="profile"),
    path("weather/profile/detail", ProfileDetailView.as_view(), name="profile_detail"),
    path(
        "weather/profile/<int:user_id>/infochange",
        ChangeProfileView.as_view(),
        name="profile_info_change",
    ),
    path(
        "weather/profile/<int:user_id>/passwordchange",
        ChangePasswordView.as_view(),
        name="profile_pass_change",
    ),
    path("weather/profile/disable", DeleteAccountView.as_view(), name="disable_acc"),
    path("weather/about/", About.as_view(), name="about"),
    path(
        "weather/detail/<int:city_id>", WeatherDetail.as_view(), name="weather_detail"
    ),
    path(
        "weather/forecast/<int:city_id>",
        WeatherForcast.as_view(),
        name="weather_forecast",
    ),
    path("weather/add-fav/<int:city_id>/", AddToFavorite.as_view(), name="add_fav"),
    path("weather/del-fav/<int:city_id>/", DeleteFromFav.as_view(), name="del_fav"),
]
