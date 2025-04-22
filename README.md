# info de la materia: ST0263-7290

# Estudiante(s):
- Daniel Correa Botero, dcorreab2@eafit.edu.co
- Miguel Ángel Cano Salinas, macanos1@eafit.edu.co
- Santiago Acevedo Urrego, sacevedou1@eafit.edu.co

# Profesor:
- Edwin Montoya, emontoya@eafit.edu.co

# Proyecto 1: Diseño e Implementación de un MOM entre aplicaciones

## 1. Breve descripción de la actividad

### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

## 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

## 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

como se compila y ejecuta.
detalles del desarrollo.
detalles técnicos
descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)

opcionalmente - si quiere mostrar resultados o pantallazos

## 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## IP o nombres de dominio en nube o en la máquina servidor:

- **Cliente React**: [http://13.219.188.33](http://13.219.188.33)
- **Servidor Backend**: [http://your-backend-ip-or-domain](http:/107.22.123.0:500) 

### Configuración de Parámetros
- **IP Cliente React**: `http://13.219.188.33`
- **IP Servidor Backend**: `http://107.22.123.0:5000`
- **Puerto del Servidor**: `5000` 

descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor:

Cada ino de los siguientes componentes deben desplegarse en maquinas virtuales diferentes.

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

Ejecutar estos comandos para generar la imagen en docker y iniciar la el contenedor (recordar cambiar la ip privada):

```{bash}
    sudo docker build --force-rm -t grpcServer/latest . --no-cache
    sudo docker run -d --restart always   -e HOST_IP=<ip_prvada_host>   -p 5001:5001 -p 50051:50051   --name grpc-server   grpcServer/latest:latest
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
De esta manera se despliega el cliente React y se usa nginx como proxy inverso para mapear el trafico al puerto 80


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


## 5. otra información que considere relevante para esta actividad.

# Referencias:
## sitio1-url
## sitio2-url
## url de donde tomo info para desarrollar este proyecto