from flask import Flask, request, abort, jsonify, make_response
import json
import requests
import datetime
from rivescript import RiveScript
from config import token, auth_token


app = Flask(__name__)

app.debug = True



@app.route('/webhook', methods=['GET'])
def verify():
    mode = request.args.get('hub.mode')
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and verify_token == auth_token:
        print('correct')
        return challenge
    else:
        return jsonify(error='Invalid Token'), 400
    
@app.route('/webhook', methods=['POST'])
def webhook():
    request_body = request.get_data(as_text=True)
    print(request_body)
    data = json.loads(request_body)
    
    if 'messages' in data['entry'][0]['changes'][0]['value']:
        timestamp = data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
        now = datetime.datetime.now()
        timestamp_datetime = datetime.datetime.fromtimestamp(int(timestamp))
        
        if (now - timestamp_datetime) < datetime.timedelta(minutes=10):
            
            if data['entry'][0]['changes'][0]['value']['messages'][0]['type'] == 'interactive':
                mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['interactive']['button_reply']['title']  
                if mensaje == 'Información':
                    mensaje = 'informacion'       
            else:
                mensaje = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
            
            bot = RiveScript()
            bot.load_file('answers.rive')
            bot.sort_replies()
            
            print(mensaje)
            
            respuesta = bot.reply("localuser", mensaje)
            
            wa_id = data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
            phone_number = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                
            wa_id = wa_id[0:2] + wa_id[3:]
            url = "https://graph.facebook.com/v15.0/113836214950869/messages"
            
            if respuesta == 'Saludo':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "Reciba un Saludo Cordial de parte de Impresox ¿Cómo podemos ayudarle?"
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton1",
                                    "title": "Información"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton2",
                                    "title": "Necesito Imprimir"
                                    }
                                }
                            ]
                        }
                    }
                })
                
            if respuesta == 'tipo_impresion':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "¿Qué tipo de Impresión desea?"
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton1",
                                    "title": "Personal"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton2",
                                    "title": "Social"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton3",
                                    "title": "Mas opciones"
                                    }
                                }
                            ]
                        }
                    }
                })
                
            if respuesta == 'mas_opciones':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "¿Qué tipo de Impresión desea?"
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton1",
                                    "title": "Comercial"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton2",
                                    "title": "Industrial"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton3",
                                    "title": "Volver"
                                    }
                                }
                            ]
                        }
                    }
                })
            
            if respuesta == 'cotizacion':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": str(wa_id),
                    "type": "text",
                    "text": {
                        "body": "¿Podría mandarme la medida y color, así como las unidades que requiere para poder realizarle una cotización?"
                    }
                })
                
            if respuesta == 'medidas':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": str(wa_id),
                    "type": "text",
                    "text": {
                        "body": "¿Cuándo requiere nuestro servicio?"
                    }
                })       
            
            if respuesta == 'paquetes':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "Para nuestros servicios de Impresión manejamos distintos Paquetes de Bajo volumen y Alto Volumen ¿Le interesa saber sobre alguno en especial? "
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton1",
                                    "title": "Bajo"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton2",
                                    "title": "Alto"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton3",
                                    "title": "No me interesa"
                                    }
                                }
                            ]
                        }
                    }
                })
                
            if respuesta == 'envios':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "Manejamos distintos puntos de entrega y envíos por paquetería para brindarle el mejor servicio a su pedido. ¿Le interesa algún punto de entrega o envió a domicilio?"
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton1",
                                    "title": "Punto de entrega"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton2",
                                    "title": "Envio a domicilio"
                                    }
                                }
                            ]
                        }
                    }
                })
                
            if respuesta == 'diseño':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "¿Cuenta con diseño previo?"
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton1",
                                    "title": "Si tengo"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton2",
                                    "title": "No tengo"
                                    }
                                }
                            ]
                        }
                    }
                })
            
            if respuesta == 'tiempo':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "Mantenemos un margen de tiempo en cuanto a la realización de cotización y realización de diseño ¿Está usted de acuerdo?"
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton1",
                                    "title": "De acuerdo"
                                    }
                                },
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton2",
                                    "title": "Desacuerdo"
                                    }
                                }
                            ]
                        }
                    }
                })
                
            if respuesta == 'diseñador':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": str(wa_id),
                    "type": "text",
                    "text": {
                        "body": "Contamos con un grupo de diseñadores para realizarle el diseño de su Impresión, es importante mencionar concreto y específicamente lo que usted requiere para trabajarlo. Con gusto le damos forma a tus ideas."
                    }
                })
            
            if respuesta == 'diseñador2':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": str(wa_id),
                    "type": "text",
                    "text": {
                        "body": "Manejamos un Catalogo de productos donde personalizamos la impresión, si no cuentas con el Diseño nuestros diseñadores con gusto les dan forma a tus ideas."
                    }
                })
                
            if respuesta == 'deposito':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "to": str(wa_id),
                    "type": "text",
                    "text": {
                        "body": "Cabe recalcar que al momento de realizar el depósito/pago con el mínimo de anticipo,  nosotros comenzamos a realizar su pedido y de aquí parte el margen de tiempo para su entrega."
                    }
                })
            
            if respuesta == 'info':
                payload = json.dumps({
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": str(wa_id),
                    "type": "interactive",
                    "interactive": {
                        "type": "button",
                        "body": {
                            "text": "En Impresox, nos dedicamos a darle impresión a tus ideas con lo último en tecnologías de Innovación. Realizamos Papelería Personal, Social, Comercial e Industrial. Contamos con Diseño Gráfico en General ofreciéndote las mejores soluciones en impresión."
                        },
                        "action": {
                            "buttons": [
                                {
                                    "type": "reply",
                                    "reply": {
                                    "id": "Boton1",
                                    "title": "Necesito imprimir"
                                    }
                                }
                            ]
                        }
                    }
                })  
                
            headers = {
                    'Content-Type': 'application/json',
                    'Authorization': token
            }
                
            response = requests.request("POST", url, headers=headers, data=payload)      
            
    response = make_response('')
    response.status_code = 200
    return response    
    
       
if __name__ == '__main__':
    app.run()
