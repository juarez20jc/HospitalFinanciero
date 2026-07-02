# Clinica Ana San Gabriel - Sistema Financiero Hospitalario

Sistema web en Python para gestionar el flujo financiero de una clinica:
pacientes, citas, facturacion, pagos, caja diaria, cuentas por cobrar,
reportes, auditoria y usuarios por rol.

## Como ejecutar

1. Abre XAMPP y enciende `MySQL`.
2. Instala dependencias si aun no lo hiciste:

```powershell
.\instalar_dependencias.bat
```

3. Abre la version web local:

```powershell
python open_web_local.py
```

Tambien puedes usar doble clic en `iniciar_web_local.bat`.

## Credenciales demo

- Administrador: `admin / Admin123!`
- Recepcion: `recepcion / Recepcion123!`
- Caja: `caja / Caja123!`
- Paciente: `paciente / Paciente123!`

## Base de datos

La version principal usa MySQL con esta configuracion por defecto:

- Host: `127.0.0.1`
- Puerto: `3306`
- Usuario: `root`
- Password: vacio
- Base de datos: `hospital_financiero`

Para crear la base desde phpMyAdmin:

1. Ejecuta `database/hospital_financiero_mysql_completo.sql`.

Ese archivo ya incluye el esquema y los datos de demostracion en una sola importacion.

## Estructura del proyecto

```text
assets/       Estilos, JavaScript e imagenes de la interfaz.
controllers/  Clases controladoras que coordinan cada modulo.
database/     Conexion, consultas SQL, esquema y datos iniciales.
models/       Clases de datos del dominio.
reports/      Carpeta reservada para exportaciones.
views/        Construccion HTML de las pantallas.
main.py       Servidor HTTP, rutas, sesiones y permisos.
open_web_local.py  Arranque web local con navegador.
desktop_app.py     Arranque opcional como ventana de escritorio.
```
