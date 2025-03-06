"""Conjunto de métodos destinados a la gestión del sistema de ficheros.

NOTA: Solo situar utilidades de ficheros de uso genérico!!
"""

import logging
from pathlib import Path
import pandas as pd
import yaml

logger = logging.getLogger(__name__)

MSG_1 = '[INFO]: limpieza de directorios.'
MSG_2 = '[INFO]: generando lista de ficheros.'
MSG_3 = '[ERROR]: imposible acceder al path especificado.'
MSG_4 = '[ERROR]: inesperado: %s'
MSG_5 = '[INFO]: limpieza finalizada.'
MSG_6 = '[INFO]: limpieza de ficheros por extensión.]'
MSG_7 = '[PTH->]: %s'
MSG_8 = '[EXT->]: %s'
MSG_9 = '[INFO]: limpieza de todos los ficheros.'
MSG_10 = '[ERROR]: fichero %s inaccesible. %s'
MSG_11 = '[ERROR]: fichero %s inadecuado.'
MSG_12 = '[ERROR]: %s al convertir los datos a DataFrame para el archivo %s.'
MSG_13 = '[ERROR]: formato %s no válido. Debe ser csv o excel'
MSG_14 = '[INFO]: Archivo %s generado correctamente.'
MSG_15 = '[ERROR]: %s al intentar guardar el archivo %s.'
MSG_16 = '[ERROR]: %s al generar el archivo %s.'

class FileUtilities:
    """Utilidades de gestión del sistema de ficheros."""

    @staticmethod
    def recursive_file_listing(path, extension, files_excluded):
        """Listado recursivo de ficheros con una extensión dada.

        Se parte de un path dado y se excluyen aquellos ficheros cuyo
        nombre está en la lista file_excluded.

        :param path: Path del repositorio.
        :param extension: Extensión de los ficheros a listar.
        :param files_excluded: Lista de ficheros a excluir.
        :return: Lista de ficheros.
        """
        path = Path(path)
        files = []

        try:
            if path.exists():
                logger.info(MSG_7, path)
                logger.info(MSG_8, extension)
                for child in path.rglob(extension):
                    if child.is_file():
                        if child.stem not in files_excluded:
                            files.append(child)
                logger.info(MSG_2)
            else:
                logger.error(MSG_3)
        except Exception as e:
            logger.error(MSG_4, e)
        return files


    @staticmethod
    def recursive_file_listing_test(path, extension, files_excluded):
        """Listado recursivo de ficheros con una extensión dada.

        Se parte de un path dado y se excluyen aquellos ficheros cuyo
        nombre está en la lista file_excluded.

        :param path: Path del repositorio.
        :param extension: Extensión de los ficheros a listar.
        :param files_excluded: Lista de ficheros a excluir.
        :return: Lista de ficheros.
        """
        files = []
        if path.exists():
            logger.info(MSG_7, path)
            logger.info(MSG_8, extension)
            for child in path.rglob(extension):
                if child.is_file():
                    if child.stem not in files_excluded:
                        files.append(child)
                        # TODO: td_ref_01
            logger.info(MSG_2)
        else:
            logger.info(MSG_3)
        return files


    @staticmethod
    def remove_file_if_extension_not_equal(path, extension):
        """Elimina los ficheros cuya extensión no coincida con la dada.

        :param path: Path del repositorio.
        :param extension: Extensión de los ficheros a listar.
        """
        if path.exists():
            logger.info(MSG_7, path)
            logger.info(MSG_6)
            for child in path.rglob('*.*'):
                if child.is_file():
                    if child.suffix not in extension or child.suffix == '':
                        child.unlink()
            logger.info(MSG_5)
        else:
            logger.info(MSG_3)


    @staticmethod
    def remove_directory_if_name_in_list(path, removable_directories):
        """Elimina los directorios si su nombre están en la lista.

        :param path: Path del repositorio.
        :param removable_directories: Directorios a eliminar.
        """
        if path.exists():
            logger.info(MSG_7, path)
            logger.info(MSG_1)
            for child in path.rglob('**/*'):
                if child.is_dir():
                    if child.name in removable_directories:
                        logger.info(child)
                        child.rmdir()
            logger.info(MSG_5)
        else:
            logger.error(MSG_3)


    @staticmethod
    def remove_all_files(path):
        """Elimina todos los ficheros del path.

        :param path: Path a limpiar.
        """
        if path.exists():
            logger.info(MSG_7, path)
            logger.info(MSG_9)
            for child in path.rglob('*.*'):
                if child.is_file():
                    child.unlink()
            logger.info(MSG_5)
        else:
            logger.info(MSG_3)


    @staticmethod
    def read_yaml(yaml_file):
        """Load the yaml file and return the contents as a dictionary.

        :param yaml_file: Path to the yaml file.
        :return: Dictionary with the contents of the yaml file or None
            if the file is not accessible.
        """
        try:
            with open(yaml_file, 'r', encoding='utf8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError as e:
            logger.error(MSG_10, yaml_file, e)
            return None
        except yaml.YAMLError:
            logger.error(MSG_11, yaml_file)
            return None


    @staticmethod
    def data_out_file(output_filename, data, output_format):
        """Generate data file, in csv or excel, from the provided data.

        :param output_filename: Name of the output file (without extension).
        :param data: Data to be exported to CSV/Excel format.
        :param output_format: Format of the output file. Can be 'csv' or 'excel'.
        :return: True if the file is generated successfully, False otherwise.
        """
        try:
            df = pd.DataFrame(data)
        except (TypeError, pd.errors.ParserError) as e:
            logger.error(MSG_12, e, output_filename)
            raise

        if output_format == 'csv':
            file_path = Path(f"{output_filename}.csv").resolve()
        elif output_format == 'excel':
            file_path = Path(f"{output_filename}.xlsx").resolve()
        else:
            logger.error(MSG_13, output_format)
            return False

        try:
            if output_format == 'csv':
                df.to_csv(file_path, index=False)
            elif output_format == 'excel':
                df.to_excel(file_path, index=False)
            else:
                logger.error(MSG_13, output_format)
                return False
        except Exception as e:
            logger.error(MSG_16, e, output_filename)
            raise

        logger.info(MSG_14, file_path)
        return True
