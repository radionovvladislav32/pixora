/* PIXORA
   Замените STUDIO_EMAIL — на этот адрес откроется письмо с заказом.
   Заявки хранятся в браузере и не уходят на сервер сами.
*/
const STUDIO_EMAIL = "hello@pixora.studio";
const STORAGE_KEY = "pixora.orders.v1";
const DRAFT_KEY = "pixora.draft.v1";
const TYPES = ["landing", "company", "shop", "service", "unsure"];

const ESTIMATE = {
  landing: "Ориентир для лендинга — от 19 000 ₽, срок 10–14 дней. Точную смету подтвердим после брифа.",
  company: "Ориентир для сайта компании — от 39 000 ₽, срок 3–5 недель. Точную смету подтвердим после брифа.",
  shop: "Ориентир для магазина — от 89 000 ₽, срок 4–7 недель. Точную смету подтвердим после брифа.",
  service: "Ориентир для сервиса — от 129 000 ₽, срок от 6 недель. Точную смету подтвердим после брифа.",
  unsure: "Формат подскажем после брифа. Оставьте бюджет, даже если он примерный."
};

const form = document.getElementById("order-form");
const success = document.getElementById("success");
const formError = document.getElementById("form-error");
const btnBack = document.getElementById("btn-back");
const btnNext = document.getElementById("btn-next");
const btnSubmit = document.getElementById("btn-submit");
const summary = document.getElementById("summary");
const successSummary = document.getElementById("success-summary");
const ordersBlock = document.getElementById("orders-block");
const ordersList = document.getElementById("orders-list");
const copyNote = document.getElementById("copy-note");
const navToggle = document.getElementById("nav-toggle");
const navPanel = document.getElementById("nav-panel");

let step = 1;
let ready = false;
let placing = false;
let orders = loadOrders();
let lastOrder = null;

document.querySelectorAll("[data-studio-email]").forEach((el) => {
  el.textContent = STUDIO_EMAIL;
  el.href = `mailto:${STUDIO_EMAIL}`;
});

const year = document.getElementById("year");
if (year) year.textContent = String(new Date().getFullYear());

function loadOrders() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function saveOrders() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(orders.slice(0, 30)));
}

function loadDraft() {
  try {
    const parsed = JSON.parse(sessionStorage.getItem(DRAFT_KEY) || "null");
    return parsed && typeof parsed === "object" ? parsed : null;
  } catch {
    return null;
  }
}

function saveDraft() {
  if (!ready || form.hidden) return;
  const data = readForm();
  data.step = step;
  data.consent = form.consent.checked;
  try {
    sessionStorage.setItem(DRAFT_KEY, JSON.stringify(data));
  } catch {
    /* черновик необязателен */
  }
}

function clearDraft() {
  try {
    sessionStorage.removeItem(DRAFT_KEY);
  } catch {
    /* ignore */
  }
}

function selectedLabel(name) {
  const el = form.elements[name];
  if (!el || !el.selectedOptions || !el.selectedOptions[0] || !el.value) return "";
  return el.selectedOptions[0].textContent.replace(/\s+/g, " ").trim();
}

function typeLabel() {
  const input = form.querySelector('input[name="type"]:checked');
  if (!input) return "";
  return input.closest("label").querySelector(".choice-title").textContent.trim();
}

function extraLabels() {
  return [...form.querySelectorAll('input[name="extras"]:checked')].map((el) => el.dataset.label);
}

function readForm() {
  return {
    type: form.querySelector('input[name="type"]:checked')?.value || "",
    typeLabel: typeLabel(),
    scale: form.scale.value,
    scaleLabel: selectedLabel("scale"),
    budget: form.budget.value,
    budgetLabel: selectedLabel("budget"),
    deadline: form.deadline.value,
    deadlineLabel: selectedLabel("deadline"),
    extras: extraLabels(),
    extrasValues: [...form.querySelectorAll('input[name="extras"]:checked')].map((el) => el.value),
    name: form.name.value.trim(),
    company: form.company.value.trim(),
    email: form.email.value.trim(),
    phone: form.phone.value.trim(),
    contact: form.contact.value,
    contactLabel: selectedLabel("contact"),
    reference: form.reference.value.trim(),
    message: form.message.value.trim()
  };
}

