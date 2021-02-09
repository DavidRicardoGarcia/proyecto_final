import datetime
import random
from faker import Faker
import json
import os.path

class datos_de_suministro:

    def __init__(self,id,producto,lugar,max_palets,cantidad,valor):
        self.id=id
        self.producto=producto
        self.lugar=lugar
        self.max_palets=max_palets
        self.cant=cantidad
        self.cantidad_reservada=0
        self.cantidad_adicional=0
        self.estado_minimo=self.cant*0.1
        self.cantidad_pedida=0
        self.valor=valor

    def get_dict(self):
        data={'id':self.id,'producto':self.producto,'lugar':self.lugar,
        'max palets':self.max_palets,'cantidad':self.cant,'cant. reservada':self.cantidad_reservada,
        'cant. adicional':self.cantidad_adicional,'minimo':self.estado_minimo,'cant. pedida':self.cantidad_pedida,
        'valor':self.valor}
        return data

class suministro():

    def __init__(self):
        super().__init__()

    def generar(self):


        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'data_S'

        completeName = os.path.join(save_path, name_of_file+".txt") 
        
        lists={}
        lists['suministros']=[]

        fake=Faker()
        #inicializacion de materiales
        for i in range(0,10):

            mprima=suministro(i,'material'+str(i),'0A0',10,10,50000)
            lists['suministros'].append(mprima.get_dict())
        
        with open(completeName,'w') as outfile:
            json.dump(lists,outfile)
        