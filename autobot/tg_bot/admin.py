from django.contrib import admin
from tg_bot.models import *

# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Automobile)
class AutomobileAdmin(admin.ModelAdmin):
    pass

@admin.register(Refuilings)
class Refuilings(admin.ModelAdmin):
    pass
