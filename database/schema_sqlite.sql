CREATE TABLE IF NOT EXISTS Rol (
  id_rol INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE,
  descripcion TEXT,
  estado INTEGER NOT NULL DEFAULT 1,
  eliminado INTEGER NOT NULL DEFAULT 0,
  fecha_creacion TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS Usuario (
  id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  nombres TEXT NOT NULL,
  apellidos TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  telefono TEXT,
  direccion TEXT,
  estado_activo INTEGER NOT NULL DEFAULT 1,
  eliminado INTEGER NOT NULL DEFAULT 0,
  fecha_creacion TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  id_rol INTEGER NOT NULL,
  FOREIGN KEY(id_rol) REFERENCES Rol(id_rol)
);

CREATE TABLE IF NOT EXISTS TipoPago (
  id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE,
  descripcion TEXT,
  estado INTEGER NOT NULL DEFAULT 1,
  eliminado INTEGER NOT NULL DEFAULT 0,
  fecha_creacion TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS Estado (
  id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE,
  descripcion TEXT,
  estado INTEGER NOT NULL DEFAULT 1,
  eliminado INTEGER NOT NULL DEFAULT 0,
  fecha_creacion TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS Especialidad (
  id_especialidad INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE,
  descripcion TEXT,
  precio_base REAL NOT NULL DEFAULT 80.00,
  estado INTEGER NOT NULL DEFAULT 1,
  eliminado INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Medico (
  id_medico INTEGER PRIMARY KEY AUTOINCREMENT,
  nombres TEXT NOT NULL,
  apellidos TEXT NOT NULL,
  genero TEXT NOT NULL CHECK (genero IN ('M','F')),
  fecha_nacimiento TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  telefono TEXT,
  numero_colegiatura TEXT UNIQUE,
  id_especialidad INTEGER NOT NULL,
  estado INTEGER NOT NULL DEFAULT 1,
  eliminado INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(id_especialidad) REFERENCES Especialidad(id_especialidad)
);

CREATE TABLE IF NOT EXISTS Paciente (
  id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
  dni TEXT UNIQUE,
  nombres TEXT NOT NULL,
  apellidos TEXT NOT NULL,
  genero TEXT CHECK (genero IN ('M','F')),
  fecha_nacimiento TEXT NOT NULL,
  email TEXT UNIQUE,
  telefono TEXT,
  direccion TEXT,
  grupo_sanguineo TEXT,
  contacto_emergencia TEXT,
  telefono_emergencia TEXT,
  alergias TEXT,
  enfermedades_cronicas TEXT,
  observaciones TEXT,
  estado INTEGER NOT NULL DEFAULT 1,
  eliminado INTEGER NOT NULL DEFAULT 0,
  fecha_creacion TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE IF NOT EXISTS Reservacion (
  id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  nota TEXT,
  mensaje TEXT,
  fecha_cita TEXT NOT NULL,
  hora_cita TEXT NOT NULL,
  sintomas TEXT,
  observaciones TEXT,
  precio REAL NOT NULL CHECK (precio >= 0),
  creado_en TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  estado INTEGER NOT NULL DEFAULT 1,
  eliminado INTEGER NOT NULL DEFAULT 0,
  id_paciente INTEGER NOT NULL,
  id_usuario INTEGER NOT NULL,
  id_medico INTEGER NOT NULL,
  id_pago INTEGER NOT NULL,
  id_estado INTEGER NOT NULL,
  FOREIGN KEY(id_paciente) REFERENCES Paciente(id_paciente),
  FOREIGN KEY(id_usuario) REFERENCES Usuario(id_usuario),
  FOREIGN KEY(id_medico) REFERENCES Medico(id_medico),
  FOREIGN KEY(id_pago) REFERENCES TipoPago(id_pago),
  FOREIGN KEY(id_estado) REFERENCES Estado(id_estado)
);

CREATE TABLE IF NOT EXISTS Factura (
  id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
  numero_factura TEXT NOT NULL UNIQUE,
  id_paciente INTEGER NOT NULL,
  id_reserva INTEGER,
  fecha_factura TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  subtotal REAL NOT NULL DEFAULT 0,
  igv REAL NOT NULL DEFAULT 0,
  total REAL NOT NULL DEFAULT 0,
  estado_pago TEXT NOT NULL CHECK (estado_pago IN ('PENDIENTE','REPORTADO','PAGADO','ANULADO')),
  motivo_anulacion TEXT,
  eliminado INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY(id_paciente) REFERENCES Paciente(id_paciente),
  FOREIGN KEY(id_reserva) REFERENCES Reservacion(id_reserva)
);

CREATE TABLE IF NOT EXISTS DetalleFactura (
  id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
  id_factura INTEGER NOT NULL,
  descripcion TEXT NOT NULL,
  cantidad INTEGER NOT NULL CHECK (cantidad > 0),
  precio_unitario REAL NOT NULL CHECK (precio_unitario >= 0),
  subtotal REAL NOT NULL CHECK (subtotal >= 0),
  FOREIGN KEY(id_factura) REFERENCES Factura(id_factura)
);

CREATE TABLE IF NOT EXISTS Pago (
  id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
  id_factura INTEGER NOT NULL,
  id_pago INTEGER NOT NULL,
  monto REAL NOT NULL CHECK (monto >= 0),
  fecha_pago TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  usuario_registro INTEGER NOT NULL,
  observacion TEXT,
  FOREIGN KEY(id_factura) REFERENCES Factura(id_factura),
  FOREIGN KEY(id_pago) REFERENCES TipoPago(id_pago),
  FOREIGN KEY(usuario_registro) REFERENCES Usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS PagoReportado (
  id_reporte INTEGER PRIMARY KEY AUTOINCREMENT,
  id_factura INTEGER NOT NULL,
  id_pago INTEGER NOT NULL,
  monto REAL NOT NULL CHECK (monto >= 0),
  fecha_reporte TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  usuario_registro INTEGER NOT NULL,
  observacion TEXT,
  estado TEXT NOT NULL DEFAULT 'REPORTADO' CHECK (estado IN ('REPORTADO','VALIDADO','RECHAZADO')),
  FOREIGN KEY(id_factura) REFERENCES Factura(id_factura),
  FOREIGN KEY(id_pago) REFERENCES TipoPago(id_pago),
  FOREIGN KEY(usuario_registro) REFERENCES Usuario(id_usuario)
);

CREATE TABLE IF NOT EXISTS Auditoria (
  id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
  tabla TEXT NOT NULL,
  accion TEXT NOT NULL,
  usuario_bd TEXT NOT NULL,
  fecha TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  datos_anteriores TEXT,
  datos_nuevos TEXT
);

CREATE INDEX IF NOT EXISTS IX_Reservacion_Fecha ON Reservacion(fecha_cita);
CREATE INDEX IF NOT EXISTS IX_Reservacion_Medico ON Reservacion(id_medico);
CREATE INDEX IF NOT EXISTS IX_Factura_Paciente ON Factura(id_paciente);
CREATE INDEX IF NOT EXISTS IX_Factura_Estado ON Factura(estado_pago);
