# info de la materia: ST0263-7290

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
- **Definición de arquitectura distribuida**: Imlementamos una arquitectura distribuida con múltiples instancias de MOM y un Routing Tier
- **Tolerancia a fallos en servidores**: Usamos la redundancia a través de la creación de varias instancias de la MOM. Sin embargo, somos dependientes de que el Zookeeper no se caiga.
- **Modelo de interacción asíncrona**: Dado que las MOM funcionan perfectamente
- **Multiusuario**: Cualquier usuario se puede autenticar para interactuar con la aplicación.
- **Consideraciones de escalabilidad**
- **Transparencia**: El usuario nunca tiene acceso unicamente al auth, el envío y la recepción de mensajes.
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

### **Mejores prácticas**
- **Escalabilidad**: La arquitectura distribuida permite agregar más instancias MOM según la demanda.
- **Separación de responsabilidades**: Cada componente (Routing Tier, MOM, Cliente) tiene una función específica.
- **Uso de APIs REST**: Los servicios están expuestos como APIs REST, facilitando la integración con otros sistemas.
- **Tolerancia a fallos**: Se implementa redundancia en las instancias MOM, aunque dependan de la disponibilidad de Zookeeper.
- **Modelo síncrono y asíncrono**: El sistema utiliza colas y tópicos para manejar mensajes de manera asíncrona en la comunicación con la MOM. Además, usa gRPC para que las peticiones del cliente lleguen a la MOM y se permita esta comunicación exitosamente.



## 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

como se compila y ejecuta.
detalles del desarrollo.
detalles técnicos
descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)

opcionalmente - si quiere mostrar resultados o pantallazos

## 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

IP o nombres de dominio en nube o en la máquina servidor.

descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

como se lanza el servidor.

una mini guia de como un usuario utilizaría el software o la aplicación

opcionalmente - si quiere mostrar resultados o pantallazos

## 5. otra información que considere relevante para esta actividad.

# Referencias:
## sitio1-url
## sitio2-url
## url de donde tomo info para desarrollar este proyecto
