import datetime
import json
import os.path
import copy

class ingreso:

    def __init__(self,id,nombre,tipo,cant_und_bas,cant_und_doc,und_doc,f_c,precio,lote,fecha_caducidad,fecha_produccion,n_palet):
        self.id=id
        self.nombre=nombre
        self.tipo=tipo
        self.cant_und_bas=cant_und_bas
        self.cant_und_doc=cant_und_doc
        self.f_c=f_c
        self.precio=precio
        self.lote=lote
        self.caducidad=fecha_caducidad
        self.produccion=fecha_produccion
        self.tipo_palet='std'
        self.n_palet=n_palet

    def get_dict(self):
        data={'id':self.id,'tipo': self.tipo,'cantidad und basica':self.cant_und_bas,'cantidad und doc': self.cant_und_doc,
        'unidad doc':'palet','F_C':'f_C','precio':self.precio,'lote':self.lote,'caducidad':self.caducidad,'produccion':self.produccion,
        'n palets':self.n_palet}
        return data

class racks:

    def __init__(self):
        super().__init__()


    def get_dict(self):
        data={'id':self.id,'# niveles':self.niveles,'# secciones':self.secciones,'contenido':self.estante}
        return data

    def crear_racks(self,id,niveles,secciones):
        self.id=id
        self.niveles=niveles
        self.secciones=secciones
        self.estante=[]
        niveles=['A','B','C','D','E']
        c=0
        for i in niveles[:self.niveles]:
            cont=0
            lista=[]
            for x in range(secciones):
                a=palet(i+str(cont),'std',0,0,0)
                lista.append(a.get_dict())
                cont+=1
            self.estante.append(lista)
            c+=1


class palet:
    def __init__(self,id,tipo,cantidad,vencimiento,precio):
        self.id=id
        self.tipo=tipo
        self.cantidad=cantidad
        self.vencimiento=vencimiento
        self.precio=precio

    def get_dict(self):
        data={'id':self.id,'tipo': self.tipo,'cantidad':self.cantidad,'vencimiento':self.vencimiento,'precio':self.precio}
        return data

