const scenarioData = {
  rental: {
    overline: 'PARC DE LOCATION · UNITÉ #LOC-014', title: 'De la réservation<br>au retour en atelier.',
    desc: 'Une unité, une période, un historique clair. La disponibilité suit l’équipement du départ jusqu’à son inspection de retour.',
    level: 'L1–L2 · Standard & paramétrage', eyebrow: 'CYCLE DE LOCATION', flowTitle: 'Motoculteur · LOC-014', note: 'Historique de l’unité conservé à chaque étape.',
    steps: [['Réservation','12 juin'],['Dépôt reçu','25 $'],['En location','Actif'],['Inspection','À venir'],['Disponible','À venir']], records: [['JT','Jordan Tremblay','Dépôt reçu · 25,00 $','CONFIRMÉ'],['LOC','LOC-014 · Motoculteur compact','Retour prévu · 14 juin','SÉRIALISÉ']], action: 'Simuler un retour avec dommage', actionType: 'damage'
  },
  special: {
    overline: 'ACHATS & VENTES · COMMANDE #SO-1084', title: 'La commande complète.<br>Sans perdre le fil.',
    desc: 'Cinq articles, trois fournisseurs, une commande client. Les reçus partiels, les reliquats et la réservation restent visibles ensemble.',
    level: 'L1–L2 · Achats, ventes & stock', eyebrow: 'COMMANDE SPÉCIALE', flowTitle: 'Commande #SO-1084 · Tremblay', note: 'Avis prêt à retirer bloqué tant qu’une ligne manque.',
    steps: [['Commande','5 articles'],['Achats','3 fournisseurs'],['Réception','3 / 5 reçus'],['Réservé client','En attente'],['Prêt','Bloqué']], records: [['SO','Commande client · SO-1084','Dépôt · 150,00 $','PARTIEL'],['PO','Fournisseurs A · B · C','3 articles reçus · 2 en attente','SUIVI']], action: 'Réceptionner les 2 pièces manquantes', actionType: 'receive'
  },
  repair: {
    overline: 'SERVICE ATELIER · DOSSIER #REP-0231', title: 'Du diagnostic à la<br>facture, sans détour.',
    desc: 'L’équipement, le devis, l’accord du client, les pièces et le temps du mécanicien restent liés dans un même dossier.',
    level: 'L1–L2 · Atelier & facturation', eyebrow: 'DOSSIER DE RÉPARATION', flowTitle: 'Tondeuse · Honda HRX', note: 'Chaque changement de travaux conserve son approbation.',
    steps: [['Réception','Dossier'],['Diagnostic','Prêt'],['Approbation','Client'],['Réparation','Pièce reçue'],['Terminé','Contrôle']], records: [['REP','Dossier REP-0231 · M. Gagnon','Lame · 1 h 20 · devis 148 $','APPROUVÉ'],['STOCK','Lame compatible · 1 unité','Réservée au dossier REP-0231','RÉSERVÉ']], action: 'Ajouter des travaux et redemander l’accord', actionType: 'approval'
  }
};

const panel = document.querySelector('#scenario-panel');
const tabs = [...document.querySelectorAll('.scenario-tab')];
let scenario = 'rental';
let progress = 2;
let scenarioActionDone = false;

function renderScenario(key, reset = true) {
  scenario = key;
  if (reset) { progress = key === 'rental' ? 2 : key === 'special' ? 2 : 2; scenarioActionDone = false; }
  const data = scenarioData[key];
  document.querySelector('#scenario-overline').textContent = data.overline;
  document.querySelector('#scenario-title').innerHTML = data.title;
  document.querySelector('#scenario-desc').textContent = data.desc;
  document.querySelector('#scenario-level').textContent = data.level;
  document.querySelector('#flow-eyebrow').textContent = data.eyebrow;
  document.querySelector('#flow-title').textContent = data.flowTitle;
  document.querySelector('#flow-note').textContent = data.note;
  const actions = document.querySelector('#scenario-actions');
  actions.innerHTML = `<button id="scenario-action">${scenarioActionDone ? '✓ Action enregistrée' : data.action}</button>`;
  document.querySelector('#flow-steps').innerHTML = data.steps.map((step, i) => `<div class="flow-step ${i < progress ? 'done' : ''} ${i === progress ? 'current' : ''}"><span class="step-dot"></span>${step[0]}<small>${step[1]}</small></div>`).join('');
  document.querySelector('.flow-board').querySelectorAll('.flow-record').forEach(el => el.remove());
  const board = document.querySelector('.flow-steps');
  const records = data.records.map((row, i) => `<div class="flow-record"><span class="record-avatar">${row[0]}</span><div><b>${row[1]}</b><small>${row[2]}</small></div><span class="record-tag">${row[3]}</span></div>`).join('');
  board.insertAdjacentHTML('afterend', records);
  document.querySelector('#advance-flow').innerHTML = `${progress >= data.steps.length - 1 ? 'Recommencer le scénario' : 'Faire avancer le scénario'} <b>→</b>`;
  tabs.forEach(tab => { const active = tab.dataset.tab === key; tab.classList.toggle('active', active); tab.setAttribute('aria-selected', String(active)); });
  document.querySelector('#scenario-action').addEventListener('click', runScenarioAction);
}

