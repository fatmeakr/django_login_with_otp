from random import Random
from django.db import models
from django.contrib.auth import models as django_auth_models
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from utils.validators import mobile_number_validator
from .managers import CustomUserManager
from .tasks import send_otp

TIME_OUT = 120


class User(django_auth_models.AbstractUser):
    username = None
    mobile_number = models.CharField(
        _("Mobile"), max_length=13, unique=True, validators=[mobile_number_validator]
    )
    otp_last_login = models.DateTimeField(
        _("Last login with otp"), blank=True, null=True
    )
    USERNAME_FIELD = "mobile_number"
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def set_otp(self) -> None:
        otp = str(Random().randint(10000, 99999))
        cache.set(self.mobile_number, otp, timeout=TIME_OUT)
        send_otp.delay(otp, self.mobile_number)

    def login_with_otp(self, value: str) -> bool:
        otp = cache.get(self.mobile_number)
        if value == otp:
            cache.delete(self.mobile_number)
            self.otp_last_login = timezone.now()
            return True
        return False

    def __str__(self):
        return f"{self.mobile_number}"

    def __repr__(self):
        return self.__str__()

