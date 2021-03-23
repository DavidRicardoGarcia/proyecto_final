import json
import os.path
import copy
from datetime import timedelta,datetime,date
from elementos_modelo import recursos_humanos as rh
from elementos_modelo import transporte as tr
from elementos_modelo import almacen as alm
    
class planificador:
    def __init__(self):
        super().__init__()
        self.lista_asignar=[]
        self.cargar_datos_iniciales()
        self.separar_por_cantidad()
        self.book=agenda()
        self.fecha=datetime.now()
        self.rh=rh.horarios()
        self.tipos_insumos=['8-st','8-sl','12-st','12-sl','16-st','quimico 0','quimico 1','quimico 2','quimico 3','quimico 4']
        self.almacen=alm.almacen()


    def cargar_datos_iniciales(self):
        
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'
        #tiempos de cada elemento y de viajes
        name_of_file = 'modelsettings'
        completeName = os.path.join(save_path, name_of_file+".txt") 
        with open(completeName) as json_file:
            self.settings = json.load(json_file)
        #dias de mtto
        name_of_file = 'datam'
        completeName = os.path.join(save_path, name_of_file+".txt") 
        with open(completeName) as json_file:
            self.mantenimiento = json.load(json_file)

        name_of_file = 'data_S'
        completeName = os.path.join(save_path, name_of_file+".txt") 
        with open(completeName) as json_file:
            self.materiales = json.load(json_file)
        #las tareas
        name_of_file = 'data'
        completeName = os.path.join(save_path, name_of_file+".txt") 
        with open(completeName) as json_file:
            self.pedidos = json.load(json_file)

    def separar_por_cantidad(self):
        for val in self.pedidos['pedidos']:
            for x in range(val['cantidad']):
                k=val.copy()
                k['cantidad']=1
                self.lista_asignar.append(k)

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

        cont=0
        for x in data['horario empleados']:
            if(x['estado']=='incapacidad'):
                data[cont]={"id": -1, "nombre y apellido": "sustituto" + str(cont), "email": "------@gmail.com", 
                "telefono": 000000000, "empresa": "Punta Delicia", "cargo": "operario", "departamento": x['departamento'],
                 "estacion de trabajo": x['estacion'], "salario": x['salario']*1.1, "horas_extra": 25, 
                 "hinicio": 8, "hsalida": 18, "estado": "sustituyendo"}
            cont+=1
        self.trabajadores=data

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

    def buscar_pedidos_en_camino(self,bookp):
        lista_De_pedidos=[]
        for i in bookp:
            if (i.pedidos_insumos !=[]):
                lista_De_pedidos.append(i.getpedidos())
        return lista_De_pedidos

    def revisar_los_tanques(self,fecha):

        B=False
        for i in self.book.bookR:
            if(fecha==i.fecha):
                if(i.recursoB1['ESTADO']=='disponible'):
                    B=True
                elif(i.recursoB2['ESTADO']=='disponible'):
                    B=True
                elif(i.recursoB3['ESTADO']=='disponible'):
                    B=True
                elif(i.recursoB4['ESTADO']=='disponible'):
                    B=True
                return B
    def revisar_transformar(self,fecha):
        B=False
        for i in self.book.bookR:
            if(fecha==i.fecha):
                if(i.recursoA[0]['HINICIO']==0):
                    B=True
                    return B
                else:
                    return B
    def revisar_enlatar(self,fecha):
        B=False
        for i in self.book.bookR:
            if(fecha==i.fecha):
                if(i.recursoC[0]['HINICIO']==0):
                    B=True
                    return B
                else:
                    return B
    def condiciones(self,fecha,tipo):
        # primero se revisa halla algo en la lista
        if(tipo=='banano' or tipo=='guanabana'):
            if(self.lista_asignar==[]):
                f=False
            else:
                f=True
            #revisar el recurso en el book
            h=self.revisar_transformar(fecha)
            #revisar el recurso en el book
            c=self.revisar_los_tanques(fecha)

            w=self.revisar_dia(fecha)

            y=self.revisar_mantenimiento(fecha)
            
            condicion1=(f and c and w != 6 and (y[0] and y[1]))
            return condicion1
        if(tipo=='vino'):
            if(self.lista_asignar==[]):
                f=False
            else:
                f=True
            #revisar el recurso en el book
            c=self.revisar_los_tanques(fecha)

            w=self.revisar_dia(fecha)

            y=self.revisar_mantenimiento(fecha)
            
            condicion2=(f and c and w != 6 and y[1])
            return condicion2

    def condiciones_enlatar(self,fecha):

            f=self.condiciones_enlatar(fecha)
            
            w=self.revisar_dia(fecha)

            y=self.revisar_mantenimiento(fecha)
            
            condicion3=(f and w != 6 and (y[2]))

            return condicion3
    
    def asignacion(self):
        lista=self.buscar_pedidos_en_camino(self.book.bookP)
        print('hola')
        fecha_inicial=self.fecha
        flag=False
        #se asignan las tareas en orden
        for i in self.lista_asignar:
            while(flag):
                tipo=i['tipo'].split()
                #se elige la fecha tentativa
                tagendar=fecha_inicial+timedelta(days=(self.settings['tareas'][tipo[0]]['Tinsumo']))
                #se consulta en el libro si se puede




