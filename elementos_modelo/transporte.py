import datetime
import json
import math
import random
import os.path

class viajes:

    def __init__(self,id,nombre,tipo,origen,destino,descripcion,cantidad,peso,vencimiento,tipo_empaque):
        self.id=id
        self.nombre=nombre
        self.tipo=tipo
        self.origen=origen
        self.destino=destino
        self.descripcion=descripcion
        self.cant=cantidad
        self.peso=peso
        self.vencimiento=vencimiento
        self.tipo_empaque=tipo_empaque
        self.costo=0

    def asignar_vehiculos(self):
        #40 pulgadas guarda 21 pallets
        if(self.tipo=='40'):
            cantidad_vehiculos=math.ceil(float(self.cant/21))
        else:#20 pulgadas guarda 10 pallets
            cantidad_vehiculos=math.ceil(float(self.cant/10))

        if(self.origen=='empresa' and self.destino=='almacen'):
            distancia=10
        else:
            distancia=20#random.uniform(1,100)

        self.costo=(distancia*100+self.peso*2)*cantidad_vehiculos


        self.data={'id':self.id,'nombre':self.nombre,'tipo':self.tipo,
        'origen':self.origen,'destino':self.destino,'descripcion':self.descripcion,
        'cantidad':self.cant,'peso':self.peso,'vencimiento':self.vencimiento,'tipo empaque':self.tipo_empaque,'costo':self.costo}

    def guardar(self):

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'datav'

        completeName = os.path.join(save_path, name_of_file+".txt") 
        
        vlist={}
        #vlist['viajes']=[]

        with open(completeName) as json_file:
            datan = json.load(json_file)

        vlist=datan
        vlist['viajes'].append(self.data)

        with open(completeName,'w') as outfile:
            json.dump(vlist,outfile)

'''
if __name__ == "__main__":

    viaje_prueba=viajes(1,'wallmart','20','empresa','almacen','todo normal',20,1000,datetime.date(2020,12,2),'lata')
    viaje_prueba.asignar_vehiculos()
'''