from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from utils.validators import mobile_number_validator


UserModel = get_user_model()


class OtpGeneratForm(forms.Form):
    mobile_number = forms.CharField(required=True, validators=[mobile_number_validator])

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data["mobile_number"] or None
        try:
            UserModel.objects.get(mobile_number=mobile_number)
        except ObjectDoesNotExist:
            raise forms.ValidationError(_("Access Denied."))
        return mobile_number


class OtpVerificationForm(forms.Form):
    otp = forms.CharField(required=True, label='Code')


# admin form
class UpdateUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_("To change your password " 'use <a href="../password/">this form</a>.'),
    )

    class Meta:
        model = UserModel
        fields = "__all__"
