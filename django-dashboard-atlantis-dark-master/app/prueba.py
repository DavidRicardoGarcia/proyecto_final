import json
import os.path

# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/david/Desktop/optimizacion_final/elementos_modelo')

import mantenimiento as mto

x=mto.generar_mantenimiento_planificado()