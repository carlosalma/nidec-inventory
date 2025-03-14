"""Módulo principal, gestiona los parámetros de entrada."""

import os
import sys
from pathlib import Path

from cli_parameters import get_cli_parameters
from helpers.file_helpers import FileUtilities
from nidec.drive_inventory import inventory_generator

root_path = Path(os.path.dirname(__file__))

MSG_0 = '[ERROR]: No se ha podido ejecutar el programa o ha ocurrido un error.'
MSG_1 = '[INFO]: Proceso concluido.'

# ARCHIVO DE LOCALIZACIÓN
LOC_FILE = Path(f"{root_path}/resources/es.yaml")
loc = FileUtilities.read_yaml(LOC_FILE)

# ARCHIVO DE CONFIGURACIÓN
CONFIG_FILE = Path(f"{root_path}/resources/config.yaml")
config = FileUtilities.read_yaml(CONFIG_FILE)

resources = {'loc': loc, 'config': config}


def main():
    """Función principal."""
    path_repo, file_out, out_type = get_cli_parameters(resources)
    return inventory_generator(path_repo, file_out, out_type, resources)


if __name__ == '__main__':
    if loc is not None and config is not None:
        if main():
            print(MSG_1)
        else:
            print(MSG_0)
            sys.exit(1)
    else:
        print(MSG_0)
        sys.exit(1)
