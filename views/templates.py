from html import escape


ASSET_VERSION = "20260605-anulacion-buscador"


NAV = [
    ("Dashboard", "/dashboard", "dashboard", {"ADMINISTRADOR", "RECEPCION", "CAJA"}),
    ("Pacientes", "/pacientes", "patients", {"ADMINISTRADOR", "RECEPCION", "CAJA"}),
    ("Nuevo usuario paciente", "/usuarios/paciente", "users", {"ADMINISTRADOR", "RECEPCION"}),
    ("Nuevo usuario", "/usuarios", "users", {"ADMINISTRADOR"}),
    ("Citas", "/citas", "calendar", {"ADMINISTRADOR", "RECEPCION"}),
    ("Facturación", "/facturas", "invoice", {"ADMINISTRADOR", "RECEPCION", "CAJA"}),
    ("Pagos", "/pagos", "payments", {"ADMINISTRADOR", "CAJA"}),
    ("Caja diaria", "/caja", "cash", {"ADMINISTRADOR", "CAJA"}),
    ("Cuentas por cobrar", "/cuentas", "receivable", {"ADMINISTRADOR", "CAJA", "RECEPCION"}),
    ("Reportes", "/reportes", "reports", {"ADMINISTRADOR", "CAJA"}),
    ("Auditoría", "/auditoria", "audit", {"ADMINISTRADOR"}),
]

PATIENT_NAV = [
    ("Mi portal", "/dashboard", "dashboard"),
    ("Mis facturas", "/portal/facturas", "invoice"),
    ("Mis citas", "/portal/citas", "calendar"),
    ("Mis datos", "/portal/perfil", "patients"),
]

ICONS = {
    "dashboard": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 13h6V4H4v9Zm0 7h6v-5H4v5Zm10 0h6v-9h-6v9Zm0-11h6V4h-6v5Z"/></svg>""",
    "patients": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 12a4 4 0 1 0-4-4 4 4 0 0 0 4 4Zm-7 8a7 7 0 0 1 14 0Z"/></svg>""",
    "calendar": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3v3M17 3v3M4 9h16M6 5h12a2 2 0 0 1 2 2v12H4V7a2 2 0 0 1 2-2Zm3 8h3v3H9v-3Z"/></svg>""",
    "invoice": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h9l3 3v15H6V3Zm8 1v4h4M9 11h6M9 15h6M9 18h4"/></svg>""",
    "payments": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 7h18v10H3V7Zm0 3h18M7 15h4M16 14h2"/></svg>""",
    "cash": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 8h16v10H4V8Zm3-3h10l3 3H4l3-3Zm5 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/></svg>""",
    "receivable": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21a9 9 0 1 0-9-9 9 9 0 0 0 9 9Zm0-14v10M8.5 9.5A2.5 2.5 0 0 1 12 8c1.7 0 3 1 3 2.4 0 3-6 1.6-6 4.2 0 1.3 1.2 2.4 3 2.4a3.7 3.7 0 0 0 3.5-1.8"/></svg>""",
    "reports": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 20V9M12 20V4M19 20v-7M3 20h18"/></svg>""",
    "audit": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s7-3 7-9V5l-7-3-7 3v7c0 6 7 9 7 9Zm-3-9 2 2 4-5"/></svg>""",
    "users": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 11a3.5 3.5 0 1 0-3.5-3.5A3.5 3.5 0 0 0 9 11Zm-6 9a6 6 0 0 1 12 0Zm12-9a3 3 0 1 0-2.8-4M15 14a5.5 5.5 0 0 1 6 5.5"/></svg>""",
    "settings": """<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15.5A3.5 3.5 0 1 0 8.5 12 3.5 3.5 0 0 0 12 15.5Zm8-3.5a7 7 0 0 0-.1-1.2l2-1.5-2-3.5-2.4 1a8 8 0 0 0-2-1.1L15.2 3h-4l-.4 2.7a8 8 0 0 0-2 1.1l-2.4-1-2 3.5 2 1.5A7 7 0 0 0 6.3 12a7 7 0 0 0 .1 1.2l-2 1.5 2 3.5 2.4-1a8 8 0 0 0 2 1.1l.4 2.7h4l.4-2.7a8 8 0 0 0 2-1.1l2.4 1 2-3.5-2-1.5A7 7 0 0 0 20 12Z"/></svg>""",
}


def money(value):
    return f"S/ {float(value or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def text(value):
    return escape(str(value or ""))


def login_shell(title, action, admin=False, error=""):
    note = "Ingreso administrativo" if admin else "Portal de pacientes y personal autorizado"
    button = "Entrar como administrador" if admin else "Ingresar al sistema"
    admin_link = "" if admin else '<a class="admin-link" href="/admin">Esto es para mí</a>'
    back_link = '<a class="admin-link" href="/">Volver al ingreso principal</a>' if admin else ""
    hint = "admin / Admin123!" if admin else "recepcion / Recepcion123! | caja / Caja123! | paciente / Paciente123!"
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="/assets/css/style.css?v={ASSET_VERSION}">
</head>
<body class="login-page">
  <main class="login-wrap">
    <section class="login-brand">
      <div class="brand-mark">ASG</div>
      <h1>Clínica Ana San Gabriel</h1>
      <p>Sistema financiero hospitalario para citas, facturación, caja diaria y reportes gerenciales.</p>
      <div class="clinic-photo" role="img" aria-label="Recepción clínica moderna"></div>
    </section>
    <section class="login-card">
      <p class="login-note">{note}</p>
      <h2>{title}</h2>
      {'<div class="alert">' + text(error) + '</div>' if error else ''}
      <form method="post" action="{action}" class="stack">
        <label>Usuario<input name="username" autocomplete="username" required></label>
        <label>Contraseña<input name="password" type="password" autocomplete="current-password" required></label>
        <button class="primary" type="submit">{button}</button>
      </form>
      <p class="demo">Demo: {hint}</p>
      {admin_link}{back_link}
    </section>
  </main>
