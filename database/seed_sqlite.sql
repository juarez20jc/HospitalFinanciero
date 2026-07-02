INSERT INTO Rol(nombre, descripcion) VALUES
('ADMINISTRADOR', 'Control total del sistema'),
('RECEPCION', 'Gestion de pacientes, citas y facturacion'),
('CAJA', 'Control de pagos, caja diaria y cuentas por cobrar'),
('PACIENTE', 'Portal basico del paciente');

INSERT INTO Usuario(username, nombres, apellidos, email, password_hash, telefono, direccion, id_rol) VALUES
('admin', 'Ana', 'Benavides', 'admin@clinicaanasangabriel.pe', '664819d8c5343676c9225b5ed00a5cdc6f3a1ff3', '999111222', 'Av. Primavera 1500, Surco', 1),
('recepcion', 'Lucia', 'Mendoza', 'recepcion@clinicaanasangabriel.pe', '14652ecd8150050c255e426499c622a782857f85', '999333444', 'Surco', 2),
('caja', 'Mateo', 'Rivas', 'caja@clinicaanasangabriel.pe', 'e104ac1d7e740920d8e4fdc3f66f4f54fd6c87e7', '999555666', 'Surco', 3),
('paciente', 'Juan', 'Perez', 'juan.perez@mail.com', 'f927aa5d95179fb135e8adbde27dc130087f8710', '987654321', 'Miraflores', 4),
('40881234', 'Maria', 'Gonzales', 'maria.gonzales@mail.com', 'd046f2babd914cd37e8b1981f90b1429c23eac20', '976543210', 'Surco', 4),
('72123456', 'Carlos', 'Ramos', 'carlos.ramos@mail.com', 'bb9bd77195c371899172e8db5d764e6e4f6b5360', '965432109', 'Barranco', 4),
('70234567', 'Ana', 'Castro', 'ana.castro@mail.com', 'e437fecd1cc5bf93e71b46c86cd930147a716edb', '954321098', 'San Borja', 4),
('73456789', 'Luis', 'Medina', 'luis.medina@mail.com', '56e4d19df80d6f1782e1eb543dcf27f3879e4198', '943210987', 'Chorrillos', 4),
('62345678', 'Sofia', 'Vega', 'sofia.vega@mail.com', '207d863d7df134fe17b8f3e6959860a5ebdb3eab', '932109876', 'Miraflores', 4),
('61234567', 'Roberto', 'Flores', 'roberto.flores@mail.com', 'c2e5b3622deeccfea6cc667b4e8506ca978a21d0', '921098765', 'Surquillo', 4);

INSERT INTO TipoPago(nombre, descripcion) VALUES
('EFECTIVO', 'Pago en efectivo'),
('TARJETA', 'Pago con tarjeta'),
('TRANSFERENCIA', 'Transferencia bancaria'),
('YAPE', 'Pago por Yape'),
('PLIN', 'Pago por Plin');

INSERT INTO Estado(nombre, descripcion) VALUES
('PENDIENTE', 'Cita pendiente'),
('CONFIRMADA', 'Cita confirmada'),
('CANCELADA', 'Cita cancelada'),
('ATENDIDA', 'Paciente atendido');

INSERT INTO Especialidad(nombre, descripcion, precio_base) VALUES
('Consulta General', 'Medicina general y evaluacion inicial', 80.00),
('Cardiologia', 'Consulta cardiologica especializada', 150.00),
('Pediatria', 'Atencion integral pediatrica', 100.00),
('Dermatologia', 'Consulta dermatologica', 120.00);

