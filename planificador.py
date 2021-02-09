#!/usr/bin/python
import json
import os.path
from datetime import timedelta,datetime,date
import graficar as tablero
import copy
from elementos_modelo import recursos_humanos as rh
from elementos_modelo import transporte as tr
from elementos_modelo import almacen as alm
#calcula el uso de recursos para la transformacion de fruta a jugo
class proceso:
    def __init__(self):
        self.tareas=[]

        self.fecha_Referencia=datetime.now()
        self.tarea={}
        self.estadot='disponible'
        self.listadedatos=[
        {'TIPO':'desembarque','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'1','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'pesado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'2','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'lavado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'3','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'pelado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'4','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'molienda','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'5','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'centrifuga','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'6','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'UHT','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'7','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0}]
        
        self.tanques=[
        {'TIPO':'tanque1','HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'tanque2','HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'tanque3','HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'tanque4','HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':{},'DIA':0,'INSUMOS':0}]
        self.b=0
        self.c=0
        self.d=0
            
        self.listadedatos1=[
        {'TIPO':'mezclado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'8','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'carbonatado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'9','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'enlatado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'10','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'embarque','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'11','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0}]


        self.listatotal=[]
        self.listater=[]
        self.listaenlatar=[]

    def check(self,a):
        if(a =='j'):
            self.jugo.pop(0)
        if(a =='v'):
            self.vino.pop(0)
        if(a =='a'):
            self.agua.pop(0)
        if(a=='d'):
            print('no hubo orden')

    def verificar_si_almacenar(self,a):
        
        contador=0
        for tanque in self.tanques:
            if(tanque['ESTADO']=='disponible'):
                contador=contador+1
        if(contador>=a):
            return True
        else:
            return False

    def agregar_al_registro(self,a):

        for x in a:
            self.listatotal.append(x)
     
    def organizar_lista_enlatar(self):
        y={}
        lista=[]
        cont=0
        h=self.listaenlatar.copy()
        for x in h:
            y['index']=cont
            y['dias']=(datetime.strptime(x['TAREA']['fecha_limite'],'%m %d %Y')-self.fecha_Referencia)
            lista.append(y.copy())
            cont+=1
        lista=sorted(lista,key=lambda k: k['dias'],reverse=False)

        aux=self.listaenlatar.copy()

        cont=0
        for k in lista:

            self.listaenlatar[cont]=aux[k['index']]
            cont+=1

    def asignar_tanque(self,a):
        B=0
        if(self.tanques[0]['ESTADO']=='disponible'):
            self.tanques[0]['ESTADO']='ocupado'
            self.tanques[0]['TAREA']=a.copy()
            B=self.tanques[0]['TIPO']
        elif(self.tanques[1]['ESTADO']=='disponible'):
            self.tanques[1]['ESTADO']='ocupado'
            self.tanques[1]['TAREA']=a.copy()
            B=self.tanques[1]['TIPO']
        elif(self.tanques[2]['ESTADO']=='disponible'):
            self.tanques[2]['ESTADO']='ocupado'
            self.tanques[2]['TAREA']=a.copy()
            B=self.tanques[2]['TIPO']
        elif(self.tanques[3]['ESTADO']=='disponible'):
            self.tanques[3]['ESTADO']='ocupado'
            self.tanques[3]['TAREA']=a.copy()
            B=self.tanques[3]['TIPO']
        else: 
          print('todos los tanques estan llenos')
          self.estadot='no disponible'
          B='0'
        return B

    def restaurar_estado(self,t):
        if(t==18):
          self.estado='disponible'

    def entregar_lista(self):
        return self.listadedatos

    def agregar_Tarea(self,a):
        self.tarea=a

    def entregar_producto(self):
        return self.tarea

    def poner_fecha_salida(self,lista,d):

        cont=0
        for x in lista:
            lista[cont]['TAREA']['fecha_finalizacion']=(self.fecha_Referencia+timedelta(days=(d-1))).strftime("%m %d %Y")
            cont+=1
        print('.')
        return lista

    def calcular_procesos_jugo(self,t,d,cond1,cond2,a,trabajadores,insumos1,insumos2,insumos3):

        #si es la hora de inicio de la jornada laboral y hay tanques disponible se procesa una tarea
        if(cond1):
 
            #se le asigna un tanque a la tarea
            self.b=self.asignar_tanque(a)

            self.listadedatos=[
            {'TIPO':'desembarque','HINICIO':8,'HORAS':1,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][0],'TAREA':a,'DIA':d,'INSUMOS':0},
            {'TIPO':'pesado','HINICIO':9,'HORAS':2,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][1],'TAREA':a,'DIA':d,'INSUMOS':0},
            {'TIPO':'lavado','HINICIO':9,'HORAS':2,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][2],'TAREA':a,'DIA':d,'INSUMOS':insumos1},
            {'TIPO':'pelado','HINICIO':9,'HORAS':2,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][3],'TAREA':a,'DIA':d,'INSUMOS':0},
            {'TIPO':'molienda','HINICIO':9,'HORAS':2,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][4],'TAREA':a,'DIA':d,'INSUMOS':insumos2},
            {'TIPO':'centrifuga','HINICIO':10,'HORAS':3,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][5],'TAREA':a,'DIA':d,'INSUMOS':0},
            {'TIPO':'UHT','HINICIO':11,'HORAS':2,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][6],'TAREA':a,'DIA':d,'INSUMOS':0}]
        if(cond2) : #si es la hora de finalizar la tarea de procesamiento se guardan los datos y se limpian, ademas se pasa la tarea al tanque que se le haya asignado
            
            #self.listadedatos=self.poner_fecha_salida(self.listadedatos,d)
            self.agregar_al_registro(self.listadedatos)
            self.listadedatos=[
            {'TIPO':'desembarque','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'1','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
            {'TIPO':'pesado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'2','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
            {'TIPO':'lavado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'3','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
            {'TIPO':'pelado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'4','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
            {'TIPO':'molienda','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'5','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
            {'TIPO':'centrifuga','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'6','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
            {'TIPO':'UHT','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'7','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0}]
            #se asigna la tarea a un tanque
            cont=0
            for tank in self.tanques:
              if(tank['TIPO']==self.b): 
                self.tanques[cont]['HINICIO']=13
                self.tanques[cont]['HORAS']=67
                self.tanques[cont]['DIA']=d
                self.tanques[cont]['INSUMOS']=insumos3
                self.b=' '
              cont=cont+1

    def calcular_procesos_tanques(self,t,d,cond1,a,insumos):
        #se le suma cada hora que pase un producto en un tanque cuando ya esta listo para ser enlatado y no se enlata
        cont=0
        for enlatar in self.listaenlatar:
            self.listaenlatar[cont]['HORAS'] +=1
            cont+=1
        if(cond1):
            cont=0
            self.c=self.asignar_tanque(a)

            for tank in self.tanques:
                if(tank['TIPO']==self.c): 
                    self.tanques[cont]['HINICIO']=8
                    self.tanques[cont]['HORAS']=24
                    self.tanques[cont]['DIA']=d
                    self.tanques[cont]['INSUMOS']=insumos
                    self.c=' '
                cont=cont+1      
        #tiempo que tiene que pasar una tarea en su tanque
        cont=0
        for tank in self.tanques:
          if(tank['ESTADO'] == 'ocupado'):
              vacd=tank['DIA']+int((tank['HINICIO']+tank['HORAS'])/24)#DIA EN QUE PASA A LA LISTA DE PRODUCTOS A ENLATAR  
              vach=(tank['HINICIO']+tank['HORAS'])%24 # tiempo en que pasa a la lista para enlatar
              if(vacd==d and vach==t):
                  self.tanques[cont]['ESTADO']='para enlatar'
                  self.listaenlatar.append(self.tanques[cont].copy())
          cont=cont+1  

    def proceso_enlatar(self,t,d,cond1,cond2,cond3,x,trabajadores,insumo1,insumo2,insumo3):


        if(cond2):#si es el inicio de la jornada laboral se comienza a enlatar
          #se revisa que haya algo en la lista de agua   
            if(cond1):
            #se pasa la tarea de agua que este de primera a la lista de enlatar
                self.listaenlatar.append({'TIPO':'tanque0','HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':x,'DIA':d,'INSUMOS':0})  
            if(self.listaenlatar):
               #se ordena la lista de enlatar de forma creciente segun eL DI 
                self.organizar_lista_enlatar()
                #se saca la primera tarea a enlatar de la lista
                a=self.listaenlatar[0]
                self.listaenlatar.pop(0)
                aux=copy.deepcopy(a)
                aux['TAREA']['fecha_inicio']=(self.fecha_Referencia+timedelta(days=(d-1))).strftime("%m %d %Y")
                #saco la tarea de la lista a enlatar porque ya la voy a asignar   
                
                #como ya pase una tarea lista para enlatar al proceso de enlatar,lo guardo en el registro y libero el recurso
                if(a['TIPO']=='tanque0'):
                    print('.')
                else:
                    var=a.copy()
                    var['TAREA']['fecha_finalizacion']=(self.fecha_Referencia+timedelta(days=(d-1))).strftime("%m %d %Y")
                    #se agrega al registro el uso del tanque para la tarea en especifico
                    self.listatotal.append(var)
                   
                    #se busca en la lista de tanques cual es el que se libero y se limpia el recurso
                    cont=0
                    for tanque in self.tanques:
                        if(a['TIPO']==tanque['TIPO']):
                            self.tanques[cont]={'TIPO':a['TIPO'],'HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':{},'DIA':0,'INSUMOS':0}
                            if(self.estadot=='no disponible'):
                                self.estadot='disponible'
                        cont=cont+1
                #se asignan los recursos par enlatar la tarea 
                aux=aux['TAREA']
                self.listadedatos1=[
                {'TIPO':'mezclado','HINICIO':8,'HORAS':6,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][7],'TAREA':aux,'DIA':d,'INSUMOS':insumo1},
                {'TIPO':'carbonatado','HINICIO':10,'HORAS':6,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][8],'TAREA':aux,'DIA':d,'INSUMOS':insumo2},
                {'TIPO':'enlatado','HINICIO':12,'HORAS':4,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][9],'TAREA':aux,'DIA':d,'INSUMOS':insumo3},
                {'TIPO':'embarque','HINICIO':16,'HORAS':2,'COSTO':0.5,'EMPLEADO':trabajadores['horario empleados'][10],'TAREA':aux,'DIA':d,'INSUMOS':0}]
        if(cond3): # fin de la jornada laboral, se limpian los recursos
            self.listadedatos1=self.poner_fecha_salida(self.listadedatos1,d)
            #guardo el registro de uso de los recursos
            self.agregar_al_registro(self.listadedatos1)
            #agrego la tarea terminada a la lista de tareas terminadas
            self.listater.append(self.listadedatos1[0]['TAREA'])
            #se pone disponible de nuevo el tanque de almacenamiento que contenia la tarea
            #reseteo los recursos
            self.listadedatos1=[
            {'TIPO':'mezclado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'8','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
            {'TIPO':'carbonatado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'9','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
            {'TIPO':'enlatado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'10','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
            {'TIPO':'embarque','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'11','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0}]


#calcula el costo de produccion del sector operaciones
class funcion_De_costo:
    def __init__(self):
        self.funcion={}
    def actualizar_Datos(self):
        print(1)
    def calcular_Funcion(self):
        print(1)
#actualiza el tiempo de la simulacion en horas
class update:
    def __init__(self):
        self.tiempo=0
        self.dias=0
    def incrementar(self):
        self.tiempo=self.tiempo+1
    def calcular_dias(self):
        if(self.tiempo%24==0):
            self.dias =self.dias+1
            self.tiempo=0

def separar_las_actividades(a):

    lista_de_equipos=[
        {'TIPO':'Desembarque','Actividad':[]},{'TIPO':'Pesado','Actividad':[]},{'TIPO':'Lavado','Actividad':[]},
        {'TIPO':'Pelado','Actividad':[]},{'TIPO':'Molienda','Actividad':[]},{'TIPO':'Centrifuga','Actividad':[]},
        {'TIPO':'UHT','Actividad':[]},{'TIPO':'Tanque1','Actividad':[]},{'TIPO':'Tanque2','Actividad':[]},
        {'TIPO':'Tanque3','Actividad':[]},{'TIPO':'Tanque4','Actividad':[]},{'TIPO':'Mezclado','Actividad':[]},
        {'TIPO':'Carbonatado','Actividad':[]},{'TIPO':'Enlatado','Actividad':[]},{'TIPO':'Embarque','Actividad':[]}
        ]
            #recorro la lista de tareas efectuadas y se asignan a una estructura que separa las actividades por etapa
    for tareas in a:

        if(tareas['TIPO']=='desembarque'):
            lista_de_equipos[0]['Actividad'].append(tareas)
        if(tareas['TIPO']=='pesado'):
            lista_de_equipos[1]['Actividad'].append(tareas)
        if(tareas['TIPO']=='lavado'):
            lista_de_equipos[2]['Actividad'].append(tareas)
        if(tareas['TIPO']=='pelado'):
            lista_de_equipos[3]['Actividad'].append(tareas)
        if(tareas['TIPO']=='molienda'):
            lista_de_equipos[4]['Actividad'].append(tareas)
        if(tareas['TIPO']=='centrifuga'):
            lista_de_equipos[5]['Actividad'].append(tareas)
        if(tareas['TIPO']=='UHT'):
            lista_de_equipos[6]['Actividad'].append(tareas)
        if(tareas['TIPO']=='tanque1'):
            lista_de_equipos[7]['Actividad'].append(tareas)
        if(tareas['TIPO']=='tanque2'):
            lista_de_equipos[8]['Actividad'].append(tareas)
        if(tareas['TIPO']=='tanque3'):
            lista_de_equipos[9]['Actividad'].append(tareas)
        if(tareas['TIPO']=='tanque4'):
            lista_de_equipos[10]['Actividad'].append(tareas)
        if(tareas['TIPO']=='mezclado'):
            lista_de_equipos[11]['Actividad'].append(tareas)
        if(tareas['TIPO']=='carbonatado'):
            lista_de_equipos[12]['Actividad'].append(tareas)
        if(tareas['TIPO']=='enlatado'):
            lista_de_equipos[13]['Actividad'].append(tareas)
        if(tareas['TIPO']=='embarque'):
            lista_de_equipos[14]['Actividad'].append(tareas)
    return lista_de_equipos


class Planificador():

    def __init__(self):
        super().__init__()
        self.lista_de_tareas={}
        self.lista_de_mantenimiento={}
        self.lista_de_materiales={}
        self.cargar_datos_iniciales()
        #etapa de transformacion del jugo
        self.dayzero=datetime.now()
        self.day_of_the_week=datetime.now()  
        self.transformacion=proceso() 
        self.day=0
        self.hour=0
        self.fecha=0
        self.tareas=self.lista_de_tareas
        self.jugo=[]
        self.vino=[]
        self.agua=[]
        #self.separar_por_tipos()
        self.RH=rh.horarios()
        self.trabajadores=0
        self.productof=len(self.transformacion.listater)
        self.registro_viajes=[]
        self.almacen=alm.almacen()
        self.producto_almacenado=[]
        self.tipos_insumos=['8-st','8-sl','12-st','12-sl','16-st','quimico 0','quimico 1','quimico 2','quimico 3','quimico 4']

    def cargar_datos_iniciales(self):
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'
        '''
        name_of_file = 'data'
        completeName = os.path.join(save_path, name_of_file+".txt") 
        with open(completeName) as json_file:
            clientes = json.load(json_file)
        self.lista_de_tareas=clientes
        '''
        name_of_file = 'datam'
        completeName = os.path.join(save_path, name_of_file+".txt") 
        with open(completeName) as json_file:
            mantenimiento = json.load(json_file)
        self.lista_de_mantenimiento=mantenimiento

        name_of_file = 'data_S'
        completeName = os.path.join(save_path, name_of_file+".txt") 
        with open(completeName) as json_file:
            materiales = json.load(json_file)
        self.lista_de_materiales=materiales

    def revisar_dia(self,d):
        dias=timedelta(days=d-1)
        a=self.dayzero+dias
        return a.weekday()
                
    def revisar_mantenimiento(self,d):
        resultado=[True,True,True]
        dias=timedelta(days=d-1)
        a=self.dayzero+dias
        tipo1=['desembarque','banda transportadora','lavado','pelado','molienda','centrifuga','uht']
        tipo2=['tanque1','tanque2','tanque3','tanque4']
        tipo3=['tanque mecanico','tanque carbonatacion','enlatadora','embarque']
        for x in self.lista_de_mantenimiento['preventivo']:
            b=datetime.strptime(x['fecha planificada'],'%m %d %Y')
            if((a-b).days == 0):
                for i in tipo1:
                    if(x['objeto'] == i):
                        resultado[0]=False
                for i in tipo2:
                    if(x['objeto'] == i):
                        resultado[1]=False
                for i in tipo3:
                    if(x['objeto'] == i):
                        resultado[2]=False
        return resultado

    def revisar_las_listas(self):
        #se revisa si las listas de tareas de cada producto estan vacias
        if(self.jugo):
          j=False
        else:
          j=True
        if(self.vino):
          v=False
        else:
          v=True
        if(self.agua):
          a=False
        else:
          a=True
        return (j,v,a)            

    def separar_por_tipos(self):

        for val in self.lista_de_tareas['pedidos']:
            tipo=val['tipo'].split()
            if(tipo[0]=='vino'):
                for x in range(val['cantidad']):
                    k=val.copy()
                    k['cantidad']=1
                    self.vino.append(k)
                #print('v')
            if(tipo[0]=='agua'):
                for x in range(val['cantidad']):
                    k=val.copy()
                    k['cantidad']=1
                    self.agua.append(k)
                #print('a')
            if(tipo[0]=='banano' or tipo[0]=='guanabana'):
                for x in range(val['cantidad']):
                    k=val.copy()
                    k['cantidad']=1
                    self.jugo.append(k)
                #print('j')

    def revisar_los_tanques(self):

        B=False
        if(self.transformacion.tanques[0]['ESTADO']=='disponible'):
            B=True
        elif(self.transformacion.tanques[1]['ESTADO']=='disponible'):
            B=True
        elif(self.transformacion.tanques[2]['ESTADO']=='disponible'):
            B=True
        elif(self.transformacion.tanques[3]['ESTADO']=='disponible'):
            B=True
        return B

    def pedir_horario_a_RH(self,d):

        nombre='horario' + str(d)
        #self.RH.asignar_horario(nombre)

        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = nombre

        completeName = os.path.join(save_path, name_of_file+".txt") 

        with open(completeName) as json_file:
            data = json.load(json_file)

        cont=0
        for x in data['horario empleados']:
            if(x['estado']=='incapacidad'):
                data[cont]={"id": -1, "nombre y apellido": "sustituto" + str(cont), "email": "------@gmail.com", 
                "telefono": 000000000, "empresa": "Punta Delicia", "cargo": "operario", "departamento": x['departamento'],
                 "estacion de trabajo": x['estacion de trabajo'], "salario": x['salario']*1.1, "horas_extra": 25, 
                 "hinicio": 8, "hsalida": 18, "estado": "sustituyendo"}
            cont+=1
        self.trabajadores=data

    def asignar_proceso_transformar(self,t,d):

        # primero se revisa si la lista de jugo tiene algo adentro
        f=self.revisar_las_listas()

        c=self.revisar_los_tanques()

        w=self.revisar_dia(d)

        y=self.revisar_mantenimiento(d)
        
        condicion1=(t==8 and f[0]==False and c and w != 6 and (y[0] and y[1]))

        condicion2=(t==13 and self.transformacion.listadedatos[0]['HORAS'] !=0)

        a=''
        insumo1=''
        insumo2=''
        insumo3=''

        if(condicion1):
            insumo1=self.almacen.asignar_recurso_quimico('quimico 0',1)
            insumo2=self.almacen.asignar_recurso_quimico('quimico 1',1)
            a=self.jugo[0]
            a['fecha_inicio']=(self.dayzero+timedelta(days=(d-1))).strftime("%m %d %Y")

        if(condicion2):
            insumo1=self.almacen.asignar_recurso_quimico('quimico 2',1)
            self.jugo.pop(0)

        self.transformacion.calcular_procesos_jugo(t,d,condicion1,condicion2,a,self.trabajadores,insumo1,insumo2,insumo3)

    def asignar_proceso_almacenar(self,t,d):


        f=self.revisar_las_listas()

        c=self.revisar_los_tanques()

        w=self.revisar_dia(d)

        y=self.revisar_mantenimiento(d)

        a=''
        insumo=''
        condicion1=(t==8 and f[1] == False and c and w != 6 and y[1])

        if(condicion1):
            insumo=self.almacen.asignar_recurso_quimico('quimico 2',1)
            a=self.vino[0] 
            a['fecha_inicio']=(self.dayzero+timedelta(days=(d-1))).strftime("%m %d %Y")
            self.vino.pop(0)
        self.transformacion.calcular_procesos_tanques(t,d,condicion1,a,insumo)
 
    def asignar_proceso_enlatar(self,t,d):

        f=self.revisar_las_listas()

        a=''

        w=self.revisar_dia(d)

        y=self.revisar_mantenimiento(d)

        condicion1=(f[2] == False)

        condicion2=(t==8 and w != 6 and y[2])

        condicion3=(t==18 and self.transformacion.listadedatos1[0]['HORAS'] != 0)

        insumo1=''
        insumo2=''
        lata=''

        if(condicion1 and condicion2):
            #se saca la tarea de agua de la lista de tareas de agua
            a=self.agua[0] 
            a['fecha_inicio']=(self.dayzero+timedelta(days=(d-1))).strftime("%m %d %Y")
            self.agua.pop(0)
            tipo=a['tipo'].split()
            tipo=tipo[1]
            insumo1=self.almacen.asignar_recurso_quimico('quimico 3',1)
            insumo2=self.almacen.asignar_recurso_quimico('quimico 4',1)
            lata=self.almacen.asignar_recurso_lata(tipo,8)
            

        self.transformacion.proceso_enlatar(t,d,condicion1,condicion2,condicion3,a,self.trabajadores,insumo1,insumo2,lata)

    def entrega_producto_final(self,d):

        fecha_actual=self.dayzero+timedelta(days=d-1)
        unidad_basica={'8-st':10839,'8-sl':8283,'12-st':11436,'12-sl':9314,'16-st':12170}

        h=len(self.transformacion.listater)
        if( h != self.productof):
            self.productof=h
            tarean=self.transformacion.listater[-1]
            # almacenar o entregar
            c=fecha_actual-datetime.strptime(tarean['fecha_limite'],'%m %d %Y')
            if(c.days >= 0): # se entrega porque significa que la fecha actual es mayor que la limite
                tipo=tarean['tipo'].split()
                tipo=tipo[1]
                viajen=tr.viajes(h,tarean['contratista'],20,'empresa',tarean['nombre'],'descripción',tarean['cantidad'],unidad_basica[tipo],fecha_actual.strftime("%m %d %Y"),'lata '+tipo)
                viajen.asignar_vehiculos()
                self.registro_viajes.append(viajen)
            else: # si da negativo es porque la fecha limite es mayor y se esta a tiempo, se almacena en tal caso 
                tipo=tarean['tipo'].split()
                tipo=tipo[1]
                self.almacen.almacenar_producto_terminado(tarean['nombre'],tipo,tarean['cantidad']*8,fecha_actual.strftime("%m %d %Y"))
                self.producto_almacenado.append(tarean)
        k=0
        for i in self.producto_almacenado:
            c=fecha_actual-datetime.strptime(i['fecha_limite'],'%m %d %Y')
            if(c.days==0):
                tipo=i['tipo'].split()
                tipo=tipo[1]
                numpalets=self.buscar_hoja_ingreso(i['nombre'])
                self.almacen.entregar_producto(numpalets)
                viajen=tr.viajes(h,i['contratista'],20,'empresa',i['nombre'],'descripción',i['cantidad'],unidad_basica[tipo],fecha_actual.strftime("%m %d %Y"),'lata '+tipo)
                viajen.asignar_vehiculos()
                self.registro_viajes.append(viajen)

    def buscar_hoja_ingreso(self,nombre):

        for i in self.almacen.ingresos:
            if(i.nombre==nombre):
                return i.n_palet

    def pedir_insumos(self,lista,fecha):
        cantidad=0
        cont=0
        for i in lista:
            if(i<=0.25):
                cantidad=10*(1-i)
                self.almacen.ingreso_De_insumos(self.tipos_insumos[cont],cantidad,fecha.strftime("%m %d %Y"))
            cont+=1

    def ejecutar_proceso(self):
            
         
        tiempo=update()   

        totaltareas=len(self.jugo)+len(self.vino)+len(self.agua)

        tareasterminadas=0

        while(totaltareas != tareasterminadas):
            self.fecha=self.dayzero+timedelta(days=(tiempo.dias-1))
            if(tiempo.tiempo==8):
                self.pedir_horario_a_RH(tiempo.dias)
            self.asignar_proceso_transformar(tiempo.tiempo,tiempo.dias)
            self.asignar_proceso_almacenar(tiempo.tiempo,tiempo.dias)
            self.asignar_proceso_enlatar(tiempo.tiempo,tiempo.dias)
            #pedir transporte o almacenamiento del producto terminado
            if(tiempo.tiempo==18):
                self.entrega_producto_final(tiempo.dias)
                m=self.almacen.revisar_Stock()
                self.pedir_insumos(m,self.fecha)
            tareasterminadas=len(self.registro_viajes)
            #si el tiempo igual a 18 revisar el stock
            tiempo.calcular_dias()
            tiempo.incrementar()
            
        print('hola')

'''
if __name__ == '__main__':


    schedule=Planificador()
    schedule.ejecutar_proceso()
    actividades_por_equipo=separar_las_actividades(schedule.transformacion.listatotal) 
    diagrama=tablero.gantt_diagram(schedule.dayzero,datetime.strptime(schedule.transformacion.listatotal[-1]['TAREA']['fecha finalizacion'],'%m %d %Y'))
    diagrama.cargar_datos(actividades_por_equipo)
    diagrama.graficar()
    print(schedule.dayzero.weekday())

    #gantt=gantt_diagram()

    #gantt.cargar_datos(actividades_por_equipo)

    #print(actividades_por_equipo[11])
    #print(len(gantt.startDate))
    #print(len(gantt.endDate))
    #print(len(gantt.taskno))
    #gantt.graficar()
   
'''   