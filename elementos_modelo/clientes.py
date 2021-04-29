import datetime
import random
from faker import Faker
import json
import os.path
import copy

class orden_de_venta:

    def __init__(self,id_pedido,tipo_de_producto,cantidad,nombre,contratista,fecha_limite,fecha_recepcion,penalizacion):
        self.id_pedido=id_pedido
        self.tipo_de_producto=tipo_de_producto
        self.cantidad=cantidad
        self.nombre=nombre
        self.descripcion="informacion a agregar"
        self.contratista=contratista
        self.fecha_inicio=datetime.date(2020,1,1)
        self.fecha_finalizacion=datetime.date(2020,1,1)
        self.fecha_limite=fecha_limite
        self.fecha_recepcion=fecha_recepcion
        self.penalizacion=penalizacion
        self.comentarios="sin comentarios"
    
    def get_dict(self):
        data={'id':self.id_pedido,'tipo':self.tipo_de_producto,'cantidad':self.cantidad,
        'nombre':self.nombre,'descripcion':self.descripcion,'contratista':self.contratista,'fecha_inicio':'---','fecha_finalizacion':'---',
        'fecha_limite':self.fecha_limite.strftime("%m %d %Y"),'fecha_recepcion':self.fecha_recepcion.strftime("%m %d %Y"),
        'penalizacion':self.penalizacion,'comentarios':self.comentarios}
        return data

class generar_tareas_aleatorias():

    def __init__(self):
        super().__init__()

    def generar(self,fecha,nclientes,cpedidos):

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'data'

        completeName = os.path.join(save_path, name_of_file+".json") 

        hclist={}
        hclist['pedidos']=[]
        id=0

        with open(completeName) as json_file:
            data = json.load(json_file)
            hclist=copy.deepcopy(data)
            if(data['pedidos']!=[]):
                id=data['pedidos'][-1]['id']+1

        tipos_de_productos,tinsumos=cargar_tipos_de_tareas()
        tipos_de_lata=['8-st','8-sl','12-st','12-sl','16-st']
        tipo=['con-gas','sin-gas']

        
        fake=Faker()
        #inicializacion de clientes
        for i in range(nclientes):
            tp=random.randint(0,len(tipos_de_productos)-1)
            if(tipos_de_productos[tp]=='vino'):
                t=1
            else:
                t=random.randint(0,len(tipo)-1)
            tl=random.randint(0,len(tipos_de_lata)-1)
            t1=tinsumos[tipos_de_productos[tp]]['Tinsumo']
            cotainf=datetime.timedelta(days=t1)
            t2=tinsumos[tipos_de_productos[tp]]['Tprocesamiento']
            cotasup=datetime.timedelta(days=t2)
            prioridad=datetime.timedelta(days=(random.randint(0,5)))
            dialim=fecha+(cotainf+cotasup+prioridad)
            cliente=orden_de_venta(id+i,tipos_de_productos[tp]+' '+tipos_de_lata[tl]+' '+tipo[t],random.randint(1,cpedidos),fake.name(),fake.name(),dialim,fecha,1000)
            hclist['pedidos'].append(cliente.get_dict())

        with open(completeName,'w') as outfile:
            json.dump(hclist,outfile)
        
    def resetear(self):

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'data'

        completeName = os.path.join(save_path, name_of_file+".json") 
        hclist={}
        hclist['pedidos']=[]
        with open(completeName,'w') as outfile:
            json.dump(hclist,outfile)

def cargar_tipos_de_tareas():
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'
        name_of_file = 'modelsettings'
        completeName = os.path.join(save_path, name_of_file+".txt") 
        with open(completeName) as json_file:
            tipos = json.load(json_file)
        a=[]
        a=list(tipos['tareas'].keys())
        return a,tipos['tareas']
#x=cargar_tipos_de_tareas()
#x=generar_tareas_aleatorias()
#fecha=datetime.datetime.now()+datetime.timedelta(days=1)
#x.generar_Dia(save=False,fecha=fecha,nclientes=4,cpedidos=2)
#x.resetear()
#x.generar(fecha,4,2)
#print('vida gran hpta')
