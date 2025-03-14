# nidec-inventory

Generador de inventario para accionamientos **Nidec Unidrive M**.

## Description

**nidec-inventory** permite generar un inventario de accionamientos **Nidec**, mediante el análisis de los ficheros de parámetros `*.parfile` situados en un repositorio.

## Features

- Rastreo recursivo sobre un path dado.
- Recopilación de información básica de todos los accionamientos del repositorio:

    - Nombre del producto.
    - Modelo del dispositivo.
    - Número de serie del dispositivo.
    - Versión del firmware del dispositivo.
    - Tensión nominal del dispositivo.
    - Corriente nominal del dispositivo.
    - Nombre asignado al dispositivo.
    - Modo de trabajo del dispositivo.
    - ip o nodo (si emplea comunicación modbus).
    - Contenido del slot 1
    - Contenido del slot 2
    - Contenido del slot 3
    - Contenido del slot 4
    - Path del fichero de parámetros.

- Generación de fichero de salida en formato **csv** o **excel**.

## Getting Started

### Dependencies

- pandas~=2.2.3
- PyYAML~=6.0.2
- setuptools~=75.8.2
- openpyxl~=3.1.5

### Installing

```shell
pip install nidec-inventory
```

### Usage

Ejemplos de ejecución:

```
# Ejemplos de salida en formato csv
$ python nidec-inventory.py -p "../REPO/Unidrive M Connect/" -f log
$ python nidec-inventory.py -p "../REPO/Unidrive M Connect/" -o csv -f log

# Ejemplo de salida en formato excel
$ python nidec-inventory.py -p "../REPO/Unidrive M Connect/" -o excel -f log
```

> [!NOTE]
> Por defecto, si solo se especifica el `path` del repositorio de parámetros, se generará un inventario en un fichero de tipo `csv`.

### Common arguments

- `--help` `(-h)`: muestra esta ayuda y sale.
- `--path_repo` `(-p)`: path del repositorio de ficheros de parámetros.
- `--file_out` `(-f)`: nombre del fichero de salida (sin extensión).
- `--output_format` `(-o)`: formato del fichero de salida, csv o excel.

## Author

- Carlos Alonso Martín

## Changelog

* 0.0a14
  * Bugs fixed 
* 0.0a5
  * Code rearrangement
* 0.0a4
  * Bugs fixed with excel format

## License

This project is licensed under the MIT License - see the LICENSE file for details.