from tutorial_interfaces.srv import Agregarpedido     # CHANGE
import rclpy
from rclpy.node import Node
import json
import copy
import os.path

class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(Agregarpedido, 'agregar_nuevo_pedido', self.pedido_callback)        # CHANGE

    def pedido_callback(self, request, response):
        response.respuesta = 'ok'
        print(str(request.nuevopedido))
        try:
            pedido=json.loads(request.nuevopedido)
        except ValueError as e:
            print("neel")
        else:
            if(pedido["sol"=="p"]):
                del pedido["sol"]
                save_path = '/home/optimizacion_final/datos_json'
                name_of_file = 'data'
                completeName = os.path.join(save_path, name_of_file+".json")
                hclist={}
                hclist['pedidos']=[]
                id=0
                with open(completeName) as json_file:
                    data = json.load(json_file)
                    hclist=copy.deepcopy(data)
                    if(data['pedidos']!=[]):
                        id=data['pedidos'][-1]['id']+1
                pedido['id']=id
                hclist['pedidos'].append(pedido)
                with open(completeName,'w') as outfile:
                    json.dump(hclist,outfile)
                print("too good")
            if(pedido["sol"=="m"]):
                del pedido["sol"]
                save_path = '/home/optimizacion_final/datos_json'
                name_of_file = 'datam'
                completeName = os.path.join(save_path, name_of_file+".json")
                hclist={}
                hclist['preventivo']=[]
                id=0
                with open(completeName) as json_file:
                    data = json.load(json_file)
                    hclist=copy.deepcopy(data)
                    if(data['preventivo']!=[]):
                        id=data['preventivo'][-1]['id']+1
                pedido['id']=id
                hclist['preventivo'].append(pedido)
                with open(completeName,'w') as outfile:
                    json.dump(hclist,outfile)
                print("too good")
        return response

def main(args=None):
    rclpy.init(args=args)

    minimal_service = MinimalService()

    rclpy.spin(minimal_service)

    rclpy.shutdown()

if __name__ == '__main__':
    main()