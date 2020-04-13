from django.contrib.auth.models import User
from rest_framework import serializers
from msclone.tasks.models import *

class GlobalMetaForPickers:
    fields = ('id', 'display_as', 'list_display')
    ordering = ('id',)

class PickerSerializerSkeleton(serializers.ModelSerializer):
    display_as = serializers.SerializerMethodField()
    list_display = serializers.SerializerMethodField()

    get_display_as = lambda self, obj: f'{obj.title}'
    get_list_display = lambda self, obj: f'<b>{obj.title}</b>'

class UserPickerSerializer(PickerSerializerSkeleton):
    class Meta(GlobalMetaForPickers):
        model = User

    get_display_as = lambda self, obj: f'{obj.first_name} {obj.last_name}'
    get_list_display = lambda self, obj: f'<b>{obj.first_name} {obj.last_name}</b> {obj.email}'

class UnitPickerSerializer(PickerSerializerSkeleton):
    class Meta(GlobalMetaForPickers):
        model = TaskUnit

    get_display_as = lambda self, obj: f'{obj.definition}'
    get_list_display = lambda self, obj: f'<b>{obj.definition}</b>'

class StatusPickerSerializer(PickerSerializerSkeleton):
    class Meta(GlobalMetaForPickers):
        model = TaskStatus


class PremissionPickerSerializer(PickerSerializerSkeleton):
    class Meta(GlobalMetaForPickers):
        model = TaskPermission

    get_list_display = lambda self, obj: f'<b>{obj.title}</b> {obj.description}'