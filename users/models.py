from django.db      import models
from core.models    import TimeStampModel

class User(TimeStampModel):
    email        = models.EmailField(max_length=45, unique=True)
    password     = models.CharField(max_length=200)
    name         = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=17, blank=True)
    address      = models.CharField(max_length=1000, blank=True)
    deleted_at   = models.DateTimeField(null=True)

    class Meta:
        db_table = 'users'