#se crea un objeto de tipo dia que guarda las tareas a realizar esa fecha
class dia:
    def __init__(self,fecha):
        super().__init__()
        self.fecha=fecha
        self.recursoA=[
        {'TIPO':'desembarque','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'1','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'pesado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'2','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'lavado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'3','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'pelado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'4','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'molienda','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'5','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'centrifuga','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'6','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'UHT','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'7','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0}]
        self.recursoB1={'TIPO':'tanque1','HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':{},'DIA':0,'INSUMOS':0}
        self.recursoB2={'TIPO':'tanque2','HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':{},'DIA':0,'INSUMOS':0}
        self.recursoB3={'TIPO':'tanque3','HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':{},'DIA':0,'INSUMOS':0}
        self.recursoB4={'TIPO':'tanque4','HINICIO':0,'HORAS':0,'COSTO':0.5,'ESTADO':'disponible','TAREA':{},'DIA':0,'INSUMOS':0}
        self.recursoC=[
        {'TIPO':'mezclado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'8','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'carbonatado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'9','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'enlatado','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'10','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0},
        {'TIPO':'embarque','HINICIO':0,'HORAS':0,'COSTO':0.5,'EMPLEADO':{'NOMBRE':'11','ESTADO':0,'SUELDO':1,'HORAS':0},'TAREA':{},'DIA':0,'INSUMOS':0}]
    
    def get_dict(self):
        data={'fecha':self.fecha,'recursoA':self.recursoA,'recursoB1':self.recursoB1,'recursoB2':self.recursoB2,'recursoB3':self.recursoB3,
        'recursoB4':self.recursoB4,'recursoC':self.recursoC}
        return data
    def setFecha(self,fecha):
        self.fecha=fecha
    def setRecurso(self,tipo,tarea,empleados,insumos):
        if(tipo=='A'):
            cont=0
            for i in self.recursoA:
                i['TAREA']=tarea
                i['EMPLEADO']=empleados[cont]
                i['INSUMOS']=insumos[cont]
                cont+=1
        if(tipo=='B'):  
            self.asignar_tanque(tarea,empleados,insumos)
        if(tipo=='C'):
            for i in self.recursoC:
                i['TAREA']=tarea
                i['EMPLEADO']=empleados[cont]
                i['INSUMOS']=insumos[cont]
                cont+=1
    def asignar_tanque(self,tarea,empleado,insumos):
        if(self.recursoB1['ESTADO']=='disponible'):
            self.recursoB1['ESTADO']='ocupado'
            self.recursoB1['TAREA']=tarea
            self.recursoB1['EMPLEADO']=empleado
            self.recursoB1['INSUMOS']= insumos
        elif(self.recursoB2['ESTADO']=='disponible'):
            self.recursoB2['ESTADO']='ocupado'
            self.recursoB2['TAREA']=tarea
            self.recursoB2['EMPLEADO']=empleado
            self.recursoB2['INSUMOS']= insumos
        elif(self.recursoB3['ESTADO']=='disponible'):
            self.recursoB3['ESTADO']='ocupado'
            self.recursoB3['TAREA']=tarea
            self.recursoB3['EMPLEADO']=empleado
            self.recursoB3['INSUMOS']= insumos
        else:
            self.recursoB4['ESTADO']='ocupado'
            self.recursoB4['TAREA']=tarea
            self.recursoB4['EMPLEADO']=empleado
            self.recursoB4['INSUMOS']= insumos
    def revisar_los_tanques(self):

        B=False
        if(self.recursoB1['ESTADO']=='disponible'):
            B=True
        elif(self.recursoB2['ESTADO']=='disponible'):
            B=True
        elif(self.recursoB3['ESTADO']=='disponible'):
            B=True
        elif(self.recursoB4['ESTADO']=='disponible'):
            B=True
        return B