class almacen():
    
    def __init__(self):
        super().__init__()
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'Punta Delicia'

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)
        
        self.estantes=data
        self.ingresos=[]

    
    def asignar_recurso_lata(self,tipo,cantidad):

        lista=[]
        tipos_de_lata=['8-st','8-sl','12-st','12-sl','16-st']

        cant=0
        k=0
        for x in self.estantes['racks'][0]['contenido']:
            cont=0
            for i in x:
                if(tipo==i['tipo']):
                    lista.append(copy.deepcopy(i))
                    self.estantes['racks'][0]['contenido'][k][cont]['cantidad']=0
                    cant+=1
                    if(cant==cantidad):
                        return lista
                cont+=1
            k+=1

    def asignar_recurso_quimico(self,tipo,cantidad):

        lista=[]

        cant=0
        k=0
        for x in self.estantes['racks'][1]['contenido']:
            cont=0
            for i in x:
                if(tipo==i['tipo']):
                    lista.append(copy.deepcopy(i))
                    self.estantes['racks'][1]['contenido'][k][cont]['cantidad']=0
                    cant+=1
                    if(cant==cantidad):
                        return lista
                cont+=1
            k+=1
    
    def almacenar_producto_terminado(self,nombre,tipo,cantidad,fecha):
        n_palet=[]
        cant=0
        unidad_basica={'8-st':5130,'8-sl':4050,'12-st':3780,'12-sl':2970,'16-st':2970,'quimico 0':25,'quimico 1':25,'quimico 2':25,'quimico 3':25,'quimico 4':25}
        t=2
        for l in self.estantes['racks'][2:]:
            k=0
            for x in l['contenido']:
                cont=0
                for i in x:
                    if(i['cantidad']==0):
                        self.estantes['racks'][t]['contenido'][k][cont]['tipo']=tipo
                        self.estantes['racks'][t]['contenido'][k][cont]['cantidad']=unidad_basica[tipo]
                        n_palet.append([l['id'],i['id']])
                        cant+=1
                        if(cant==cantidad):
                            self.ingresos.append(ingreso(id,nombre,tipo,unidad_basica[tipo],cantidad,'palet','f_C',0,'lote',0,fecha,n_palet))
                            return 'ok'
                    cont+=1
                k+=1
            t+=1
        print('hola')
        if(cant!=cantidad):
            return cantidad-cant

    def entregar_producto(self,lista):

        cant=0
        k=0
        niveles=['A','B','C','D','E']
        for x in lista:
            
            for i in self.estantes['racks'][x[0]]['contenido'][niveles.index(x[1][0])]:
                if(i['id']==x[1]):
                    i['cantidad']=0
                    i['tipo']='-'
                    i['vencimiento']=0
                    i['precio']=0

    def ingreso_De_insumos(self,tipo,cantidad,fecha):

        cant=0
        n_palet=[]
        unidad_basica={'8-st':5130,'8-sl':4050,'12-st':3780,'12-sl':2970,'16-st':2970,'quimico 0':25,'quimico 1':25,'quimico 2':25,'quimico 3':25,'quimico 4':25}
        t=0
        for l in self.estantes['racks'][:2]:
            k=0
            for x in l['contenido']:
                cont=0
                for i in x:
                    if(i['tipo']==tipo and i['cantidad']==0):
                        self.estantes['racks'][t]['contenido'][k][cont]['cantidad']=unidad_basica[tipo]
                        n_palet.append([l['id'],i['id']])
                        cant+=1
                        if(cant==cantidad):
                            nombre='ingreso de insumos'
                            self.ingresos.append(ingreso(id,nombre,tipo,unidad_basica[tipo],cantidad,'palet','f_C',0,'lote',0,fecha,n_palet))
                            break
                    cont+=1
                k+=1
            t+=1

    def revisar_Stock(self):

        faltantes=[]
        stock=['8-st','8-sl','12-st','12-sl','16-st','quimico 0','quimico 1','quimico 2','quimico 3','quimico 4']
        
        
        for n in stock:
            cant=0
            for l in self.estantes['racks'][:2]:
                k=0
                for x in l['contenido']:
                    
                    for i in x:
                        if(i['tipo']==n):
                            cant+=i['cantidad']
            faltantes.append(cant)          

        return [faltantes[0]/51300,faltantes[1]/40500,faltantes[2]/37800,faltantes[3]/29700,faltantes[4]/29700,
        faltantes[5]/250,faltantes[6]/250,faltantes[7]/250,faltantes[8]/250,faltantes[9]/250]

    def inicializar_Racks(self,nombre,cantidad):

            save_path = '/home/david/Desktop/optimizacion_final/datos_json'

            name_of_file = nombre

            completeName = os.path.join(save_path, name_of_file+".txt") 
            
            listracks={}
            listracks['racks']=[]
            for i in range(cantidad):

                newrack=racks()
                newrack.crear_racks(i,5,10)
                listracks['racks'].append(newrack.get_dict())
            a=self.cargar_Con_material(listracks)
            with open(completeName,'w') as outfile:
                json.dump(a,outfile)
            
    def cargar_Con_material(self,a):

        tipos=['quimicos 0', 'quimicos 1', 'quimicos 2', 'quimicos 3', 'latas']
        tipos_de_lata=['8-st','8-sl','12-st','12-sl','16-st']
        tipos_de_quimicos=['quimico 0','quimico 1','quimico 2','quimico 3','quimico 4']
        latas_palet=[5130,4050,3780,2970,2970]
        #llenando los pallets con latas
        
        for j in a['racks'][0]['contenido']:
            cont=0
            for i in j:
                
                if(i['id'][0]=='A'):
                    a['racks'][0]['contenido'][0][cont]['tipo']=tipos_de_lata[0]
                    a['racks'][0]['contenido'][0][cont]['cantidad']=latas_palet[0]
                if(i['id'][0]=='B'):
                    a['racks'][0]['contenido'][1][cont]['tipo']=tipos_de_lata[1]
                    a['racks'][0]['contenido'][1][cont]['cantidad']=latas_palet[1]
                if(i['id'][0]=='C'):
                    a['racks'][0]['contenido'][2][cont]['tipo']=tipos_de_lata[2]
                    a['racks'][0]['contenido'][2][cont]['cantidad']=latas_palet[2]
                if(i['id'][0]=='D'):
                    a['racks'][0]['contenido'][3][cont]['tipo']=tipos_de_lata[3]
                    a['racks'][0]['contenido'][3][cont]['cantidad']=latas_palet[3]
                if(i['id'][0]=='E'):
                    a['racks'][0]['contenido'][4][cont]['tipo']=tipos_de_lata[4]
                    a['racks'][0]['contenido'][4][cont]['cantidad']=latas_palet[4]
                cont+=1
        #llenando los palets con quimicos
        for j in a['racks'][1]['contenido']:
            cont=0
            for i in j:
                
                if(i['id'][0]=='A'):
                    a['racks'][1]['contenido'][0][cont]['tipo']=tipos_de_quimicos[0]
                    a['racks'][1]['contenido'][0][cont]['cantidad']=25
                if(i['id'][0]=='B'):
                    a['racks'][1]['contenido'][1][cont]['tipo']=tipos_de_quimicos[1]
                    a['racks'][1]['contenido'][1][cont]['cantidad']=25
                if(i['id'][0]=='C'):
                    a['racks'][1]['contenido'][2][cont]['tipo']=tipos_de_quimicos[2]
                    a['racks'][1]['contenido'][2][cont]['cantidad']=25
                if(i['id'][0]=='D'):
                    a['racks'][1]['contenido'][3][cont]['tipo']=tipos_de_quimicos[3]
                    a['racks'][1]['contenido'][3][cont]['cantidad']=25
                if(i['id'][0]=='E'):
                    a['racks'][1]['contenido'][4][cont]['tipo']=tipos_de_quimicos[4]
                    a['racks'][1]['contenido'][4][cont]['cantidad']=25
                cont+=1
        
        return a


#a=almacen()
#y=a.asignar_recurso_lata('8-st',8)
#x=a.revisar_Stock()
#w=a.ingreso_De_insumos('8-st',8,'mañana')
#x=a.almacenar_producto_terminado('vino',20,2300)
#x=a.almacenar_producto_terminado('vino',81,2300)
#x=a.asignar_recurso_lata('8-st',8)
#print('hola')
#a.inicializar_Racks('Punta Delicia',4)
#a.inicializar_Racks('Servicio de almacen',10)