</body>
</html>"""


def login_view(error=""):
    return login_shell("Ingreso principal", "/login", False, error)


def admin_login_view(error=""):
    return login_shell("Ingreso administrador", "/login/admin", True, error)


def page(user, title, content, active=""):
    nav = []
    if user["rol"] == "PACIENTE":
        for label, href, icon in PATIENT_NAV:
            current = "active" if href == active else ""
            nav.append(f'<a class="{current}" href="{href}"><span class="nav-icon">{ICONS[icon]}</span>{label}</a>')
    else:
        for label, href, icon, roles in NAV:
            if user["rol"] in roles:
                current = "active" if href == active else ""
                nav.append(f'<a class="{current}" href="{href}"><span class="nav-icon">{ICONS[icon]}</span>{label}</a>')
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{text(title)} | Clínica Ana San Gabriel</title>
  <link rel="stylesheet" href="/assets/css/style.css?v={ASSET_VERSION}">
  <script defer src="/assets/js/app.js?v={ASSET_VERSION}"></script>
</head>
<body>
  <aside class="sidebar">
    <a class="brand" href="/dashboard">
      <span class="brand-mark small">ASG</span>
      <span><strong>Clínica Ana<br>San Gabriel</strong></span>
    </a>
    <nav>{''.join(nav)}</nav>
  </aside>
  <main class="app">
    <header class="topbar">
      <div>
        <p class="section-label">Sistema financiero hospitalario</p>
        <h1>{text(title)}</h1>
      </div>
      <div class="user-chip">
        <span>{text(user['nombres'])} {text(user['apellidos'])}</span>
        <strong>{text(user['rol'].title())}</strong>
        <a href="/logout" title="Cerrar sesión">Salir</a>
      </div>
    </header>
    {content}
  </main>
</body>
</html>"""


def dashboard_view(user, data):
    k = data["kpis"]
    c = data["citas"]
    kpis = [
        ("Total facturado hoy", money(k["facturado_hoy"]), "good"),
        ("Total facturado mes actual", money(k["facturado_mes"]), "ink"),
        ("Total cobrado", money(k["cobrado"]), "good"),
        ("Total pendiente", money(k["pendiente"]), "warn"),
        ("Facturas emitidas", int(k["facturas"] or 0), "ink"),
        ("Citas cobradas", int(c["cobradas"] or 0), "good"),
        ("Citas pendientes de pago", int(c["pendientes_pago"] or 0), "warn"),
    ]
    day_labels = [("1", "Lun"), ("2", "Mar"), ("3", "Mié"), ("4", "Jue"), ("5", "Vie"), ("6", "Sáb"), ("0", "Dom")]
    day_totals = {str(r["dia"]): float(r["total"] or 0) for r in data["por_dia"]}
    max_day = max(day_totals.values() or [1])
    week_label = f'{text(data.get("inicio_semana"))} al {text(data.get("fin_semana"))}'
    bars = "".join(
        f'<div class="bar-row"><span>{label}</span><div><b style="width:{(day_totals.get(key, 0)/max_day)*100 if max_day else 0:.0f}%"></b></div><em>{money(day_totals.get(key, 0))}</em></div>'
        for key, label in day_labels
    )
    max_pay = max([float(r["total"] or 0) for r in data["por_pago"]] or [1])
    pagos = "".join(
        f'<div class="pay-line"><span>{text(r["nombre"])}</span><strong>{money(r["total"])}</strong><i style="height:{35 + ((float(r["total"] or 0)/max_pay)*95 if max_pay else 0):.0f}px"></i></div>'
        for r in data["por_pago"]
    )
    recientes = "".join(
        f'<tr><td><a href="/factura?id={r["id_factura"]}">{text(r["numero_factura"])}</a></td><td>{text(r["paciente"])}</td><td>{money(r["total"])}</td><td>{badge(r["estado_pago"])}</td><td>{text(r["fecha"])}</td></tr>'
        for r in data["recientes"]
    )
    cards = "".join(f'<article class="metric {tone}"><span>{label}</span><strong>{value}</strong></article>' for label, value, tone in kpis)
    content = f"""
    <section class="metrics-grid">{cards}</section>
    <section class="dashboard-grid">
      <article class="panel wide">
        <div class="panel-head"><h2>Ingresos cobrados por día</h2><span>Semana actual: {week_label}</span></div>
        <div class="bar-chart">{bars or empty('Sin facturación registrada')}</div>
      </article>
      <article class="panel">
        <div class="panel-head"><h2>Tipo de pago</h2><span>Caja</span></div>
        <div class="payment-chart">{pagos}</div>
      </article>
      <article class="panel table-panel">
        <div class="panel-head"><h2>Facturas recientes</h2><a href="/facturas">Ver todas</a></div>
        <table><thead><tr><th>Número</th><th>Paciente</th><th>Total</th><th>Estado</th><th>Fecha</th></tr></thead><tbody>{recientes}</tbody></table>
      </article>
    </section>"""
    return page(user, "Dashboard financiero", content, "/dashboard")


