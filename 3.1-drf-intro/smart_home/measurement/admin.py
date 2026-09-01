from django.contrib import admin

from measurement.models import Sensor, Measurement


class MeasurementInline(admin.TabularInline):
    model = Measurement
    extra = 3

@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [MeasurementInline]

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('temperature', 'recorded_at')