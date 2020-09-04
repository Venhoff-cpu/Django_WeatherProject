from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, View, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic.base import ContextMixin

from .utils import hourly_temperature_plot, forecast_temperature_plot
from .models import City
from .forms import (
    CityForm,
    CreateUserForm,
    ChangePasswordForm,
    ChangeProfileForm,
    DeleteProfileForm,
)
from .api_processor import (
    api_current_ctx_processor,
    api_forecast_processor,
    get_hourly_temperature,
    get_df_forecast,
    fetch_current_data,
    fetch_forecast_data,
    get_city_name,
)


class Index(TemplateView):
    template_name = "WeatherLookup/base.html"


class About(TemplateView):
    template_name = "WeatherLookup/about.html"


class WeatherCurrent(FormView):
    template_name = "WeatherLookup/weather_homepage.html"
    form_class = CityForm

    def form_valid(self, form):
        ctx = {}
        city = form.cleaned_data.get("name")
        data = fetch_current_data(city)
        print(data)
        if data['cod'] == '404':
            messages.info(self.request, "Incorrect city name. Try again")
        else:
            ctx = api_current_ctx_processor(data)
        user = self.request.user
        if not user.is_anonymous:
            fav_cities = [city.name for city in City.objects.filter(user=user)]
            ctx['fav_cities'] = fav_cities
        ctx['form'] = form
        return render(self.request, "WeatherLookup/weather_homepage.html", ctx)


class WeatherDetail(TemplateView):
    template_name = "WeatherLookup/weather_detail.html"

    def get_context_data(self, **kwargs):
        city_id = kwargs["city_id"]
        data_cur = fetch_current_data(city_id)

        if data_cur:
            lon = data_cur["coord"]["lon"]
            lat = data_cur["coord"]["lat"]
            json_data_hourly = fetch_forecast_data(lat, lon)
            data_hourly = get_hourly_temperature(json_data_hourly)
            temperature_graph = hourly_temperature_plot(data_hourly)
            ctx = api_current_ctx_processor(data_cur)
            ctx['graph'] = temperature_graph
        return ctx


class WeatherForcast(TemplateView):
    template_name = "WeatherLookup/weather_forecast.html"

    def get_context_data(self, **kwargs):
        ctx = {}
        city_id = kwargs["city_id"]
        temp_data = fetch_current_data(city_id)
        lon = temp_data["coord"]["lon"]
        lat = temp_data["coord"]["lat"]
        data = fetch_forecast_data(lat, lon)
        if data:
            city_name = get_city_name(temp_data)
            forecast_data = api_forecast_processor(data)
            df = get_df_forecast(forecast_data)
            ctx["city"] = city_name
            ctx["table"] = df.to_html(
                index=False,
                classes="table",
            )
            ctx["graph"] = forecast_temperature_plot(df)
        else:
            messages.error(self.request, "No forecast for specified location.")
        return ctx


class AddToFavorite(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request, city_id):
        user = get_object_or_404(User, pk=request.user.id)
        city_data = fetch_current_data(city_id)
        city, created = City.objects.get_or_create(
            name=city_data["name"],
            city_id=city_data["id"],
            lon=city_data["coord"]["lon"],
            lat=city_data["coord"]["lat"],
            user=user,
        )
        if created:
            city.save()
            messages.success(request, f"{city} added to observed")
        else:
            messages.error(request, f"{city} already observed")
            return redirect(reverse_lazy("index"))
        return redirect(reverse_lazy("profile"))


class DeleteFromFav(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request, city_id):
        city = get_object_or_404(City, city_id=city_id, user=request.user.id)
        city.delete()
        messages.success(request, f"{city} deleted from observed")
        return redirect(reverse_lazy("profile"))


class RegisterView(FormView):
    template_name = "WeatherLookup/register.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f"Signing successful. You can now login.")
        return super().form_valid(form)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "WeatherLookup/login.html"
    success_url = reverse_lazy("profile")

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            messages.info(self.request, "Incorrect username or password.")
            return redirect(reverse_lazy("login"))
        return super().form_valid(form)


class LogoutView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")

    def post(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect(reverse_lazy("index"))


class ProfileMixin(LoginRequiredMixin, ContextMixin):
    login_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        user = get_object_or_404(User, pk=self.request.user.id)
        ctx.update({"user": user})
        return ctx


class ProfileView(ProfileMixin, TemplateView):
    template_name = "WeatherLookup/profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        user = get_object_or_404(User, pk=self.request.user.id)
        cities_query = City.objects.filter(user=user.id)
        cities = []
        for city in cities_query:
            city_data = fetch_current_data(city.city_id)
            city_ctx = api_current_ctx_processor(city_data)
            cities.append(city_ctx)
        ctx.update(
            {
                "user": user,
                "cities": cities,
            }
        )
        return ctx


class ProfileDetailView(ProfileMixin, TemplateView):
    template_name = "WeatherLookup/profile_personal.html"


class ChangeProfileView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    form_class = ChangeProfileForm
    success_url = reverse_lazy("profile")
    template_name = "WeatherLookup/change_info.html"

    def get_object(self, queryset=None):
        return self.request.user

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the error below.")
        return super().form_invalid(form)


class ChangePasswordView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy("login")
    form_class = ChangePasswordForm
    fields = "__all__"
    template_name = "WeatherLookup/change_pass.html"

    def form_valid(self, form):
        user = get_object_or_404(User, pk=self.kwargs.get("user_id"))
        if user is not None:
            user.set_password(form.cleaned_data["password1"])
            user.save()
            messages.success(self.request, "Password changed successfully.")
        else:
            messages.success(self.request, "Something went wrong.")
            return redirect(
                reverse_lazy(
                    "profile_pass_change", kwargs={"user_id": self.request.user.id}
                )
            )

        return redirect(reverse_lazy("index"))


class DeleteAccountView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy("login")
    form_class = DeleteProfileForm
    template_name = "WeatherLookup/profile_delete.html"

    def form_valid(self, form):
        user = self.request.user
        user.is_active = False
        user.save()
        messages.success(self.request, "Profile successfully disabled.")
        return redirect(reverse_lazy("index"))
