# ST0263-7290

# Estudiante(s):
- Daniel Correa Botero, dcorreab2@eafit.edu.co
- Miguel Ángel Cano Salinas, macanos1@eafit.edu.co
- Santiago Acevedo Urrego, sacevedou1@eafit.edu.co

# Profesor:
- Edwin Montoya, emontoya@eafit.edu.co

# Proyecto 1: Diseño e Implementación de un MOM entre aplicaciones

## 1. Breve descripción de la actividad

Nuestro proyecto consiste en un Middleware Orientado a Mensajes (MOM), el cual lo diseñamos para facilitar la comunicación entre aplicaciones usando intercambio de mensajes a través de colas o tópicos.

Para esto decidimos implementar un Routing Tier como intermediario permitiéndonos así enrutar las solicitudes de los clientes hacia las instancias MOM, balanceando la carga y asegurando disponibilidad.

Para hacer la comunicación un poco más amigable con el usuario final, implementamos una interfaz en el cliente para enviar las solicitudes de mensaje y recibir la respuesta.


### 1.1. Aspectos cumplidos

- **Envío y recepción de mensajes identificando usuarios**
- **Exposición de servicios como API REST**
- **Implementación del cliente y su interfaz**
- **Implementación de la Routing Tier**
- **Replicación y particionamiento**
- **Definición de arquitectura distribuida**: Implementamos una arquitectura distribuida con múltiples instancias de MOM y un Routing Tier
- **Tolerancia a fallos en servidores**: Usamos la redundancia a través de la creación de varias instancias de la MOM. Sin embargo, somos dependientes de que el Zookeeper no se caiga.
- **Modelo de interacción asíncrona**: Dado que las MOM funcionan perfectamente
- **Multiusuario**: Cualquier usuario se puede autenticar para interactuar con la aplicación.
- **Consideraciones de escalabilidad**
- **Transparencia**: El usuario nunca tiene acceso únicamente al auth, el envío y la recepción de mensajes.
- **Extensibilidad**
### 1.2. Aspectos no cumplidos
- **Transporte de mensajes encriptado**: Actualmente usamos un token en el usuario para el envío y recepción de los mensajes pero la estructura base del mensaje no está encriptada.
- **Desconexión con usuarios autenticados**
- **Desconexión de usuarios**
- **Tolerancia a Fallos por el Zookeeper**

## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

### **Arquitectura**
El proyecto implementa una arquitectura distribuida basada en un **Middleware Orientado a Mensajes (MOM)**. Esto incluye lo siguiente:

- **Routing Tier**: Es la que actúa como intermediario entre los clientes y las instancias MOM, balanceando la carga y asegurando disponibilidad.
- **Instancias MOM**: Tres instancias que manejan colas y tópicos para el intercambio de mensajes.
- **Cliente**: Una interfaz que permite a los usuarios interactuar con el sistema para enviar y recibir mensajes.

