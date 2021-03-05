import planificador as sc
import json
import os.path
from datetime import timedelta,datetime,date
import random

def Calcular_Costo(tareas):

    funcion=sc.Planificador()
    #a=random.sample(tareas['pedidos'],len(tareas['pedidos']))
    #dic={'pedidos':a}
    funcion.lista_de_tareas=tareas
    funcion.separar_por_tipos()
    funcion.ejecutar_proceso()
    costo_maquinas=0
    costo_trabajadores=0
    costo_insumos=0
    costo_penalizacion=0
    costo_Transporte=0
    costo_almacenaje=0
    x=funcion.transformacion.listatotal
    for i in x:
        costo_maquinas+=i['COSTO']*i['HORAS']
        if(i['TIPO']=='tanque0' or i['TIPO']=='tanque1' or i['TIPO']=='tanque2' or i['TIPO']=='tanque3' or i['TIPO']=='tanque4'):
            costo_trabajadores+=0
        else:
            costo_trabajadores+=i['EMPLEADO']['salario']*(i['EMPLEADO']['hsalida']-i['EMPLEADO']['hinicio'])
        if(i['INSUMOS']==0 or i['INSUMOS']==''):
            costo_insumos+=0
        else:
            costo_insumos+=i['INSUMOS'][0]['cantidad']*i['INSUMOS'][0]['precio']
        if(i['TAREA']['fecha_finalizacion']=='---'):
            costo_penalizacion+=0
        else:
            fechal=datetime.strptime(i['TAREA']['fecha_limite'],'%m %d %Y')
            fechaf=datetime.strptime(i['TAREA']['fecha_finalizacion'],'%m %d %Y')
            dif=fechaf-fechal
            if(dif.days<=0):
                costo_penalizacion+=0
            else:
                costo_penalizacion+=(i['TAREA']['penalizacion']*dif.days)
        
    x=funcion.registro_viajes
    for j in x:
        costo_Transporte+=j.costo
       

    x=funcion.producto_almacenado
    for j in x:
        #penalizacion por almacenar productos
        costo_almacenaje+= j['cantidad']*50

    del funcion
    
    return costo_maquinas+costo_trabajadores+costo_Transporte+costo_almacenaje+costo_insumos+costo_penalizacion

def Calcular_span(tareas):
    funcion=sc.Planificador()
    #a=random.sample(tareas['pedidos'],len(tareas['pedidos']))
    #dic={'pedidos':a}
    funcion.lista_de_tareas=tareas
    funcion.separar_por_tipos()
    funcion.ejecutar_proceso()
    diazero=funcion.dayzero
    x=funcion.registro_viajes
    dias=0
    for i in x:
        
        fecha=datetime.strptime(i.vencimiento,'%m %d %Y')
        dias+=(fecha-diazero).days

    return dias

def cargar_tareas():
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'
        name_of_file = 'data'
        completeName = os.path.join(save_path, name_of_file+".txt") 
        with open(completeName) as json_file:
            clientes = json.load(json_file)
        return clientes

#x=cargar_tareas()
#print(Calcular_Costo(x))