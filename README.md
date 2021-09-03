# 70-anios-de-nuestro-chaco

Aplicación Quiz hecha en Django para conmemorar los 70 años de la provincia del Chaco, siguiendo el patrón MVT y haciendo uso de base de datos PostgreSQL.

### Resumen

- Perfil Administrador: Habilitado a cargar preguntas y respuestas a un banco aleatorio y conocer estadísticas de acceso y participantes.

    ![Image description](https://i.imgur.com/XlaA3Fh.png)

- Perfil Usuario: Habilitado a registrarse, autenticarse, jugar y compartir resultados.

El esquema de base de datos propuesto es el siguiente (sin tener en cuenta las tablas generadas por el ORM de Django):

  ![Image description](https://i.imgur.com/yUzOZnw.png)

### Para correr localmente el proyecto

- Se recomienda crear un entorno virtual ejecutando el siguiente comando desde su consola:
		
      virtualenv [nombre del entorno]

- Moverse a la carpeta creada, entrar a la carpeta Scripts y ejecutar el comando _activate_

      cd [nombre del entorno]/Scripts
    
      activate
    
- Paso siguiente, clonar este repositorio, entrar a la carpeta correspondiente, y ejecutar los siguientes comandos:

      pip install -r requirements.txt

      python manage.py makemigrations

      python manage.py migrate

      python manage.py runserver

- En un navegador web, acceder a _http://localhost:8000_

- Para el perfil del administrador, acceder a _http://localhost:8000/admin_