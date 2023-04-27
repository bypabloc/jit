from os import system as os_system

from json import dumps as json_dumps
from datetime import datetime


__version__ = '4.0.0'

# ==============================================================================
# CONFIGURACIONES DE COLORES SOLO CON MODO DEBUG
# ==============================================================================
GRAY = '\033[90m'
RED = '\033[91m'
RED_BOLD = '\033[1m\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
END = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

LEVEL = {
    'SPAM': GRAY,
    'ERROR': RED,
    'CRITICAL': RED_BOLD,
    'SUCCESS': GREEN,
    'DEBUG': GREEN,
    'WARNING': YELLOW,
    'VERBOSE': BLUE,
    'NOTICE': PURPLE,
    'HEADER': CYAN,
    'INFO': WHITE
}


class Logger(object):
    """
    Clase constructura de logs estandarizados.

    Attributes
    ----------
    debug : bool
        Indica si el log debe ejecutarse en modo debug. True en caso positivo y False en caso
        contrario

    :Authors:
        - Pablo Contreras

    :Created:
        - 2022-12-24
    """
    debug = False

    def clean(self):
        """
        Limpia la consola

        :Authors:
            - Pablo Contreras

        :Created:
            - 2022-12-24
        """
        os_system('clear')

    def info(self, message, traceback=None, extra={}):
        """
        Crea un log de tipo INFO

        Parameters
        ----------
        message : str
            Texto a imprimir como log
        traceback : str
            Texto correspondiente al traceback
        extra : dict
            Diccionario de variables que se quieren imprimir en el log

        :Authors:
            - Pablo Contreras

        :Created:
            - 2022-12-24
        """
        self.default('INFO', message, traceback, extra)

    def success(self, message, traceback=None, extra={}):
        """
        Crea un log de tipo SUCCESS

        Parameters
        ----------
        message : str
            Texto a imprimir como log
        traceback : str
            Texto correspondiente al traceback
        extra : dict
            Diccionario de variables que se quieren imprimir en el log

        :Authors:
            - Pablo Contreras

        :Created:
            - 2022-12-24
        """
        self.default('SUCCESS', message, traceback, extra)

    def warn(self, message, traceback=None, extra={}):
        """
        Crea un log de tipo WARNING

        Parameters
        ----------
        message : str
            Texto a imprimir como log
        traceback : str
            Texto correspondiente al traceback
        extra : dict
            Diccionario de variables que se quieren imprimir en el log

        :Authors:
            - Pablo Contreras

        :Created:
            - 2022-12-24
        """
        self.default('WARNING', message, traceback, extra)

    def error(self, message, traceback=None, extra={}):
        """
        Crea un log de tipo ERROR

        Parameters
        ----------
        message : str
            Texto a imprimir como log
        traceback : str
            Texto correspondiente al traceback
        extra : dict
            Diccionario de variables que se quieren imprimir en el log

        :Authors:
            - Pablo Contreras

        :Created:
            - 2022-12-24
        """
        self.default('ERROR', message, traceback, extra)

    def critical(self, message, traceback=None, extra={}):
        """
        Crea un log de tipo CRITICAL

        Parameters
        ----------
        message : str
            Texto a imprimir como log
        traceback : str
            Texto correspondiente al traceback
        extra : dict
            Diccionario de variables que se quieren imprimir en el log

        :Authors:
            - Pablo Contreras

        :Created:
            - 2022-12-24
        """
        self.default('CRITICAL', message, traceback, extra)

    def debugger(self, message, traceback=None, extra={}):
        """
        Crea un log de tipo DEBUG

        Parameters
        ----------
        message : str
            Texto a imprimir como log
        traceback : str
            Texto correspondiente al traceback
        extra : dict
            Diccionario de variables que se quieren imprimir en el log

        :Authors:
            - Pablo Contreras

        :Created:
            - 2022-12-24
        """
        if self.debug:
            self.default('DEBUG', message, traceback, extra)

    def default(self, level, message, traceback=None, extra={}):
        """
        Formato general de prints.

        Parameters
        ----------
        level : str
            Indica el tipo de log a imprimir
        message : str
            Texto a imprimir como log
        traceback : str
            Texto correspondiente al traceback
        extra : dict
            Diccionario de variables que se quieren imprimir en el log

        :Authors:
            - Pablo Contreras

        :Created:
            - 2022-12-24
        """
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f'[{date}][{level}] {message}'
        if extra != {}:
            message += f' {json_dumps(extra, default=str)}'
        if traceback is not None:
            message += f' {traceback}'
        print(
            LEVEL[level],
            message,
            END
        )