def paciente_dashboard_view(user, data, tipos_pago):
    paciente = data["paciente"]
    if not paciente:
        content = """
        <article class="panel">
          <div class="panel-head"><h2>Perfil no vinculado</h2></div>
          <p>No encontramos un paciente asociado a este usuario. Recepcion debe vincular el email del usuario con la ficha del paciente.</p>
        </article>"""
        return page(user, "Mi portal", content, "/dashboard")
    k = data["kpis"]
    proximas = data["citas"][:4]
    pendientes = [f for f in data["facturas"] if f["estado_pago"] in {"PENDIENTE", "REPORTADO"}]
    cards = "".join([
        f'<article class="metric warn"><span>Saldo pendiente</span><strong>{money(k["pendiente"])}</strong></article>',
        f'<article class="metric good"><span>Total pagado</span><strong>{money(k["pagado"])}</strong></article>',
        f'<article class="metric ink"><span>Mis facturas</span><strong>{k["facturas"]}</strong></article>',
        f'<article class="metric ink"><span>Mis citas</span><strong>{k["citas"]}</strong></article>',
    ])
    invoice_rows = patient_invoice_rows(pendientes[:5], tipos_pago)
    appointment_rows = "".join(
        f'<tr><td>{text(c["fecha_cita"])} {text(c["hora_cita"])}</td><td>{text(c["titulo"])}</td><td>{text(c["medico"])}</td><td>{text(c["especialidad"])}</td><td>{badge(c["estado"])}</td></tr>'
        for c in proximas
    )
    appointment_panel = f"""
        <div class="portal-panel-default">
          <div class="panel-head"><h2>Mis ultimas citas</h2><a href="/portal/citas">Ver citas</a></div>
          <table><thead><tr><th>Fecha</th><th>Consulta</th><th>Medico</th><th>Especialidad</th><th>Estado</th></tr></thead><tbody>{appointment_rows or empty_row(5, "No tienes citas registradas")}</tbody></table>
        </div>"""
    content = f"""
    <section class="patient-hero">
      <div>
        <p class="section-label">Portal del paciente</p>
        <h2>Hola, {text(paciente["nombres"])}</h2>
        <p>Aqui puedes revisar tus citas, tus facturas y pagar los pendientes registrados a tu nombre.</p>
      </div>
      <a class="primary link-button" href="/portal/facturas">Ver mis facturas</a>
    </section>
    <section class="metrics-grid patient-metrics">{cards}</section>
    <section class="dashboard-grid">
      <article class="panel table-panel">
        <div class="panel-head"><h2>Pagos pendientes</h2><span>Solo tus facturas</span></div>
        <table><thead><tr><th>Factura</th><th>Concepto</th><th>Total</th><th>Estado</th><th>Accion</th></tr></thead><tbody>{invoice_rows or empty_row(5, "No tienes pagos pendientes")}</tbody></table>
      </article>
      {portal_payment_panel(pendientes[:5], tipos_pago, appointment_panel)}
    </section>"""
    return page(user, "Mi portal", content, "/dashboard")


def paciente_facturas_view(user, data, tipos_pago, detalle=None, notice=""):
    rows = patient_invoice_rows(data["facturas"], tipos_pago, include_paid=True)
    detail_html = ""
    notice_html = f'<div class="alert">{text(notice)}</div>' if notice else ""
    if detalle:
        cab = detalle["cabecera"]
        lines = "".join(f'<tr><td>{text(d["descripcion"])}</td><td>{d["cantidad"]}</td><td>{money(d["precio_unitario"])}</td><td>{money(d["subtotal"])}</td></tr>' for d in detalle["detalle"])
        detail_html = f"""
        <article class="panel invoice-detail">
          <div class="panel-head"><h2>Detalle {text(cab["numero_factura"])}</h2><span>{badge(cab["estado_pago"])}</span></div>
          <table><thead><tr><th>Descripcion</th><th>Cantidad</th><th>Precio</th><th>Subtotal</th></tr></thead><tbody>{lines}</tbody></table>
          <div class="totals"><span>Subtotal {money(cab["subtotal"])}</span><span>IGV 18% {money(cab["igv"])}</span><strong>Total {money(cab["total"])}</strong></div>
        </article>"""
    content = f"""
    {notice_html}
    <section class="dashboard-grid portal-billing-layout">
      <article class="panel table-panel">
        <div class="panel-head"><h2>Mis facturas</h2><span>Documentos emitidos a tu nombre</span></div>
        <table><thead><tr><th>Factura</th><th>Concepto</th><th>Total</th><th>Estado</th><th>Accion</th></tr></thead><tbody>{rows or empty_row(5, "No tienes facturas registradas")}</tbody></table>
      </article>
      {portal_payment_panel(data["facturas"], tipos_pago, portal_payment_empty())}
    </section>
    {detail_html}"""
    return page(user, "Mis facturas", content, "/portal/facturas")


def paciente_citas_view(user, data):
    rows = "".join(
        f'<tr><td>{text(c["fecha_cita"])} {text(c["hora_cita"])}</td><td>{text(c["titulo"])}</td><td>{text(c["medico"])}</td><td>{text(c["especialidad"])}</td><td>{money(c["precio"])}</td><td>{badge(c["estado"])}</td></tr>'
        for c in data["citas"]
    )
    content = f"""
    <article class="panel table-panel">
      <div class="panel-head"><h2>Mis citas</h2><span>Historial de atenciones y reservas</span></div>
      <table><thead><tr><th>Fecha</th><th>Consulta</th><th>Medico</th><th>Especialidad</th><th>Costo</th><th>Estado</th></tr></thead><tbody>{rows or empty_row(6, "No tienes citas registradas")}</tbody></table>
    </article>"""
    return page(user, "Mis citas", content, "/portal/citas")


def paciente_perfil_view(user, data):
    paciente = data["paciente"]
    if not paciente:
        rows = "<p>No hay ficha de paciente vinculada.</p>"
    else:
        rows = f"""
        <dl class="profile-grid">
          <div><dt>DNI</dt><dd>{text(paciente["dni"])}</dd></div>
          <div><dt>Nombre</dt><dd>{text(paciente["nombre_completo"])}</dd></div>
          <div><dt>Email</dt><dd>{text(paciente["email"])}</dd></div>
          <div><dt>Telefono</dt><dd>{text(paciente["telefono"])}</dd></div>
          <div><dt>Grupo sanguineo</dt><dd>{text(paciente["grupo_sanguineo"])}</dd></div>
          <div><dt>Contacto emergencia</dt><dd>{text(paciente["contacto_emergencia"])}</dd></div>
          <div><dt>Alergias</dt><dd>{text(paciente["alergias"])}</dd></div>
          <div><dt>Enfermedades cronicas</dt><dd>{text(paciente["enfermedades_cronicas"])}</dd></div>
        </dl>"""
    content = f"""<article class="panel"><div class="panel-head"><h2>Mis datos</h2><span>Ficha del paciente</span></div>{rows}</article>"""
    return page(user, "Mis datos", content, "/portal/perfil")


