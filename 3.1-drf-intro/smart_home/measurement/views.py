# TODO: опишите необходимые обработчики, рекомендуется использовать
# generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from bson import is_valid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Sensor
from .serializers import SensorDetailSerializer, MeasurementSerializer


class ApiBaseView(APIView):
    renderer_classes = [JSONRenderer]


class MeasurementView(ApiBaseView):
    def post(self, request, format=None):
        _m = MeasurementSerializer(data=request.data)
        if _m.is_valid():
            measurement = _m.save()
        _r = SensorDetailSerializer(measurement)
        return Response(_r.data)


class SensorView(ApiBaseView):

    def get(self, request, id=None, format=None):
        if id is None:
            sensors = Sensor.objects.all()
            _s = SensorDetailSerializer(sensors, many=True)
            return Response(_s.data)
        sensor = Sensor.objects.get(id=id)
        _r = SensorDetailSerializer(sensor)
        return Response(_r.data)

    def post(self, request, format=None):
        _s = SensorDetailSerializer(data=request.data)
        if _s.is_valid():
            sensor = _s.save()
        _r = SensorDetailSerializer(sensor)
        return Response(_r.data)

    def patch(self, request, id, format=None):
        sensor = Sensor.objects.get(id=id)
        _s = SensorDetailSerializer(sensor, data=request.data, partial=True)
        if _s.is_valid():
            sensor = _s.update(sensor, _s.validated_data)
            print(sensor)
        _r = SensorDetailSerializer(sensor)
        return Response(_r.data)
