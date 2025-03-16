# nidec-inventory

Inventory generator for **Nidec Unidrive M** and **Commander C** drives.

## Description

**nidec-inventory** allows you to generate an inventory for **Nidec Unidrive M and Commander C** drives, by analyzing the `*.parfile` parameter files located in a repository.

## Features

- Recursive tracing on a given path.
- Collection of basic information from all drives in the repository:

    - Product **name**.
    - Device **model**.
    - Device **serial number**.
    - Device **firmware** version.
    - Device **rated voltage**.
    - Device **rated current**.
    - **Name** assigned to the device.
    - Device **operating mode**.
    - **IP** or **node** (if using Modbus communication).
    - Contents of **slot 1**.
    - Contents of **slot 2**.
    - Contents of **slot 3**.
    - Contents of **slot 4**.
    - **Path** of the parameter file.

- Generation of output file in **csv** or **excel** format.

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

Examples of execution:

```
# Examples of output in csv format
$ python nidec-inventory.py -p "../REPO/Unidrive M Connect/" -f log
$ python nidec-inventory.py -p "../REPO/Unidrive M Connect/" -o csv -f log
```

```
# Example of output in Excel format
$ python nidec-inventory.py -p "../REPO/Unidrive M Connect/" -o excel -f log
```

> By default, if only the `path` of the parameter repository is specified, an inventory will be generated in a `csv` file.

### Common arguments

- `--help` `(-h)`: show this help and exit.
- `--path_repo` `(-p)`: path of the parameter file repository.
- `--file_out` `(-f)`: output file name (without extension).
- `--output_format` `(-o)`: output file format, csv or excel.

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