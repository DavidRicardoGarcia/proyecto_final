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
# some_file.py
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '/home/david/Desktop/optimizacion_final')

from elementos_modelo import mantenimiento as mto
from elementos_modelo import clientes as clt

mant=mto.generar_mantenimiento_planificado()
tareas=clt.generar_tareas_aleatorias()

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
        context['segment'] = load_template
        context['tareas']=cargar_tareas()
        context['mantenimiento']=cargar_mantenimiento()
        context['empleados']=cargar_personal()
        context['almacen']=cargar_almacen()
        if request.method == "POST":
            data=request.POST
        else:
            data=" "
        #print(load_template)
        ejecutar_form(load_template,data)
        
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

def cargar_tareas():
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'data'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        return data['pedidos']

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