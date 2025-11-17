# PROYECTO VIAJEROS

## Introduccion

En el presente se encuentra el contenido del trabajo realizado como proyecto final para la carrera de Ingenieria en la universidad del Norte - Barranquilla, Colombia.

Con este se busca proveer un lugar digital en el que acumular el conocimiento cultural de la costa colombiana y principalmente de la urbanidad de Puerto Colombia.

Este proyecto fue encargado por las PROFESORAS_ del departamento de la Universidad del Norte con intencion de manejarlo y verlo funcionar en el futuro, y encuentra su publico en los estudiantes de primaria y bachillerato de los colegios en la zona aledaña al caso urbano de Puerto Colombia, quienes se verian beneficiados de entender y conocer sus raices historicas y entorno cultural. 

En la actualidad el equipo de desarrollo conformado por los estudiantes cursando ultimo semestre cumplen el rol de administradores de la pagina. A esto en un plazo de tiempo se le otorgara a las profesoras el permiso de manager del sitio.

## Informacion de la Plataforma

Se construyo' en la plataforma Moodle que se encuentra en modalidad opensouce bajo la licensia GNU v3.  

Documentacion en el siguiente enlace [(link)](https://docs.moodle.org/501/en/Main_page)

Este proyecto tambien esta abierto a modificacion y duplicacion aditiva mediante repositorio de Github.

Sobre el stack podemos decir que esta compuesto por PHP como lenguaje principal, Apache o Nginx como servidor web, MySQL/MariaDB o PostgreSQL como base de datos, y una interfaz web basada en HTML, CSS y JavaScript, además de soportar extensiones mediante plugins y ejecutarse típicamente bajo Linux en entornos LAMP/LEMP.



## Metodo de Uso

Para correrlo visite la pagina apropiada y cargue en su navegador el sitio con la herramienta y catalogo de cursos desde cualquier sistema operativo o plataforma. Su manejo es similar al de cualquier sitio con funcion de sistema de administracion de cursos (LMS).  
Dependiendo del rol asociado del usuario podra':  
crear cursos  
inscribir estudiantes  
subir contenido  
hacer evaluaciones  
hacer seguimiento academico

## Filosofia de Producto/Servicio

Buscamos ofrecer una plataforma para que los tenientes de contenido cultural relevante, asi como los estudiantes, o en su defecto personas interesadas en mantener vivo la identidad cultural de Puerto Colombia y su patrimonio, puedan unirse en un lugar en linea y hecho para sus necesidades.

## Gestion de Desarrollo

En el desarrollo del proyecto se aplicó la metodología Scrum, organizando el trabajo en sprints iterativos y gestionando el avance mediante artefactos como el Product Backlog y el Sprint Backlog. El equipo colaboró de forma continua a través de ceremonias clave —Daily Scrum, Sprint Planning y Sprint Review— lo que permitió priorizar requisitos, ajustar entregables de manera ágil y garantizar una mejora incremental del producto en cada iteración.

## Blackbox Unit Testing

Se implementaron sistemas de testeo de caja negra para demostrar la validez y funcionalidad de los valores asociados y stack de desarrollo.


Lo que Prueban los Tests:  

**Tests de Base de Datos:**

Contenedor corriendo
Puerto 3306 expuesto
Configuración UTF-8
Base de datos Moodle existe
Usuario Moodle tiene acceso


**Tests del Contenedor Web:**

Contenedor corriendo
Apache responde en puerto 8080
PHP 8.2 instalado
Extensiones PHP requeridas (mysqli, pdo, gd, zip, intl, soap, opcache, exif)
Permisos correctos (775)
Directorio de datos Moodle existe
Mapeo de puerto 8080→80


**Tests de Instalación Moodle:**

Archivos esenciales existen (index.php, version.php, archivos lib)
Interfaz web accesible
Archivo config existe
Archivos de temas presentes
Versión es 4.4
Archivos propiedad de www-data


**Tests de Docker Compose:**

Archivo existe y YAML válido
Ambos servicios definidos (web & db)
Imágenes correctas (php:8.2-apache, mariadb:11)
Mapeo de puertos configurado
Volúmenes mapeados correctamente
Variables de entorno establecidas
Dependencias de servicios configuradas


**Tests de Volúmenes:**

Directorios en host existen (www/, db_data/)
Directorios no vacíos
Volúmenes montados en contenedores
Datos persisten entre reinicios