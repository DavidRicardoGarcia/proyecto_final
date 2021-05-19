import datetime
import random
from faker import Faker
import json
import os.path

class orden_de_mantenimiento:

    def __init__(self,id,tipo,objeto,encargado,actividades,fecha_planificada,fuente_de_costos,empresa_responsable):
        self.id=id
        self.tipo=tipo
        self.objeto=objeto
        self.encargado=encargado
        self.descripcion="informacion a agregar"
        self.actividades=actividades
        self.fecha_planficada=fecha_planificada
        self.fuente_de_costos=fuente_de_costos
        self.empresa_responsable=empresa_responsable

    
    def get_dict(self):
        data={'id':self.id,'tipo':self.tipo,'objeto':self.objeto,
        'encargado':self.encargado,'descripcion':self.descripcion,'actividades':self.actividades,
        'fecha planificada':self.fecha_planficada.strftime("%m %d %Y"),'fuente de costos':self.fuente_de_costos,
        'empresa_responsable':self.empresa_responsable}
        return data

class generar_mantenimiento_planificado():

    def __init__(self):
        super().__init__()
    
    def generar(self,rdiaz=10,tordenes=0.2):
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'datam'

        completeName = os.path.join(save_path, name_of_file+".txt") 
        #dias a simular
        Rdiaz=rdiaz#rdiaz
        listm={}
        listm['preventivo']=[]
        objeto=['desembarque','banda transportadora','lavado','pelado','molienda','centrifuga','uht',
        'tanque1','tanque2','tanque3','tanque4','tanque mecanico','tanque carbonatacion','enlatadora','embarque']
        tipo=['inspeccion','renovacion','servicio externo','inspeccion UDT','anotacion del mostrador','manual','trabajos adicionales']
        fake=Faker()
        #inicializacion de clientes
        for i in range(0,int(Rdiaz*tordenes)):

            plan=datetime.timedelta(days=random.randint(1,Rdiaz))
            diaplan=datetime.datetime.now()+plan
            tipo_mantenimiento=tipo[random.randint(0,len(tipo)-1)]
            if(tipo_mantenimiento=='servicio externo' or tipo_mantenimiento=='inspeccion UDT'):
                empresaR=fake.name()
            else: 
                empresaR='punta delicia'
            mantenimiento=orden_de_mantenimiento(i,tipo_mantenimiento,objeto[random.randint(0,len(objeto)-1)],
            fake.name(),'actividades',diaplan,'costos proyecto'+' '+fake.name(),empresaR)
            listm['preventivo'].append(mantenimiento.get_dict())
        
        with open(completeName,'w') as outfile:
            json.dump(listm,outfile)
    
#x=generar_mantenimiento_planificado()
#x.generar()
