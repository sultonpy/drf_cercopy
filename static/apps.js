"use strict";
const $ = (s, r = document) => r.querySelector(s);
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// ---------- i18n ----------
const I18N = {
  uz: {
    home: "Bosh sahifa", cond: "Ijara shartlari", hero: "Toshkentda avtomobil ijarasi",
    hero_sub: "Haydovchisiz, shaffof narxlar, tezkor bron", from: "Olish sanasi", to: "Qaytarish sanasi",
    search: "Topish", all: "Barchasi", per_day: "kun", sum: "so'm", from_price: "dan", book: "Bron qilish",
    details: "Batafsil", no_cars: "Bu categoriyada avtomobil topilmadi.", seats: "o'rindiq", km: "km/kun",
    deposit: "Depozit", faq: "Ko'p beriladigan savollar", reviews: "Mijozlar fikri", blog: "Yangiliklar",
    tariffs: "Tariflar", days: "kun", pickup: "Olish joyi", ret: "Qaytarish joyi", name: "Ismingiz",
    phone: "Telefon (+998...)", email: "Email (ixtiyoriy)", extras: "Qo'shimcha xizmatlar", calc: "Hisob-kitob",
    rent: "Ijara", extras_sum: "Xizmatlar", fees: "Joy to'lovi", total: "Jami", km_limit: "Kilometr limiti",
    pay: "Hozir to'lash", checking: "Tekshirilmoqda...", paid: "To'lov muvaffaqiyatli", cancelled: "To'lov bekor qilindi",
    pending: "To'lov kutilmoqda...", err: "Xatolik yuz berdi", fuel: "Yoqilg'i (l/100km)", doors: "Eshiklar",
    exp: "Minimal tajriba (yil)", back: "Orqaga", not_found: "Topilmadi",
    f_ac: "Konditsioner", f_auto: "Avtomat", f_parking_sensor: "Parktronik", f_airbag: "Airbag", f_abs: "ABS",
    cond_items: ["Hujjatlar: pasport va amaldagi haydovchilik guvohnomasi.", "Depozit avtomobil klassiga bog'liq va tekshiruvdan so'ng qaytariladi.",
      "Kunlik limit 300 km; oshgan kilometrlar uchun qo'shimcha to'lov.", "Avtomobil to'liq bak bilan beriladi va to'liq bak bilan qaytariladi.",
      "Aeroportda topshirish/olish uchun qo'shimcha to'lov mavjud."],
    footer: "Toshkent, O'zbekiston · Har kuni 9:00–18:00",
  },
  ru: {
    home: "Главная", cond: "Условия аренды", hero: "Аренда автомобилей в Ташкенте",
    hero_sub: "Без водителя, прозрачные цены, быстрая бронь", from: "Дата получения", to: "Дата возврата",
    search: "Найти", all: "Все", per_day: "сутки", sum: "сум", from_price: "от", book: "Забронировать",
    details: "Подробнее", no_cars: "На эти даты нет свободных автомобилей.", seats: "мест", km: "км/сутки",
    deposit: "Залог", faq: "Частые вопросы", reviews: "Отзывы клиентов", blog: "Новости",
    tariffs: "Тарифы", days: "дн.", pickup: "Место получения", ret: "Место возврата", name: "Ваше имя",
    phone: "Телефон (+998...)", email: "Email (необязательно)", extras: "Доп. услуги", calc: "Расчёт",
    rent: "Аренда", extras_sum: "Услуги", fees: "Сбор за место", total: "Итого", km_limit: "Лимит пробега",
    pay: "Оплатить", checking: "Проверяем...", paid: "Оплата прошла успешно", cancelled: "Оплата отменена",
    pending: "Ожидаем оплату...", err: "Произошла ошибка", fuel: "Расход (л/100км)", doors: "Двери",
    exp: "Мин. стаж (лет)", back: "Назад", not_found: "Не найдено",
    f_ac: "Кондиционер", f_auto: "Автомат", f_parking_sensor: "Парктроник", f_airbag: "Подушки", f_abs: "ABS",
    cond_items: ["Документы: паспорт и действующие водительские права.", "Залог зависит от класса авто и возвращается после проверки.",
      "Лимит 300 км в сутки; за превышение — доплата.", "Автомобиль выдаётся с полным баком и возвращается с полным баком.",
      "За получение/возврат в аэропорту взимается дополнительный сбор."],
    footer: "Ташкент, Узбекистан · Ежедневно 9:00–18:00",
  },
};
let lang = localStorage.getItem("lang") || "uz";
const t = k => I18N[lang][k] ?? I18N.uz[k] ?? k;
const money = n => Number(n).toLocaleString("ru-RU") + " " + t("sum");