#guarda los datos importantes de la llegada de insumo
class datos_de_suministro:

    def __init__(self,id,producto,cantidad,valor):
        self.id=id
        self.producto=producto
        self.cant=cantidad
        self.valor=valor

    def get_dict(self):
        data={'id':self.id,'producto':self.producto,'cantidad':self.cant,'valor':self.valor}
        return data

#genera la hoja de datos del pedido que va a ingresar
class ingreso:

    def __init__(self,id,nombre,tipo,cant_und_bas,cant_und_doc,und_doc,f_c,precio,lote,fecha_caducidad,fecha_produccion,n_palet,estado):
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
        self.estado=estado

    def get_dict(self):
        data={'id':self.id,'tipo': self.tipo,'cantidad und basica':self.cant_und_bas,'cantidad und doc': self.cant_und_doc,
        'unidad doc':'palet','F_C':'f_C','precio':self.precio,'lote':self.lote,'caducidad':self.caducidad,'produccion':self.produccion,
        'n palets':self.n_palet,'estado':self.estado}
        return data

#guarda los pedidos y los ingresos de insumos por fecha
class dia_registro:
    def __init__(self,fecha):
        super().__init__()
        self.fecha=fecha
        #registro del dia que se pidieron insumos
        self.pedidos_insumos=[]
        #registro del dia que llegaron
        self.ingresos_insumos=[]
        self.salida_productos=0

    def get_dict(self):
        data={'fecha':self.fecha,'pedidosI':self.pedidos_insumos,'ingresosI':self.ingresos_insumos,'salidasP':self.salida_productos}
        return data

    def setFecha(self,fecha):
        self.fecha=fecha
    #orden de pedido
    def setPedido_insumo(self,id,nombre,tipo,precio,lote,fecha_caducidad,estado):
        self.pedidos_insumos.append(ingreso(id,nombre,tipo,1,1,1,1,precio,lote,fecha_caducidad,0,0,estado))

    #ingreso del pedido que se ordenó previamente
    def setIngreso_insumo(self,id,producto,cantidad,valor):
        self.ingresos_insumos.append(datos_de_suministro(id,producto,cantidad,valor))
    #regresa la lista de pedidos que se han hecho
    def getpedidos(self):
        pedidos_en_Espera=[]
        for i in self.pedidos_insumos:
            if(i.estado=='en camino'):
                pedidos_en_Espera.append(i)
        return pedidos_en_Espera

# Tiene las listas con la informacion de asignaciones y pedidos por fecha
class agenda:
    def __init__(self):
        super().__init__()
        self.bookR=[]
        self.bookP=[]
        diainicial=datetime.now()
        diafinal=diainicial+timedelta(days=365)
        self.crear_AgendaP(diainicial,diafinal)
        self.crear_AgendaR(diainicial,diafinal)
    def crear_AgendaR(self,diao,diaf):
        dias=diaf-diao
        for i in range(dias.days):
            self.bookR.append(dia(diao+timedelta(days=i)))
    def crear_AgendaP(self,diao,diaf):
        dias=diaf-diao
        for i in range(dias.days):
            self.bookP.append(dia_registro(diao+timedelta(days=i)))

# ag=agenda()
# diainicial=datetime.now()
# diafinal=diainicial+timedelta(days=365)
# ag.crear_AgendaR(diainicial,diafinal)
# ag.crear_AgendaP(diainicial,diafinal)
# settings,mantenimiento,materiales,pedidos=cargar_datos_iniciales()
# print('hola')
prueba=planificador()
prueba.asignacion()