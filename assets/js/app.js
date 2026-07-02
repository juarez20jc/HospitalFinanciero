function syncDoctorPrice() {
  const select = document.querySelector("#doctorSelect");
  const price = document.querySelector("#priceInput");
  const title = document.querySelector("#titleInput");
  if (!select || !price) return;
  const setPrice = () => {
    const option = select.options[select.selectedIndex];
    if (!option) return;
    price.value = option.dataset.price || "";
    if (title && !title.value) title.value = option.dataset.title || "";
  };
  select.addEventListener("change", () => {
    const option = select.options[select.selectedIndex];
    price.value = option ? option.dataset.price || "" : "";
    if (title) title.value = option ? option.dataset.title || "" : "";
  });
  setPrice();
}

function patientPicker() {
  const input = document.querySelector("#patientSearch");
  const hidden = document.querySelector("#patientId");
  const list = document.querySelector("#patientsList");
  if (!input || !hidden || !list) return;

  const options = Array.from(list.options);
  const sync = () => {
    const match = options.find((option) => option.value === input.value);
    hidden.value = match ? match.dataset.id || "" : "";
    input.setCustomValidity(hidden.value ? "" : "Selecciona un paciente de la lista.");
  };

  input.addEventListener("input", sync);
  input.addEventListener("change", sync);
  input.form?.addEventListener("submit", sync);
  sync();
}

function syncInvoiceAmount() {
  const select = document.querySelector("#invoiceSelect");
  const amount = document.querySelector("#amountInput");
  const payment = document.querySelector("#paymentMethodSelect");
  if (!select || !amount) return;
  const setAmount = () => {
    const option = select.options[select.selectedIndex];
    amount.value = option ? option.dataset.total || "" : "";
    if (payment && option && option.dataset.payment) {
      payment.value = option.dataset.payment;
    }
  };
  select.addEventListener("change", setAmount);
  setAmount();
}

function tableFilter() {
  const input = document.querySelector("[data-table-filter]");
  if (!input) return;
  const rows = Array.from(document.querySelectorAll("tbody tr"));
  input.addEventListener("input", () => {
    const q = input.value.toLowerCase();
    rows.forEach((row) => {
      row.style.display = row.textContent.toLowerCase().includes(q) ? "" : "none";
    });
  });
}

function invoiceCancelPicker() {
  const form = document.querySelector("[data-invoice-cancel-form]");
  if (!form) return;

  const search = form.querySelector("[data-invoice-search]");
  const hidden = form.querySelector("[data-invoice-id]");
  const submit = form.querySelector("[data-invoice-submit]");
  const results = form.querySelector("[data-invoice-results]");
  if (!search || !hidden || !submit || !results) return;

  const options = Array.from(results.querySelectorAll("[data-invoice-option]"));
  const empty = document.createElement("p");
  empty.className = "muted-text invoice-empty";
  empty.textContent = "Escribe al menos 2 caracteres para filtrar por numero, paciente o monto.";
  results.prepend(empty);

  const clearSelection = () => {
    hidden.value = "";
    submit.disabled = true;
    search.setCustomValidity("Selecciona una factura de los resultados.");
  };

  const updateResults = () => {
    const query = search.value.trim().toLowerCase();
    clearSelection();

    if (query.length < 2) {
      empty.textContent = "Escribe al menos 2 caracteres para filtrar por numero, paciente o monto.";
      options.forEach((option) => {
        option.hidden = true;
      });
      return;
    }

    let visible = 0;
    options.forEach((option) => {
      const matches = (option.dataset.search || "").toLowerCase().includes(query);
      option.hidden = !matches;
      if (matches) visible += 1;
    });

    empty.textContent = visible ? `${visible} coincidencia${visible === 1 ? "" : "s"}` : "No hay facturas que coincidan.";
  };

  options.forEach((option) => {
    option.hidden = true;
    option.addEventListener("click", () => {
      hidden.value = option.dataset.id || "";
      search.value = option.dataset.label || option.textContent.trim();
      search.setCustomValidity("");
      submit.disabled = !hidden.value;
      options.forEach((other) => {
        other.hidden = other !== option;
        other.classList.toggle("selected", other === option);
      });
      empty.textContent = "Factura seleccionada.";
    });
  });

  search.addEventListener("input", updateResults);
  form.addEventListener("submit", (event) => {
    if (!hidden.value) {
      event.preventDefault();
      search.reportValidity();
    }
  });
  updateResults();
}