function rowsOf(data) {
  return [
    ["Формат", data.typeLabel || "—"],
    ["Объём", data.scaleLabel || "—"],
    ["Бюджет", data.budgetLabel || "—"],
    ["Срок", data.deadlineLabel || "—"],
    ["Дополнительно", data.extras.length ? data.extras.join(", ") : "—"],
    ["Имя", data.name || "—"],
    ["Компания", data.company || "—"],
    ["Почта", data.email || "—"],
    ["Телефон", data.phone || "—"],
    ["Связь", data.contactLabel || "—"],
    ["Ориентир", data.reference || "—"],
    ["Задача", data.message || "—"]
  ];
}

function renderRows(target, rows) {
  target.replaceChildren();
  rows.forEach(([key, value]) => {
    const wrap = document.createElement("div");
    const dt = document.createElement("dt");
    const dd = document.createElement("dd");
    dt.textContent = key;
    dd.textContent = value;
    wrap.append(dt, dd);
    target.append(wrap);
  });
}

function orderText(order) {
  return [
    `Заказ ${order.id}`,
    "PIXORA — сайты на заказ",
    "",
    ...rowsOf(order).map(([key, value]) => `${key}: ${value}`)
  ].join("\n");
}

function shortText(order) {
  const brief = order.message.length > 280 ? `${order.message.slice(0, 280)}…` : order.message;
  return [
    `Заказ ${order.id}`,
    `Имя: ${order.name}`,
    `Почта: ${order.email}`,
    `Телефон: ${order.phone}`,
    `Формат: ${order.typeLabel}`,
    `Бюджет: ${order.budgetLabel}`,
    `Срок: ${order.deadlineLabel}`,
    "",
    "Задача:",
    brief,
    "",
    "Полный текст сохранён в браузере на странице заказа."
  ].join("\n");
}

function mailto(body, id) {
  return `mailto:${STUDIO_EMAIL}?subject=${encodeURIComponent(`Заказ ${id} — PIXORA`)}&body=${encodeURIComponent(body)}`;
}

function mailHref(order) {
  const full = mailto(orderText(order), order.id);
  if (full.length <= 1800) return full;
  return mailto(shortText(order), order.id);
}

function makeId() {
  let id;
  do {
    id = `PX-${Math.floor(1000 + Math.random() * 9000)}`;
  } while (orders.some((order) => order.id === id));
  return id;
}

function copyText(text) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text);
  }
  const area = document.createElement("textarea");
  area.value = text;
  area.setAttribute("readonly", "");
  area.style.position = "fixed";
  area.style.left = "-9999px";
  document.body.append(area);
  area.select();
  document.execCommand("copy");
  area.remove();
  return Promise.resolve();
}

function syncChoices() {
  form.querySelectorAll(".choice").forEach((label) => {
    label.classList.toggle("is-selected", label.querySelector("input").checked);
  });
}

function updateEstimate() {
  const type = form.querySelector('input[name="type"]:checked')?.value;
  const text = type && ESTIMATE[type]
    ? ESTIMATE[type]
    : "Выберите формат — покажем ориентир по сроку и бюджету.";
  document.querySelectorAll("[data-estimate]").forEach((el) => {
    el.textContent = text;
  });
}

function clearErrors() {
  form.querySelectorAll(".field-error").forEach((el) => {
    el.hidden = true;
    el.textContent = "";
  });
  form.querySelectorAll(".is-invalid").forEach((el) => el.classList.remove("is-invalid"));
  form.querySelectorAll("[aria-invalid]").forEach((el) => el.removeAttribute("aria-invalid"));
  formError.hidden = true;
  formError.textContent = "";
}

function focusField(name) {
  const field = form.elements[name];
  if (!field) return;
  const el = typeof field.focus === "function" ? field : field[0];
  el?.focus();
}

function showError(name, message) {
  const box = document.getElementById(`${name}-error`);
  if (box) {
    box.hidden = false;
    box.textContent = message;
  }
  if (name === "type") {
    form.querySelector(".choices")?.classList.add("is-invalid");
  } else if (form.elements[name] && typeof form.elements[name].classList?.add === "function") {
    form.elements[name].classList.add("is-invalid");
    form.elements[name].setAttribute("aria-invalid", "true");
  }
  if (formError.hidden) {
    formError.hidden = false;
    formError.textContent = message;
  }
}

