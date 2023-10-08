from django.contrib import admin
from .models import Nursery
from .models import TemporaryNursery
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

admin.site.register(Nursery)

admin.site.register(TemporaryNursery)


admin.site.register(CustomUser)

# Register your models here.
