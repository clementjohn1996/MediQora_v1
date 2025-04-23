from django.contrib import admin
from .models import (
    Doctor,
    ConsultationType,
    SurgeryType,
    PatientCategory,
    StateEntry,
    CityEntry,
    PincodeEntry,
    DynamicField,
    EnquiryFor
    
)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name', 'department')


@admin.register(ConsultationType)
class ConsultationTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name',)
    search_fields = ('type_name',)


@admin.register(SurgeryType)
class SurgeryTypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'type_name')
    search_fields = ('title', 'type_name')


@admin.register(PatientCategory)
class PatientCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(StateEntry)
class StateEntryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CityEntry)
class CityEntryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(PincodeEntry)
class PincodeEntryAdmin(admin.ModelAdmin):
    list_display = ('value',)
    search_fields = ('value',)


@admin.register(DynamicField)
class DynamicFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'field_type', 'required')
    list_filter = ('field_type', 'required')
    search_fields = ('name',)

@admin.register(EnquiryFor)
class EnquiryForAdmin(admin.ModelAdmin):
    list_display = ['id', 'name'] 