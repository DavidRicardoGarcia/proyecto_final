
import json
import os.path
import copy
from datetime import timedelta,datetime,date

   
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
        data={'fecha':self.fecha.strftime("%m %d %Y"),'recursoA':self.recursoA,'recursoB1':self.recursoB1,'recursoB2':self.recursoB2,'recursoB3':self.recursoB3,
        'recursoB4':self.recursoB4,'recursoC':self.recursoC}
        return data
    def setFecha(self,fecha):
        self.fecha=fecha
    def setRecurso(self,tipo,tarea,empleados,insumos):
        if(tipo=='A'):
            self.cont=0
            for i in self.recursoA:
                i['TAREA']=tarea
                i['EMPLEADO']=empleados[self.cont]
                i['INSUMOS']=insumos[self.cont]
                self.cont+=1
        if(tipo=='B'):  
            self.asignar_tanque(tarea,empleados,insumos)
        if(tipo=='C'):
            for i in self.recursoC:
                i['TAREA']=tarea
                i['EMPLEADO']=empleados[self.cont]
                i['INSUMOS']=insumos[self.cont]
                self.cont+=1
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

    def __init__(self,id,nombre,tipo,cant_und_bas,cant_und_doc,und_doc,f_c,precio,lote,fecha_caducidad,fecha_produccion,n_palet,estado,ident):
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
        self.ident=ident

    def get_dict(self):
        data={'id':self.id,'tipo': self.tipo,'cantidad und basica':self.cant_und_bas,'cantidad und doc': self.cant_und_doc,
        'unidad doc':'palet','F_C':'f_C','precio':self.precio,'lote':self.lote,'caducidad':self.caducidad,'produccion':self.produccion,
        'n palets':self.n_palet,'estado':self.estado,'ident':self.ident}
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
        data={'fecha':self.fecha.strftime("%m %d %Y"),'pedidosI':self.pedidos_insumos,'ingresosI':self.ingresos_insumos,'salidasP':self.salida_productos}
        return data

    def setFecha(self,fecha):
        self.fecha=fecha
    #orden de pedido
    def setPedido_insumo(self,id,nombre,tipo,precio,lote,fecha_caducidad,estado,ident):
        a=ingreso(id,nombre,tipo,1,1,1,1,precio,lote,fecha_caducidad,0,0,estado,ident)
        self.pedidos_insumos.append(a.get_dict())

    #ingreso del pedido que se ordenó previamente
    def setIngreso_insumo(self,id,producto,cantidad,valor):
        a=datos_de_suministro(id,producto,cantidad,valor)
        self.ingresos_insumos.append(a.get_dict())
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
        #diainicial=datetime.now()
        #diafinal=diainicial+timedelta(days=365)
        #self.crear_AgendaP(diainicial,diafinal)
        #self.crear_AgendaR(diainicial,diafinal)
    def crear_AgendaR(self,diao,diaf):
        dias=diaf-diao
        for i in range(dias.days):
            self.bookR.append(dia(diao+timedelta(days=i)))
    def crear_AgendaP(self,diao,diaf):
        dias=diaf-diao
        for i in range(dias.days):
            self.bookP.append(dia_registro(diao+timedelta(days=i)))
    def cargarR(self,a):
        
        for idx, i in enumerate(self.bookR):
            i.recursoA=a[idx]['recursoA']
            i.recursoB1=a[idx]['recursoB1']
            i.recursoB2=a[idx]['recursoB2']
            i.recursoB3=a[idx]['recursoB3']
            i.recursoB4=a[idx]['recursoB4']
            i.recursoC=a[idx]['recursoC']
            

    def cargarP(self,a):
        
        for idx, i in enumerate(self.bookP):
            i.pedidos_insumos=a[idx]['pedidosI']
            i.ingresos_insumos=a[idx]['ingresosI']
            i.salida_productos=a[idx]['salidasP']
            
    
    def guardarR(self):
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'book_recursos'

        completeName = os.path.join(save_path, name_of_file+".json") 
        Rlist={}
        Rlist['calendario']=[]
        for i in self.bookR:
            Rlist['calendario'].append(i.get_dict())
        
        with open(completeName,'w') as outfile:
            json.dump(Rlist,outfile)

    def guardarP(self):
        save_path = '/home/david/Desktop/optimizacion_final/datos_json'

        name_of_file = 'book_pedidos'

        completeName = os.path.join(save_path, name_of_file+".json") 
        Rlist={}
        Rlist['calendario']=[]
        for i in self.bookP:
            Rlist['calendario'].append(i.get_dict())
        
        with open(completeName,'w') as outfile:
            json.dump(Rlist,outfile)
