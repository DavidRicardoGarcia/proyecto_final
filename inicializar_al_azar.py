from elementos_modelo import clientes as cl
from elementos_modelo import mantenimiento as mto


a=cl.generar_tareas_aleatorias()
a.generar(20,0.5,4)

b=mto.generar_mantenimiento_planificado()
b.generar(20)