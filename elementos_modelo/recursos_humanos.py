from datetime import timedelta, datetime
import random
from faker import Faker
import json
import os.path

class trabajador:

    def __init__(self,id,nom_ape,email,telefono,empresa,estacion_trabajo):
        self.id=id
        self.nom_ape=nom_ape
        self.email=email
        self.telefono=telefono
        self.empresa=empresa
        self.cargo='operario'
        self.departamento='produccion y operaciones'
        self.estacion_trabajo=estacion_trabajo
        self.salario=16 #pesos hora
        self.horas_Extra=25 #pesos hora 

    def get_dict(self):
        data={'id':self.id,'nombre':self.nom_ape,'email':self.email,
        'telefono':self.telefono,'empresa':self.empresa,'cargo':self.cargo,'departamento':self.departamento,
        'estacion':self.estacion_trabajo,'salario':self.salario,'horas_extra':self.horas_Extra}
        return data

class horarios():

    def __init__(self):
        super().__init__()
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'datae'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)
        
        self.data=data
        

    def crear_lista_De_Empleados(self):

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'datae'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        elist={}
        elist['empleados']=[]
        estacion_De_trabajo=['desembarque','banda transportadora','lavado','pelado','molienda','centrifuga','uht',
        'tanque mecanico','tanque carbonatacion','enlatadora','embarque']
        fake=Faker()
        #inicializacion de clientes
        for i in range(0,int(len(estacion_De_trabajo))):
            
            empleado=trabajador(i,fake.name(),fake.name()+'@gmail.com',3001231234,
            'Punta Delicia',estacion_De_trabajo[i])
            elist['empleados'].append(empleado.get_dict())

        with open(completeName,'w') as outfile:
            json.dump(elist,outfile)

    def asignar_horario(self,nombre):

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'datae'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)
        
        
        name_of_file_1 = nombre

        completeName_1 = os.path.join(save_path, name_of_file_1+".txt") 

        hlist={}
        hlist['horario empleados']=[]
        for i in data['empleados']:
            r=random.uniform(0,1)
            if (r>0.8):
                i['hinicio']=0
                i['hsalida']=0
                i['estado']='incapacidad'
                #en el caso de incapacidad suponer que la maquina no se opera ese dia o que alguien hace relevo y toca pagarle un extra?
            else:
                i['hinicio']=8
                i['hsalida']=18
                i['estado']='disponible'
            hlist['horario empleados'].append(i)
        
        with open(completeName_1,'w') as outfile:
            json.dump(hlist,outfile)
            
    def asignar_horario_ng(self):
 
        hlist={}
        hlist['horario empleados']=[]

        for i in self.data['empleados']:
            r=random.uniform(0,1)
            if (r>1):
                i['hinicio']=0
                i['hsalida']=0
                i['estado']='incapacidad'
                #en el caso de incapacidad suponer que la maquina no se opera ese dia o que alguien hace relevo y toca pagarle un extra?
            else:
                i['hinicio']=8
                i['hsalida']=18
                i['estado']='disponible'
            hlist['horario empleados'].append(i)
        return hlist


#x=horarios()
#x.crear_lista_De_Empleados()
#x.asignar_horario('prueba1')
