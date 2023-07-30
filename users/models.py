from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    class Meta:
        verbose_name = 'Подтверждение почты'
        verbose_name_plural = 'Подтверждения почты'

    def __str__(self):
        return f'{self.user.username} - {self.code}'

    def send_verification_email(self, is_expired=False):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = settings.DOMAIN_NAME + link
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = f'Для подтверждения учетной записи {self.user.email} на портале {settings.DOMAIN_NAME} пройдите по ссылке: {verification_link}'

        if is_expired:
            subject = f'Ваша ссылка для подтверждения учетной записи на портале {settings.DOMAIN_NAME} устарела'
            message = f'Для подтверждения учетной записи {self.user.email} на портале {settings.DOMAIN_NAME} пройдите по ссылке: {verification_link}'

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    @property
    def is_expired(self):
        return now() >= self.expiration

