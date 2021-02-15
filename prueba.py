import Funcion_objetivo as fo

def ordenar_Tareas(state,tareas):
    h={}
    newtareas=[]
    for i in state:
        for x in tareas:
            if(i == x['id']):
                newtareas.append(x)
    h['pedidos']=newtareas
    return h

x=fo.cargar_tareas()
estado=[3, 8, 7, 0, 6, 5, 1, 2, 4, 9]
x=ordenar_Tareas(estado,x['pedidos'])
print(fo.Calcular_Costo(x))