// ---------- API ----------
async function get(path, params = {}) {
  const r = await fetch(`/api/${path}?${new URLSearchParams({ lang, ...params })}`);
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw data;
  return data;
}
async function post(path, body) {
  const r = await fetch(`/api/${path}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) throw data;
  return data;
}
function errText(e) {
  if (!e) return t("err");
  if (typeof e === "string") return e;
  if (e.detail) return String(e.detail);
  const parts = Object.values(e).flat().map(x => (typeof x === "object" && x ? errText(x) : x));
  return parts.join(" ") || t("err");
}

// ---------- holat ----------
function dtLocal(addDays, hour) {
  const d = new Date(); d.setDate(d.getDate() + addDays); d.setHours(hour, 0, 0, 0);
  const p = n => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}T${p(d.getHours())}:00`;
}
const S = { start: dtLocal(1, 10), end: dtLocal(4, 10), category: "" };

const app = () => $("#app");
const feat = f => t("f_" + f);
const carImg = (c, cls = "") => c.cover ? `<img src="${esc(c.cover)}" alt="${esc(c.name)}">` : "🚗";

// ---------- sahifalar ----------
async function home() {
  const [cats, faq, reviews, posts] = await Promise.all([get("categories/"), get("faq/"), get("reviews/"), get("posts/")]);
  app().innerHTML = `
    <section class="hero">
      <h1>${t("hero")}</h1><p>${t("hero_sub")}</p>
      <div class="row">
        <div class="fld"><label>${t("from")}</label><input type="datetime-local" id="s-start" value="${S.start}"></div>
        <div class="fld"><label>${t("to")}</label><input type="datetime-local" id="s-end" value="${S.end}"></div>
        <button class="btn" id="s-go">${t("search")}</button>
      </div>
    </section>
    <div class="chips" id="cats">
      <button class="chip ${S.category === "" ? "on" : ""}" data-c="">${t("all")}</button>
      ${cats.map(c => `<button class="chip ${S.category === c.slug ? "on" : ""}" data-c="${esc(c.slug)}">${esc(c.name)}</button>`).join("")}
    </div>
    <div class="grid" id="cars"></div>
    <h2>${t("faq")}</h2>
    ${faq.map(f => `<details><summary>${esc(f.question)}</summary><p>${esc(f.answer)}</p></details>`).join("")}
    <h2>${t("reviews")}</h2>
    <div class="grid">${reviews.map(r => `<div class="box"><b>${esc(r.author)}</b> ${"★".repeat(r.rating)}<p>${esc(r.text)}</p></div>`).join("")}</div>
    <h2>${t("blog")}</h2>
    <div class="grid">${posts.map(p => `<a class="box" href="#/blog/${esc(p.slug)}"><b>${esc(p.title)}</b><p class="meta">${esc(p.excerpt)}</p></a>`).join("")}</div>`;

  $("#cats").onclick = e => {
    const b = e.target.closest("[data-c]"); if (!b) return;
    S.category = b.dataset.c;
    document.querySelectorAll("#cats .chip").forEach(x => x.classList.toggle("on", x === b));
    loadCars();
  };
  $("#s-go").onclick = () => { S.start = $("#s-start").value; S.end = $("#s-end").value; loadCars(true); };
  loadCars();
}

async function loadCars(filterDates = false) {
  const box = $("#cars"); if (!box) return;
  const params = {};
  if (S.category) params.category = S.category;
  if (filterDates) { params.start = S.start; params.end = S.end; }
  try {
    const cars = await get("cars/", params);
    box.innerHTML = cars.length ? cars.map(c => `
      <article class="card">
        <a class="ph" href="#/car/${c.id}">${carImg(c)}</a>
        <div class="cb">
          <h3>${esc(c.name)}</h3>
          <div class="meta">👥 ${c.seats} ${t("seats")} · 🛣 ${c.daily_limit_km} ${t("km")} · ${t("deposit")}: ${money(c.deposit)}</div>
          <div class="meta">${c.features.map(f => esc(feat(f))).join(" · ")}</div>
          <div class="price">${t("from_price")} <b>${money(c.price_from ?? 0)}</b> / ${t("per_day")}</div>
          <a class="btn" href="#/book/${c.id}">${t("book")}</a>
        </div>
      </article>`).join("") : `<p>${t("no_cars")}</p>`;
  } catch (e) { box.innerHTML = `<p class="err">${esc(errText(e))}</p>`; }
}

async function carPage(id) {
  const c = await get(`cars/${id}/`);
  app().innerHTML = `
    <a href="#/" class="meta">← ${t("back")}</a>
    <div class="two" style="margin-top:12px">
      <div>
        <div class="gal">${c.images.length ? `<img src="${esc(c.images[0].image)}" alt="">` : "🚗"}</div>
        <h1>${esc(c.name)}</h1>
        <p>${esc(c.description)}</p>
        <div class="specs">
          <div><small>${t("seats")}</small>${c.seats}</div><div><small>${t("doors")}</small>${c.doors}</div>
          <div><small>${t("fuel")}</small>${c.fuel_per_100}</div><div><small>${t("exp")}</small>${c.min_experience}</div>
          <div><small>${t("km_limit")}</small>${c.daily_limit_km} ${t("km")}</div><div><small>${t("deposit")}</small>${money(c.deposit)}</div>
        </div>
        <p class="meta">${c.features.map(f => esc(feat(f))).join(" · ")}</p>
      </div>
      <div class="box">
        <h3 style="margin-top:0">${t("tariffs")}</h3>
        <table>${c.prices.map(p => `<tr><td>${p.from_day}–${p.to_day} ${t("days")}</td><td><b>${money(p.price)}</b></td></tr>`).join("")}</table>
        <a class="btn" style="display:block;margin-top:14px" href="#/book/${c.id}">${t("book")}</a>
      </div>
    </div>`;
}

async function bookPage(id) {
  const [car, locs, extras] = await Promise.all([get(`cars/${id}/`), get("locations/"), get("extras/")]);
  const locOpts = locs.map(l => `<option value="${l.id}">${esc(l.name)}${l.fee ? ` (+${money(l.fee)})` : ""}</option>`).join("");
  app().innerHTML = `
    <a href="#/car/${car.id}" class="meta">← ${t("back")}</a>
    <h1>${esc(car.name)}</h1>
    <div class="two">
      <div class="box">
        <div class="row">
          <div class="fld"><label>${t("pickup")}</label><select id="pickup">${locOpts}</select></div>
          <div class="fld"><label>${t("ret")}</label><select id="ret">${locOpts}</select></div>
        </div>
        <div class="row" style="margin-top:12px">
          <div class="fld"><label>${t("from")}</label><input type="datetime-local" id="start" value="${S.start}"></div>
          <div class="fld"><label>${t("to")}</label><input type="datetime-local" id="end" value="${S.end}"></div>
        </div>
        <h3>${t("extras")}</h3>
        ${extras.map(x => `<div class="ex"><span>${esc(x.name)} — ${money(x.price)}</span><input class="exq" type="number" min="0" max="5" value="0" data-code="${esc(x.code)}"></div>`).join("")}
        <h3>&nbsp;</h3>
        <div class="row">
          <div class="fld"><label>${t("name")}</label><input id="cname" autocomplete="name"></div>
          <div class="fld"><label>${t("phone")}</label><input id="cphone" type="tel" placeholder="+998901234567" autocomplete="tel"></div>
        </div>
        <div class="fld" style="margin-top:12px"><label>${t("email")}</label><input id="cemail" type="email"></div>
      </div>
      <div class="box sum" id="sum"></div>
    </div>`;

  const quoteBody = () => ({
    car: car.id, start_at: $("#start").value, end_at: $("#end").value,
    pickup_location: +$("#pickup").value, return_location: +$("#ret").value,
    extras: [...document.querySelectorAll(".exq")].map(i => ({ code: i.dataset.code, qty: +i.value })).filter(e => e.qty > 0),
  });
  let ok = false, timer;
  const renderSum = q => {
    $("#sum").innerHTML = `<h3 style="margin-top:0">${t("calc")}</h3>
      <div><span>${t("rent")} (${q.days} ${t("days")} × ${money(q.daily_price)})</span><b>${money(q.rent_sum)}</b></div>
      <div><span>${t("extras_sum")}</span><b>${money(q.extras_sum)}</b></div>
      <div><span>${t("fees")}</span><b>${money(q.fees_sum)}</b></div>
      <div class="tot"><span>${t("total")}</span><span>${money(q.total_sum)}</span></div>
      <div class="meta">${t("km_limit")}: ${q.km_limit} km · ${t("deposit")}: ${money(q.deposit)}</div>
      <p id="msg" class="err"></p><button class="btn" id="pay" style="width:100%">${t("pay")}</button>`;
    $("#pay").onclick = submit;
  };
  const recalc = () => {
    clearTimeout(timer);
    timer = setTimeout(async () => {
      try { renderSum(await post("bookings/quote/", quoteBody())); ok = true; }
      catch (e) { ok = false; $("#sum").innerHTML = `<p class="err">${esc(errText(e))}</p>`; }
    }, 250);
  };
  async function submit() {
    const btn = $("#pay"), msg = $("#msg"); msg.textContent = ""; btn.disabled = true;
    try {
      const d = await post("bookings/", {
        ...quoteBody(), customer_name: $("#cname").value.trim(),
        phone: $("#cphone").value.replace(/[\s()-]/g, ""), email: $("#cemail").value.trim(),
      });
      location.href = d.pay_url;   // Octo (mock) to'lov sahifasiga
    } catch (e) { msg.textContent = errText(e); btn.disabled = false; }
  }
  app().querySelectorAll("input, select").forEach(el => el.addEventListener("input", recalc));
  recalc();
}

async function paymentPage(id) {
  app().innerHTML = `<div class="box" style="max-width:480px;margin:40px auto"><h2 id="pt" style="margin-top:0">${t("checking")}</h2><p id="pd"></p><a class="btn ghost" href="#/">${t("home")}</a></div>`;
  for (let i = 0; i < 6; i++) {  // webhook biroz kechikishi mumkin
    const b = await get(`bookings/${id}/`);
    if (!$("#pt")) return;         // foydalanuvchi boshqa sahifaga o'tib ketgan
    $("#pt").textContent = t(b.status);
    $("#pt").className = b.status === "paid" ? "ok" : b.status === "cancelled" ? "err" : "";
    $("#pd").textContent = `${b.car_name} — ${money(b.total_sum)}`;
    if (b.status !== "pending") return;
    await new Promise(r => setTimeout(r, 2000));
  }
}

function condPage() {
  app().innerHTML = `<h1>${t("cond")}</h1><div class="box"><ul>${t("cond_items").map(x => `<li>${esc(x)}</li>`).join("")}</ul></div>`;
}

async function blogPage(slug) {
  const p = await get(`posts/${slug}/`);
  app().innerHTML = `<a href="#/" class="meta">← ${t("back")}</a><h1>${esc(p.title)}</h1><div class="box">${esc(p.body).replace(/\n/g, "<br>")}</div>`;
}

// ---------- router ----------
const routes = [
  [/^(#\/?)?$/, home], [/^#\/car\/(\d+)$/, carPage], [/^#\/book\/(\d+)$/, bookPage],
  [/^#\/payment\/([0-9a-fA-F-]{36})$/, paymentPage], [/^#\/conditions$/, condPage], [/^#\/blog\/([\w-]+)$/, blogPage],
];
async function route() {
  const h = location.hash;
  for (const [re, fn] of routes) {
    const m = h.match(re);
    if (m) {
      window.scrollTo(0, 0);
      try { await fn(...m.slice(1)); } catch (e) { app().innerHTML = `<p class="err">${esc(errText(e))}</p>`; }
      return;
    }
  }
  app().innerHTML = `<h2>404</h2><a href="#/">${t("home")}</a>`;
}
function chrome() {
  $("#nav").innerHTML = `<a href="#/">${t("home")}</a><a href="#/conditions">${t("cond")}</a>`;
  $("#ft").textContent = t("footer");
  document.documentElement.lang = lang;
  document.querySelectorAll(".lang button").forEach(b => b.classList.toggle("on", b.dataset.l === lang));
}
document.querySelector(".lang").onclick = e => {
  const b = e.target.closest("[data-l]"); if (!b) return;
  lang = b.dataset.l; localStorage.setItem("lang", lang); chrome(); route();
};
window.addEventListener("hashchange", route);
chrome(); route();