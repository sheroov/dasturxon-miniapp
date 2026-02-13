const tg = window.Telegram.WebApp;
tg.expand();

const products = [
  { id: "plov",  title: "Osh (plov)", price: 35000 },
  { id: "manti", title: "Manti",      price: 30000 },
  { id: "lagman",title: "Lag'mon",    price: 25000 },
];

const cart = {};

function formatSum(n){ return new Intl.NumberFormat('ru-RU').format(n) + " so'm"; }
function calcTotal(){ return products.reduce((s,p)=> s + (cart[p.id]||0)*p.price, 0); }

function validate(){
  const total = calcTotal();
  const phone = document.getElementById("phone").value.trim();
  const address = document.getElementById("address").value.trim();
  if (total <= 0) return { ok:false, msg:"Savat bo‘sh" };
  if (!phone) return { ok:false, msg:"Telefon kiriting" };
  if (!address) return { ok:false, msg:"Manzil kiriting" };
  return { ok:true, msg:"" };
}

// ✅ ВЕШАЕМ ОДИН РАЗ
function handleSend(){
  const v = validate();
  if(!v.ok){
    tg.showPopup({ title: "To‘ldiring", message: v.msg, buttons: [{type:"ok"}] });
    return;
  }

  const items = products
    .filter(p => (cart[p.id]||0) > 0)
    .map(p => ({ id:p.id, title:p.title, qty:cart[p.id], price:p.price }));

  const payload = {
    items,
    total: calcTotal(),
    phone: document.getElementById("phone").value.trim(),
    address: document.getElementById("address").value.trim(),
    comment: document.getElementById("comment").value.trim(),
  };

  tg.sendData(JSON.stringify(payload));
  tg.close();
}

tg.MainButton.onClick(handleSend); // ✅ один раз

function updateMainButton(){
  const total = calcTotal();
  if(total > 0){
    tg.MainButton.setText(`✅ Yuborish (${formatSum(total)})`);
    tg.MainButton.show();
  } else {
    tg.MainButton.hide();
  }
}

function render(){
  const list = document.getElementById("list");
  list.innerHTML = "";

  products.forEach(p => {
    const qty = cart[p.id] || 0;
    const el = document.createElement("div");
    el.className = "card";
    el.innerHTML = `
      <div class="row">
        <div><b>${p.title}</b><br/><span class="muted">${formatSum(p.price)}</span></div>
        <div class="row">
          <button data-act="minus" data-id="${p.id}">-</button>
          <div class="qty">${qty}</div>
          <button data-act="plus" data-id="${p.id}">+</button>
        </div>
      </div>
    `;
    list.appendChild(el);
  });

  document.getElementById("total").textContent = formatSum(calcTotal());
  updateMainButton();
}

document.addEventListener("click", (e) => {
  const btn = e.target.closest("button");
  if(!btn) return;
  const id = btn.dataset.id;
  const act = btn.dataset.act;
  if(act === "plus") cart[id] = (cart[id]||0) + 1;
  if(act === "minus") cart[id] = Math.max(0, (cart[id]||0) - 1);
  render();
});

["phone","address","comment"].forEach(id => {
  document.getElementById(id).addEventListener("input", updateMainButton);
});

render();
