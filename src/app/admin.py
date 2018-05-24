from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from app.models import Contribution, Delegate, Node, StatusUpdate


class NodeAdmin(admin.TabularInline):
    model = Node

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 10})},
    }


class StatusUpdateAdmin(admin.TabularInline):
    model = StatusUpdate

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 10})},
    }


class ContributionAdmin(admin.TabularInline):
    model = Contribution

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': 30})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 100})},
    }


@admin.register(Delegate)
class DelegateAdmin(admin.ModelAdmin):
    search_fields = ('name', 'address',)
    readonly_fields = ['name', 'slug', 'address', 'public_key', 'created', 'updated']
    inlines = [ContributionAdmin, NodeAdmin, StatusUpdateAdmin]

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 16, 'cols': 100})},
    }
