# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
import json
import os.path
from datetime import timedelta, datetime
import time
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/david/Desktop/optimizacion_final')

from elementos_modelo import mantenimiento as mto
from elementos_modelo import clientes as clt
import ACO
import PSO
import GA
import SA
import Funcion_objetivo as fo
funcion=fo

mant=mto.generar_mantenimiento_planificado()
tareas=clt.generar_tareas_aleatorias()
consulta={}
consulta['query']={'tipo':'','hinicio':'','duracion':'','nombre':'','empleado':'','insumos':''}

@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]

       
        #print(cargar_registros())
        if request.method == "POST":
            data=request.POST
            #print(data)
        else:
            data=" "
        
        ejecutar_form(load_template,data)

        #print(data)
        
        context['segment'] = load_template
        context['tareas']=ctareas
        context['mantenimiento']=cmantenimiento
        context['empleados']=cpersonal
        context['almacen']=calmacen
        lista=separar_por_tipos(ctareas)
        context['listas']=lista
        context['estados']=cargar_estados()
        #registros=cargar_registros()
        context['dias']=recursos_por_Fecha()
        context['consultas']=consulta['query']
        context['chartga']=graficas['GA']
        context['chartsa']=graficas['SA']
        context['chartpso']=graficas['PSO']
        context['chartaco']=graficas['ACO']
        #print(graficas['GA'])
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

def ejecutar_form(a,data):
    if(a=='forma-tareas.html'):
        if(data!= " "):
            if(data['nombre']!= " " and data['contratista']!= " " and data['recepcion']!= " " and data['cantidad']!= " "):
                fecha=datetime.strptime(data['recepcion'],'%Y-%m-%d')
                limite=timedelta(days=7)
                limite=fecha+limite
                limite=limite.strftime("%m %d %Y")
                recepcion=fecha.strftime("%m %d %Y")
                datos={"id": 0, "tipo": data['tipot']+" "+data['tipol']+data['tipob'], "cantidad": data['cantidad'], "nombre": data['nombre'], 
                "descripcion": data['descripcion'], "contratista": data['contratista'], "fecha_inicio": "---",
                "fecha_finalizacion": "---", "fecha_limite": limite, "fecha_recepcion": recepcion, "penalizacion": 1000,
                "comentarios": data['comment']}
                #print(datos)
                agregar_tarea(datos)
    if(a=='tareas-aleatorio.html'):
        if(data!= " "):
            if(data['ds']!= " " and data['td']!= " "and data['mc']!= " "):
                tareas.generar(int(data['ds']),float(data['td']),int(data['mc']))
    if(a=='forma-mantenimiento.html'):
        if(data!= " "):
            if(data['encargado']!= " " and data['eresp']!= " " and data['fechaplan']!= " " and data['fuentecost']!= " "):
                fecha=datetime.strptime(data['fechaplan'],'%Y-%m-%d')
                fecha=fecha.strftime("%m %d %Y")
                datos={"id": 0, "tipo": data['tipo'], "objeto": data['estacion'], 
                "encargado": data['encargado'], "descripcion": "informacion a agregar",
                "actividades": data['actividades'], "fecha planificada": fecha, 
                "fuente de costos": data['fuentecost'], "empresa_responsable": data['eresp']}

                #print(datos)
                agregar_orden_mto(datos)

    if(a=='mantenimiento-aleatorio.html'):
        if(data!= " "):
            if(data['ds']!= " " and data['od']!= " "):
                print(data)
                mant.generar(int(data['ds']),float(data['od']))
    if(a=='Horarios-Personal.html'):
        print('hp')
    if(a=='opt-ga.html'):
        if(data!= " "):
            if(data['tp']!= " " and data['tc']!= " " and data['tm']!= " " and data['ts']!= " " and data['maxk']!= " "):
                datos={"tp":data['tp'],"tc":data['tc'],"tm":data['tm'],"ts":data['ts'],"maxk":data['maxk']}
                actualizar_opt_Settings(datos,'ga')
                print('ga')
    if(a=='opt-SA.html'):
        if(data!= " "):
            if(data['nv']!= " " and data['maxk']!= " "):
                datos={"nv":data['nv'],"maxk":data['maxk']}
                actualizar_opt_Settings(datos,'sa')
                print('sa')
    if(a=='opt-PSO.html'):
        if(data!= " "):
            if(data['tp']!= " " and data['w']!= " " and data['c1']!= " " and data['c2']!= " " and data['maxk']!= " "):
                datos={"tp":data['tp'],"w":data['w'],"c1":data['c1'],"c2":data['c2'],"maxk":data['maxk']}
                actualizar_opt_Settings(datos,'pso')
                print('pso')
    if(a=='opt-ACO.html'):
        if(data!= " "):
            if(data['tp']!= " " and data['maxk']!= " "):
                datos={"tp":data['tp'],"maxk":data['maxk']}
                actualizar_opt_Settings(datos,'aco')
                print('aco')
    if(a=='opt-NSGA.html'):
        if(data!= " "):
            if(data['tp']!= " " and data['tc']!= " " and data['tm']!= " " and data['ts']!= " " and data['maxk']!= " "):
                datos={"tp":data['tp'],"tc":data['tc'],"tm":data['tm'],"ts":data['ts'],"maxk":data['maxk']}
                actualizar_opt_Settings(datos,'nsga')
                print('nsga')
    if(a=='Registros-totales.html'):
        if(data!= " "):
            if(data['tipof']!= " "):
                lista=[]
                for i in registros['lista_total']:
                    
                    if(i['TAREA']['fecha_inicio']== data['tipof']):
                        if ('EMPLEADO' in i.keys()):
                            lista.append({'tipo':i['TIPO'],'hinicio':i['HINICIO'],'duracion':i['HORAS'],'nombre':i['TAREA']['nombre'],'empleado':i['EMPLEADO']['nombre'],'insumos':i['INSUMOS']})
                        else: 
                            lista.append({'tipo':i['TIPO'],'hinicio':i['HINICIO'],'duracion':i['HORAS'],'nombre':i['TAREA']['nombre'],'empleado':'no tiene','insumos':i['INSUMOS']})
                #         lista.append()
                if (lista == []):
                    lista.append({'tipo':'','hinicio':'','duracion':'','nombre':'','empleado':'','insumos':''})
                consulta['query']=lista
                print(lista)
    if(a=='opt-solver.html'):
        if(data!= " "):
            botones=['btnGA','btnSA','btnPSO','btnACO']
            sel=['selGA','selSA','selPSO','selACO']
            labels=['GA','SA','PSO','ACO']
            ind=0
            for x in botones:
                if x in data.keys():
                    ejecutando_algoritmo(labels[ind])
                ind+=1
            
            ind=0
            for x in sel:
                if x in data.keys():
                    selecionar_Resultado(labels[ind])
                ind+=1


