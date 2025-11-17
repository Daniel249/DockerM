# Arquitectura de la Plataforma Moodle - Docker

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USUARIO / NAVEGADOR                         │
│                     http://localhost:8080                            │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 │ HTTP Request
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        DOCKER HOST (Windows)                         │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Docker Network (mood_default)             │   │
│  │                                                               │   │
│  │  ┌──────────────────────────┐    ┌──────────────────────┐   │   │
│  │  │   WEB CONTAINER          │    │   DB CONTAINER       │   │   │
│  │  │   (mood-web-1)           │    │   (mood-db-1)        │   │   │
│  │  │                          │    │                      │   │   │
│  │  │  ┌────────────────────┐  │    │  ┌────────────────┐ │   │   │
│  │  │  │   Apache HTTP      │  │    │  │   MariaDB 11   │ │   │   │
│  │  │  │   Server           │  │    │  │                │ │   │   │
│  │  │  │   Puerto: 80       │  │    │  │   Puerto: 3306 │ │   │   │
│  │  │  └────────┬───────────┘  │    │  └────────┬───────┘ │   │   │
│  │  │           │              │    │           │         │   │   │
│  │  │  ┌────────▼───────────┐  │    │  ┌────────▼───────┐ │   │   │
│  │  │  │   PHP 8.2          │  │◄───┼──┤  Base de Datos │ │   │   │
│  │  │  │                    │  │    │  │  - moodle      │ │   │   │
│  │  │  │  Extensiones:      │  │    │  │  - utf8mb4     │ │   │   │
│  │  │  │  • mysqli          │  │    │  │                │ │   │   │
│  │  │  │  • pdo_mysql       │  │    │  │  Usuario:      │ │   │   │
│  │  │  │  • gd              │  │    │  │  - moodle      │ │   │   │
│  │  │  │  • zip             │  │    │  └────────────────┘ │   │   │
│  │  │  │  • intl            │  │    │                      │   │   │
│  │  │  │  • soap            │  │    └──────────────────────┘   │   │
│  │  │  │  • opcache         │  │              ▲                │   │
│  │  │  │  • exif            │  │              │                │   │
│  │  │  └────────┬───────────┘  │              │ SQL Queries   │   │
│  │  │           │              │              │                │   │
│  │  │  ┌────────▼───────────┐  │              │                │   │
│  │  │  │  Moodle 4.4        │  │──────────────┘                │   │
│  │  │  │                    │  │                                │   │
│  │  │  │  /var/www/html/    │  │                                │   │
│  │  │  │  • index.php       │  │                                │   │
│  │  │  │  • config.php      │  │                                │   │
│  │  │  │  • themes/         │  │                                │   │
│  │  │  │  • mod/            │  │                                │   │
│  │  │  │  • blocks/         │  │                                │   │
│  │  │  └────────────────────┘  │                                │   │
│  │  │                          │                                │   │
│  │  │  Puerto: 8080:80         │                                │   │
│  │  └──────────┬───────────────┘                                │   │
│  │             │                                                 │   │
│  └─────────────┼─────────────────────────────────────────────────┘   │
│                │                                                     │
│  ┌─────────────▼─────────────────────────────────────────────────┐  │
│  │                    VOLÚMENES PERSISTENTES                      │  │
│  │                                                                 │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐ │  │
│  │  │  ./www/          │  │  ./db_data/      │  │ moodledata/ │ │  │
│  │  │                  │  │                  │  │             │ │  │
│  │  │  Host Directory  │  │  Host Directory  │  │  Container  │ │  │
│  │  │                  │  │                  │  │  Volume     │ │  │
│  │  │  ↕                │  │  ↕                │  │  ↕          │ │  │
│  │  │  /var/www/html   │  │  /var/lib/mysql  │  │/var/        │ │  │
│  │  │  (en web)        │  │  (en db)         │  │ moodledata  │ │  │
│  │  │                  │  │                  │  │ (en web)    │ │  │
│  │  │  Archivos Moodle │  │  Datos MySQL     │  │ Archivos    │ │  │
│  │  │  • Código        │  │  • Tablas        │  │ Subidos     │ │  │
│  │  │  • Temas         │  │  • Usuarios      │  │ • Uploads   │ │  │
│  │  │  • Plugins       │  │  • Cursos        │  │ • Caché     │ │  │
│  │  │  • Config        │  │  • Actividades   │  │ • Sesiones  │ │  │
│  │  └──────────────────┘  └──────────────────┘  └─────────────┘ │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘

FLUJO DE DATOS:
═══════════════

1. Usuario → http://localhost:8080
2. Docker Host → Mapea puerto 8080 a puerto 80 del contenedor web
3. Apache → Recibe request HTTP
4. PHP → Procesa archivos Moodle en /var/www/html
5. Moodle → Consulta base de datos vía mysqli/pdo
6. MariaDB → Devuelve datos (usuarios, cursos, configuración)
7. PHP → Genera HTML/CSS/JS
8. Apache → Envía respuesta al navegador
9. Archivos persistidos en volúmenes locales (www/, db_data/)

CONFIGURACIÓN:
═══════════════

docker-compose.yml:
  • Define servicios (web, db)
  • Mapea puertos (8080:80)
  • Monta volúmenes
  • Establece red interna
  • Variables de entorno (DB credentials)

.gitignore:
  • Excluye datos sensibles (db_data/, config.php)
  • Incluye código Moodle (www/)
```

## Componentes Clave:

### Capa de Presentación:
- **Navegador** → Interfaz usuario

### Capa de Aplicación:
- **Apache HTTP Server** → Servidor web
- **PHP 8.2** → Procesamiento lógica
- **Moodle 4.4** → Sistema LMS

### Capa de Datos:
- **MariaDB 11** → Base de datos relacional
- **Volúmenes Docker** → Persistencia

### Infraestructura:
- **Docker Containers** → Aislamiento
- **Docker Network** → Comunicación interna
- **Volume Mounts** → Sincronización host-contenedor
