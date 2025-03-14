"""Motor de análisis para ficheros de parámetros de accionamientos NIDEC."""

import logging
import xml.etree.ElementTree as ET

from nidec.nidec_drive import NidecDrive

logger = logging.getLogger(__name__)

"""
Componentes de un motor de análisis
1. Entrada de Datos:
    Los datos pueden venir en diferentes formas: listas, archivos, strings,
    estructuras como DataFrames, o incluso flujos en tiempo real.
2. Procesador:
    Módulo principal que aplica reglas de análisis, algoritmos estadísticos,
    métodos de minería de datos o procesamiento lógico textual.
3. Resultado:
    Salida procesada: métricas consolidadas, patrones detectados o
    incluso visualizaciones.
"""

# ARCHIVO DE LOCALIZACIÓN
# LOC_FILE = 'es.yaml'
# loc = FileUtilities.read_yaml(LOC_FILE)
# loc = self.resources['loc']


class NidecParamFileEngine:
    """Análisis de ficheros de parametrización de los variadores Nidec.

    Proporciona métodos que permiten la extracción de las principales
    características de los variadores del repositorio así como realizar
    búsquedas de un parámetro.

    TODO: td_ref_07
    TODO: td_ref_08
    TODO: td_ref_09
    TODO: td_ref_10
    TODO: td_ref_11
    """

    def __init__(self, param_file, root_tag, resources):
        """Class constructor."""
        self.param_file = param_file
        self.root_tag = root_tag
        self.root_val = self._xml_root()
        self.resources = resources
        self.loc = resources['loc']

    def _xml_root(self):
        """Si root_tag es adecuada, retorna la estructura xml del fichero.

        Sobre la root_tag: es la primera etiqueta del fichero de parámetros,
        normalmente suele ser <ParameterFile>.

        :return: The root of the XML structure of the parameter file, or None
        """
        try:
            tree = ET.parse(self.param_file)
            root = tree.getroot()
            if root.tag == self.root_tag:
                return root
        except (FileNotFoundError, ET.ParseError) as e:
            logger.error(self.loc['err']['e5'], e)

        return None

    def _param_format(self, param):
        """Verifica el formato del número de parámetro.

        Verifica que el número de parámetro pasado como parámetro emplea el
        formato adecuado, de lo contrario lo adapta. Si no es posible adaptar
        el número de parámetro retorna None.

        Verificaciones realizadas:
        - El separador tiene que ser el punto `.`

        Adaptaciones realizadas:
        - Elimina los ceros iniciales: 01.00001 debería de tener el formato
        1.1 salvo para el 1.0

        TODO: td_ref_12
        TODO: td_ref_13
        TODO: td_ref_14
        """
        param = param.replace(',', '.')  # Corregir separador
        if '.' not in param:
            logger.error(self.loc['err']['e6'], param)
            return None

        # Dividir en partes
        param_parts = param.split('.')
        param_part_1 = param_parts[0].strip().lstrip('0') or '0'
        param_part_2 = param_parts[1].strip().lstrip('0') or '0'

        # Casos especiales, evita caso '1.0'
        if param_part_1 == '1' and param_part_2 == '0':
            return '1.0'

        return f'{param_part_1}.{param_part_2}'

    def _scan_slots(self, nidec_drive):
        """Identifica si las cartas opción instaladas en el variador."""
        if self.root_val is None:
            logger.error(self.loc['err']['e7'])
            return None

        try:
            for p in self.root_val.iter('option'):
                slot = p.attrib.get('slot')
                if slot == '1':
                    for n in p.iter('DeviceName'):
                        nidec_drive.slot1 = n.text
                elif slot == '2':
                    for n in p.iter('DeviceName'):
                        nidec_drive.slot2 = n.text
                elif slot == '3':
                    for n in p.iter('DeviceName'):
                        nidec_drive.slot3 = n.text
                elif slot == '4':
                    for n in p.iter('DeviceName'):
                        nidec_drive.slot4 = n.text
                else:
                    return None
        except KeyError:
            return '[SLOT] ERROR/NO DISPONIBLE'

    def _ip_node(self, nidec_drive):
        """Dirección IP / Nodo del variador."""
        if self.root_val is None:
            logger.error(self.loc['err']['e7'])
            return None

        try:
            for p in self.root_val.iter('Connection'):
                nidec_drive.ip_nodo = p.attrib['Address']
        except KeyError:
            return '[IP/NODO] ERROR/NO DISPONIBLE'

    def _modo_trabajo(self, nidec_drive):
        """Modo de trabajo definido en el variador."""
        if self.root_val is None:
            logger.error(self.loc['err']['e7'])
            return None

        # Utiliza ruta xml
        try:
            for p in self.root_val.findall("./drive/Configuration/Mode"):
                nidec_drive.mode = p.text
        except KeyError:
            return '[MODO] ERROR/NO DISPONIBLE'

    @staticmethod
    def _name(tag):
        """Extrae el nombre del variador.

        TODO: td_ref_15
        """
        try:
            return tag.attrib['name']
        except KeyError:
            return '[NAME] ERROR/NO DISPONIBLE'

    @staticmethod
    def _serial_number(tag):
        """Extrae el número de serie del variador.

        TODO: td_ref_16
        """
        try:
            return tag.attrib['serialnumber']
        except KeyError:
            return '[SERIAL NUMBER] ERROR'

    @staticmethod
    def _firmware(tag):
        """Extrae el número de firmware del variador.

        TODO: td_ref_17
        """
        try:
            return tag.attrib['firmware']
        except KeyError:
            return '[FIRMWARE] ERROR/NO DISPONIBLE'

    def _model_name(self):
        """Extrae el número de serie del variador.

        TODO: td_ref_18
        """
        try:
            for tag in self.root_val.iter('Model'):
                return tag.attrib['Name']
        except KeyError:
            return '[MODEL NAME] ERROR'

    def _producto(self):
        """Extrae el nombre del producto.

        TODO: td_ref_19
        """
        if self.root_val is None:
            logger.error(self.loc['err']['e7'])
            return None

        try:  # Utiliza ruta xml
            for p in self.root_val.findall("./drive/Classifier/Product"):
                return p.text
        except KeyError:
            return '[PRODUCT] ERROR'

    def _voltage(self):
        """Extrae el voltage del producto."""
        try:  # Contenido de <> <>
            for tag in self.root_val.iter('Voltage'):
                return tag.text
        except KeyError:
            return '[PRODUCT] VOLTAGE'

    def _current(self):
        """Extrae el voltage del producto."""
        try:  # Contenido de <> <>
            for p in self.root_val.iter('HDDriveRatedCurrentA'):
                return p.text
        except KeyError:
            return '[PRODUCT] CURRENT'

    def drive_header(self):
        """Retorna información sobre el variador.

        :return: The header information extracted from the Nidec parameter
        file, or None if the analysis fails.
        """
        if self.root_val is None:
            logger.error(self.loc['err']['e7'])
            return None

        # Verifica si self.root_val es iterable
        try:
            iter(self.root_val)
        except TypeError as e:
            logger.error(self.loc['err']['e7'], e)
            return None

        nidec_drive = NidecDrive()

        try:
            nidec_drive.param_file = self.param_file
        except AttributeError as e:
            logger.error(self.loc['err']['e9'], e)
            return None

        #
        # Proceso de ficheros
        #

        try:
            # Ruta XML
            nidec_drive.product = self._producto()

            self._scan_slots(nidec_drive)
            self._ip_node(nidec_drive)
            self._modo_trabajo(nidec_drive)
        except AttributeError as e:
            logger.error(self.loc['err']['e9'], e)
            return None

        # Contenido dentro de <
        try:
            for p in self.root_val.iter('drive'):
                nidec_drive.name = self._name(p)
                nidec_drive.serial_number = self._serial_number(p)
                nidec_drive.firmware = self._firmware(p)
        except AttributeError as e:
            logger.error(self.loc['err']['e9'], e)
            return None

        try:
            nidec_drive.model = self._model_name()

            # Contenido de <> <>
            nidec_drive.voltage = self._voltage()
            nidec_drive.current = self._current()
        except AttributeError as e:
            logger.error(self.loc['err']['e9'], e)
            return None

        return nidec_drive