function patientPortalPayments() {
  const forms = Array.from(document.querySelectorAll(".portal-pay-form"));
  if (!forms.length) return;

  const paymentArea = document.querySelector("[data-payment-area]");

  const showDefaultPanel = () => {
    if (!paymentArea) return;
    const defaultPanel = paymentArea.querySelector(".portal-panel-default");
    paymentArea.querySelectorAll(".portal-pay-form").forEach((form) => {
      form.hidden = true;
    });
    if (defaultPanel) defaultPanel.hidden = false;
  };

  const showPaymentForm = (form) => {
    if (!form) return;
    const area = form.closest("[data-payment-area]") || paymentArea;
    if (area) {
      const defaultPanel = area.querySelector(".portal-panel-default");
      if (defaultPanel) defaultPanel.hidden = true;
      area.querySelectorAll(".portal-pay-form").forEach((otherForm) => {
        otherForm.hidden = otherForm !== form;
      });
    }
    form.hidden = false;
    updateForm(form);
    form.scrollIntoView({ behavior: "smooth", block: "nearest" });
  };

  const updateForm = (form) => {
    const select = form.querySelector(".portal-payment-method");
    const option = select ? select.options[select.selectedIndex] : null;
    const kind = option ? option.dataset.kind || "other" : "other";
    const submit = form.querySelector(".portal-pay-submit");

    form.dataset.paymentKind = kind;
    form.querySelectorAll(".payment-fields").forEach((section) => {
      section.hidden = true;
      section.querySelectorAll("input").forEach((input) => {
        input.required = false;
        input.disabled = true;
      });
    });

    const activeSection = form.querySelector(`.payment-${kind}`);
    if (activeSection) {
      activeSection.hidden = false;
      activeSection.querySelectorAll("input").forEach((input) => {
        input.disabled = false;
      });
    }

    if (kind === "card") {
      ["card_holder", "card_number", "card_expiry", "card_cvv"].forEach((name) => {
        const input = form.querySelector(`[name="${name}"]`);
        if (input) input.required = true;
      });
    }
    if (kind === "digital") {
      const input = form.querySelector('[name="operation_code"]');
      if (input) input.required = true;
    }
    if (submit) {
      submit.disabled = kind === "cash" || kind === "other";
      submit.textContent = kind === "cash" ? "Pagar en caja" : "Confirmar pago";
    }
  };

  document.querySelectorAll("[data-pay-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      const form = document.getElementById(button.dataset.payToggle);
      if (!form) return;
      if (form.hidden) {
        showPaymentForm(form);
      } else {
        showDefaultPanel();
      }
    });
  });

  document.querySelectorAll("[data-pay-close]").forEach((button) => {
    button.addEventListener("click", () => {
      const form = document.getElementById(button.dataset.payClose);
      if (form) showDefaultPanel();
    });
  });

  forms.forEach((form) => {
    const select = form.querySelector(".portal-payment-method");
    if (select) select.addEventListener("change", () => updateForm(form));
    form.addEventListener("submit", (event) => {
      updateForm(form);
      if (form.dataset.paymentKind === "cash" || form.dataset.paymentKind === "other") {
        event.preventDefault();
      }
    });
    updateForm(form);
  });
}

syncDoctorPrice();
patientPicker();
syncInvoiceAmount();
tableFilter();
invoiceCancelPicker();
patientPortalPayments();