![MOM(1)](https://github.com/user-attachments/assets/8bcabbeb-3898-43c3-82bc-242859e0860c)


### **2. Patrones de Disponibilidad**
- **Patrón de Balanceo de Carga**:
  - El **Routing Tier** distribuye las solicitudes entre las instancias MOM utilizando un mecanismo de selección (como round-robin o selección aleatoria). Esto evita la sobrecarga en una sola instancia y mejora la disponibilidad.
- **Patrón de Redundancia**:
  - Se implementan múltiples instancias de MOM para garantizar que el sistema siga funcionando incluso si una instancia falla.
  - El uso de Zookeeper permite registrar y descubrir dinámicamente las instancias MOM disponibles, asegurando que siempre haya nodos accesibles.
### **2. Patrones de Rendimiento**
- **Patrón de Productor-Consumidor**:
    - Las colas y tópicos desacoplan la producción y el consumo de mensajes, permitiendo que los productores (clientes) y consumidores (suscriptores) trabajen a diferentes velocidades sin afectar el rendimiento general.
- **Patrón de Escalabilidad Horizontal**:
    - La arquitectura distribuida permite agregar más instancias MOM según la demanda, mejorando el rendimiento del sistema bajo alta carga.
![WhatsApp Image 2025-04-20 at 12 23 40 PM](https://github.com/user-attachments/assets/fb5eae4f-5b59-44f0-a7a4-3d344f3e3bfc)

### **Mejores prácticas**
- **Escalabilidad**: La arquitectura distribuida permite agregar más instancias MOM según la demanda.
- **Separación de responsabilidades**: Cada componente (Routing Tier, MOM, Cliente) tiene una función específica.
- **Uso de APIs REST**: Los servicios están expuestos como APIs REST, facilitando la integración con otros sistemas.
- **Tolerancia a fallos**: Se implementa redundancia en las instancias MOM, aunque dependan de la disponibilidad de Zookeeper.
- **Modelo síncrono y asíncrono**: El sistema utiliza colas y tópicos para manejar mensajes de manera asíncrona en la comunicación con la MOM. Además, usa gRPC para que las peticiones del cliente lleguen a la MOM y se permita esta comunicación exitosamente.

## 3. Ambiente local para desarrollo

El proyecto fue realizado en Python, usando Flask para la exposición de los endpoints para uso del cliente, es decir, el Routing Tier implementado usa Flask para recibir las peticiones y usando su tabla de enrutamiento, redirigir a través de gRPC la solicitud al MOM correspondiente, para esta comunicación gRPC se usó Protobuf, con sus respectivos archivos *.proto para definir y estandarizar los métodos implementados. El Routing Tier tiene una base de datos interna de SQLite para gestionar la autenticación y mantener guardados los usuarios registrados, ésta ya está configurada, no hay que hacer nada adicional. El cliente está implementado en React, el cual se conecta por API Rest al servidor de MOMs.

#### Requerimientos pre-instalados:
- Python 3.13
- Node 23
- Npm 11
- Zookeeper 3.8

Todos los paquetes y librerías de Python utilizadas se pueden encontrar en los archivos [`mom/requirements.txt`](./mom/requirements.txt) y [`routing-tier/requirements.txt`](./routing-tier/requirements.txt). Allí están especificadas las versiones de cada una de ellas.

Los paquetes y librerías de JavaScript utilizadas junto con sus versiones se reportan en [`client/package.json`](./client/package.json).

#### Ejecución
Teniendo esto en cuenta, para ejecutar el proyecto en desarrollo local se debe:

1. Activar el daemon de Zookeeper, esto puede cambiar sustancialmente en diferentes Sistemas Operativos, remítase a [Referencias](#referencias)->Apache Zookeeper Docs para verificar este proceso.

2. Instalar requerimientos del Routing Tier. Se recomienda usar un entorno virtual de Python.
```{bash}
cd routing-tier/
python -m venv .venv
source .venv/bin/activate ## para linux
pip install -r requirements.txt
```
3. Ejecutar Routing Tier. Iniciará en el puerto 5000.
```{bash}
python app.py
```

4. Instalar requerimientos del MOM. Se recomienda usar un entorno virtual de Python.
```{bash}
cd mom/
python -m venv .venv
source .venv/bin/activate ## para linux
pip install -r requirements.txt
```

5. Ejecutar MOM. Iniciará en el puerto 5001. Si usará diferentes MOMs al mismo tiempo se debe cambiar la variable `port` de [`app.py`](./mom/app.py) para cambiar el puerto usado.
```{bash}
python app.py
```

6. Instalar dependencias de JavaScript y React.
```{bash}
npm install
```

7. Ejecutar el cliente. Iniciará en el puerto 3000.
```{bash}
npm start
```

#### Estructura archivos Routing Tier
├── app.db
├── app.py
├── proto
│   └── mom.proto
├── requirements.txt
└── src
    ├── controllers
    │   ├── routing_tier_controller.py
    │   └── user_controller.py
    ├── grpc_client
    │   ├── mom_pb2_grpc.py
    │   ├── mom_pb2.py
    ├── models
    │   └── user.py
    ├── routes
    │   ├── queue_routes.py
    │   ├── topics_routes.py
    │   └── user_routes.py
    ├── services
    │   ├── grpc_client.py
    │   └── routing_tier_service.py
    └── utils
        ├── database.py
        ├── response_utils.py
        └── utils.py

#### Estructura archivos MOM
├── app.py
├── dockerfile
├── proto
│   └── mom.proto
├── README.md
├── requirements.txt
└── src
    ├── controllers
    │   ├── QueueServiceServicer.py
    │   └── TopicServiceServicer.py
    ├── models
    │   ├── message.py
    │   ├── queue.py
    │   └── topic.py
    ├── services
    │   ├── queue_service.py
    │   └── topics_services.py
    └── utils
        ├── mom_pb2_grpc.py
        ├── mom_pb2.py
        └── utils.py

#### Estructura Archivos Cliente
├── package.json
├── package-lock.json
├── public
│   ├── favicon.ico
│   ├── index.html
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   └── robots.txt
├── README.md
└── src
    ├── App.js
    ├── components
    │   ├── Button.jsx
    │   ├── chatContaincer.jsx
    │   ├── Input.jsx
    │   ├── LoginForm.jsx
    │   ├── plusOverlay.jsx
    │   └── SidebarList.jsx
    ├── config
    │   └── index.js
    ├── constants
    │   └── formFields.js
    ├── index.css
    ├── index.js
    ├── logo.svg
    ├── services
    │   ├── colas.js
    │   ├── topics.js
    │   └── user.js
    ├── styles
    │   ├── App.css
    │   ├── auth.css
    │   ├── main.css
    │   └── overlay.css
    └── views
        ├── chatView.jsx
        ├── Login.jsx
        └── Register.jsx

## 4. Ambiente de producción y despliegue

## IP o nombres de dominio en nube o en la máquina servidor:

- **Cliente React**: [http://13.219.188.33](http://13.219.188.33)
- **Servidor Backend**: [http://your-backend-ip-or-domain](http:/107.22.123.0:500) 

### Configuración de Parámetros
- **IP Cliente React**: `http://13.219.188.33`
- **IP Servidor Backend**: `http://107.22.123.0:5000`
- **Puerto del Servidor**: `5000` 

descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor:

Cada uno de los siguientes componentes deben desplegarse en máquinas virtuales diferentes.

### lanzamiento de una MOM:

Clonar el repositorio de github.
```{bash}
    git clone https://github.com/DanielC19/mom-project.git
    cd mom-project/mom/
```
Instalar docker en ubuntu:22.04:
```{bash}
    sudo apt update
    sudo apt install docker.io -y
    sudo apt install docker-compose -y

    sudo systemctl enable docker
    sudo systemctl start docker
```

Ejecutar estos comandos para generar la imagen en docker y iniciar el contenedor (recordar cambiar la ip privada):

```{bash}
    sudo docker build --force-rm -t grpcServer/latest . --no-cache
    sudo docker run -d --restart always   -e HOST_IP=<ip_privada_host>   -p 5001:5001 -p 50051:50051   --name grpc-server   grpcServer/latest:latest
```

### Lanzamiento del routing tier:
Instalar python, clonar el repositorio, configurar en entorno virtual y ejecutar el servidor:

```{bash}
    sudo apt update
    sudo apt install python3
    sudo apt install python3-pip
    sudo apt install python3-venv
    git clone https://github.com/DanielC19/mom-project.git
    cd mom-project/routing tier/
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    sudo nohup .venv/bin/python3 app.py &
```


### Lanzamiento del cliente React:


Ejecutar los siguiente comandos para instalar node.js
```{bash}
    sudo apt update
    sudo apt upgrade -y
    sudo apt install curl -y
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt install nodejs -y
```
Ejecutar para clonar y compilar:
```{bash}
    git clone https://github.com/DanielC19/mom-project.git
    cd mom-project/client/
    npm install
    npm run build
```

Ejecutar para configurar nginx:
```{bash}
    sudo apt update
    sudo apt install nginx -y
    sudo nano /etc/nginx/sites-available/reactapp
```

Pegar en el editor el siguiente texto:
```{bash}
server {
    listen 80;
    server_name tu-dominio.com;  # o tu IP pública

    root /home/ubuntu/react-app/build;
    index index.html index.htm;

    location / {
        try_files $uri /index.html;
    }
}
```

Ejecutar estos comandos para activar la aplicacion:
```{bash}
    sudo ln -s /etc/nginx/sites-available/reactapp /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
```
De esta manera se despliega el cliente React y se usa nginx como proxy inverso para mapear el tráfico al puerto 80


### Lanzamiento de zookeeeper:
Ejecutar para clonar:
```{bash}
    git clone https://github.com/DanielC19/mom-project.git
```

Instalar docker en ubuntu:22.04:
```{bash}
    sudo apt update
    sudo apt install docker.io -y
    sudo apt install docker-compose -y

    sudo systemctl enable docker
    sudo systemctl start docker
```
Iniciar el contenedor de zookeeper con la configuracion necesaria con el siguiente comando:

```{bash}
    docker-compose -f docker-compose-zookeeper.yml up -d
```

## 5. Conexión SSH a las instancias creadas
El archivo "santiago.pem" viene adjunto en el entregable del proyecto

Mom 1
```{bash}
ssh -i "santiago.pem" ubuntu@ec2-44-202-123-39.compute-1.amazonaws.com
```
Mom 2
```{bash}
ssh -i "santiago.pem" ubuntu@ec2-3-80-35-67.compute-1.amazonaws.com
```
Mom 3
```{bash}
ssh -i "santiago.pem" ubuntu@ec2-3-80-204-18.compute-1.amazonaws.com
```
Cliente
```{bash}
ssh -i "santiago.pem" ubuntu@ec2-13-219-188-33.compute-1.amazonaws.com
```
Zookeeper
```{bash}
ssh -i "santiago.pem" ubuntu@ec2-3-82-225-247.compute-1.amazonaws.com
```
Routing Tier
```{bash}
ssh -i "santiago.pem" ubuntu@ec2-107-22-123-0.compute-1.amazonaws.com
```

# Referencias:
[GitHub Copilot](https://github.com/features/copilot)
[ChatGPT](https://chatgpt.com)
[Apache Zookeeper Docs](https://zookeeper.apache.org)
[Kazoo Docs](https://kazoo.readthedocs.io/en/latest)
[Protobuf Docs](https://protobuf-dev.translate.goog/programming-guides/proto3/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc)
[Protobuf Tutorial Medium](https://medium.com/@roystatham3003/grpc-basics-creating-a-protobuf-file-proto-a80f02e0143b)