def selecionar_Resultado(a):

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'estado'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        #se le pasa el vector a la funcion planificador
        x=ctareas
        vector=data[a]['resultado']
        cargar_nueva_configuracion(vector,x)

def cargar_nueva_configuracion(state,tareas):

    x=ordenar_Tareas(state,tareas)
    a=funcion.Calcular_Costo(x,True)


def ordenar_Tareas(state,tareas):
    h={}
    newtareas=[]
    for i in state:
        for x in tareas:
            if(i == x['id']):
                newtareas.append(x)
    h['pedidos']=newtareas
    return h
            

def ejecutando_algoritmo(a):
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'estado'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        data[a]['estado']='ejecutando'

        with open(completeName,'w') as outfile:
            json.dump(data,outfile)

        if(a=='GA'):
            GA.ejecutarGA()
        

        if(a=='SA'):
            SA.ejecutarSA()
        

        if(a=='PSO'):
            PSO.ejecutarPSO()
        

        if(a=='ACO'):
            ACO.ejecutarACO()

        #se ejecuta el algoritmo en cuestion




def cargar_estados():
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'estado'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        return data



def cargar_tareas():
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'data'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        return data['pedidos']

def separar_por_tipos(tareas):

    vino=[]
    agua=[]
    jugo=[]
    #print(tareas)
    for val in tareas:
        tipo=val['tipo'].split()
        if(tipo[0]=='vino'):
            for x in range(val['cantidad']):
                k=val.copy()
                k['cantidad']=1
                vino.append(k)
            #print('v')
        if(tipo[0]=='agua'):
            for x in range(val['cantidad']):
                k=val.copy()
                k['cantidad']=1
                agua.append(k)
            #print('a')
        if(tipo[0]=='banano' or tipo[0]=='guanabana'):
            for x in range(val['cantidad']):
                k=val.copy()
                k['cantidad']=1
                jugo.append(k)

    nummax=len(vino)
    if(nummax < len(jugo)):
        nummax=len(jugo)
    if(nummax < len(agua)):
        nummax=len(agua)
    

    lista=[]
    for i in range(nummax):
        #print(i)

        if(i>=(len(jugo)-1)):
            jugov=""
        else:
            jugov=jugo[i]
        
        
        if(i>=(len(vino)-1)):
            vinov=""
        else:
            vinov=vino[i]
        
        
        if(i>=(len(agua)-1)):
            aguav=""
        else:
            aguav=agua[i]

        lista.append([jugov,vinov,aguav])

        
    return lista

