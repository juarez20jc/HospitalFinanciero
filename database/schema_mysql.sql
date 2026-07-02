CREATE DATABASE IF NOT EXISTS hospital_financiero CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hospital_financiero;

CREATE TABLE Rol (
  id_rol INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  descripcion VARCHAR(255),
  estado TINYINT(1) NOT NULL DEFAULT 1,
  eliminado TINYINT(1) NOT NULL DEFAULT 0,
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  nombres VARCHAR(100) NOT NULL,
  apellidos VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  telefono VARCHAR(20),
  direccion VARCHAR(255),
  estado_activo TINYINT(1) NOT NULL DEFAULT 1,
  eliminado TINYINT(1) NOT NULL DEFAULT 0,
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  id_rol INT NOT NULL,
  CONSTRAINT FK_Usuario_Rol FOREIGN KEY(id_rol) REFERENCES Rol(id_rol)
);

CREATE TABLE TipoPago (
  id_pago INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  descripcion VARCHAR(255),
  estado TINYINT(1) NOT NULL DEFAULT 1,
  eliminado TINYINT(1) NOT NULL DEFAULT 0,
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Estado (
  id_estado INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  descripcion VARCHAR(255),
  estado TINYINT(1) NOT NULL DEFAULT 1,
  eliminado TINYINT(1) NOT NULL DEFAULT 0,
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Especialidad (
  id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  descripcion VARCHAR(255),
  precio_base DECIMAL(10,2) NOT NULL DEFAULT 80.00,
  estado TINYINT(1) NOT NULL DEFAULT 1,
  eliminado TINYINT(1) NOT NULL DEFAULT 0
);

CREATE TABLE Medico (
  id_medico INT AUTO_INCREMENT PRIMARY KEY,
  nombres VARCHAR(100) NOT NULL,
  apellidos VARCHAR(100) NOT NULL,
  genero CHAR(1) NOT NULL CHECK (genero IN ('M','F')),
  fecha_nacimiento DATE NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  telefono VARCHAR(20),
  numero_colegiatura VARCHAR(50) UNIQUE,
  id_especialidad INT NOT NULL,
  estado TINYINT(1) NOT NULL DEFAULT 1,
  eliminado TINYINT(1) NOT NULL DEFAULT 0,
  CONSTRAINT FK_Medico_Especialidad FOREIGN KEY(id_especialidad) REFERENCES Especialidad(id_especialidad)
);

CREATE TABLE Paciente (
  id_paciente INT AUTO_INCREMENT PRIMARY KEY,
  dni VARCHAR(15) UNIQUE,
  nombres VARCHAR(100) NOT NULL,
  apellidos VARCHAR(100) NOT NULL,
  genero CHAR(1) CHECK (genero IN ('M','F')),
  fecha_nacimiento DATE NOT NULL,
  email VARCHAR(255) UNIQUE,
  telefono VARCHAR(20),
  direccion VARCHAR(255),
  grupo_sanguineo VARCHAR(5),
  contacto_emergencia VARCHAR(100),
  telefono_emergencia VARCHAR(20),
  alergias TEXT,
  enfermedades_cronicas TEXT,
  observaciones TEXT,
  estado TINYINT(1) NOT NULL DEFAULT 1,
  eliminado TINYINT(1) NOT NULL DEFAULT 0,
  fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Reservacion (
  id_reserva INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(150) NOT NULL,
  nota TEXT,
  mensaje TEXT,
  fecha_cita DATE NOT NULL,
  hora_cita TIME NOT NULL,
  sintomas TEXT,
  observaciones TEXT,
  precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
  creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  estado TINYINT(1) NOT NULL DEFAULT 1,
  eliminado TINYINT(1) NOT NULL DEFAULT 0,
  id_paciente INT NOT NULL,
  id_usuario INT NOT NULL,
  id_medico INT NOT NULL,
  id_pago INT NOT NULL,
  id_estado INT NOT NULL,
  CONSTRAINT FK_Reservacion_Paciente FOREIGN KEY(id_paciente) REFERENCES Paciente(id_paciente),
  CONSTRAINT FK_Reservacion_Usuario FOREIGN KEY(id_usuario) REFERENCES Usuario(id_usuario),
  CONSTRAINT FK_Reservacion_Medico FOREIGN KEY(id_medico) REFERENCES Medico(id_medico),
  CONSTRAINT FK_Reservacion_Pago FOREIGN KEY(id_pago) REFERENCES TipoPago(id_pago),
  CONSTRAINT FK_Reservacion_Estado FOREIGN KEY(id_estado) REFERENCES Estado(id_estado)
);

CREATE TABLE Factura (
  id_factura INT AUTO_INCREMENT PRIMARY KEY,
  numero_factura VARCHAR(50) NOT NULL UNIQUE,
  id_paciente INT NOT NULL,
  id_reserva INT NULL,
  fecha_factura DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  subtotal DECIMAL(10,2) NOT NULL DEFAULT 0,
  igv DECIMAL(10,2) NOT NULL DEFAULT 0,
  total DECIMAL(10,2) NOT NULL DEFAULT 0,
  estado_pago VARCHAR(20) NOT NULL CHECK (estado_pago IN ('PENDIENTE','REPORTADO','PAGADO','ANULADO')),
  motivo_anulacion VARCHAR(255),
  eliminado TINYINT(1) NOT NULL DEFAULT 0,
  CONSTRAINT FK_Factura_Paciente FOREIGN KEY(id_paciente) REFERENCES Paciente(id_paciente),
  CONSTRAINT FK_Factura_Reservacion FOREIGN KEY(id_reserva) REFERENCES Reservacion(id_reserva)
);

CREATE TABLE DetalleFactura (
  id_detalle INT AUTO_INCREMENT PRIMARY KEY,
  id_factura INT NOT NULL,
  descripcion VARCHAR(255) NOT NULL,
  cantidad INT NOT NULL CHECK (cantidad > 0),
  precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario >= 0),
  subtotal DECIMAL(10,2) NOT NULL CHECK (subtotal >= 0),
  CONSTRAINT FK_DetalleFactura_Factura FOREIGN KEY(id_factura) REFERENCES Factura(id_factura)
);

CREATE TABLE Pago (
  id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
  id_factura INT NOT NULL,
  id_pago INT NOT NULL,
  monto DECIMAL(10,2) NOT NULL CHECK (monto >= 0),
  fecha_pago DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  usuario_registro INT NOT NULL,
  observacion VARCHAR(255),
  CONSTRAINT FK_Pago_Factura FOREIGN KEY(id_factura) REFERENCES Factura(id_factura),
  CONSTRAINT FK_Pago_TipoPago FOREIGN KEY(id_pago) REFERENCES TipoPago(id_pago),
  CONSTRAINT FK_Pago_Usuario FOREIGN KEY(usuario_registro) REFERENCES Usuario(id_usuario)
);

CREATE TABLE PagoReportado (
  id_reporte INT AUTO_INCREMENT PRIMARY KEY,
  id_factura INT NOT NULL,
  id_pago INT NOT NULL,
  monto DECIMAL(10,2) NOT NULL CHECK (monto >= 0),
  fecha_reporte DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  usuario_registro INT NOT NULL,
  observacion VARCHAR(255),
  estado VARCHAR(20) NOT NULL DEFAULT 'REPORTADO' CHECK (estado IN ('REPORTADO','VALIDADO','RECHAZADO')),
  CONSTRAINT FK_PagoReportado_Factura FOREIGN KEY(id_factura) REFERENCES Factura(id_factura),
  CONSTRAINT FK_PagoReportado_TipoPago FOREIGN KEY(id_pago) REFERENCES TipoPago(id_pago),
  CONSTRAINT FK_PagoReportado_Usuario FOREIGN KEY(usuario_registro) REFERENCES Usuario(id_usuario)
);

CREATE TABLE Auditoria (
  id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
  tabla VARCHAR(100) NOT NULL,
  accion VARCHAR(30) NOT NULL,
  usuario_bd VARCHAR(100) NOT NULL,
  fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  datos_anteriores TEXT,
  datos_nuevos TEXT
);

CREATE INDEX IX_Reservacion_Fecha ON Reservacion(fecha_cita);
CREATE INDEX IX_Reservacion_Medico ON Reservacion(id_medico);
CREATE INDEX IX_Factura_Paciente ON Factura(id_paciente);
CREATE INDEX IX_Factura_Estado ON Factura(estado_pago);
