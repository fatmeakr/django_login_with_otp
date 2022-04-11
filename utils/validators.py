from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


mobile_number_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message=_("Mobile number format is incorrect"),
)
