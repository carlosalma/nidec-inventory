"""Analiza los ficheros de parámetros de los accionamientos NIDEC."""

import logging
from pathlib import Path

from helpers.file_helpers import FileUtilities
from nidec.nidec_param_file_engine import NidecParamFileEngine

logger = logging.getLogger(__name__)


def _analysis(parameter_file, resources):
    """Analyze the parameter file and return the header information.

    :param parameter_file: The file path to the parameter file that contains
        the configuration or data to be analyzed.
    :resources: The configuration and localization resources, otherwise None
        is returned.
    :return: The header information extracted from the Nidec parameter file,
        or None if the analysis fails.

    # TODO: td_ref_02
    # TODO: td_ref_03
    # TODO: td_ref_04
    # TODO: td_ref_05
    # TODO: td_ref_06
    """
    config = resources['config']
    loc = resources['loc']

    # ETIQUETA RAIZ
    etiqueta_raiz = config['config']['root_tag']

    try:
        # Datos del accionamiento extraidos de su fichero de parámetros
        nidec_drive = NidecParamFileEngine(
            parameter_file, etiqueta_raiz, resources)
        return nidec_drive.drive_header()
    except FileNotFoundError:
        logger.error(loc['err']['e1'], parameter_file)
        return None
    except Exception as e:
        logger.error(loc['err']['e3'], parameter_file, e)
        return None


def inventory_generator(path_repo, file_out, out_type, resources):
    """Genera el inventario de accionamientos.

    :param path_repo: Path del repositorio.
    :param file_out: Nombre del fichero de salida, sin extensión.
    :param out_type: Tipo de fichero de salida: csv o excel
    :param resources: configuración y localización
    :return True if the process concludes successfully, otherwise False.
    """
    config = resources['config']
    loc = resources['loc']

    # NOMBRES DE FICHEROS EXCLUIDOS
    files_excluded = config['config']['excluded_files']
    # EXTENSIÓN FICHERO PARÁMETROS
    ext_par_file = f"*{config['config']['ext_par_file']}"

    header_container = []

    try:
        parameter_repo = Path(path_repo).resolve()
        parameter_files = FileUtilities.recursive_file_listing(
            parameter_repo, ext_par_file, files_excluded)
    except FileNotFoundError:
        logger.error(loc['err']['e11'])
        return False

    # Acceso a cada fichero del repositorio
    try:
        for parameter_file in parameter_files:
            # Extraer información del fichero
            nidec_drive_header = _analysis(parameter_file, resources)
            # Si se ha extraido información del accionamiento, almacenarla
            if nidec_drive_header is not None:
                header_container.append(nidec_drive_header)
    except FileNotFoundError:
        return False

    # Generar fichero de salida con los datos
    if _output_data_file_generator(
            file_out, out_type, header_container, resources):
        logger.info(loc['info']['i1'])
        return True

    logger.error(loc['err']['e10'])
    return False


def _output_data_file_generator(file_out, out_type, header_container,
                                resources):
    """Generador de fichero de datos.

    Permite seleccionar el tipo de fichero de salida, pudiendo ser este
    de tipo excel o csv.

    :param file_out: Nombre del fichero de salida de datos
    :param out_type: Tipo de fichero de salida: csv o excel
    :param header_container: Contenedor de datos a guardar en el fichero.
    :return True if the process concludes successfully, otherwise False.
    """
    loc = resources['loc']

    try:
        results_file = Path(file_out).resolve()
    except FileNotFoundError:
        logger.error(loc['err']['e11'])
        return False

    try:
        if out_type in ('excel', 'csv'):
            FileUtilities.data_out_file(
                results_file, header_container, out_type)
            return True

        logger.error(loc['err']['e2'], out_type)
        return False
    except Exception as e:
        logger.error(loc['err']['e4'], e)
        return False