function runScenarioAction() {
  if (scenarioActionDone) return;
  scenarioActionDone = true;
  const data = scenarioData[scenario];
  if (scenario === 'rental') {
    data.steps[3] = ['Inspection','Dommage noté'];
    data.steps[4] = ['Maintenance','Unité bloquée'];
    data.records[1] = ['LOC','LOC-014 · Retour inspecté','Dommage déclaré · entretien requis','BLOQUÉ'];
    data.note = 'Unité bloquée jusqu’à la fin de l’entretien.';
    progress = 3;
    showToast('Retour enregistré. LOC-014 reste indisponible pendant l’entretien.');
  } else if (scenario === 'special') {
    data.steps[2] = ['Réception','5 / 5 reçus'];
    data.steps[3] = ['Réservé client','Confirmé'];
    data.steps[4] = ['Prêt','Avis à envoyer'];
    data.records[1] = ['PO','Réception complète · 5 / 5','Articles affectés à SO-1084','COMPLET'];
    data.note = 'Toutes les lignes sont reçues et réservées au client.';
    progress = 3;
    showToast('Réception complète. Les cinq articles sont réservés au client.');
  } else {
    data.steps[3] = ['Travaux modifiés','Nouvel accord requis'];
    data.records[0] = ['REP','Dossier REP-0231 · M. Gagnon','Travaux additionnels · accord demandé','EN ATTENTE'];
    data.note = 'La réparation attend l’approbation du devis mis à jour.';
    progress = 3;
    showToast('Devis mis à jour. Une nouvelle approbation est demandée au client.');
  }
  renderScenario(scenario, false);
}

tabs.forEach(tab => tab.addEventListener('click', () => renderScenario(tab.dataset.tab)));
document.querySelector('#advance-flow').addEventListener('click', () => {
  const data = scenarioData[scenario];
  if (progress >= data.steps.length - 1) { renderScenario(scenario); return; }
  progress += 1;
  renderScenario(scenario, false);
});
renderScenario('rental');

const equipment = {
  tiller: { name: 'Motoculteur compact', price: 85 },
  washer: { name: 'Laveuse à pression', price: 65 }
};
let selectedEquipment = 'tiller';
document.querySelectorAll('.equipment-card').forEach(card => card.addEventListener('click', event => {
  if (event.target.closest('.availability-dot')) return;
  document.querySelectorAll('.equipment-card').forEach(item => item.classList.toggle('selected', item === card));
  selectedEquipment = card.dataset.equipment;
  document.querySelector('#daily-price').textContent = `${equipment[selectedEquipment].price} $ / jour`;
  document.querySelector('#rental-result').textContent = '';
}));

const today = new Date();
const localDate = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
document.querySelector('#start-date').min = localDate;
document.querySelector('#end-date').min = localDate;
document.querySelector('#start-date').addEventListener('change', event => {
  document.querySelector('#end-date').min = event.target.value;
  if (document.querySelector('#end-date').value < event.target.value) document.querySelector('#end-date').value = event.target.value;
});
document.querySelector('#check-rental').addEventListener('click', () => {
  const start = document.querySelector('#start-date').value;
  const end = document.querySelector('#end-date').value;
  const result = document.querySelector('#rental-result');
  if (!start || !end) { result.textContent = 'Choisissez une date de départ et une date de retour.'; return; }
  if (end < start) { result.textContent = 'La date de retour doit être égale ou postérieure au départ.'; return; }
  const days = Math.max(1, Math.round((new Date(end) - new Date(start)) / 86400000) + 1);
  const total = days * equipment[selectedEquipment].price;
  result.textContent = `${equipment[selectedEquipment].name} · ${days} jour${days > 1 ? 's' : ''} · ${total} $ estimés. Disponibilité à confirmer avec l’équipe.`;
});

const menuToggle = document.querySelector('.menu-toggle');
menuToggle.addEventListener('click', () => {
  const nav = document.querySelector('#main-nav');
  const open = nav.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.textContent = open ? '×' : '☰';
});
document.querySelectorAll('#main-nav a').forEach(link => link.addEventListener('click', () => {
  document.querySelector('#main-nav').classList.remove('open');
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.textContent = '☰';
}));

let toastTimer;
function showToast(message) {
  const toast = document.querySelector('#toast');
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 3400);
}
const contactDemo = document.querySelector('#contact-demo');
if (contactDemo) {
  contactDemo.addEventListener('click', () => showToast('Formulaire de contact à connecter lors du paramétrage Odoo. Appelez le 819 684-8446 pour nous joindre.'));
}

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (entry.isIntersecting) { entry.target.classList.add('in-view'); observer.unobserve(entry.target); }
  }), { threshold: 0.14 });
  document.querySelectorAll('.service-card,.equipment-card,.shop-card,.workshop-copy,.connected-copy').forEach(el => { el.classList.add('reveal'); observer.observe(el); });
}