INSERT INTO Medico(nombres, apellidos, genero, fecha_nacimiento, email, telefono, numero_colegiatura, id_especialidad) VALUES
('Rafael', 'Lopez', 'M', '1978-04-12', 'rlopez@clinicaanasangabriel.pe', '944111222', 'CMP-15420', 2),
('Valeria', 'Soto', 'F', '1985-08-03', 'vsoto@clinicaanasangabriel.pe', '944222333', 'CMP-23210', 3),
('Camila', 'Torres', 'F', '1982-11-21', 'ctorres@clinicaanasangabriel.pe', '944333444', 'CMP-19888', 4),
('Diego', 'Herrera', 'M', '1975-01-19', 'dherrera@clinicaanasangabriel.pe', '944444555', 'CMP-12111', 1),
('Mariana', 'Quispe', 'F', '1980-06-09', 'mquispe@clinicaanasangabriel.pe', '944555666', 'CMP-26740', 1);

INSERT INTO Paciente(dni, nombres, apellidos, genero, fecha_nacimiento, email, telefono, direccion, grupo_sanguineo, contacto_emergencia, telefono_emergencia, alergias, enfermedades_cronicas, observaciones) VALUES
('45678912', 'Juan', 'Perez', 'M', '1992-02-15', 'juan.perez@mail.com', '987654321', 'Av. Benavides 120', 'O+', 'Maria Perez', '999888777', 'Penicilina', 'Ninguna', 'Paciente afiliado'),
('40881234', 'Maria', 'Gonzales', 'F', '1988-07-24', 'maria.gonzales@mail.com', '976543210', 'Surco', 'A+', 'Luis Gonzales', '999777666', 'Ninguna', 'Hipertension', 'Control trimestral'),
('72123456', 'Carlos', 'Ramos', 'M', '1979-12-02', 'carlos.ramos@mail.com', '965432109', 'Barranco', 'B-', 'Ana Ramos', '999666555', 'Mariscos', 'Diabetes tipo 2', 'Preferencia turno tarde'),
('70234567', 'Ana', 'Castro', 'F', '1995-03-18', 'ana.castro@mail.com', '954321098', 'San Borja', 'O-', 'Pedro Castro', '999222111', 'Ninguna', 'Ninguna', 'Paciente nuevo'),
('73456789', 'Luis', 'Medina', 'M', '1983-10-11', 'luis.medina@mail.com', '943210987', 'Chorrillos', 'AB+', 'Rosa Medina', '999333222', 'Ibuprofeno', 'Asma leve', 'Requiere seguimiento'),
('62345678', 'Sofia', 'Vega', 'F', '2001-05-29', 'sofia.vega@mail.com', '932109876', 'Miraflores', 'A-', 'Carmen Vega', '999444333', 'Ninguna', 'Ninguna', 'Estudiante'),
('61234567', 'Roberto', 'Flores', 'M', '1968-09-07', 'roberto.flores@mail.com', '921098765', 'Surquillo', 'B+', 'Elena Flores', '999555444', 'Lactosa', 'Hipertension', 'Control mensual');

INSERT INTO Reservacion(titulo, nota, mensaje, fecha_cita, hora_cita, sintomas, observaciones, precio, id_paciente, id_usuario, id_medico, id_pago, id_estado) VALUES
('Consulta Cardiologia', 'Primera cita', 'Confirmar asistencia', DATE('now'), '10:00:00', 'Dolor toracico leve', 'Se cobra en caja', 150.00, 1, 2, 1, 4, 4),
('Consulta Pediatria', 'Control regular', 'Paciente menor de edad', DATE('now','+1 day'), '12:30:00', 'Control general', 'Pago pendiente', 100.00, 2, 2, 2, 1, 2),
('Dermatologia', 'Lesion cutanea', 'Traer examenes previos', DATE('now','-1 day'), '09:30:00', 'Irritacion', 'Atendido', 120.00, 3, 2, 3, 2, 4),
('Consulta General', 'Evaluacion inicial', 'Llegar 15 minutos antes', DATE('now'), '08:30:00', 'Dolor de cabeza', 'Pago en efectivo', 80.00, 4, 2, 5, 1, 4),
('Dermatologia', 'Control de piel', 'Usar bloqueador previo', DATE('now','+1 day'), '16:00:00', 'Manchas en piel', 'Pago por transferencia', 120.00, 5, 2, 3, 3, 4),
('Consulta Cardiologia', 'Control de presion', 'Traer examenes', DATE('now','-7 days'), '11:00:00', 'Presion alta', 'Atendido', 150.00, 6, 2, 1, 2, 4),
('Consulta Pediatria', 'Revision preventiva', 'Historia clinica actualizada', DATE('now','-6 days'), '15:30:00', 'Control preventivo', 'Atendido', 100.00, 7, 2, 2, 1, 4),
('Consulta General', 'Chequeo general', 'Paciente citado por recepcion', DATE('now'), '17:00:00', 'Cansancio general', 'Pendiente de pago', 80.00, 2, 2, 5, 5, 2);