def patient_invoice_rows(facturas, tipos_pago, include_paid=False):
    rows = []
    for f in facturas:
        if not include_paid and f["estado_pago"] not in {"PENDIENTE", "REPORTADO"}:
            continue
        if f["estado_pago"] == "PENDIENTE":
            invoice_id = text(f["id_factura"])
            action = f'<button class="primary portal-pay-open" type="button" data-pay-toggle="pay-{invoice_id}">Pagar</button>'
        elif f["estado_pago"] == "REPORTADO":
            action = '<span class="muted-text">Reportado a caja</span>'
        else:
            action = '<span class="muted-text">Sin accion</span>'
        rows.append(
            f'<tr><td><a href="/portal/factura?id={f["id_factura"]}">{text(f["numero_factura"])}</a></td><td>{text(f["cita"] or "Servicio clinico")}</td><td>{money(f["total"])}</td><td>{badge(f["estado_pago"])}</td><td>{action}</td></tr>'
        )
    return "".join(rows)


def portal_payment_panel(facturas, tipos_pago, default_html):
    forms = portal_payment_forms(facturas, tipos_pago)
    return f'<article class="panel table-panel portal-side-panel" data-payment-area>{default_html}{forms}</article>'


def portal_payment_empty():
    return """
        <div class="portal-panel-default payment-empty">
          <div class="panel-head"><h2>Pasarela de pago</h2><span>Selecciona una factura</span></div>
          <p>Presiona <strong>Pagar</strong> en una factura pendiente para abrir aqui el formulario de pago.</p>
        </div>"""


def portal_payment_forms(facturas, tipos_pago):
    forms = []
    for f in facturas:
        if f["estado_pago"] != "PENDIENTE":
            continue
        invoice_id = text(f["id_factura"])
        selected_pago = str(f.get("metodo_pago_reserva") or "")
        type_options = "".join(
            f'<option value="{t["id_pago"]}" data-kind="{payment_kind(t["nombre"])}"{" selected" if str(t["id_pago"]) == selected_pago else ""}>{text(t["nombre"])}</option>'
            for t in tipos_pago
        )
        forms.append(f"""
          <form method="post" action="/portal/pagar" class="portal-pay-form" id="pay-{invoice_id}" hidden>
            <input type="hidden" name="id_factura" value="{invoice_id}">
            <div class="portal-pay-head">
              <div>
                <span>Factura {text(f["numero_factura"])}</span>
                <strong>Total fijo: {money(f["total"])}</strong>
              </div>
              <button class="ghost" type="button" data-pay-close="pay-{invoice_id}">Cancelar</button>
            </div>
            <label>Método de pago<select class="portal-payment-method" name="id_pago">{type_options}</select></label>
            <section class="payment-fields payment-card">
              <label>Titular de tarjeta<input name="card_holder" autocomplete="cc-name" placeholder="Nombre completo"></label>
              <label>Número de tarjeta<input name="card_number" inputmode="numeric" autocomplete="cc-number" placeholder="0000 0000 0000 0000"></label>
              <label>Vencimiento<input name="card_expiry" autocomplete="cc-exp" placeholder="MM/AA"></label>
              <label>CVV<input name="card_cvv" inputmode="numeric" autocomplete="cc-csc" placeholder="123"></label>
            </section>
            <section class="payment-fields payment-digital">
              <p class="payment-note">Paga el monto exacto y registra el número de operación.</p>
              <label>Número de operación<input name="operation_code" placeholder="Ej. 458912"></label>
              <label>Celular usado<input name="payer_phone" inputmode="tel" placeholder="Opcional"></label>
            </section>
            <section class="payment-fields payment-cash">
              <p class="payment-warning">El efectivo solo se confirma en caja. Tu factura seguirá pendiente hasta que caja registre el cobro.</p>
            </section>
            <div class="portal-pay-actions">
              <button class="primary portal-pay-submit" type="submit">Confirmar pago</button>
            </div>
          </form>""")
    return "".join(forms)


def payment_kind(name):
    key = str(name or "").strip().upper()
    if key == "TARJETA":
        return "card"
    if key in {"YAPE", "PLIN", "TRANSFERENCIA"}:
        return "digital"
    if key == "EFECTIVO":
        return "cash"
    return "other"


def empty_row(cols, message):
    return f'<tr><td colspan="{cols}" class="empty">{text(message)}</td></tr>'


