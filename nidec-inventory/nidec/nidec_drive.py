"""Define un accionamiento NIDEC."""

from dataclasses import dataclass


@dataclass()
class NidecDrive:
    """Define un accionamiento Nidec.

    Atributos:
        - product (str): nombre del producto.
        - model (str): modelo del dispositivo.
        - serial_number (str): número de serie del dispositivo.
        - firmware (str): versión del firmware del dispositivo.
        - voltage (str): tensión nominal del dispositivo.
        - current (str): corriente nominal del dispositivo.
        - name (str): nombre asignado al dispositivo.
        - mode (str): modo de trabajo del dispositivo.
        - ip_nodo (str): ip o nodo (si emplea comunicación modbus).
        - slot1 (str): contenido del slot, si existe.
        - slot2 (str): contenido del slot, si existe.
        - slot3 (str): contenido del slot, si existe.
        - slot4 (str): contenido del slot, si existe.
        - param_file (str): path del fichero de parámetros.
    """

    product: str = ''
    model: str = ''
    serial_number: str = ''
    firmware: str = ''
    voltage: str = ''
    current: str = ''
    name: str = ''
    mode: str = ''
    ip_nodo: str = ''
    slot1: str = 'Not available'
    slot2: str = 'Not available'
    slot3: str = 'Not available'
    slot4: str = 'Not available'
    param_file: str = ''