INSERT INTO Factura(numero_factura, id_paciente, id_reserva, fecha_factura, subtotal, igv, total, estado_pago) VALUES
('FAC-2026-000001', 1, 1, (DATE('now') || ' 10:35:00'), 150.00, 27.00, 177.00, 'PAGADO'),
('FAC-2026-000002', 2, 2, (DATE('now','+1 day') || ' 12:55:00'), 100.00, 18.00, 118.00, 'PENDIENTE'),
('FAC-2026-000003', 3, 3, (DATE('now','-1 day') || ' 10:05:00'), 120.00, 21.60, 141.60, 'PAGADO'),
('FAC-2026-000004', 4, 4, (DATE('now') || ' 09:05:00'), 80.00, 14.40, 94.40, 'PAGADO'),
('FAC-2026-000005', 5, 5, (DATE('now','+1 day') || ' 16:30:00'), 120.00, 21.60, 141.60, 'PAGADO'),
('FAC-2026-000006', 6, 6, (DATE('now','-7 days') || ' 11:40:00'), 150.00, 27.00, 177.00, 'PAGADO'),
('FAC-2026-000007', 7, 7, (DATE('now','-6 days') || ' 16:05:00'), 100.00, 18.00, 118.00, 'PAGADO'),
('FAC-2026-000008', 2, 8, (DATE('now') || ' 17:20:00'), 80.00, 14.40, 94.40, 'PENDIENTE');

INSERT INTO DetalleFactura(id_factura, descripcion, cantidad, precio_unitario, subtotal) VALUES
(1, 'Consulta Cardiologia', 1, 150.00, 150.00),
(2, 'Consulta Pediatria', 1, 100.00, 100.00),
(3, 'Consulta Dermatologia', 1, 120.00, 120.00),
(4, 'Consulta General', 1, 80.00, 80.00),
(5, 'Consulta Dermatologia', 1, 120.00, 120.00),
(6, 'Consulta Cardiologia', 1, 150.00, 150.00),
(7, 'Consulta Pediatria', 1, 100.00, 100.00),
(8, 'Consulta General', 1, 80.00, 80.00);

INSERT INTO Pago(id_factura, id_pago, monto, fecha_pago, usuario_registro, observacion) VALUES
(1, 4, 177.00, (DATE('now') || ' 10:40:00'), 3, 'Deposito por Yape'),
(3, 2, 141.60, (DATE('now','-1 day') || ' 10:15:00'), 3, 'Pago con tarjeta'),
(4, 1, 94.40, (DATE('now') || ' 09:10:00'), 3, 'Deposito en efectivo'),
(5, 3, 141.60, (DATE('now','+1 day') || ' 16:35:00'), 3, 'Deposito por transferencia'),
(6, 2, 177.00, (DATE('now','-7 days') || ' 11:45:00'), 3, 'Deposito con tarjeta'),
(7, 1, 118.00, (DATE('now','-6 days') || ' 16:10:00'), 3, 'Deposito en efectivo');

INSERT INTO Auditoria(tabla, accion, usuario_bd, datos_nuevos) VALUES
('Sistema', 'SEED', 'system', 'Datos iniciales de Clinica Ana San Gabriel para demo SQLite');