def cargar_registros():
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'registro'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        
        return data

def actualizar_opt_Settings(datos,name):

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'optsettings'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        data['opt'][name]=datos

        with open(completeName,'w') as outfile:
            json.dump(data,outfile)

def agregar_tarea(datos):

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'data'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        maxvalue = max(data['pedidos'], key=lambda x:x['id'])

        datos['id']=maxvalue['id']+1

        data['pedidos'].append(datos)

        with open(completeName,'w') as outfile:
            json.dump(data,outfile)

def agregar_orden_mto(datos):

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'datam'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        maxvalue = max(data['preventivo'], key=lambda x:x['id'])

        datos['id']=maxvalue['id']+1

        data['preventivo'].append(datos)

        with open(completeName,'w') as outfile:
            json.dump(data,outfile)

def cargar_mantenimiento():
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'datam'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        return data['preventivo']

def cargar_personal():
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'datae'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        return data['empleados']

def cargar_almacen():
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'Punta Delicia'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        return data['racks']

def cargar_datos():
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'charts'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)
        
        pasoga=int(len(data['GA']['y'])/100)
        #print(pasoga)
        y=[]
        x=[]
        cont=0
        for i in range(len(data['GA']['y'])):
            if(cont==pasoga):
                y.append(data['GA']['y'][i])
                x.append(data['GA']['x'][i])
                cont=0
            cont+=1
        data['GA']['y']=y
        data['GA']['x']=x

        pasoga=int(len(data['SA']['y'])/100)
        #print(pasoga)
        y=[]
        x=[]
        cont=0
        for i in range(len(data['SA']['y'])):
            if(cont==pasoga):
                y.append(data['SA']['y'][i])
                x.append(data['SA']['x'][i])
                cont=0
            cont+=1
        data['SA']['y']=y
        data['SA']['x']=x


        pasoga=int(len(data['PSO']['y'])/100)
        #print(pasoga)
        y=[]
        x=[]
        cont=0
        for i in range(len(data['PSO']['y'])):
            if(cont==pasoga):
                y.append(data['PSO']['y'][i])
                x.append(data['PSO']['x'][i])
                cont=0
            cont+=1
        data['PSO']['y']=y
        data['PSO']['x']=x

        pasoga=int(len(data['ACO']['y'])/100)
        #print(pasoga)
        y=[]
        x=[]
        cont=0
        for i in range(len(data['ACO']['y'])):
            if(cont==pasoga):
                y.append(data['ACO']['y'][i])
                x.append(data['ACO']['x'][i])
                cont=0
            cont+=1
        data['ACO']['y']=y
        data['ACO']['x']=x

        return data

def recursos_por_Fecha():
    inicio=datetime.strptime(registros['fecha_inicio'],'%m %d %Y')
    final=datetime.strptime(registros['fecha_final'],'%m %d %Y')
    valor=final-inicio
    lista=[]
    for i in range(valor.days+1):
        dia=inicio + timedelta(days=(i))
        lista.append(dia.strftime("%m %d %Y"))

    return lista

registros=cargar_registros()
ctareas=cargar_tareas()
cmantenimiento=cargar_mantenimiento()
cpersonal=cargar_personal()
calmacen=cargar_almacen()
graficas=cargar_datos()