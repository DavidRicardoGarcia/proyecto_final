import json
import os.path
import copy
from datetime import timedelta,datetime,date
from elementos_modelo import recursos_humanos as rh
from elementos_modelo import transporte as tr
from elementos_modelo import almacen as alm
import Agenda as ag
import itertools
import graficar as tablero
from elementos_modelo import recursos_humanos as rh
from elementos_modelo import transporte as tr
from elementos_modelo import almacen as alm

agenda_hist=ag.agenda()

    
class planificador:
    def __init__(self):
        super().__init__()
        self.book=[]
        self.lista=[]
        self.lista_asignar=[]
        self.cargar_datos_iniciales()
        #self.separar_por_cantidad()
        self.fecha=datetime(2021,5,14)
        self.rh=rh.horarios()
        self.tipos_insumos=['8-st','8-sl','12-st','12-sl','16-st','quimico 0','quimico 1','quimico 2','quimico 3','quimico 4']
        self.almacen=alm.almacen()
        self.lista_planificados=[]
        self.pedidos=[]
        self.lista_asignar=[]
    def cargar_datos_iniciales(self):
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'
        #tiempos de cada elemento y de viajes
        name_of_file = 'modelsettings'
        completeName = os.path.join(save_path, name_of_file+".json") 
        with open(completeName) as json_file:
            self.settings = json.load(json_file)
        #dias de mtto
        name_of_file = 'datam'
        completeName = os.path.join(save_path, name_of_file+".json") 
        with open(completeName) as json_file:
            self.mantenimiento = json.load(json_file)

        name_of_file = 'data_S'
        completeName = os.path.join(save_path, name_of_file+".json") 
        with open(completeName) as json_file:
            self.materiales = json.load(json_file)
        #las tareas
        # name_of_file = 'data'
        # completeName = os.path.join(save_path, name_of_file+".txt") 
        # with open(completeName) as json_file:
        #     self.pedidos = json.load(json_file)
        #pedidos
        name_of_file = 'book_pedidos'
        completeName = os.path.join(save_path, name_of_file+".json") 
        with open(completeName) as json_file:
            pedidos = json.load(json_file)
        #diao=datetime.strptime(pedidos['calendario'][0]['fecha'],'%m %d %Y')
        #diaf=datetime.strptime(pedidos['calendario'][-1]['fecha'],'%m %d %Y')
        #self.book.crear_AgendaP(diao,diaf)
        #self.Poriginal=copy.deepcopy(self.book.bookP)
        self.p=pedidos
        #self.book.cargarP(pedidos['calendario'])
        #recursos
        name_of_file = 'book_recursos'
        completeName = os.path.join(save_path, name_of_file+".json") 
        with open(completeName) as json_file:
            recursos = json.load(json_file)
        #diao=datetime.strptime(recursos['calendario'][0]['fecha'],'%m %d %Y')
        #diaf=datetime.strptime(recursos['calendario'][-1]['fecha'],'%m %d %Y')
        #self.book.crear_AgendaR(diao,diaf)
        #self.Roriginal=copy.deepcopy(self.book.bookR)
        self.r=recursos
        #self.book.cargarR(recursos['calendario'])
    def resetear(self):
        del(self.book)
        diao=datetime.strptime(self.r['calendario'][0]['fecha'],'%m %d %Y')
        diaf=datetime.strptime(self.r['calendario'][-1]['fecha'],'%m %d %Y')
        pedidos=copy.deepcopy(self.p)
        recursos=copy.deepcopy(self.r)
        
        libro=ag.agenda()
        libro.crear_AgendaR(diao,diaf)
        libro.crear_AgendaP(diao,diaf)
        #si se quiere resetear el libro se comentan las lineas de abajo
        libro.cargarP(pedidos['calendario'])
        libro.cargarR(recursos['calendario'])
        self.book=libro
    def separar_por_cantidad(self):
        
        self.lista=self.buscar_pedidos_en_camino(self.book.bookP)
        elmax=0
        self.cont=0
        if(self.lista):
            elmax=max(self.lista, key=lambda x:x['ident'])
            self.cont=elmax['ident']+1
        
        for val in self.pedidos['pedidos']:
            for x in range(val['cantidad']):
                k=val.copy()
                k['cantidad']=1
                k['ident']=self.cont
                self.lista_asignar.append(k)
                self.cont+=1
        self.lista_asignar_fija=copy.deepcopy(self.lista_asignar)
        
    def separar_por_tipos(self):

        for val in self.pedidos['pedidos']:
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
    def pedir_horario_a_RH(self,d):

        data=self.rh.asignar_horario_ng()

        self.cont=0
        for x in data['horario empleados']:
            if(x['estado']=='incapacidad'):
                data[self.cont]={"id": -1, "nombre y apellido": "sustituto" + str(self.cont), "email": "------@gmail.com", 
                "telefono": 000000000, "empresa": "Punta Delicia", "cargo": "operario", "departamento": x['departamento'],
                 "estacion de trabajo": x['estacion'], "salario": x['salario']*1.1, "horas_extra": 25, 
                 "hinicio": 8, "hsalida": 18, "estado": "sustituyendo"}
            self.cont+=1
        self.trabajadores=data
    def revisar_dia(self,d):

        a=d
        return a.weekday()       
    def revisar_mantenimiento(self,d):
        resultado=[True,True,True]

        a=d
        tipo1=['desembarque','banda transportadora','lavado','pelado','molienda','centrifuga','uht']
        tipo2=['tanque1','tanque2','tanque3','tanque4']
        tipo3=['tanque mecanico','tanque carbonatacion','enlatadora','embarque']
        for x in self.mantenimiento['preventivo']:
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
    def buscar_pedidos_en_camino(self,bookp):
        lista_De_pedidos=[]
        for i in bookp:
            if (i.pedidos_insumos !=[]):
                for x in i.pedidos_insumos:
                    lista_De_pedidos.append(x)
        return lista_De_pedidos
    def asignar_transformar(self,fecha,tarea):
        tipo=tarea['tipo'].split()
        for i in self.book.bookR:
            if((fecha-i.fecha).days == 0):
                        tarea=copy.deepcopy(tarea)
                        tarea['fecha_inicio']=fecha.strftime("%m %d %Y")
                        i.recursoA=[
        {'TIPO':'desembarque','HINICIO':self.settings['tareas'][tipo[0]]['inicio']['desembarque'],'HORAS':self.settings['tareas'][tipo[0]]['duracion']['desembarque'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0},
        {'TIPO':'pesado','HINICIO':self.settings['tareas'][tipo[0]]['inicio']['pesado'],'HORAS':self.settings['tareas'][tipo[0]]['duracion']['desembarque'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0},
        {'TIPO':'lavado','HINICIO':self.settings['tareas'][tipo[0]]['inicio']['lavado'],'HORAS':self.settings['tareas'][tipo[0]]['duracion']['desembarque'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0},
        {'TIPO':'pelado','HINICIO':self.settings['tareas'][tipo[0]]['inicio']['pelado'],'HORAS':self.settings['tareas'][tipo[0]]['duracion']['desembarque'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0},
        {'TIPO':'molienda','HINICIO':self.settings['tareas'][tipo[0]]['inicio']['molienda'],'HORAS':self.settings['tareas'][tipo[0]]['duracion']['desembarque'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0},
        {'TIPO':'centrifuga','HINICIO':self.settings['tareas'][tipo[0]]['inicio']['centrifuga'],'HORAS':self.settings['tareas'][tipo[0]]['duracion']['desembarque'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0},
        {'TIPO':'UHT','HINICIO':self.settings['tareas'][tipo[0]]['inicio']['UHT'],'HORAS':self.settings['tareas'][tipo[0]]['duracion']['desembarque'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0}] 
    def asignar_tanque(self,fecha,tarea):
        diasocupacion=[]
        tipo=tarea['tipo'].split()
        # d=copy.deepcopy(fecha)
        # for i in range(self.settings['tareas'][tipo]['Tprocesamiento']):
        #     diasocupacion.append(d)
        #     d=d+timedelta(days=1)}
        cantidaddias=self.settings['tareas'][tipo[0]]['Tprocesamiento']+1
        
        self.cont=0
        for i in self.book.bookR:
            if((fecha-i.fecha).days == 0):
                if(i.recursoB1['ESTADO']=='disponible'):
                    tarea=copy.deepcopy(tarea)
                    tarea['fecha_inicio']=fecha.strftime("%m %d %Y")
                    for j in range(cantidaddias):
                        self.book.bookR[self.cont+j].recursoB1={'TIPO':'tanque1','HINICIO':8,'HORAS':16,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                    
                    break
                elif(i.recursoB2['ESTADO']=='disponible'):
                    tarea=copy.deepcopy(tarea)
                    tarea['fecha_inicio']=fecha.strftime("%m %d %Y")
                    for j in range(cantidaddias):
                        self.book.bookR[self.cont+j].recursoB2={'TIPO':'tanque2','HINICIO':8,'HORAS':16,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                    
                    break
                elif(i.recursoB3['ESTADO']=='disponible'):
                    tarea=copy.deepcopy(tarea)
                    tarea['fecha_inicio']=fecha.strftime("%m %d %Y")
                    for j in range(cantidaddias):
                        self.book.bookR[self.cont+j].recursoB3={'TIPO':'tanque3','HINICIO':8,'HORAS':16,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                    
                    break
                else:
                    tarea=copy.deepcopy(tarea)
                    tarea['fecha_inicio']=fecha.strftime("%m %d %Y")
                    for j in range(cantidaddias):
                        self.book.bookR[self.cont+j].recursoB4={'TIPO':'tanque4','HINICIO':8,'HORAS':16,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                    
                    break
            self.cont+=1
    def asignar_enlatar(self,fecha,tarea):
        tipo=tarea['tipo'].split()
        for i in self.book.bookR:
            if((fecha-i.fecha).days == 0):
                        tarea=copy.deepcopy(tarea)
                        tarea['fecha_inicio']=fecha.strftime("%m %d %Y")
                        i.recursoC=[
        {'TIPO':'mezclado','HINICIO':self.settings['latas'][tipo[1]]['inicio'],'HORAS':self.settings['latas'][tipo[1]]['duracion'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0},
        {'TIPO':'carbonatado','HINICIO':self.settings['latas'][tipo[1]]['inicio'],'HORAS':self.settings['latas'][tipo[1]]['duracion'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0},
        {'TIPO':'enlatado','HINICIO':self.settings['latas'][tipo[1]]['inicio'],'HORAS':self.settings['latas'][tipo[1]]['duracion'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0},
        {'TIPO':'embarque','HINICIO':self.settings['latas'][tipo[1]]['inicio'],'HORAS':self.settings['latas'][tipo[1]]['duracion'],'COSTO':0.5,'EMPLEADO':0,'TAREA':tarea,'DIA':fecha.strftime("%m %d %Y"),'INSUMOS':0}]
    def asignar_pedido(self,fecha,tarea):
        tipo=tarea['tipo'].split()
        for i in self.book.bookP:
            if((fecha-i.fecha).days == 0):
                        i.setPedido_insumo(tarea['id'],tarea['nombre'],tipo[0],1000,111,fecha.strftime("%m %d %Y"),'encamino',tarea['ident'])
    def asignar_ingreso(self,fecha,tarea):
        tipo=tarea['tipo'].split()
        for i in self.book.bookP:
            if((fecha-i.fecha).days == 0):
                        i.setIngreso_insumo(tarea['id'],tipo[0],1,1000)   
    def revisar_los_tanques(self,fecha,tipo):
        flag=True
        diasocupacion=self.settings['tareas'][tipo]['Tprocesamiento']
        d=copy.deepcopy(fecha)
        B=False
        self.cont=0
        for i in self.book.bookR:
            #busco la fecha
            if((fecha - i.fecha).days == 0):
                #a partir de esa fecha cuento n dias de acuerdo al tipo
                if(i.recursoB1['ESTADO']=='disponible'):
                    v=0
                    for j in range(diasocupacion):
                        if(self.book.bookR[self.cont+j].recursoB1['ESTADO']=='disponible'):
                            v+=1
                    if(v==diasocupacion):
                        
                        return True
                elif(i.recursoB2['ESTADO']=='disponible'):
                    v=0
                    for j in range(diasocupacion):
                        if(self.book.bookR[self.cont+j].recursoB2['ESTADO']=='disponible'):
                            v+=1
                    if(v==diasocupacion):
                        
                        return True
                elif(i.recursoB3['ESTADO']=='disponible'):
                    v=0
                    for j in range(diasocupacion):
                        if(self.book.bookR[self.cont+j].recursoB3['ESTADO']=='disponible'):
                            v+=1
                    if(v==diasocupacion):
                        
                        return True
                elif(i.recursoB4['ESTADO']=='disponible'):
                    v=0
                    for j in range(diasocupacion):
                        if(self.book.bookR[self.cont+j].recursoB4['ESTADO']=='disponible'):
                            v+=1
                    if(v==diasocupacion):
                        
                        return True
                return B
            self.cont+=1   
    def revisar_transformar(self,fecha):
        B=False
        for i in self.book.bookR:
            if((fecha-i.fecha).days == 0):
                if(i.recursoA[0]['HINICIO']==0):
                    B=True
                    return B
                else:
                    return B
    def revisar_enlatar(self,fecha):
        B=False
        for i in self.book.bookR:
            if((fecha-i.fecha).days == 0):
                if(i.recursoC[0]['HINICIO']==0):
                    B=True
                    return B
                else:
                    return B
    def condiciones(self,fecha,tipo):
        # primero se revisa halla algo en la lista
        if(tipo=='banano' or tipo=='guanabana'):

            #revisar el recurso en el book
            h=self.revisar_transformar(fecha)
            #revisar el recurso en el book
            c=self.revisar_los_tanques(fecha,tipo)

            w=self.revisar_dia(fecha)

            y=self.revisar_mantenimiento(fecha)
            
            condicion1=(h and c and w != 6 and (y[0] and y[1]))
            return condicion1
        if(tipo=='vino'):
            if(self.lista_asignar==[]):
                f=False
            else:
                f=True
            #revisar el recurso en el book
            c=self.revisar_los_tanques(fecha,tipo)

            w=self.revisar_dia(fecha)

            y=self.revisar_mantenimiento(fecha)
            
            condicion2=(f and c and w != 6 and y[1])
            return condicion2
    def condiciones_enlatar(self,fecha):

            f=self.revisar_enlatar(fecha)
            
            w=self.revisar_dia(fecha)

            y=self.revisar_mantenimiento(fecha)
            
            condicion3=(f and w != 6 and (y[2]))

            return condicion3
    def revisar_asignacion_enlatar(self,tarea,fecha):
        self.cont=0
        for i in self.book.bookR:
            if((fecha-i.fecha).days == 0):
                #corregir, poner que no haya obstaculo en el siguiente dia para asignar la tarea que perdio
                if(i.recursoC[0]['TAREA']['fecha_limite']<=tarea['fecha_limite']):
                    #no hacer nada
                    self.reservar_tanque(tarea,fecha)
                    return tarea
                else:
                    flag=False
                    nuevatarea=i.recursoC[0]['TAREA']
                    tipo=tarea['tipo'].split()
                    if(i.recursoB1['TAREA']!={}):
                        if(i.recursoB1['TAREA']['ident']==nuevatarea['ident']):
                            if(self.book.bookR[self.cont+1].recursoB1['ESTADO']=='disponible'):
                                flag=True
                                self.book.bookR[self.cont+1].recursoB1={'TIPO':'tanque1','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':nuevatarea,'DIA':0,'INSUMOS':0}
                    if(i.recursoB2['TAREA']!={}):
                        if(i.recursoB2['TAREA']['ident']==nuevatarea['ident']):
                            if(self.book.bookR[self.cont+1].recursoB2['ESTADO']=='disponible'):
                                flag=True
                                self.book.bookR[self.cont+1].recursoB2={'TIPO':'tanque2','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':nuevatarea,'DIA':0,'INSUMOS':0}
                    if(i.recursoB3['TAREA']!={}):
                        if(i.recursoB3['TAREA']['ident']==nuevatarea['ident']):
                            if(self.book.bookR[self.cont+1].recursoB3['ESTADO']=='disponible'):
                                flag=True
                                self.book.bookR[self.cont+1].recursoB3={'TIPO':'tanque3','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':nuevatarea,'DIA':0,'INSUMOS':0}
                    if(i.recursoB4['TAREA']!={}):
                        if(i.recursoB4['TAREA']['ident']==nuevatarea['ident']):
                            if(self.book.bookR[self.cont+1].recursoB4['ESTADO']=='disponible'):
                                flag=True
                                self.book.bookR[self.cont+1].recursoB4={'TIPO':'tanque4','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':nuevatarea,'DIA':0,'INSUMOS':0}


                    if(flag):     
                        #lata=self.almacen.asignar_recurso_lata(tipo,8)
                        #falta retornar las latas que no se usen de la asignacion anterior
                        for x in i.recursoC:
                            x['HINICIO']=self.settings['latas'][tipo[1]]['inicio']
                            x['HORAS']=self.settings['latas'][tipo[1]]['duracion']
                            x['TAREA']=tarea
                        return nuevatarea
                    else: 
                        if(i.recursoB1['TAREA']!={}):
                            if(i.recursoB1['TAREA']['ident']==tarea['ident']):
                                if(self.book.bookR[self.cont+1].recursoB1['ESTADO']=='disponible'):
                                    
                                    self.book.bookR[self.cont+1].recursoB1={'TIPO':'tanque1','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                        if(i.recursoB2['TAREA']!={}):
                            if(i.recursoB2['TAREA']['ident']==tarea['ident']):
                                if(self.book.bookR[self.cont+1].recursoB2['ESTADO']=='disponible'):
                                    
                                    self.book.bookR[self.cont+1].recursoB2={'TIPO':'tanque2','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                        
                        if(i.recursoB3['TAREA']!={}):
                            if(i.recursoB3['TAREA']['ident']==tarea['ident']):
                                if(self.book.bookR[self.cont+1].recursoB3['ESTADO']=='disponible'):
                                    
                                    self.book.bookR[self.cont+1].recursoB3={'TIPO':'tanque3','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                        
                        if(i.recursoB4['TAREA']!={}):
                            if(i.recursoB4['TAREA']['ident']==tarea['ident']):
                                if(self.book.bookR[self.cont+1].recursoB4['ESTADO']=='disponible'):
                                    
                                    self.book.bookR[self.cont+1].recursoB4={'TIPO':'tanque4','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                            
                        return tarea
            self.cont+=1
        
    def reservar_tanque(self,tarea,fecha):
        self.cont=0
        for i in self.book.bookR:
            if((fecha-i.fecha).days == 0):
                if(i.recursoB1['TAREA']!={}):
                    if(i.recursoB1['TAREA']['ident']==tarea['ident']):
                        
                            self.book.bookR[self.cont+1].recursoB1={'TIPO':'tanque1','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                
                if(i.recursoB2['TAREA']!={}):
                    if(i.recursoB2['TAREA']['ident']==tarea['ident']):
                        
                            self.book.bookR[self.cont+1].recursoB2={'TIPO':'tanque2','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                
                if(i.recursoB3['TAREA']!={}):
                    if(i.recursoB3['TAREA']['ident']==tarea['ident']):
                        
                            self.book.bookR[self.cont+1].recursoB3={'TIPO':'tanque3','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
                
                if(i.recursoB4['TAREA']!={}):
                    if(i.recursoB4['TAREA']['ident']==tarea['ident']):
                    
                            self.book.bookR[self.cont+1].recursoB4={'TIPO':'tanque4','HINICIO':8,'HORAS':24,'COSTO':0.5,'ESTADO':'ocupado','TAREA':tarea,'DIA':0,'INSUMOS':0}
            self.cont=self.cont+1
        
    def asignacion(self,save=False):
        #self.book.bookP=[]
        #self.book.bookR=[]
        #self.book.bookP=copy.deepcopy(self.Poriginal)
        #self.book.bookR=copy.deepcopy(self.Roriginal)
        #buscar pedidos en camino
        
        lista=self.lista
        #reasignar segun el orden de la lista a asignar y los pedidos en camino
        flag=False
        self.cont=0
        for x in lista:
            self.cont=0
            lista_actividades=[]
            for j in self.lista_asignar:
                tipo=j['tipo'].split()
                tipo=tipo[0]
                if(x['tipo'] == tipo):
                    
                    id=x['id']
                    ident=x['ident']
                    for p in self.book.bookR:
                        if(p.recursoA[0]['TAREA'] != {} ):
                            if(p.recursoA[0]['TAREA']['id']==id and p.recursoA[0]['TAREA']['ident']==ident):
                                tarea=copy.deepcopy(j)
                                tarea['fecha_inicio']=p.fecha.strftime("%m %d %Y")
                                p.recursoA[0]['TAREA']=tarea
                                p.recursoA[1]['TAREA']=tarea
                                p.recursoA[2]['TAREA']=tarea
                                p.recursoA[3]['TAREA']=tarea
                                p.recursoA[4]['TAREA']=tarea
                                p.recursoA[5]['TAREA']=tarea
                                p.recursoA[6]['TAREA']=tarea
                                lista_actividades.append(copy.deepcopy(p))
                                #print(p.fecha)

                        if(p.recursoB1['TAREA'] != {} ):
                            if(p.recursoB1['TAREA']['id']==id and p.recursoB1['TAREA']['ident']==ident):
                                tarea=copy.deepcopy(j)
                                tarea['fecha_inicio']=p.fecha.strftime("%m %d %Y")
                                p.recursoB1['TAREA']=tarea
                                lista_actividades.append(copy.deepcopy(p))
                                #print(p.fecha)

                        if(p.recursoB2['TAREA'] != {} ):
                            if(p.recursoB2['TAREA']['id']==id and p.recursoB2['TAREA']['ident']==ident):
                                tarea=copy.deepcopy(j)
                                tarea['fecha_inicio']=p.fecha.strftime("%m %d %Y")
                                p.recursoB2['TAREA']=tarea
                                lista_actividades.append(copy.deepcopy(p))
                                #print(p.fecha)
                            
                        if(p.recursoB3['TAREA'] != {} ):
                            if(p.recursoB3['TAREA']['id']==id and p.recursoB3['TAREA']['ident']==ident):
                                tarea=copy.deepcopy(j)
                                tarea['fecha_inicio']=p.fecha.strftime("%m %d %Y")
                                p.recursoB3['TAREA']=tarea
                                lista_actividades.append(copy.deepcopy(p))
                                #print(p.fecha)

                        if(p.recursoB4['TAREA'] != {} ):
                            if(p.recursoB4['TAREA']['id']==id and p.recursoB4['TAREA']['ident']==ident):
                                tarea=copy.deepcopy(j)
                                tarea['fecha_inicio']=p.fecha.strftime("%m %d %Y")
                                p.recursoB4['TAREA']=tarea
                                lista_actividades.append(copy.deepcopy(p))
                                #print(p.fecha)

                        if(p.recursoC[0]['TAREA'] != {} ):
                            if(p.recursoC[0]['TAREA']['id']==id and p.recursoC[0]['TAREA']['ident']==ident):
                                tarea=copy.deepcopy(j)
                                tarea['fecha_inicio']=p.fecha.strftime("%m %d %Y")
                                p.recursoC[0]['TAREA']=tarea
                                p.recursoC[1]['TAREA']=tarea
                                p.recursoC[2]['TAREA']=tarea
                                p.recursoC[3]['TAREA']=tarea
                                lista_actividades.append(copy.deepcopy(p))
                                flag=True
                                break
                                #print(p.fecha)
                if(flag):
                    self.lista_asignar.pop(self.cont)
                    flag=False
                    tdefinitiva=lista_actividades[0].fecha
                    self.lista_planificados.append((j,tdefinitiva))
                    del(lista_actividades)
                    break        
                self.cont+=1
        

        #definir fecha inicial
        fecha_inicial=self.fecha
        
        #se asignan las tareas que faltan por asignar en orden
        for i in self.lista_asignar:
            #banderas para los ciclos while
            flagAB=True
            flagABC=True
            flagB=True
            flagC=True
            #tipo de tarea
            tipo=i['tipo'].split()
            tipo=tipo[0]
            #se elige la fecha tentativa empezando por la fecha actual
            tagendar=fecha_inicial+timedelta(days=(self.settings['tareas'][tipo]['Tinsumo']))
            #variable auxiliar para asignar la tarea de la lista
            tarea=copy.deepcopy(i)
            tdefinitivo=tagendar
            #se trata de asignar la tarea tipo A
            if(tipo=='banano' or tipo=='guanabana'):
                while(flagAB):
                    #se consulta en el libro si se puede
                    value=self.condiciones(tagendar,tipo)
                    if(value):
                        tdefinitivo=tagendar
                        flagAB=False
                        self.asignar_transformar(tagendar,tarea)

                        self.asignar_tanque(tagendar,tarea)
                        tenlatar=tagendar+timedelta(days=self.settings['tareas'][tipo]['Tprocesamiento'])
                        while(flagABC):
                            value=self.condiciones_enlatar(tenlatar)
                            d=self.revisar_dia(tenlatar)
                            m=self.revisar_mantenimiento(tenlatar)
                            if(value):
                                flagABC=False
                                self.asignar_enlatar(tenlatar,tarea)
                            elif(d != 6 and m[2]):
                                #en caso self.contrario se va a comparar la tarea que se quiere asignar con la que ya esta asignada y se va a decidir cual tiene prioridad
                                #debido a su deadline, la tarea que sale sigue intentando ser asignadaen algun momento
                                tarea=self.revisar_asignacion_enlatar(tarea,tenlatar)
                                tenlatar=tenlatar+timedelta(days=1)

                                #reservar nuevo dia de uso de tanque
                            else:
                                self.reservar_tanque(tarea,tenlatar)
                                tenlatar=tenlatar+timedelta(days=1)
                                
                                #reservar nuevo dia de uso de tanque
                                

                    else:
                        tagendar=tagendar+timedelta(days=1)
            if(tipo=='vino'):
                while(flagB):
                    value=self.condiciones(tagendar,tipo)
                    if(value):
                        tdefinitivo=tagendar
                        flagB=False
                        self.asignar_tanque(tagendar,tarea)
                        tenlatar=tagendar+timedelta(days=self.settings['tareas'][tipo]['Tprocesamiento'])
                        while(flagC):
                            value=self.condiciones_enlatar(tenlatar)
                            d=self.revisar_dia(tenlatar)
                            m=self.revisar_mantenimiento(tenlatar)
                            if(value):
                                flagC=False
                                self.asignar_enlatar(tenlatar,tarea)
                            elif(d != 6 and m[2]):
                                tarea=self.revisar_asignacion_enlatar(tarea,tenlatar)
                                tenlatar=tenlatar+timedelta(days=1)
                                #reservar nuevo dia de uso de tanque
                            else:
                                self.reservar_tanque(tarea,tenlatar)
                                tenlatar=tenlatar+timedelta(days=1)
                                
                                #reservar nuevo dia de uso de tanque
                    else:
                        tagendar=tagendar+timedelta(days=1)
                        #reservar nuevo dia de uso de tanque
            
            if(tipo=='agua'):
                while(flagC):
                    value=self.condiciones_enlatar(tagendar)
                    
                    if(value):
                        flagC=False
                        tdefinitivo=tagendar
                        self.asignar_enlatar(tagendar,tarea)
                    else:
                        #en caso self.contrario se va a comparar la tarea que se quiere asignar con la que ya esta asignada y se va a decidir cual tiene prioridad
                        #debido a su deadline, la tarea que sale sigue intentando ser asignadaen algun momento
                        #tarea=self.revisar_asignacion_enlatar(tarea,tagendar)
                        tagendar=tagendar+timedelta(days=1)
            self.lista_planificados.append((tarea,tdefinitivo))

            #agregar los insumos y los empleados 
        if(save):
            diao=datetime.strptime(self.r['calendario'][0]['fecha'],'%m %d %Y')
            diaf=datetime.strptime(self.r['calendario'][-1]['fecha'],'%m %d %Y')
            libro=ag.agenda()
            libro.crear_AgendaP(diao,diaf)
            self.book.bookP=libro.bookP
            #al final despues de haber asignado los recursos a las tareas ,se les pasan los insumos, trabajadores, ordenes de pedido y ordenes de ingreso
            for i in self.lista_planificados:
                tfecha=i[1]
                tipo=i[0]['tipo'].split()
                taux=timedelta(days=self.settings['tareas'][tipo[0]]['Tinsumo'])
                tpedido=tfecha-taux
                self.asignar_pedido(tpedido,i[0])
                self.asignar_ingreso(tfecha,i[0])
            self.book.guardarR()
            self.book.guardarP()
            #print('amonos')
        #print('amonos')           
    def Calcular_Costo(self,listapedidos):
        del(self.pedidos)
        del(self.lista_asignar)
        del(self.lista_planificados)
        self.lista_planificados=[]
        self.pedidos=[]
        self.lista_asignar=[]
        self.pedidos=listapedidos
        
        self.resetear()

        self.separar_por_cantidad()

        self.asignacion(False)
        lista=[]
        #print(self.pedidos['pedidos'])
        for i in self.pedidos['pedidos']:
            for p in self.book.bookR:
                if(p.recursoC[0]['TAREA']!= {}):
                    if(p.recursoC[0]['TAREA']['id']==i['id']):
                        lista.append((p.recursoC[0]['TAREA']['id'],p.fecha,p.recursoC[0]['TAREA']['tipo']))
        #print(lista)
        listadef=[]
        total=0
        for i in self.pedidos['pedidos']:
            max=self.fecha-timedelta(days=100)
            for x in lista:
                if(x[0]==i['id']):
                    if(max<x[1]):
                        max=x[1]
            dif=max-datetime.strptime(i['fecha_recepcion'],'%m %d %Y')
            if(dif.days < 0):
                dif=timedelta(days=0)
            pe=datetime.strptime(i['fecha_limite'],'%m %d %Y')
            if(pe<max):
                total+=10
                #print('se paso')
                #print(i['id'])
            listadef.append((i['id'],dif,i['fecha_limite'],i['fecha_recepcion']))
            total+=dif.days
        #print(listadef)
        return total
    def Asignar_insumos_personal(self,listapedidos):
            del(self.pedidos)
            del(self.lista_asignar)
            del(self.lista_planificados)
            self.lista_planificados=[]
            self.pedidos=[]
            self.lista_asignar=[]
            self.pedidos=listapedidos
            
            self.resetear()
            self.separar_por_cantidad()
            self.asignacion(True)
            #self.asignacion(False)

            # for j in self.lista_asignar_fija:
            #     tipot=j['tipo'].split()
            #     tipo=tipot[0]
            #     tipol=tipot[1]
            #     id=j['id']
            #     ident=j['ident']
            #     if(tipo=='banano' or tipo=='guanabana'):
            #         insumo1=self.almacen.asignar_recurso_quimico('quimico 0',1)
            #         insumo2=self.almacen.asignar_recurso_quimico('quimico 1',1)
            #         insumo3=self.almacen.asignar_recurso_quimico('quimico 2',1)
            #     if(tipo=='vino'):
            #         insumo3=self.almacen.asignar_recurso_quimico('quimico 2',1)
            #     insumoa=self.almacen.asignar_recurso_quimico('quimico 3',1)
            #     insumob=self.almacen.asignar_recurso_quimico('quimico 4',1)
            #     lata=self.almacen.asignar_recurso_lata(tipol,8)
            #     trabajadores=self.pedir_horario_a_RH()
            #     for p in self.book.bookR:
            #                 if(p.recursoA[0]['TAREA'] != {} ):
            #                     if(p.recursoA[0]['TAREA']['id']==id and p.recursoA[0]['TAREA']['ident']==ident):
            #                         p.recursoA[0]['INSUMOS']=0
            #                         p.recursoA[1]['INSUMOS']=0
            #                         p.recursoA[2]['INSUMOS']=insumo1
            #                         p.recursoA[3]['INSUMOS']=0
            #                         p.recursoA[4]['INSUMOS']=insumo2
            #                         p.recursoA[5]['INSUMOS']=0
            #                         p.recursoA[6]['INSUMOS']=0

            #                         p.recursoA[0]['EMPLEADO']=trabajadores['horario empleados'][0]
            #                         p.recursoA[1]['EMPLEADO']=trabajadores['horario empleados'][1]
            #                         p.recursoA[2]['EMPLEADO']=trabajadores['horario empleados'][2]
            #                         p.recursoA[3]['EMPLEADO']=trabajadores['horario empleados'][3]
            #                         p.recursoA[4]['EMPLEADO']=trabajadores['horario empleados'][4]
            #                         p.recursoA[5]['EMPLEADO']=trabajadores['horario empleados'][5]
            #                         p.recursoA[6]['EMPLEADO']=trabajadores['horario empleados'][6]
            #                         #print(p.fecha)

            #                 if(p.recursoB1['TAREA'] != {} ):
            #                     if(p.recursoB1['TAREA']['id']==id and p.recursoB1['TAREA']['ident']==ident):
            #                         p.recursoB1['INSUMOS']=insumo3
            #                         #print(p.fecha)

            #                 if(p.recursoB2['TAREA'] != {} ):
            #                     if(p.recursoB2['TAREA']['id']==id and p.recursoB2['TAREA']['ident']==ident):
            #                         p.recursoB2['INSUMOS']=insumo3
            #                         #print(p.fecha)
                                
            #                 if(p.recursoB3['TAREA'] != {} ):
            #                     if(p.recursoB3['TAREA']['id']==id and p.recursoB3['TAREA']['ident']==ident):
            #                         p.recursoB3['INSUMOS']=insumo3
            #                         #print(p.fecha)

            #                 if(p.recursoB4['TAREA'] != {} ):
            #                     if(p.recursoB4['TAREA']['id']==id and p.recursoB4['TAREA']['ident']==ident):
            #                         p.recursoB4['INSUMOS']=insumo3
            #                         #print(p.fecha)

            #                 if(p.recursoC[0]['TAREA'] != {} ):
            #                     if(p.recursoC[0]['TAREA']['id']==id and p.recursoC[0]['TAREA']['ident']==ident):
            #                         p.recursoC[0]['INSUMOS']=insumoa
            #                         p.recursoC[1]['INSUMOS']=insumob
            #                         p.recursoC[2]['INSUMOS']=lata
            #                         p.recursoC[3]['INSUMOS']=0

            #                         p.recursoC[0]['EMPLEADO']=trabajadores['horario empleados'][7]
            #                         p.recursoC[1]['EMPLEADO']=trabajadores['horario empleados'][8]
            #                         p.recursoC[2]['EMPLEADO']=trabajadores['horario empleados'][9]
            #                         p.recursoC[3]['EMPLEADO']=trabajadores['horario empleados'][10]
            #                         #print(p.fecha)
            #                         fecha=p.fecha
            #     m=self.almacen.revisar_Stock()
            #     self.pedir_insumos(m,fecha)               
    def pedir_horario_a_RH(self):

        data=self.rh.asignar_horario_ng()

        cont=0
        for x in data['horario empleados']:
            if(x['estado']=='incapacidad'):
                data[cont]={"id": -1, "nombre y apellido": "sustituto" + str(cont), "email": "------@gmail.com", 
                "telefono": 000000000, "empresa": "Punta Delicia", "cargo": "operario", "departamento": x['departamento'],
                 "estacion de trabajo": x['estacion'], "salario": x['salario']*1.1, "horas_extra": 25, 
                 "hinicio": 8, "hsalida": 18, "estado": "sustituyendo"}
            cont+=1
        return data
    def pedir_insumos(self,lista,fecha):
        cantidad=0
        cont=0
        for i in lista:
            if(i<=0.25):
                cantidad=10*(1-i)
                self.almacen.ingreso_De_insumos(self.tipos_insumos[cont],cantidad,fecha.strftime("%m %d %Y"))
            cont+=1
    def listar_todas_las_actividades(self):
        lista=[]
        for i in self.pedidos['pedidos']:
            
            for p in self.book.bookR:
                if(p.recursoA[0]['TAREA'] != {} ):
                    if(p.recursoA[0]['TAREA']['id']==i['id']):
                        lista.append((p.recursoA[0],p.fecha))
                        lista.append((p.recursoA[1],p.fecha))
                        lista.append((p.recursoA[2],p.fecha))
                        lista.append((p.recursoA[3],p.fecha))
                        lista.append((p.recursoA[4],p.fecha))
                        lista.append((p.recursoA[5],p.fecha))
                        lista.append((p.recursoA[6],p.fecha))
                        #print(p.fecha)

                if(p.recursoB1['TAREA'] != {} ):
                    if(p.recursoB1['TAREA']['id']==i['id']):
                        lista.append((p.recursoB1,p.fecha))
                        #print(p.fecha)

                if(p.recursoB2['TAREA'] != {} ):
                    if(p.recursoB2['TAREA']['id']==i['id']):
                        lista.append((p.recursoB2,p.fecha))
                        #print(p.fecha)
                    
                if(p.recursoB3['TAREA'] != {} ):
                    if(p.recursoB3['TAREA']['id']==i['id']):
                        lista.append((p.recursoB3,p.fecha))
                        #print(p.fecha)

                if(p.recursoB4['TAREA'] != {} ):
                    if(p.recursoB4['TAREA']['id']==i['id']):
                        lista.append((p.recursoB4,p.fecha))
                        #print(p.fecha)

                if(p.recursoC[0]['TAREA'] != {} ):
                    if(p.recursoC[0]['TAREA']['id']==i['id']):
                        lista.append((p.recursoC[0],p.fecha))
                        lista.append((p.recursoC[1],p.fecha))
                        lista.append((p.recursoC[2],p.fecha))
                        lista.append((p.recursoC[3],p.fecha))
        return lista

def separar_las_actividades(a,pedidos):

    lista_de_equipos=[
        {'TIPO':'Desembarque','Actividad':[]},{'TIPO':'Pesado','Actividad':[]},{'TIPO':'Lavado','Actividad':[]},
        {'TIPO':'Pelado','Actividad':[]},{'TIPO':'Molienda','Actividad':[]},{'TIPO':'Centrifuga','Actividad':[]},
        {'TIPO':'UHT','Actividad':[]},{'TIPO':'Tanque1','Actividad':[]},{'TIPO':'Tanque2','Actividad':[]},
        {'TIPO':'Tanque3','Actividad':[]},{'TIPO':'Tanque4','Actividad':[]},{'TIPO':'Mezclado','Actividad':[]},
        {'TIPO':'Carbonatado','Actividad':[]},{'TIPO':'Enlatado','Actividad':[]},{'TIPO':'Embarque','Actividad':[]}
        ]
            #recorro la lista de tareas efectuadas y se asignan a una estructura que separa las actividades por etapa
    for tareas in a:

        if(tareas[0]['TIPO']=='desembarque'):
            lista_de_equipos[0]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='pesado'):
            lista_de_equipos[1]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='lavado'):
            lista_de_equipos[2]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='pelado'):
            lista_de_equipos[3]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='molienda'):
            lista_de_equipos[4]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='centrifuga'):
            lista_de_equipos[5]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='UHT'):
            lista_de_equipos[6]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='tanque1'):
            lista_de_equipos[7]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='tanque2'):
            lista_de_equipos[8]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='tanque3'):
            lista_de_equipos[9]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='tanque4'):
            lista_de_equipos[10]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='mezclado'):
            lista_de_equipos[11]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='carbonatado'):
            lista_de_equipos[12]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='enlatado'):
            lista_de_equipos[13]['Actividad'].append(tareas)
        if(tareas[0]['TIPO']=='embarque'):
            lista_de_equipos[14]['Actividad'].append(tareas)

    values_of_key = [a_dict[0]['TAREA']['id'] for a_dict in lista_de_equipos[7]['Actividad']]
    list1=set(values_of_key)
    elements=(list(list1))
    lista1=[]
    for i in elements:
        lista1.append(list(filter(lambda dias: dias[0]['TAREA']['id']==i,lista_de_equipos[7]['Actividad'])))
    listadef=[]
    for j in lista1:
        elemento=copy.deepcopy(j[0][0])
        valor_max=max(j, key=lambda item:item[1])
        valor_min=min(j, key=lambda item:item[1])
        elemento['TAREA']['fecha_finalizacion']=valor_max[1].strftime("%m %d %Y")
        elemento['TAREA']['fecha_inicio']=valor_min[1].strftime("%m %d %Y")
        listadef.append((elemento,0))
    lista_de_equipos[7]['Actividad']=listadef

    values_of_key = [a_dict[0]['TAREA']['id'] for a_dict in lista_de_equipos[8]['Actividad']]
    list1=set(values_of_key)
    elements=(list(list1))
    lista1=[]
    for i in elements:
        lista1.append(list(filter(lambda dias: dias[0]['TAREA']['id']==i,lista_de_equipos[8]['Actividad'])))
    listadef=[]
    for j in lista1:
        elemento=copy.deepcopy(j[0][0])
        valor_max=max(j, key=lambda item:item[1])
        valor_min=min(j, key=lambda item:item[1])
        elemento['TAREA']['fecha_finalizacion']=valor_max[1].strftime("%m %d %Y")
        elemento['TAREA']['fecha_inicio']=valor_min[1].strftime("%m %d %Y")
        listadef.append((elemento,0))
    lista_de_equipos[8]['Actividad']=listadef


    values_of_key = [a_dict[0]['TAREA']['id'] for a_dict in lista_de_equipos[9]['Actividad']]
    list1=set(values_of_key)
    elements=(list(list1))
    lista1=[]
    for i in elements:
        lista1.append(list(filter(lambda dias: dias[0]['TAREA']['id']==i,lista_de_equipos[9]['Actividad'])))
    listadef=[]
    for j in lista1:
        elemento=copy.deepcopy(j[0][0])
        valor_max=max(j, key=lambda item:item[1])
        valor_min=min(j, key=lambda item:item[1])
        elemento['TAREA']['fecha_finalizacion']=valor_max[1].strftime("%m %d %Y")
        elemento['TAREA']['fecha_inicio']=valor_min[1].strftime("%m %d %Y")
        listadef.append((elemento,0))
    lista_de_equipos[9]['Actividad']=listadef


    values_of_key = [a_dict[0]['TAREA']['id'] for a_dict in lista_de_equipos[10]['Actividad']]
    list1=set(values_of_key)
    elements=(list(list1))
    lista1=[]
    for i in elements:
        lista1.append(list(filter(lambda dias: dias[0]['TAREA']['id']==i,lista_de_equipos[10]['Actividad'])))
    listadef=[]
    for j in lista1:
        elemento=copy.deepcopy(j[0][0])
        valor_max=max(j, key=lambda item:item[1])
        valor_min=min(j, key=lambda item:item[1])
        elemento['TAREA']['fecha_finalizacion']=valor_max[1].strftime("%m %d %Y")
        elemento['TAREA']['fecha_inicio']=valor_min[1].strftime("%m %d %Y")
        listadef.append((elemento,0))
    lista_de_equipos[10]['Actividad']=listadef

    #print('hola')
        
    return lista_de_equipos
def cargar_tareas():
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'
        name_of_file = 'data'
        completeName = os.path.join(save_path, name_of_file+".json") 
        with open(completeName) as json_file:
            clientes = json.load(json_file)
        return clientes
def get_id_list(lista):

    newlist=[]
    for i in lista:
        newlist.append(i['id'])
    return newlist
def ordenar_Tareas(state,tareas):
    h={}
    newtareas=[]
    for i in state:
        for x in tareas:
            if(i == x['id']):
                newtareas.append(x)
    h['pedidos']=newtareas
    return h
def combinaciones(plan,vector,tareas):
    lista=[]
    for subset in itertools.permutations(vector):
        a=ordenar_Tareas(subset,tareas['pedidos'])
        lista.append((subset,plan.Calcular_Costo(a)))
        #s=repr(plan.Calcular_Costo(a))+ " " + repr(subset) 
        #print(s)
    print(min(lista, key=lambda item:item[1]))


#x=cargar_tareas()
#lista_id=get_id_list(x['pedidos'])
#lista_id=[2,0,1]
#lista_id=[1, 5, 4, 2, 0, 3]
#lista_id=[5, 6, 7, 4, 2, 0, 1, 3]
#lista_id=[5, 2, 8, 7, 9, 1, 4, 6, 3, 0]
#a=ordenar_Tareas(lista_id,x['pedidos'])
#prueba=planificador()
#prueba.Asignar_insumos_personal(a)
#combinaciones(prueba,lista_id,x)
#print(prueba.Calcular_Costo(a))
# listamamalona=prueba.listar_todas_las_actividades()
# fechamax=max(listamamalona, key=lambda item:item[1])
# actividades_por_equipo=separar_las_actividades(listamamalona,x)
# diagrama=tablero.gantt_diagram(prueba.fecha,fechamax[1])
# diagrama.cargar_datos(actividades_por_equipo)
# diagrama.graficar()
# print("goooo")
#print(prueba.Calcular_Costo(a))
