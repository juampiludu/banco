import random

def generar_cvu() -> str:
    cvu_digits = [str(random.randint(0, 9)) for _ in range(22)]
    return ''.join(cvu_digits)