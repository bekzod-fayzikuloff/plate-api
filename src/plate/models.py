import uuid

from django.core.validators import RegexValidator
from django.db import models


class PlateArea(models.Model):
    """Model for plate areas there plate was registered"""
    code = models.CharField(max_length=3, unique=True)
    region = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self) -> str:
        return f"Plate Area - {self.region}[{self.code}]"

    class Meta:
        verbose_name = "Plate Area"
        verbose_name_plural = "Plate Areas"
        ordering = ["region"]


class Plate(models.Model):
    """Plate model
        id: uuid for identifying of plate
        plate_number: plate number should be unique for each plate area and should be exact for regex mark like `C111CC`
        plate_area: foreign key to the plate area
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    plate_number = models.CharField(max_length=6, validators=[
        RegexValidator(
            regex=r"^[АВЕКМНОРСТУХ]{1}[\d]{3}[АВЕКМНОРСТУХ]{2}$",
            message='Plate number need be exactly to specifications',
            code='invalid_plate_number'
        ),
    ])
    plate_area = models.ForeignKey(PlateArea, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"Plate {self.plate_number} [{self.plate_area.code}]"

    class Meta:
        verbose_name = "Plate"
        verbose_name_plural = "Plates"
        unique_together = (("plate_number", "plate_area"), )
