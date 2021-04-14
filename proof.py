
import json
import os.path

def terminado_algoritmo(res,tiempo,valor):
        
    save_path = '/home/david/Desktop/optimizacion_final/datos_json'

    name_of_file = 'estado'

    completeName = os.path.join(save_path, name_of_file+".txt") 

    with open(completeName) as json_file:
        data = json.load(json_file)

    data['GA']['estado']='terminado'
    data['GA']['resultado']=res
    data['GA']['tiempo']=tiempo
    data['GA']['valor']=valor

    #se ejecuta el algoritmo en cuestion

    with open(completeName,'w') as outfile:
        json.dump(data,outfile)

terminado_algoritmo([1,2,3,4],12,11)