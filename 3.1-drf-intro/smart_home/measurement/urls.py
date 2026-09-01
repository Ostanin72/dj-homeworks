from django.urls import path

from measurement.views import SensorView, SensorDetailView, MeasurementView

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('sensors/', SensorView.as_view()),
    path('sensors/<int:pk>', SensorDetailView.as_view()),
    path('measurements/', MeasurementView.as_view()),
]