def pacientes_view(user, pacientes, active="/pacientes"):
    rows = "".join(
        f'<tr><td>{text(p["dni"])}</td><td>{text(p["nombre_completo"])}</td><td>{text(p["telefono"])}</td><td>{text(p["email"])}</td><td>{text(p["grupo_sanguineo"])}</td></tr>'
        for p in pacientes
    )
    blood_options = "".join(f'<option value="{value}">{value}</option>' for value in ["No especificado", "O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
    if user["rol"] not in {"ADMINISTRADOR", "RECEPCION"}:
        content = f"""
    <article class="panel table-panel">
      <div class="panel-head"><h2>Pacientes</h2><form action="/pacientes"><input name="q" placeholder="DNI, nombre, apellido o teléfono"></form></div>
      <table><thead><tr><th>DNI</th><th>Paciente</th><th>Teléfono</th><th>Email</th><th>Grupo</th></tr></thead><tbody>{rows or empty_row(5, "No hay pacientes registrados")}</tbody></table>
    </article>"""
        return page(user, "Gestión de pacientes", content, active)
    content = f"""
    <section class="split">
      <article class="panel">
        <div class="panel-head"><h2>Registrar paciente</h2><span>Historia económica habilitada</span></div>
        <form class="form-grid" method="post" action="/pacientes/crear">
          <label>DNI<input name="dni" required></label>
          <label>Nombres<input name="nombres" required></label>
          <label>Apellidos<input name="apellidos" required></label>
          <label>Género<select name="genero"><option value="M">Masculino</option><option value="F">Femenino</option></select></label>
          <label>Fecha nacimiento<input type="date" name="fecha_nacimiento" required></label>
          <label>Teléfono<input name="telefono"></label>
          <label>Email<input type="email" name="email"></label>
          <label>Dirección<input name="direccion"></label>
          <label>Grupo sanguíneo<select name="grupo_sanguineo">{blood_options}</select></label>
          <label>Contacto emergencia<input name="contacto_emergencia"></label>
          <label>Teléfono emergencia<input name="telefono_emergencia"></label>
          <label>Alergias<input name="alergias"></label>
          <label>Enfermedades crónicas<input name="enfermedades_cronicas"></label>
          <label class="span-2">Observaciones<textarea name="observaciones"></textarea></label>
          <button class="primary span-2" type="submit">Guardar paciente</button>
        </form>
      </article>
      <article class="panel table-panel">
        <div class="panel-head"><h2>Pacientes</h2><form action="/pacientes"><input name="q" placeholder="DNI, nombre, apellido o teléfono"></form></div>
        <table><thead><tr><th>DNI</th><th>Paciente</th><th>Teléfono</th><th>Email</th><th>Grupo</th></tr></thead><tbody>{rows or empty_row(5, "No hay pacientes registrados")}</tbody></table>
      </article>
    </section>"""
    return page(user, "Gestión de pacientes", content, active)


def citas_view(user, catalogos, citas):
    patient_options = "".join(
        f'<option value="{text(p["dni"])} - {text(p["nombre"])}" data-id="{p["id_paciente"]}">{text(p["nombre"])}</option>'
        for p in catalogos["pacientes"]
    )
    doctor_options = "".join(
        f'<option value="{m["id_medico"]}" data-price="{m["precio_base"]}" data-title="Consulta {text(m["especialidad"])}">{text(m["nombre"])} - {text(m["especialidad"])} ({money(m["precio_base"])})</option>'
        for m in catalogos["medicos"]
    )
    pay_options = "".join(f'<option value="{p["id_pago"]}">{text(p["nombre"])}</option>' for p in catalogos["pagos"])
    state_options = "".join(f'<option value="{e["id_estado"]}">{text(e["nombre"])}</option>' for e in catalogos["estados"])
    rows = "".join(
        f'<tr><td>{text(c["fecha_cita"])} {text(c["hora_cita"])}</td><td>{text(c["paciente"])}</td><td>{text(c["medico"])}</td><td>{money(c["precio"])}</td><td>{text(c["tipo_pago"])}</td><td>{badge(c["estado"])}</td><td>{text(c["numero_factura"] or "Sin factura")}</td></tr>'
        for c in citas
    )
    buttons = "".join(
        f'<form method="post" action="/facturas/generar"><input type="hidden" name="id_reserva" value="{c["id_reserva"]}"><button class="ghost" type="submit">Generar factura #{c["id_reserva"]}</button></form>'
        for c in citas if not c["numero_factura"]
    )
    content = f"""
    <section class="split">
      <article class="panel">
        <div class="panel-head"><h2>Nueva cita con cobro</h2><span>Precio automático por especialidad</span></div>
        <form class="form-grid" method="post" action="/citas/crear">
          <label class="span-2">Paciente
            <input id="patientSearch" list="patientsList" autocomplete="off" placeholder="Escribe DNI, nombre o apellido" required>
            <input type="hidden" id="patientId" name="id_paciente">
            <datalist id="patientsList">{patient_options}</datalist>
          </label>
          <label>Médico<select name="id_medico" id="doctorSelect" required>{doctor_options}</select></label>
          <label>Fecha<input type="date" name="fecha_cita" required></label>
          <label>Hora<input type="time" name="hora_cita" required></label>
          <label>Tipo de pago<select name="id_pago">{pay_options}</select></label>
          <label>Estado<select name="id_estado">{state_options}</select></label>
          <label>Costo<input id="priceInput" name="precio" type="number" step="0.01" min="0" readonly></label>
          <label>Título<input id="titleInput" name="titulo" placeholder="Consulta Cardiología"></label>
          <label class="span-2">Síntomas<textarea name="sintomas"></textarea></label>
          <label class="check span-2"><input type="checkbox" name="generar_factura"> Generar factura automáticamente</label>
          <button class="primary span-2" type="submit">Guardar cita</button>
        </form>
        <div class="action-stack">{buttons}</div>
      </article>
      <article class="panel table-panel">
        <div class="panel-head"><h2>Citas registradas</h2><span>Reservación + cobro</span></div>
        <table><thead><tr><th>Fecha</th><th>Paciente</th><th>Médico</th><th>Costo</th><th>Pago</th><th>Estado</th><th>Factura</th></tr></thead><tbody>{rows or empty_row(7, "No hay citas registradas")}</tbody></table>
      </article>
    </section>"""
    return page(user, "Gestión de citas", content, "/citas")


def facturas_view(user, facturas, detalle=None):
    rows = "".join(
        f'<tr><td><a href="/factura?id={f["id_factura"]}">{text(f["numero_factura"])}</a></td><td>{text(f["paciente"])}</td><td>{text(f["cita"] or "Servicio clínico")}</td><td>{money(f["subtotal"])}</td><td>{money(f["igv"])}</td><td>{money(f["total"])}</td><td>{badge(f["estado_pago"])}</td></tr>'
        for f in facturas
    )
    detail_html = ""
    if detalle:
        cab = detalle["cabecera"]
        lines = "".join(f'<tr><td>{text(d["descripcion"])}</td><td>{d["cantidad"]}</td><td>{money(d["precio_unitario"])}</td><td>{money(d["subtotal"])}</td></tr>' for d in detalle["detalle"])
        detail_html = f"""
        <article class="panel invoice-detail">
          <div class="panel-head"><h2>Factura N° {text(cab["numero_factura"])}</h2><span>{badge(cab["estado_pago"])}</span></div>
          <p><strong>Paciente:</strong> {text(cab["paciente"])} &nbsp; <strong>DNI:</strong> {text(cab["dni"])}</p>
          <table><thead><tr><th>Descripción</th><th>Cantidad</th><th>Precio</th><th>Subtotal</th></tr></thead><tbody>{lines}</tbody></table>
          <div class="totals"><span>Subtotal {money(cab["subtotal"])}</span><span>IGV 18% {money(cab["igv"])}</span><strong>Total {money(cab["total"])}</strong></div>
        </article>"""
    cancel_options = "".join(f'<option value="{f["id_factura"]}">{text(f["numero_factura"])} - {text(f["paciente"])}</option>' for f in facturas if f["estado_pago"] != "ANULADO")
    content = f"""
    <section class="dashboard-grid">
      <article class="panel table-panel wide">
        <div class="panel-head"><h2>Facturación electrónica interna</h2><span>Numeración FAC-AAAA-000001</span></div>
        <table><thead><tr><th>Número</th><th>Paciente</th><th>Detalle</th><th>Subtotal</th><th>IGV</th><th>Total</th><th>Estado</th></tr></thead><tbody>{rows}</tbody></table>
      </article>
      <article class="panel">
        <div class="panel-head"><h2>Anulación</h2><span>Auditable</span></div>
        <form class="stack" method="post" action="/facturas/anular">
          <label>Factura<select name="id_factura">{cancel_options}</select></label>
          <label>Motivo<select name="motivo"><option>Error de emisión</option><option>Duplicidad</option><option>Solicitud administrativa</option></select></label>
          <button class="danger" type="submit">Anular factura</button>
        </form>
      </article>
      {detail_html}
    </section>"""
    return page(user, "Facturación", content, "/facturas")


def facturas_view(user, facturas, detalle=None):
    rows = "".join(
        f'<tr><td><a href="/factura?id={f["id_factura"]}">{text(f["numero_factura"])}</a></td><td>{text(f["paciente"])}</td><td>{text(f["cita"] or "Servicio clinico")}</td><td>{money(f["subtotal"])}</td><td>{money(f["igv"])}</td><td>{money(f["total"])}</td><td>{badge(f["estado_pago"])}</td></tr>'
        for f in facturas
    )
    detail_html = ""
    if detalle:
        cab = detalle["cabecera"]
        lines = "".join(
            f'<tr><td>{text(d["descripcion"])}</td><td>{d["cantidad"]}</td><td>{money(d["precio_unitario"])}</td><td>{money(d["subtotal"])}</td></tr>'
            for d in detalle["detalle"]
        )
        detail_html = f"""
        <article class="panel invoice-detail">
          <div class="panel-head"><h2>Factura {text(cab["numero_factura"])}</h2><span>{badge(cab["estado_pago"])}</span></div>
          <p><strong>Paciente:</strong> {text(cab["paciente"])} &nbsp; <strong>DNI:</strong> {text(cab["dni"])}</p>
          <table><thead><tr><th>Descripcion</th><th>Cantidad</th><th>Precio</th><th>Subtotal</th></tr></thead><tbody>{lines}</tbody></table>
          <div class="totals"><span>Subtotal {money(cab["subtotal"])}</span><span>IGV 18% {money(cab["igv"])}</span><strong>Total {money(cab["total"])}</strong></div>
        </article>"""

    cancel_items = []
    for f in facturas:
        if f["estado_pago"] == "ANULADO":
            continue
        label = f'{f["numero_factura"]} - {f["paciente"]}'
        search = f'{f["numero_factura"]} {f["paciente"]} {f["cita"] or ""} {money(f["total"])} {f["estado_pago"]}'
        cancel_items.append(f"""
          <button type="button" class="invoice-result" data-invoice-option data-id="{f["id_factura"]}" data-label="{text(label)}" data-search="{text(search)}">
            <strong>{text(f["numero_factura"])}</strong>
            <span>{text(f["paciente"])} - {money(f["total"])} - {badge(f["estado_pago"])}</span>
          </button>""")
    cancel_results = "".join(cancel_items) or '<p class="muted-text">No hay facturas disponibles para anular.</p>'

    content = f"""
    <section class="dashboard-grid">
      <article class="panel invoice-cancel-panel wide">
        <div class="panel-head"><h2>Anulacion</h2><span>Auditable</span></div>
        <form class="invoice-cancel-form" method="post" action="/facturas/anular" data-invoice-cancel-form>
          <label class="invoice-search-label">Buscar factura
            <input id="cancelInvoiceSearch" autocomplete="off" placeholder="Escribe numero, paciente o monto" data-invoice-search>
            <input type="hidden" name="id_factura" data-invoice-id>
          </label>
          <label>Motivo<select name="motivo"><option>Error de emision</option><option>Duplicidad</option><option>Solicitud administrativa</option></select></label>
          <button class="danger" type="submit" data-invoice-submit disabled>Anular factura</button>
          <div class="invoice-results" data-invoice-results>{cancel_results}</div>
        </form>
      </article>
      {detail_html}
      <article class="panel table-panel wide">
        <div class="panel-head"><h2>Facturacion electronica interna</h2><span>Numeracion FAC-AAAA-000001</span></div>
        <table><thead><tr><th>Numero</th><th>Paciente</th><th>Detalle</th><th>Subtotal</th><th>IGV</th><th>Total</th><th>Estado</th></tr></thead><tbody>{rows}</tbody></table>
      </article>
    </section>"""
    return page(user, "Facturacion", content, "/facturas")


def pagos_view(user, pendientes, tipos):
    invoice_options = "".join(
        f'<option value="{f["id_factura"]}" data-total="{f["total"]}" data-payment="{text(f["id_pago_pactado"])}">{text(f["numero_factura"])} - {text(f["paciente"])} - {text(f["metodo_pago"])} - {money(f["total"])}</option>'
        for f in pendientes
    )
    type_options = "".join(f'<option value="{t["id_pago"]}">{text(t["nombre"])}</option>' for t in tipos)
    rows = "".join(
        f'<tr><td>{text(f["numero_factura"])}</td><td>{text(f["paciente"])}</td><td>{text(f["medico"])}</td><td>{text(f["metodo_pago"])}</td><td>{money(f["total"])}</td><td>{badge(f["estado_pago"])}</td><td>{text(f["pago_reportado"] or "")}</td></tr>'
        for f in pendientes
    )
    content = f"""
    <section class="split">
      <article class="panel">
        <div class="panel-head"><h2>Validar pago</h2><span>Solo caja confirma PAGADO</span></div>
        <form class="stack" method="post" action="/pagos/registrar">
          <label>Factura<select id="invoiceSelect" name="id_factura">{invoice_options}</select></label>
          <label>Método de pago sugerido<select id="paymentMethodSelect" name="id_pago">{type_options}</select></label>
          <label>Monto<input id="amountInput" name="monto" type="number" step="0.01"></label>
          <label>Observación<input name="observacion" placeholder="Operación, voucher o nota"></label>
          <button class="primary" type="submit">Confirmar pago en caja</button>
        </form>
      </article>
      <article class="panel table-panel">
        <div class="panel-head"><h2>Facturas por validar</h2><span>Incluye pagos reportados por pacientes</span></div>
        <table><thead><tr><th>Factura</th><th>Paciente</th><th>Médico</th><th>Método sugerido</th><th>Total</th><th>Estado</th><th>Reporte</th></tr></thead><tbody>{rows or empty_row(7, "No hay facturas por validar")}</tbody></table>
      </article>
    </section>"""
    return page(user, "Control de pagos", content, "/pagos")


def caja_view(user, data):
    cards = "".join(f'<article class="metric good"><span>{text(r["nombre"])}</span><strong>{money(r["total"])}</strong></article>' for r in data["totales"])
    rows = "".join(f'<tr><td>{text(m["fecha_pago"])}</td><td>{text(m["numero_factura"])}</td><td>{text(m["tipo_pago"])}</td><td>{money(m["monto"])}</td><td>{text(m["username"])}</td></tr>' for m in data["movimientos"])
    content = f"""
    <section class="metrics-grid">{cards}<article class="metric ink"><span>Total del día</span><strong>{money(data["total"])}</strong></article></section>
    <article class="panel table-panel">
      <div class="panel-head"><h2>Movimientos de caja diaria</h2><span>Ingresos registrados hoy</span></div>
      <table><thead><tr><th>Fecha</th><th>Factura</th><th>Tipo</th><th>Monto</th><th>Usuario</th></tr></thead><tbody>{rows}</tbody></table>
    </article>"""
    return page(user, "Caja diaria", content, "/caja")


def cuentas_view(user, pendientes):
    rows = "".join(f'<tr><td>{text(f["numero_factura"])}</td><td>{text(f["paciente"])}</td><td>{text(f["medico"])}</td><td>{money(f["total"])}</td><td>{badge(f["estado_pago"])}</td></tr>' for f in pendientes)
    content = f"""
    <article class="panel table-panel">
      <div class="panel-head"><h2>Cuentas por cobrar</h2><form><input placeholder="Filtrar por fecha, paciente o médico" data-table-filter></form></div>
      <table><thead><tr><th>Factura</th><th>Paciente</th><th>Médico</th><th>Total</th><th>Estado</th></tr></thead><tbody>{rows}</tbody></table>
    </article>"""
    return page(user, "Cuentas por cobrar", content, "/cuentas")


def reportes_view(user, data):
    diario = "".join(f'<tr><td>{text(r["periodo"])}</td><td>{r["facturas"]}</td><td>{money(r["total"])}</td><td>{money(r["cobrado"])}</td><td>{money(r["pendiente"])}</td></tr>' for r in data["diario"])
    medico = "".join(f'<tr><td>{text(r["medico"])}</td><td>{r["consultas"]}</td><td>{money(r["facturado"])}</td></tr>' for r in data["medico"])
    espec = "".join(f'<tr><td>{text(r["especialidad"])}</td><td>{money(r["ingresos"])}</td></tr>' for r in data["especialidad"])
    pago = "".join(f'<tr><td>{text(r["tipo_pago"])}</td><td>{money(r["ingresos"])}</td></tr>' for r in data["pago"])
    content = f"""
    <section class="report-actions"><a class="primary link-button" href="/reportes/exportar">Exportar Excel/CSV</a></section>
    <section class="report-grid">
      {report_table("Reporte diario", "<th>Fecha</th><th>Facturas</th><th>Monto total</th><th>Cobrado</th><th>Pendiente</th>", diario)}
      {report_table("Reporte por médico", "<th>Médico</th><th>Consultas</th><th>Facturado</th>", medico)}
      {report_table("Reporte por especialidad", "<th>Especialidad</th><th>Ingresos</th>", espec)}
      {report_table("Reporte por tipo de pago", "<th>Tipo de pago</th><th>Ingresos</th>", pago)}
    </section>"""
    return page(user, "Reportes financieros", content, "/reportes")


def auditoria_view(user, rows):
    body = "".join(f'<tr><td>{text(r["fecha"])}</td><td>{text(r["tabla"])}</td><td>{text(r["accion"])}</td><td>{text(r["usuario_bd"])}</td><td>{text(r["datos_nuevos"])}</td></tr>' for r in rows)
    content = f"""
    <article class="panel">
      <div class="panel-head"><h2>Para qué sirve</h2><span>Control interno</span></div>
      <p class="muted-copy">La auditoría no es para operar caja; sirve como historial de seguridad: registra creaciones, pagos y anulaciones para saber quién hizo cada movimiento y cuándo.</p>
    </article>
    <article class="panel table-panel"><div class="panel-head"><h2>Auditoría financiera</h2><span>Creación, pago y anulación</span></div><table><thead><tr><th>Fecha</th><th>Tabla</th><th>Acción</th><th>Usuario</th><th>Detalle</th></tr></thead><tbody>{body or empty_row(5, "No hay movimientos de auditoría")}</tbody></table></article>"""
    return page(user, "Auditoría", content, "/auditoria")


def usuarios_view(user, rows, selected_rol=""):
    body = "".join(f'<tr><td>{text(r["username"])}</td><td>{text(r["nombre"])}</td><td>{text(r["email"])}</td><td>{text(r["rol"])}</td><td>{badge("ACTIVO" if r["estado_activo"] else "INACTIVO")}</td></tr>' for r in rows)
    roles = [("", "Todos"), ("ADMINISTRADOR", "Administrador"), ("CAJA", "Caja"), ("RECEPCION", "Recepción"), ("PACIENTE", "Paciente")]
    roles = [role for role in roles if role[0] != "PACIENTE"]
    filters = "".join(
        f'<a class="filter-pill {"active" if value == selected_rol else ""}" href="/usuarios{("?rol=" + value) if value else ""}">{label}</a>'
        for value, label in roles
    )
    content = f"""
    <section class="split">
      <article class="panel">
        <div class="panel-head"><h2>Nuevo usuario</h2><span>Caja o recepción</span></div>
        <form class="form-grid" method="post" action="/usuarios/crear">
          <label>Usuario<input name="username" required></label>
          <label>Rol<select name="rol"><option value="RECEPCION">Recepción</option><option value="CAJA">Caja</option></select></label>
          <label>Nombres<input name="nombres" required></label>
          <label>Apellidos<input name="apellidos" required></label>
          <label>Email<input type="email" name="email" required></label>
          <label>Teléfono<input name="telefono"></label>
          <label>Contraseña<input type="password" name="password" required></label>
          <label>Dirección<input name="direccion"></label>
          <button class="primary span-2" type="submit">Guardar usuario</button>
        </form>
      </article>
      <article class="panel table-panel">
        <div class="panel-head"><h2>Usuarios y roles</h2><div class="role-filters">{filters}</div></div>
        <table><thead><tr><th>Usuario</th><th>Nombre</th><th>Email</th><th>Rol</th><th>Estado</th></tr></thead><tbody>{body or empty_row(5, "No hay usuarios para este rol")}</tbody></table>
      </article>
    </section>"""
    return page(user, "Usuarios", content, "/usuarios")


def usuarios_paciente_view(user, pacientes):
    options = "".join(
        f'<option value="{p["id_paciente"]}">{text(p["dni"])} - {text(p["nombre"])} - {text(p["email"])}</option>'
        for p in pacientes if not p.get("username") and p.get("email")
    )
    rows = "".join(
        f'<tr><td>{text(p["dni"])}</td><td>{text(p["nombre"])}</td><td>{text(p["email"])}</td><td>{text(p["username"] or "Sin usuario")}</td></tr>'
        for p in pacientes
    )
    content = f"""
    <section class="split">
      <article class="panel">
        <div class="panel-head"><h2>Nuevo usuario paciente</h2><span>Acceso al login</span></div>
        <form class="form-grid" method="post" action="/usuarios/paciente/crear">
          <label class="span-2">Paciente<select name="id_paciente" required>{options}</select></label>
          <label>Usuario<input name="username" placeholder="DNI del paciente" required></label>
          <label>Contraseña<input type="password" name="password" placeholder="DNI del paciente" required></label>
          <button class="primary span-2" type="submit">Guardar usuario paciente</button>
        </form>
      </article>
      <article class="panel table-panel">
        <div class="panel-head"><h2>Pacientes y acceso</h2><span>Portal</span></div>
        <table><thead><tr><th>DNI</th><th>Paciente</th><th>Email</th><th>Usuario</th></tr></thead><tbody>{rows or empty_row(4, "No hay pacientes registrados")}</tbody></table>
      </article>
    </section>"""
    return page(user, "Nuevo usuario paciente", content, "/usuarios/paciente")


def configuracion_view(user):
    content = """
    <section class="dashboard-grid">
      <article class="panel"><div class="panel-head"><h2>Conexión</h2><span>Producción</span></div><p>El proyecto utiliza <strong>database/schema_mysql.sql</strong> y <strong>database/seed_mysql.sql</strong> para trabajar con MySQL.</p></article>
      <article class="panel"><div class="panel-head"><h2>Impuestos</h2><span>IGV</span></div><p>La facturación calcula IGV al 18% y numera comprobantes con formato FAC-AAAA-000001.</p></article>
      <article class="panel"><div class="panel-head"><h2>Clínica</h2><span>Marca temporal</span></div><p>Nombre de trabajo: Clínica Ana San Gabriel. El logo puede reemplazarse en assets/logos cuando esté aprobado.</p></article>
    </section>"""
    return page(user, "Configuración", content, "/configuracion")


def report_table(title, headers, rows):
    return f'<article class="panel table-panel"><div class="panel-head"><h2>{title}</h2></div><table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table></article>'


def badge(status):
    key = str(status or "").lower()
    cls = "ok" if key in {"pagado", "atendida", "confirmada", "activo"} else "bad" if key in {"anulado", "cancelada", "inactivo"} else "pending"
    return f'<span class="badge {cls}">{text(status)}</span>'


def empty(message):
    return f'<p class="empty">{text(message)}</p>'