function validate(n) {
  clearErrors();
  if (n === 1 && !form.querySelector('input[name="type"]:checked')) {
    showError("type", "Выберите формат сайта.");
    focusField("type");
    return false;
  }
  if (n === 2) {
    if (!form.scale.value) {
      showError("scale", "Выберите объём.");
      focusField("scale");
      return false;
    }
    if (!form.budget.value) {
      showError("budget", "Выберите бюджет.");
      focusField("budget");
      return false;
    }
    if (!form.deadline.value) {
      showError("deadline", "Выберите срок.");
      focusField("deadline");
      return false;
    }
  }
  if (n === 3) {
    if (form.name.value.trim().length < 2) {
      showError("name", "Как к вам обращаться?");
      focusField("name");
      return false;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.value.trim())) {
      showError("email", "Нужна почта в формате name@example.com.");
      focusField("email");
      return false;
    }
    if (form.phone.value.trim().length < 5) {
      showError("phone", "Оставьте телефон или Telegram.");
      focusField("phone");
      return false;
    }
    if (!form.contact.value) {
      showError("contact", "Выберите удобный способ связи.");
      focusField("contact");
      return false;
    }
    if (form.message.value.trim().length < 20) {
      showError("message", "Опишите задачу чуть подробнее — хотя бы пару предложений.");
      focusField("message");
      return false;
    }
  }
  if (n === 4 && !form.consent.checked) {
    showError("consent", "Нужно согласие, чтобы ответить на заявку.");
    focusField("consent");
    return false;
  }
  return true;
}

function validateAll() {
  for (let i = 1; i <= 4; i += 1) {
    if (!validate(i)) {
      showStep(i);
      validate(i);
      return false;
    }
  }
  return true;
}

function paintProgress() {
  document.querySelectorAll("#progress li").forEach((li) => {
    const n = Number(li.dataset.step);
    li.classList.toggle("is-current", n === step);
    li.classList.toggle("is-done", n < step);
  });
}

function showStep(n) {
  step = n;
  document.querySelectorAll(".step").forEach((el) => {
    el.hidden = Number(el.dataset.step) !== n;
  });
  btnBack.hidden = n === 1;
  btnNext.hidden = n === 4;
  btnSubmit.hidden = n !== 4;
  paintProgress();
  if (n === 4) renderRows(summary, rowsOf(readForm()));
  clearErrors();
  saveDraft();
}

function showForm() {
  success.hidden = true;
  form.hidden = false;
}

function renderOrders() {
  ordersList.replaceChildren();
  ordersBlock.hidden = orders.length === 0;
  orders.forEach((order) => {
    const card = document.createElement("article");
    card.className = "saved";

    const text = document.createElement("div");
    const title = document.createElement("strong");
    const meta = document.createElement("p");
    const who = document.createElement("p");
    title.textContent = order.id;
    const when = new Date(order.createdAt).toLocaleString("ru-RU", {
      day: "numeric",
      month: "short",
      hour: "2-digit",
      minute: "2-digit"
    });
    meta.textContent = `${order.typeLabel} · ${when}`;
    who.textContent = `${order.name} · ${order.email}`;
    text.append(title, meta, who);

    const actions = document.createElement("div");
    actions.className = "saved-actions";

    const copyBtn = document.createElement("button");
    copyBtn.type = "button";
    copyBtn.dataset.action = "copy";
    copyBtn.dataset.id = order.id;
    copyBtn.textContent = "Копия";

    const mail = document.createElement("a");
    mail.href = mailHref(order);
    mail.textContent = "Письмо";

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.dataset.action = "delete";
    removeBtn.dataset.id = order.id;
    removeBtn.textContent = "Удалить";

    actions.append(copyBtn, mail, removeBtn);
    card.append(text, actions);
    ordersList.append(card);
  });
}

function fillSuccess(order) {
  document.getElementById("success-number").textContent = order.id;
  document.getElementById("success-title").textContent = `${order.name}, заявка сохранена`;
  document.getElementById("success-lead").textContent =
    `Письмо откроется на ${STUDIO_EMAIL}. Если почтовая программа не настроена, скопируйте текст и отправьте его сами.`;
  renderRows(successSummary, rowsOf(order));
  document.getElementById("mail-order").href = mailHref(order);
  copyNote.hidden = true;
}

