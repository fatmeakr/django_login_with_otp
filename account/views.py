from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from .forms import OtpGeneratForm, OtpVerificationForm

UserModel = get_user_model()


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = "/login/"
    template_name = "index.html"


class OtpGenerateView(View):
    def post(self, request, *args, **kwargs):
        context = {}
        form = OtpGeneratForm(request.POST or None)
        if form.is_valid():
            mobile_number = form.cleaned_data["mobile_number"]
            request.session["mobile_number"] = mobile_number
            otp = cache.get(mobile_number)
            if not otp:
                user = UserModel.objects.get(mobile_number=mobile_number)
                user.set_otp()
            return redirect("login_verification")
        context["form"] = form
        return render(request, "login.html", context)

    def get(self, request):
        form = OtpGeneratForm()
        context = {
            "form": form,
        }
        return render(request, "login.html", context)


class OtpVerificationView(View):
    def post(self, request, *args, **kwargs):
        context = {}
        form = OtpVerificationForm(request.POST or None)
        if form.is_valid():
            otp = form.cleaned_data["otp"]
            mobile_number = request.session.get("mobile_number")
            user = UserModel.objects.get(mobile_number=mobile_number)
            if user.login_with_otp(otp):
                login(request, user)
                return redirect("home")
            else:
                context["form"] = OtpVerificationForm()
                context["error_message"] = "Otp does not match!"
        else:
            context["form"] = form
        return render(request, "login_verification.html", context)

    def get(self, request):
        form = OtpVerificationForm()
        mobile_number = request.session.get("mobile_number")
        ttl = cache.ttl(mobile_number)
        context = {
            "error_message": f"There are {ttl} second left to request another code.",
            "form": form
        }
        return render(request, "login_verification.html", context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

