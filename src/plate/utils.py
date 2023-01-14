import random
from plate.resources import PLATE_ACCESS_LETTERS, PLATE_ACCESS_AREA


def generate_plate_number() -> str:
    """Generate a plate number"""
    plate_number = random.randint(0, 999)
    if plate_number < 10:
        plate_number = f"00{plate_number}"
    elif plate_number < 100:
        plate_number = f"0{plate_number}"
    return f'{random.choice(PLATE_ACCESS_LETTERS)}{plate_number}{random.choice(PLATE_ACCESS_LETTERS)}' \
           f'{random.choice(PLATE_ACCESS_LETTERS)}'


def generate_plate_area() -> dict:
    """Generate a plate area"""
    return random.choice(PLATE_ACCESS_AREA)
