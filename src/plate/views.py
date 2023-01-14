from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import services
from .models import Plate
from .serializers import PlateAddSerializer


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def generate_plate(request: Request) -> Response:
    amount = request.query_params.get("amount", 1)
    result = services.generate_plate(plate_amount_qs=amount)
    return Response(result)


@api_view(http_method_names=["GET"])
@permission_classes([IsAuthenticated])
def get_plate(request: Request, pk=None) -> Response:
    if pk is None:
        plate_id = request.query_params.get("id", None)
        if not plate_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        plate = services.get_plate(plate_id=plate_id)
        return Response(plate)
    plate = services.get_plate(plate_id=pk)
    return Response(plate)


class AddPlate(generics.CreateAPIView):
    queryset = Plate.objects.all()
    serializer_class = PlateAddSerializer
    permission_classes = [IsAuthenticated]