function placeOrder() {
  if (placing) return;
  placing = true;
  try {
    const order = {
      ...readForm(),
      id: makeId(),
      createdAt: new Date().toISOString()
    };
    lastOrder = order;
    orders.unshift(order);
    let saved = true;
    try {
      saveOrders();
    } catch {
      saved = false;
      orders.shift();
    }
    clearDraft();
    ready = false;
    form.reset();
    syncChoices();
    updateEstimate();
    ready = true;
    form.hidden = true;
    showStep(1);
    fillSuccess(order);
    if (!saved) {
      document.getElementById("success-lead").textContent =
        "Браузер не дал сохранить заявку локально. Скопируйте текст и отправьте письмо вручную.";
    }
    success.hidden = false;
    renderOrders();
    success.scrollIntoView({ behavior: "smooth", block: "start" });
    document.getElementById("success-title").focus();
  } finally {
    placing = false;
  }
}

function applyDraft(draft) {
  if (TYPES.includes(draft.type)) {
    const input = form.querySelector(`input[name="type"][value="${draft.type}"]`);
    if (input) input.checked = true;
  }
  ["scale", "budget", "deadline", "contact"].forEach((name) => {
    if (typeof draft[name] === "string") form.elements[name].value = draft[name];
  });
  ["name", "company", "email", "phone", "reference", "message"].forEach((name) => {
    if (typeof draft[name] === "string") form.elements[name].value = draft[name];
  });
  const extras = new Set(draft.extrasValues || []);
  form.querySelectorAll('input[name="extras"]').forEach((el) => {
    el.checked = extras.has(el.value);
  });
  form.consent.checked = Boolean(draft.consent);
  syncChoices();
  updateEstimate();
  const savedStep = Math.min(4, Math.max(1, Number(draft.step) || 1));
  showStep(savedStep);
}

function closeMenu() {
  navPanel.hidden = true;
  navToggle.setAttribute("aria-expanded", "false");
  document.body.classList.remove("menu-open");
}

function openMenu() {
  navPanel.hidden = false;
  navToggle.setAttribute("aria-expanded", "true");
  document.body.classList.add("menu-open");
}

navToggle.addEventListener("click", () => {
  if (navPanel.hidden) openMenu();
  else closeMenu();
});

navPanel.addEventListener("click", (event) => {
  if (event.target.closest("a")) closeMenu();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") closeMenu();
});

window.addEventListener("resize", () => {
  if (window.innerWidth > 860) closeMenu();
});

document.querySelectorAll("[data-pick]").forEach((link) => {
  link.addEventListener("click", () => {
    const input = form.querySelector(`input[name="type"][value="${link.dataset.pick}"]`);
    if (!input) return;
    showForm();
    input.checked = true;
    syncChoices();
    updateEstimate();
    showStep(1);
  });
});

form.addEventListener("input", () => {
  syncChoices();
  updateEstimate();
  saveDraft();
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  if (step < 4) {
    if (validate(step)) showStep(step + 1);
    return;
  }
  if (!validateAll()) return;
  placeOrder();
});

btnNext.addEventListener("click", () => {
  if (validate(step)) showStep(step + 1);
});

btnBack.addEventListener("click", () => showStep(step - 1));

document.getElementById("progress").addEventListener("click", (event) => {
  const button = event.target.closest("[data-goto]");
  if (!button || form.hidden) return;
  const target = Number(button.dataset.goto);
  if (target <= step) {
    showStep(target);
    return;
  }
  for (let i = 1; i < target; i += 1) {
    if (!validate(i)) {
      showStep(i);
      validate(i);
      return;
    }
  }
  showStep(target);
});

document.getElementById("copy-order").addEventListener("click", async () => {
  if (!lastOrder) return;
  await copyText(orderText(lastOrder));
  copyNote.hidden = false;
});

document.getElementById("new-order").addEventListener("click", () => {
  ready = false;
  form.reset();
  clearDraft();
  ready = true;
  syncChoices();
  updateEstimate();
  showForm();
  showStep(1);
  form.querySelector("input, select, textarea")?.focus();
});

ordersList.addEventListener("click", async (event) => {
  const button = event.target.closest("button");
  if (!button) return;
  const order = orders.find((item) => item.id === button.dataset.id);
  if (!order) return;
  if (button.dataset.action === "delete") {
    orders = orders.filter((item) => item.id !== order.id);
    try { saveOrders(); } catch { /* останется в памяти до перезагрузки */ }
    renderOrders();
    return;
  }
  if (button.dataset.action === "copy") {
    await copyText(orderText(order));
    button.textContent = "Готово";
    window.setTimeout(() => {
      button.textContent = "Копия";
    }, 1600);
  }
});

ready = true;
renderOrders();
const draft = loadDraft();
if (draft) applyDraft(draft);
else {
  syncChoices();
  updateEstimate();
  showStep(1);
}
