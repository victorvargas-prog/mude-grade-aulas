import base64, json

with open("/home/claude/mude-dashboard/logo_b64.txt") as f:
    logo_b64 = f.read().strip()

logo_src = f"data:image/png;base64,{logo_b64}"

html = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Mude · Grade de Aulas</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@2.44.0/tabler-icons.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --primary:#ed1847;--primary-dk:#c4143c;--primary-lt:#fde8ed;
  --bg:#f3f2ee;--surf:#fff;--surf2:#edece8;--surf3:#e5e4e0;
  --bdr:rgba(0,0,0,.08);--bdr2:rgba(0,0,0,.13);
  --tx:#18180f;--txm:#65655e;--txf:#9c9c95;
  --green:#1D9E75;--gdk:#0F6E56;--glt:#dff5ed;
  --amber:#b87010;--alt:#fef0d5;
  --red:#c0362a;--rlt:#fdecea;
  --blue:#1860b8;--blt:#e2eefb;
  --r:8px;--rl:13px;
}
html[data-theme="dark"]{
  --bg:#111110;--surf:#1b1b18;--surf2:#222220;--surf3:#2a2a26;
  --bdr:rgba(255,255,255,.07);--bdr2:rgba(255,255,255,.12);
  --tx:#efede7;--txm:#999890;--txf:#57574f;
  --primary-lt:#3a0510;--glt:#0a2e1f;--alt:#2a1d06;--rlt:#2a0f0d;--blt:#0a1e34;
}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--tx);font-size:14px;line-height:1.5;min-height:100vh;transition:background .2s,color .2s}

/* LOGIN */
#loginScreen{display:flex;align-items:center;justify-content:center;min-height:100vh;padding:1.5rem}
.login-card{background:var(--surf);border:.5px solid var(--bdr2);border-radius:18px;padding:2.5rem 2rem;width:100%;max-width:380px}
.login-logo-wrap{display:flex;justify-content:center;margin-bottom:1.75rem}
.login-logo-img{height:44px;width:auto}
.login-title{font-size:17px;font-weight:600;margin-bottom:.35rem}
.login-desc{font-size:12px;color:var(--txm);margin-bottom:1.75rem;line-height:1.6}
.login-label{display:block;font-size:11px;font-weight:500;color:var(--txm);margin-bottom:5px}
.login-input{width:100%;padding:10px 14px;font-size:14px;font-family:'Inter',sans-serif;border:.5px solid var(--bdr2);border-radius:var(--r);background:var(--surf2);color:var(--tx);outline:none;letter-spacing:.05em}
.login-input:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(237,24,71,.12)}
.login-err{font-size:11px;color:var(--red);margin-top:.5rem;min-height:16px;display:flex;align-items:center;gap:4px}
.login-btn{width:100%;margin-top:1.25rem;padding:11px;font-size:14px;font-family:'Inter',sans-serif;font-weight:500;background:var(--primary);color:#fff;border:none;border-radius:var(--r);cursor:pointer;transition:background .15s;display:flex;align-items:center;justify-content:center;gap:6px}
.login-btn:hover{background:var(--primary-dk)}
.login-footer{margin-top:1.75rem;padding-top:1.25rem;border-top:.5px solid var(--bdr);font-size:11px;color:var(--txf);text-align:center;line-height:1.7}
.shake{animation:shake .35s ease}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}

#appScreen{display:none}

/* NAV */
nav{background:var(--surf);border-bottom:.5px solid var(--bdr);padding:0 1.5rem;display:flex;align-items:center;gap:0;position:sticky;top:0;z-index:100}
.logo-img{height:28px;width:auto;margin-right:1.5rem;display:block}
.nav-tab{height:48px;padding:0 .9rem;display:flex;align-items:center;gap:5px;font-size:12px;font-weight:500;color:var(--txm);cursor:pointer;border:none;background:none;font-family:'Inter',sans-serif;border-bottom:2px solid transparent;white-space:nowrap;transition:color .15s}
.nav-tab:hover{color:var(--tx)}
.nav-tab.active{color:var(--primary);border-bottom-color:var(--primary)}
.nav-tab i{font-size:14px}
.nav-end{margin-left:auto;display:flex;align-items:center;gap:10px}
.date-badge{font-size:11px;color:var(--txm);display:flex;align-items:center;gap:5px;background:var(--surf2);padding:4px 10px;border-radius:20px;border:.5px solid var(--bdr)}
.date-badge i{font-size:13px;color:var(--primary)}
.theme-btn{width:30px;height:30px;border-radius:var(--r);border:.5px solid var(--bdr2);background:var(--surf2);color:var(--txm);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:15px;transition:all .12s}
.theme-btn:hover{background:var(--surf3);color:var(--tx)}
.logout-btn{font-size:11px;font-family:'Inter',sans-serif;font-weight:500;padding:4px 10px;border-radius:var(--r);border:.5px solid var(--bdr2);background:var(--surf2);color:var(--txm);cursor:pointer;display:flex;align-items:center;gap:4px;transition:all .12s}
.logout-btn:hover{background:var(--primary-lt);color:var(--primary);border-color:var(--primary)}

/* PAGES */
.page{display:none}.page.active{display:block}

/* HERO */
.hero{background:var(--primary);padding:1.5rem 1.5rem 0;color:#fff}
.hero-eye{font-size:10px;font-weight:500;letter-spacing:.1em;text-transform:uppercase;opacity:.75;margin-bottom:4px}
.hero-title{font-size:22px;font-weight:600;letter-spacing:-.02em}
.hero-sub{font-size:12px;opacity:.75;margin-top:4px}
.hero-kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:rgba(255,255,255,.18);margin-top:1.25rem}
.kpi{background:rgba(0,0,0,.15);padding:.75rem 1rem}
.kpi-v{font-size:20px;font-weight:600;color:#fff}
.kpi-l{font-size:10px;color:rgba(255,255,255,.65);margin-top:1px}

/* LAYOUT */
.wrap{max-width:1300px;margin:0 auto;padding:1.25rem 1.5rem}
.section-hd{display:flex;align-items:center;justify-content:space-between;margin-bottom:.9rem;flex-wrap:wrap;gap:8px}
.section-title{font-size:14px;font-weight:600}
.section-sub{font-size:11px;color:var(--txm);margin-top:1px}

/* WEEK TABS */
.week-tabs{display:flex;gap:5px;flex-wrap:wrap}
.wtab{font-size:11px;font-family:'Inter',sans-serif;font-weight:500;padding:4px 12px;border-radius:20px;border:.5px solid var(--bdr2);background:var(--surf);color:var(--txm);cursor:pointer;transition:all .12s}
.wtab:hover{background:var(--surf2)}
.wtab.active{background:var(--primary);border-color:var(--primary);color:#fff}

/* FILTERS */
.fbar{display:flex;gap:5px;flex-wrap:wrap;margin-bottom:1rem;align-items:center}
.flabel{font-size:11px;color:var(--txf);margin-right:2px}
.fbtn{font-size:11px;font-family:'Inter',sans-serif;font-weight:500;padding:3px 10px;border-radius:16px;border:.5px solid var(--bdr2);background:var(--surf);color:var(--txm);cursor:pointer;transition:all .12s}
.fbtn:hover{background:var(--surf2)}
.fbtn.active{background:var(--tx);border-color:var(--tx);color:var(--surf)}

/* WEEK GRID */
.wgrid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:7px}
.dcol{background:var(--surf);border:.5px solid var(--bdr);border-radius:var(--rl);overflow:hidden}
.dcol.today{border-color:var(--primary);border-width:1.5px}
.dhead{padding:8px 9px 7px;border-bottom:.5px solid var(--bdr)}
.dcol.today .dhead{background:var(--primary)}
.dname{font-size:9px;font-weight:500;letter-spacing:.07em;text-transform:uppercase;color:var(--txf)}
.dcol.today .dname{color:rgba(255,255,255,.7)}
.dnum{font-size:17px;font-weight:600;letter-spacing:-.02em;color:var(--tx);line-height:1.2}
.dcol.today .dnum{color:#fff}
.today-pill{display:inline-block;font-size:8px;font-weight:500;background:rgba(255,255,255,.25);color:#fff;border-radius:3px;padding:1px 5px;margin-top:2px}
.dclasses{padding:5px;display:flex;flex-direction:column;gap:4px;min-height:50px}
.dempty{padding:10px 6px;text-align:center;font-size:10px;color:var(--txf)}

/* CLASS CARDS */
.cc{border-radius:6px;padding:5px 7px;cursor:pointer;transition:transform .1s}
.cc:hover{transform:scale(1.018)}
.cc-time{font-size:9px;font-weight:600;margin-bottom:1px}
.cc-name{font-size:10px;font-weight:500;line-height:1.3}
.cc-loc{font-size:9px;margin-top:1px;opacity:.75}
.cc-sp{display:inline-flex;align-items:center;gap:2px;font-size:8px;font-weight:600;margin-top:3px;padding:1px 5px;border-radius:4px}
.sp-d{background:rgba(29,158,117,.18);color:#0F6E56}
.sp-i{background:rgba(184,112,16,.18);color:#7a4c00}
.sp-o{background:rgba(237,24,71,.15);color:#9c0f2e}
.cat-yoga{background:#e1f5ee}.cat-yoga .cc-time{color:#0F6E56}.cat-yoga .cc-name{color:#085041}.cat-yoga .cc-loc{color:#1D9E75}
.cat-musculacao{background:#e6f1fb}.cat-musculacao .cc-time{color:#185FA5}.cat-musculacao .cc-name{color:#0C447C}.cat-musculacao .cc-loc{color:#378ADD}
.cat-crossfit{background:#faece7}.cat-crossfit .cc-time{color:#993C1D}.cat-crossfit .cc-name{color:#712B13}.cat-crossfit .cc-loc{color:#D85A30}
.cat-danca{background:#fbeaf0}.cat-danca .cc-time{color:#993556}.cat-danca .cc-name{color:#72243E}.cat-danca .cc-loc{color:#D4537E}
.cat-meditacao{background:#eeedfe}.cat-meditacao .cc-time{color:#534AB7}.cat-meditacao .cc-name{color:#3C3489}.cat-meditacao .cc-loc{color:#7F77DD}
.cat-pilates{background:#faeeda}.cat-pilates .cc-time{color:#854F0B}.cat-pilates .cc-name{color:#633806}.cat-pilates .cc-loc{color:#BA7517}
.cat-hiit{background:#fcebeb}.cat-hiit .cc-time{color:#A32D2D}.cat-hiit .cc-name{color:#791F1F}.cat-hiit .cc-loc{color:#E24B4A}

/* LEGEND */
.legend{display:flex;flex-wrap:wrap;gap:10px;margin-top:1rem;padding-top:1rem;border-top:.5px solid var(--bdr)}
.li{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--txm)}
.ld{width:9px;height:9px;border-radius:2px;flex-shrink:0}

/* MODAL */
.overlay{display:none;min-height:500px;background:rgba(0,0,0,.45);align-items:center;justify-content:center;padding:1rem}
.overlay.open{display:flex}
.modal{background:var(--surf);border-radius:var(--rl);border:.5px solid var(--bdr2);padding:1.5rem;width:100%;max-width:440px}
.modal-title{font-size:15px;font-weight:600;margin-bottom:1.1rem;display:flex;align-items:center;justify-content:space-between}
.modal-close{background:none;border:none;font-size:18px;cursor:pointer;color:var(--txm);font-family:'Inter',sans-serif}
.field{margin-bottom:.9rem}
.field label{display:block;font-size:11px;font-weight:500;color:var(--txm);margin-bottom:4px}
.field input,.field select{width:100%;padding:7px 10px;font-size:13px;font-family:'Inter',sans-serif;border:.5px solid var(--bdr2);border-radius:var(--r);background:var(--surf2);color:var(--tx);outline:none}
.field input:focus,.field select:focus{border-color:var(--primary)}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.btn-row{display:flex;gap:8px;margin-top:1.1rem;justify-content:flex-end}
.btn{font-size:12px;font-family:'Inter',sans-serif;font-weight:500;padding:7px 16px;border-radius:var(--r);cursor:pointer;border:.5px solid var(--bdr2);background:var(--surf2);color:var(--tx);transition:all .12s}
.btn.primary{background:var(--primary);border-color:var(--primary);color:#fff}
.btn.primary:hover{background:var(--primary-dk)}
.btn.danger{background:var(--rlt);border-color:var(--red);color:var(--red)}

/* TABLES */
.tbl-wrap{background:var(--surf);border:.5px solid var(--bdr);border-radius:var(--rl);overflow:hidden;margin-bottom:1.5rem}
.tbl-hd{padding:.75rem 1rem;border-bottom:.5px solid var(--bdr);display:flex;align-items:center;justify-content:space-between}
.tbl-title{font-size:13px;font-weight:600}
table{width:100%;border-collapse:collapse}
th{font-size:9px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:var(--txf);padding:.55rem .9rem;text-align:left;border-bottom:.5px solid var(--bdr);white-space:nowrap}
td{font-size:12px;color:var(--tx);padding:.6rem .9rem;border-bottom:.5px solid var(--bdr)}
tr:last-child td{border-bottom:none}
tr:hover td{background:var(--surf2)}
.badge{display:inline-flex;align-items:center;gap:2px;font-size:9px;font-weight:600;padding:2px 7px;border-radius:4px}
.b-open{background:var(--primary-lt);color:var(--primary)}
.b-inc{background:var(--alt);color:var(--amber)}
.b-dir{background:var(--glt);color:var(--gdk)}
.b-cat{font-size:9px;font-weight:500;padding:2px 6px;border-radius:4px;background:var(--surf3);color:var(--txm)}
.brand-pills{display:flex;gap:4px;flex-wrap:wrap}
.bpill{font-size:9px;font-weight:500;padding:2px 7px;border-radius:4px;background:var(--surf3);color:var(--txm)}

/* CHARTS */
.cgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:1.5rem}
.cc-card{background:var(--surf);border:.5px solid var(--bdr);border-radius:var(--rl);padding:1rem 1.1rem}
.cc-card.full{grid-column:1/-1}
.cc-title{font-size:13px;font-weight:600;margin-bottom:2px}
.cc-sub{font-size:11px;color:var(--txm);margin-bottom:.9rem}
.cleg{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:.75rem}
.cli{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--txm)}
.clsq{width:10px;height:10px;border-radius:2px;flex-shrink:0}

/* INSIGHTS */
.ins-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin-bottom:1.25rem}
.ins{background:var(--surf);border:.5px solid var(--bdr);border-radius:var(--rl);padding:.9rem 1rem;display:flex;gap:10px}
.ins-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0}
.ic-p{background:var(--primary-lt);color:var(--primary)}
.ic-g{background:var(--glt);color:var(--green)}
.ic-a{background:var(--alt);color:var(--amber)}
.ic-r{background:var(--rlt);color:var(--red)}
.ic-b{background:var(--blt);color:var(--blue)}
.ins-lbl{font-size:9px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;color:var(--txf);margin-bottom:3px}
.ins-txt{font-size:11px;color:var(--tx);line-height:1.5}

/* SPONSOR PAGE */
.sp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin-bottom:1.5rem}
.sp-card{background:var(--surf);border:.5px solid var(--bdr);border-radius:var(--rl);overflow:hidden}
.sp-card-head{padding:.85rem 1rem;border-bottom:.5px solid var(--bdr);display:flex;align-items:center;justify-content:space-between}
.sp-card-name{font-size:13px;font-weight:600}
.sp-card-seg{font-size:10px;color:var(--txm);margin-top:1px}
.sp-card-body{padding:.75rem 1rem}
.sp-class-row{display:flex;align-items:center;justify-content:space-between;padding:.4rem 0;border-bottom:.5px solid var(--bdr);font-size:11px}
.sp-class-row:last-child{border-bottom:none}
.sp-class-left{display:flex;flex-direction:column;gap:1px}
.sp-class-name{font-weight:500;color:var(--tx)}
.sp-class-meta{font-size:10px;color:var(--txm)}
.sp-stat{display:flex;gap:1rem;padding:.6rem 1rem;background:var(--surf2);border-top:.5px solid var(--bdr);font-size:11px;color:var(--txm)}
.sp-stat strong{color:var(--tx)}
.no-sp-card{background:var(--surf);border:.5px solid var(--bdr);border-radius:var(--rl);padding:1.25rem 1rem}
.no-sp-head{font-size:13px;font-weight:600;margin-bottom:.75rem;display:flex;align-items:center;gap:6px;color:var(--primary)}

/* TOAST */
.toast{display:none;align-items:center;gap:8px;background:var(--tx);color:var(--surf);font-size:12px;font-weight:500;padding:10px 16px;border-radius:var(--r);margin-bottom:.75rem}
.toast.show{display:flex}
.toast i{font-size:14px;color:var(--primary)}

/* EXCEL UPLOAD */
.upload-zone{border:1.5px dashed var(--bdr2);border-radius:var(--rl);padding:2rem;text-align:center;margin-bottom:1.5rem;transition:border-color .15s,background .15s;cursor:pointer}
.upload-zone:hover,.upload-zone.drag{border-color:var(--primary);background:var(--primary-lt)}
.upload-zone i{font-size:32px;color:var(--primary);margin-bottom:.75rem}
.upload-title{font-size:14px;font-weight:600;margin-bottom:.35rem}
.upload-sub{font-size:12px;color:var(--txm)}
#fileInput{display:none}
.upload-result{font-size:12px;padding:.6rem 1rem;border-radius:var(--r);margin-bottom:1rem;display:none;align-items:center;gap:6px}
.upload-result.ok{background:var(--glt);color:var(--gdk);display:flex}
.upload-result.err{background:var(--rlt);color:var(--red);display:flex}

@media(max-width:900px){.wgrid{grid-template-columns:repeat(4,1fr)}.cgrid{grid-template-columns:1fr}.ins-grid{grid-template-columns:1fr 1fr}.hero-kpis{grid-template-columns:repeat(3,1fr)}}
@media(max-width:600px){.wgrid{grid-template-columns:repeat(2,1fr)}.ins-grid{grid-template-columns:1fr}.hero-kpis{grid-template-columns:repeat(2,1fr)}.wrap{padding:1rem}.sp-grid{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){.cc,.btn,.fbtn,.wtab{transition:none}}
</style>
</head>
<body>

<!-- LOGIN -->
<div id="loginScreen">
  <div class="login-card">
    <div class="login-logo-wrap">
      <img class="login-logo-img" src="LOGO_SRC_PLACEHOLDER" alt="Mude">
    </div>
    <div class="login-title">Acesso restrito</div>
    <div class="login-desc">Este painel é de uso interno da equipe Mude. Insira o código de acesso para continuar.</div>
    <label class="login-label" for="codeInput">Código de acesso</label>
    <input class="login-input" id="codeInput" type="password" placeholder="••••••••" autocomplete="off" onkeydown="if(event.key==='Enter')tryLogin()">
    <div class="login-err" id="loginErr"></div>
    <button class="login-btn" onclick="tryLogin()"><i class="ti ti-lock-open" style="font-size:15px" aria-hidden="true"></i>Entrar</button>
    <div class="login-footer">Mude · Ipanema, Rio de Janeiro<br>Acesso autorizado apenas para equipe interna</div>
  </div>
</div>

<!-- APP -->
<div id="appScreen">
<nav>
  <img class="logo-img" src="LOGO_SRC_PLACEHOLDER" alt="Mude">
  <button class="nav-tab active" id="tab-grade" onclick="setPage('grade')"><i class="ti ti-calendar-week" aria-hidden="true"></i>Grade</button>
  <button class="nav-tab" id="tab-sponsors" onclick="setPage('sponsors')"><i class="ti ti-building-store" aria-hidden="true"></i>Patrocinadores</button>
  <button class="nav-tab" id="tab-trends" onclick="setPage('trends')"><i class="ti ti-chart-line" aria-hidden="true"></i>Tendências</button>
  <button class="nav-tab" id="tab-import" onclick="setPage('import')"><i class="ti ti-file-spreadsheet" aria-hidden="true"></i>Importar Excel</button>
  <div class="nav-end">
    <div class="date-badge"><i class="ti ti-calendar" aria-hidden="true"></i><span id="todayLabel"></span></div>
    <button class="theme-btn" id="themeBtn" onclick="toggleTheme()" title="Alternar modo claro/escuro"><i class="ti ti-moon" id="themeIcon" aria-hidden="true"></i></button>
    <button class="logout-btn" onclick="doLogout()"><i class="ti ti-logout" style="font-size:12px" aria-hidden="true"></i>Sair</button>
  </div>
</nav>

<!-- GRADE PAGE -->
<div class="page active" id="page-grade">
  <div class="hero">
    <div class="hero-eye">Grade de aulas · Mude Ipanema</div>
    <div class="hero-title">Próximas 4 semanas</div>
    <div class="hero-sub">Modalidade, horário, local e status de patrocínio</div>
    <div class="hero-kpis">
      <div class="kpi"><div class="kpi-v" id="kpi-total">—</div><div class="kpi-l">Total de aulas</div></div>
      <div class="kpi"><div class="kpi-v" id="kpi-open">—</div><div class="kpi-l">Sem patrocínio</div></div>
      <div class="kpi"><div class="kpi-v" id="kpi-inc">—</div><div class="kpi-l">Via incentivo</div></div>
      <div class="kpi"><div class="kpi-v" id="kpi-dir">—</div><div class="kpi-l">Patrocinadas</div></div>
      <div class="kpi"><div class="kpi-v" id="kpi-pub">—</div><div class="kpi-l">Público estimado</div></div>
    </div>
  </div>
  <div class="wrap">
    <div id="toast" class="toast"><i class="ti ti-check" aria-hidden="true"></i><span id="toastMsg"></span></div>
    <div class="section-hd">
      <div><div class="section-title">Selecione a semana</div><div class="section-sub">Clique em uma aula para editar patrocinador</div></div>
      <div class="week-tabs" id="weekTabs"></div>
    </div>
    <div class="fbar" id="catF">
      <span class="flabel">Modalidade:</span>
      <button class="fbtn active" data-v="all">Todas</button>
      <button class="fbtn" data-v="yoga">Yoga</button>
      <button class="fbtn" data-v="musculacao">Musculação</button>
      <button class="fbtn" data-v="crossfit">CrossFit</button>
      <button class="fbtn" data-v="danca">Dança</button>
      <button class="fbtn" data-v="meditacao">Meditação</button>
      <button class="fbtn" data-v="pilates">Pilates</button>
      <button class="fbtn" data-v="hiit">HIIT</button>
    </div>
    <div class="fbar" id="spF">
      <span class="flabel">Patrocínio:</span>
      <button class="fbtn active" data-v="all">Todos</button>
      <button class="fbtn" data-v="open" style="color:var(--primary)">Sem patrocínio</button>
      <button class="fbtn" data-v="incentive" style="color:var(--amber)">Via incentivo</button>
      <button class="fbtn" data-v="direct" style="color:var(--green)">Patrocinada</button>
    </div>
    <div class="wgrid" id="wgrid"></div>
    <div class="legend">
      <div class="li"><div class="ld" style="background:#1D9E75"></div>Yoga</div>
      <div class="li"><div class="ld" style="background:#378ADD"></div>Musculação</div>
      <div class="li"><div class="ld" style="background:#D85A30"></div>CrossFit</div>
      <div class="li"><div class="ld" style="background:#D4537E"></div>Dança</div>
      <div class="li"><div class="ld" style="background:#7F77DD"></div>Meditação</div>
      <div class="li"><div class="ld" style="background:#BA7517"></div>Pilates</div>
      <div class="li"><div class="ld" style="background:#E24B4A"></div>HIIT</div>
      <div class="li" style="margin-left:1rem"><div class="ld" style="background:var(--green)"></div>Patrocinada</div>
      <div class="li"><div class="ld" style="background:var(--amber)"></div>Via incentivo</div>
      <div class="li"><div class="ld" style="background:var(--primary)"></div>Sem patrocínio</div>
    </div>
    <div style="margin-top:1.75rem">
      <div class="section-hd">
        <div><div class="section-title">Aulas sem patrocínio — oportunidades</div><div class="section-sub">Semana selecionada · clique na linha para editar</div></div>
        <span style="font-size:11px;color:var(--txf)" id="oppCount"></span>
      </div>
      <div class="tbl-wrap"><div style="overflow-x:auto"><table>
        <thead><tr><th>Dia</th><th>Hora</th><th>Aula</th><th>Modalidade</th><th>Local</th><th>Público</th><th>Marcas sugeridas</th></tr></thead>
        <tbody id="oppBody"></tbody>
      </table></div></div>
    </div>
  </div>
</div>

<!-- SPONSORS PAGE -->
<div class="page" id="page-sponsors">
  <div class="hero" style="padding-bottom:1.5rem">
    <div class="hero-eye">Patrocinadores · Mude Ipanema</div>
    <div class="hero-title">Patrocínio por aula</div>
    <div class="hero-sub">Visão consolidada de todas as marcas ativas e slots sem patrocínio</div>
  </div>
  <div class="wrap">
    <div class="fbar" id="spWeekF">
      <span class="flabel">Semana:</span>
      <button class="fbtn active" data-v="all">Todas</button>
      <button class="fbtn" data-v="0">Sem. 1</button>
      <button class="fbtn" data-v="1">Sem. 2</button>
      <button class="fbtn" data-v="2">Sem. 3</button>
      <button class="fbtn" data-v="3">Sem. 4</button>
    </div>
    <div class="fbar" id="spTypeF">
      <span class="flabel">Tipo:</span>
      <button class="fbtn active" data-v="all">Todos</button>
      <button class="fbtn" data-v="direct" style="color:var(--green)">Patrocinada direta</button>
      <button class="fbtn" data-v="incentive" style="color:var(--amber)">Via incentivo</button>
      <button class="fbtn" data-v="open" style="color:var(--primary)">Sem patrocínio</button>
    </div>
    <div id="sponsorGrid"></div>
  </div>
</div>

<!-- TRENDS PAGE -->
<div class="page" id="page-trends">
  <div class="hero" style="padding-bottom:1.5rem">
    <div class="hero-eye">Análise comparativa · 4 semanas</div>
    <div class="hero-title">Tendências &amp; Oportunidades</div>
    <div class="hero-sub">Patrocínio, modalidades e potencial de ativação por semana</div>
  </div>
  <div class="wrap">
    <div class="ins-grid">
      <div class="ins"><div class="ins-icon ic-p"><i class="ti ti-clock" aria-hidden="true"></i></div><div><div class="ins-lbl">Janela aberta</div><div class="ins-txt" id="ins1"></div></div></div>
      <div class="ins"><div class="ins-icon ic-a"><i class="ti ti-alert-triangle" aria-hidden="true"></i></div><div><div class="ins-lbl">Atenção</div><div class="ins-txt" id="ins2"></div></div></div>
      <div class="ins"><div class="ins-icon ic-g"><i class="ti ti-trending-up" aria-hidden="true"></i></div><div><div class="ins-lbl">Melhor semana</div><div class="ins-txt" id="ins3"></div></div></div>
      <div class="ins"><div class="ins-icon ic-b"><i class="ti ti-building-store" aria-hidden="true"></i></div><div><div class="ins-lbl">Vivo</div><div class="ins-txt" id="ins4"></div></div></div>
      <div class="ins"><div class="ins-icon ic-g"><i class="ti ti-users" aria-hidden="true"></i></div><div><div class="ins-lbl">Público feminino</div><div class="ins-txt">65% do app é feminino. Yoga, Pilates e Dança concentram esse público.</div></div></div>
      <div class="ins"><div class="ins-icon ic-a"><i class="ti ti-percentage" aria-hidden="true"></i></div><div><div class="ins-lbl">Cobertura</div><div class="ins-txt" id="ins6"></div></div></div>
    </div>
    <div class="cgrid">
      <div class="cc-card full">
        <div class="cc-title">Distribuição de patrocínio por semana</div>
        <div class="cc-sub">Comparação entre aulas patrocinadas, via incentivo e sem patrocínio</div>
        <div class="cleg"><div class="cli"><div class="clsq" style="background:#1D9E75"></div>Patrocinada</div><div class="cli"><div class="clsq" style="background:#b87010"></div>Via incentivo</div><div class="cli"><div class="clsq" style="background:#ed1847"></div>Sem patrocínio</div></div>
        <div style="position:relative;height:240px"><canvas id="ch1" role="img" aria-label="Barras empilhadas de patrocínio por semana"></canvas></div>
      </div>
      <div class="cc-card">
        <div class="cc-title">Tendência: slots sem patrocínio</div>
        <div class="cc-sub">Evolução semanal de aulas disponíveis para marcas</div>
        <div class="cleg"><div class="cli"><div class="clsq" style="background:#ed1847"></div>Sem patrocínio</div><div class="cli"><div class="clsq" style="border:1.5px dashed #1860b8;background:none"></div>Meta (&lt;15)</div></div>
        <div style="position:relative;height:200px"><canvas id="ch2" role="img" aria-label="Linha de tendência"></canvas></div>
      </div>
      <div class="cc-card">
        <div class="cc-title">Oportunidades por modalidade</div>
        <div class="cc-sub">Slots sem patrocínio nas 4 semanas</div>
        <div style="position:relative;height:200px;display:flex;gap:12px;align-items:center">
          <div style="flex:1;min-width:0;height:200px;position:relative"><canvas id="ch3" role="img" aria-label="Rosca por modalidade"></canvas></div>
          <div id="ch3leg" style="flex-shrink:0;font-size:10px;display:flex;flex-direction:column;gap:5px"></div>
        </div>
      </div>
      <div class="cc-card full">
        <div class="cc-title">Slots abertos por modalidade e semana</div>
        <div class="cc-sub">Onde há mais espaço para ativação por categoria</div>
        <div class="cleg" id="ch4leg"></div>
        <div style="position:relative;height:240px"><canvas id="ch4" role="img" aria-label="Barras agrupadas"></canvas></div>
      </div>
      <div class="cc-card full">
        <div class="cc-title">Público estimado por tipo de patrocínio</div>
        <div class="cc-sub">Base: médias históricas Mude</div>
        <div class="cleg"><div class="cli"><div class="clsq" style="background:#1D9E75"></div>Patrocinada</div><div class="cli"><div class="clsq" style="background:#b87010"></div>Via incentivo</div><div class="cli"><div class="clsq" style="background:#ed1847"></div>Sem patrocínio (potencial)</div></div>
        <div style="position:relative;height:220px"><canvas id="ch5" role="img" aria-label="Área de público"></canvas></div>
      </div>
    </div>
    <div class="tbl-wrap">
      <div class="tbl-hd"><span class="tbl-title">Recomendações por marca parceira</span></div>
      <div style="overflow-x:auto"><table style="table-layout:auto">
        <thead><tr><th>Marca</th><th>Segmento</th><th>Modalidades</th><th>Semanas</th><th>Slots</th><th>Público est.</th><th>Ativação</th></tr></thead>
        <tbody id="brandRec"></tbody>
      </table></div>
    </div>
  </div>
</div>

<!-- IMPORT PAGE -->
<div class="page" id="page-import">
  <div class="hero" style="padding-bottom:1.5rem">
    <div class="hero-eye">Importação · Excel</div>
    <div class="hero-title">Atualizar grade via planilha</div>
    <div class="hero-sub">Importe um arquivo .xlsx para substituir toda a grade de aulas</div>
  </div>
  <div class="wrap">
    <div class="tbl-wrap" style="margin-bottom:1.25rem">
      <div class="tbl-hd"><span class="tbl-title">Formato esperado da planilha</span></div>
      <div style="overflow-x:auto"><table style="table-layout:auto">
        <thead><tr><th>semana</th><th>dia</th><th>horario</th><th>nome</th><th>modalidade</th><th>local</th><th>patrocinio</th><th>marca</th><th>publico</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>Segunda</td><td>06:30</td><td>Yoga ao ar livre</td><td>yoga</td><td>Estação Ipanema Norte</td><td>direct</td><td>Eleiko</td><td>120</td></tr>
          <tr><td>1</td><td>Terça</td><td>07:00</td><td>Pilates</td><td>pilates</td><td>Estação Ipanema Sul</td><td>incentive</td><td>Bradesco Saúde</td><td>65</td></tr>
          <tr><td>2</td><td>Sexta</td><td>18:00</td><td>CrossFit</td><td>crossfit</td><td>Estação Leblon</td><td>open</td><td></td><td>110</td></tr>
        </tbody>
      </table></div>
    </div>
    <div class="upload-zone" id="uploadZone" onclick="document.getElementById('fileInput').click()" ondragover="event.preventDefault();this.classList.add('drag')" ondragleave="this.classList.remove('drag')" ondrop="handleDrop(event)">
      <input type="file" id="fileInput" accept=".xlsx,.xls,.csv" onchange="handleFile(this.files[0])">
      <i class="ti ti-file-spreadsheet" aria-hidden="true"></i>
      <div class="upload-title">Clique ou arraste o arquivo aqui</div>
      <div class="upload-sub">.xlsx, .xls ou .csv · A grade atual será substituída</div>
    </div>
    <div class="upload-result" id="uploadResult"></div>
    <div id="previewSection" style="display:none">
      <div class="section-hd"><div><div class="section-title">Pré-visualização</div><div class="section-sub" id="previewCount"></div></div><button class="btn primary" onclick="applyImport()"><i class="ti ti-check" style="margin-right:4px;font-size:12px" aria-hidden="true"></i>Confirmar importação</button></div>
      <div class="tbl-wrap"><div style="overflow-x:auto"><table style="table-layout:auto"><thead><tr><th>Sem.</th><th>Dia</th><th>Hora</th><th>Aula</th><th>Modalidade</th><th>Local</th><th>Patrocínio</th><th>Marca</th><th>Público</th></tr></thead><tbody id="previewBody"></tbody></table></div></div>
    </div>
  </div>
</div>

<!-- MODAL EDIT -->
<div class="overlay" id="overlay" onclick="if(event.target===this)closeModal()">
  <div class="modal">
    <div class="modal-title"><span id="modalTitle">Editar aula</span><button class="modal-close" onclick="closeModal()">×</button></div>
    <div class="field"><label>Nome da aula</label><input type="text" id="fName"></div>
    <div class="row2">
      <div class="field"><label>Horário</label><input type="time" id="fTime"></div>
      <div class="field"><label>Público estimado</label><input type="number" id="fAud" min="10" max="500"></div>
    </div>
    <div class="field"><label>Local</label><select id="fLocal"><option>Estação Ipanema Norte</option><option>Estação Ipanema Sul</option><option>Estação Leblon</option><option>Estação Copacabana</option><option>Estação Botafogo</option><option>Rio Academia</option></select></div>
    <div class="row2">
      <div class="field"><label>Patrocínio</label><select id="fSp"><option value="open">Sem patrocínio</option><option value="incentive">Via incentivo</option><option value="direct">Patrocinada direta</option></select></div>
      <div class="field"><label>Marca / Patrocinador</label><input type="text" id="fBrand" placeholder="Ex: Vivo, Eleiko..."></div>
    </div>
    <div class="btn-row">
      <button class="btn" onclick="closeModal()">Cancelar</button>
      <button class="btn primary" onclick="saveClass()"><i class="ti ti-check" style="margin-right:4px;font-size:12px" aria-hidden="true"></i>Salvar</button>
    </div>
  </div>
</div>
</div><!-- /appScreen -->

<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<script>
const ACCESS_CODE='Mud3Aulas';
const SESSION_KEY='mude_auth_v3';
const STORAGE_KEY='mude_classes_v3';

/* ── AUTH ── */
function tryLogin(){
  const val=document.getElementById('codeInput').value;
  const err=document.getElementById('loginErr');
  if(val===ACCESS_CODE){
    sessionStorage.setItem(SESSION_KEY,'1');
    document.getElementById('loginScreen').style.display='none';
    document.getElementById('appScreen').style.display='block';
    err.innerHTML='';
    initApp();
  } else {
    err.innerHTML='<i class="ti ti-alert-circle"></i> Código incorreto.';
    const card=document.querySelector('.login-card');
    card.classList.remove('shake');void card.offsetWidth;card.classList.add('shake');
    document.getElementById('codeInput').value='';document.getElementById('codeInput').focus();
  }
}
function doLogout(){
  sessionStorage.removeItem(SESSION_KEY);
  document.getElementById('appScreen').style.display='none';
  document.getElementById('loginScreen').style.display='flex';
  document.getElementById('codeInput').value='';
}
function checkSession(){
  if(sessionStorage.getItem(SESSION_KEY)==='1'){
    document.getElementById('loginScreen').style.display='none';
    document.getElementById('appScreen').style.display='block';
    initApp();
  }
}

/* ── THEME ── */
function initTheme(){
  const saved=localStorage.getItem('mude_theme');
  const prefersDark=window.matchMedia('(prefers-color-scheme:dark)').matches;
  const dark=saved?saved==='dark':prefersDark;
  applyTheme(dark);
}
function applyTheme(dark){
  document.documentElement.setAttribute('data-theme',dark?'dark':'light');
  document.getElementById('themeIcon').className=dark?'ti ti-sun':'ti ti-moon';
  localStorage.setItem('mude_theme',dark?'dark':'light');
}
function toggleTheme(){
  const isDark=document.documentElement.getAttribute('data-theme')==='dark';
  applyTheme(!isDark);
}

/* ── DATE ── */
function setTodayLabel(){
  const now=new Date();
  const opts={weekday:'short',day:'numeric',month:'short',year:'numeric'};
  document.getElementById('todayLabel').textContent=now.toLocaleDateString('pt-BR',opts);
}

/* ── DATA ── */
const WEEKS_META=[{label:'Sem. 1',range:'16–22 jun'},{label:'Sem. 2',range:'23–29 jun'},{label:'Sem. 3',range:'30 jun–6 jul'},{label:'Sem. 4',range:'7–13 jul'}];
const BASE=new Date(2026,5,16);
const DAYNAMES=['Seg','Ter','Qua','Qui','Sex','Sáb','Dom'];
const DAYFULL=['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo'];
const CATCOLORS={yoga:'#1D9E75',musculacao:'#378ADD',crossfit:'#D85A30',danca:'#D4537E',meditacao:'#7F77DD',pilates:'#BA7517',hiit:'#E24B4A'};
const CATLABELS={yoga:'Yoga',musculacao:'Musculação',crossfit:'CrossFit',danca:'Dança',meditacao:'Meditação',pilates:'Pilates',hiit:'HIIT'};
const BRANDMAP={yoga:['Vivo','Danone YoPRO'],musculacao:['Danone YoPRO','Under Armour'],crossfit:['Amstel Ultra','Under Armour'],danca:['Vivo','Santander'],meditacao:['Vivo','Bradesco Saúde'],pilates:['Danone YoPRO','Bradesco Saúde'],hiit:['Amstel Ultra','Under Armour']};

function seedData(){
  const t=[
    [{time:'06:30',name:'Yoga ao ar livre',cat:'yoga',local:'Estação Ipanema Norte',sp:'direct',brand:'Eleiko',aud:120},{time:'08:00',name:'Musculação',cat:'musculacao',local:'Estação Ipanema Sul',sp:'incentive',brand:'Bradesco Saúde',aud:80},{time:'10:00',name:'Meditação',cat:'meditacao',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:60},{time:'12:00',name:'HIIT Express',cat:'hiit',local:'Estação Leblon',sp:'open',brand:'',aud:90},{time:'18:00',name:'CrossFit',cat:'crossfit',local:'Estação Leblon',sp:'incentive',brand:'Unimed',aud:110},{time:'19:30',name:'Dança Afro',cat:'danca',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:70}],
    [{time:'07:00',name:'Pilates',cat:'pilates',local:'Estação Ipanema Sul',sp:'incentive',brand:'Bradesco Saúde',aud:65},{time:'09:00',name:'Yoga Vinyasa',cat:'yoga',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:100},{time:'11:00',name:'Musculação',cat:'musculacao',local:'Estação Leblon',sp:'direct',brand:'Amil',aud:75},{time:'17:00',name:'HIIT',cat:'hiit',local:'Estação Leblon',sp:'open',brand:'',aud:95},{time:'18:30',name:'Meditação',cat:'meditacao',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:55},{time:'20:00',name:'CrossFit',cat:'crossfit',local:'Estação Ipanema Sul',sp:'open',brand:'',aud:100}],
    [{time:'06:30',name:'Yoga ao ar livre',cat:'yoga',local:'Estação Ipanema Norte',sp:'direct',brand:'Eleiko',aud:115},{time:'08:00',name:'CrossFit',cat:'crossfit',local:'Estação Leblon',sp:'open',brand:'',aud:105},{time:'10:00',name:'Pilates',cat:'pilates',local:'Estação Ipanema Sul',sp:'incentive',brand:'Bradesco Saúde',aud:60},{time:'12:00',name:'HIIT Express',cat:'hiit',local:'Estação Leblon',sp:'open',brand:'',aud:88},{time:'19:00',name:'Dança Contemporânea',cat:'danca',local:'Estação Ipanema Norte',sp:'direct',brand:'YoPRO',aud:72},{time:'20:30',name:'Meditação Noturna',cat:'meditacao',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:48}],
    [{time:'07:00',name:'Yoga Restaurativa',cat:'yoga',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:95},{time:'09:00',name:'Musculação',cat:'musculacao',local:'Estação Leblon',sp:'incentive',brand:'Unimed',aud:80},{time:'11:00',name:'Pilates',cat:'pilates',local:'Estação Ipanema Sul',sp:'open',brand:'',aud:62},{time:'17:30',name:'CrossFit',cat:'crossfit',local:'Estação Leblon',sp:'open',brand:'',aud:112},{time:'19:00',name:'HIIT',cat:'hiit',local:'Estação Leblon',sp:'direct',brand:'Amil',aud:98},{time:'20:30',name:'Dança de Salão',cat:'danca',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:68}],
    [{time:'06:30',name:'Yoga ao ar livre',cat:'yoga',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:110},{time:'08:00',name:'Musculação',cat:'musculacao',local:'Estação Ipanema Sul',sp:'direct',brand:'Eleiko',aud:85},{time:'10:00',name:'CrossFit',cat:'crossfit',local:'Estação Leblon',sp:'incentive',brand:'Unimed',aud:108},{time:'12:00',name:'Pilates',cat:'pilates',local:'Estação Ipanema Sul',sp:'open',brand:'',aud:58},{time:'18:00',name:'HIIT Power',cat:'hiit',local:'Estação Leblon',sp:'open',brand:'',aud:102},{time:'19:30',name:'Meditação',cat:'meditacao',local:'Estação Ipanema Norte',sp:'incentive',brand:'Bradesco Saúde',aud:52}],
    [{time:'07:00',name:'Yoga ao Nascer do Sol',cat:'yoga',local:'Estação Ipanema Norte',sp:'direct',brand:'YoPRO',aud:140},{time:'09:00',name:'CrossFit',cat:'crossfit',local:'Estação Leblon',sp:'open',brand:'',aud:130},{time:'10:30',name:'Dança Afro',cat:'danca',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:90},{time:'12:00',name:'Pilates',cat:'pilates',local:'Estação Ipanema Sul',sp:'incentive',brand:'Bradesco Saúde',aud:70},{time:'15:00',name:'HIIT',cat:'hiit',local:'Estação Leblon',sp:'open',brand:'',aud:120}],
    [{time:'08:00',name:'Yoga ao ar livre',cat:'yoga',local:'Estação Ipanema Norte',sp:'direct',brand:'Eleiko',aud:150},{time:'09:30',name:'Meditação',cat:'meditacao',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:65},{time:'11:00',name:'Pilates',cat:'pilates',local:'Estação Ipanema Sul',sp:'incentive',brand:'Unimed',aud:72},{time:'16:00',name:'Dança Contemporânea',cat:'danca',local:'Estação Ipanema Norte',sp:'open',brand:'',aud:85}],
  ];
  const cycles=[['direct','incentive','open'],['open','direct','incentive'],['incentive','open','direct'],['open','incentive','direct']];
  const brands={direct:['Eleiko','Amil','YoPRO'],incentive:['Unimed','Bradesco Saúde','Itaú']};
  const all=[];
  for(let w=0;w<4;w++) for(let d=0;d<7;d++) t[d].forEach((c,ci)=>{
    let sp=c.sp,brand=c.brand;
    if(w>0){sp=cycles[w][ci%3];brand=sp==='direct'?brands.direct[ci%3]:sp==='incentive'?brands.incentive[ci%3]:'';}
    all.push({id:`${w}-${d}-${ci}`,week:w,day:d,time:c.time,name:c.name,cat:c.cat,local:c.local,sp,brand,aud:c.aud});
  });
  return all;
}

let classes=[],curWeek=0,catFilter='all',spFilter='all',editingId=null,charts={};
let spWeekFilter='all',spTypeFilter='all';
let pendingImport=[];

async function loadClasses(){
  try{
    if(window.storage){const r=await window.storage.get(STORAGE_KEY,true);if(r&&r.value){classes=JSON.parse(r.value);return;}}
    const local=localStorage.getItem(STORAGE_KEY);
    if(local){classes=JSON.parse(local);return;}
  }catch(e){}
  classes=seedData();await saveClasses();
}
async function saveClasses(){
  const json=JSON.stringify(classes);
  try{if(window.storage)await window.storage.set(STORAGE_KEY,json,true);}catch(e){}
  try{localStorage.setItem(STORAGE_KEY,json);}catch(e){}
}

/* ── PAGE NAV ── */
function setPage(p){
  document.querySelectorAll('.page').forEach(e=>e.classList.remove('active'));
  document.querySelectorAll('.nav-tab').forEach(e=>e.classList.remove('active'));
  document.getElementById('page-'+p).classList.add('active');
  document.getElementById('tab-'+p).classList.add('active');
  if(p==='trends')rebuildCharts();
  if(p==='sponsors')renderSponsors();
}

/* ── WEEK TABS ── */
function buildWeekTabs(){
  const c=document.getElementById('weekTabs');c.innerHTML='';
  WEEKS_META.forEach((w,i)=>{
    const b=document.createElement('button');
    b.className='wtab'+(i===0?' active':'');
    b.textContent=w.label+' · '+w.range;
    b.onclick=()=>{curWeek=i;document.querySelectorAll('.wtab').forEach(x=>x.classList.remove('active'));b.classList.add('active');renderGrid();renderOppTable();};
    c.appendChild(b);
  });
}

/* ── KPIs ── */
function updateKPIs(){
  document.getElementById('kpi-total').textContent=classes.length;
  document.getElementById('kpi-open').textContent=classes.filter(c=>c.sp==='open').length;
  document.getElementById('kpi-inc').textContent=classes.filter(c=>c.sp==='incentive').length;
  document.getElementById('kpi-dir').textContent=classes.filter(c=>c.sp==='direct').length;
  document.getElementById('kpi-pub').textContent=(classes.reduce((s,c)=>s+c.aud,0)/1000).toFixed(0)+'k';
}

/* ── GRID ── */
const SP_LABEL={direct:'Patrocinada',incentive:'Via incentivo',open:'Sem patrocínio'};
const SP_CLS={direct:'sp-d',incentive:'sp-i',open:'sp-o'};
const SP_ICO={direct:'ti-check',incentive:'ti-discount',open:'ti-circle-dotted'};

function renderGrid(){
  const grid=document.getElementById('wgrid');grid.innerHTML='';
  const today=new Date();
  for(let d=0;d<7;d++){
    const date=new Date(BASE);date.setDate(date.getDate()+curWeek*7+d);
    const isToday=date.toDateString()===today.toDateString();
    const dc=classes.filter(c=>c.week===curWeek&&c.day===d&&(catFilter==='all'||c.cat===catFilter)&&(spFilter==='all'||c.sp===spFilter)).sort((a,b)=>a.time.localeCompare(b.time));
    const col=document.createElement('div');col.className='dcol'+(isToday?' today':'');
    const tp=isToday?'<div class="today-pill">hoje</div>':'';
    const items=dc.length===0?'<div class="dempty">—</div>':dc.map(c=>`<div class="cc cat-${c.cat}" onclick="openEditModal('${c.id}')"><div class="cc-time">${c.time}</div><div class="cc-name">${c.name}</div><div class="cc-loc">${c.local.replace('Estação ','')}</div><div class="cc-sp ${SP_CLS[c.sp]}"><i class="ti ${SP_ICO[c.sp]}" aria-hidden="true"></i>${c.sp==='direct'&&c.brand?c.brand:SP_LABEL[c.sp]}</div></div>`).join('');
    col.innerHTML=`<div class="dhead"><div class="dname">${DAYNAMES[d]}</div><div class="dnum">${date.getDate()}</div>${tp}</div><div class="dclasses">${items}</div>`;
    grid.appendChild(col);
  }
}

/* ── OPP TABLE ── */
function renderOppTable(){
  const rows=classes.filter(c=>c.week===curWeek&&c.sp==='open').sort((a,b)=>a.day-b.day||a.time.localeCompare(b.time));
  document.getElementById('oppCount').textContent=rows.length+' disponíveis';
  document.getElementById('oppBody').innerHTML=rows.length===0?'<tr><td colspan="7" style="text-align:center;color:var(--txf);padding:1.5rem">Nenhuma aula sem patrocínio nesta semana.</td></tr>':
    rows.map(r=>{const date=new Date(BASE);date.setDate(date.getDate()+r.week*7+r.day);const brands=(BRANDMAP[r.cat]||[]).map(b=>`<span class="bpill">${b}</span>`).join('');return`<tr onclick="openEditModal('${r.id}')" style="cursor:pointer"><td>${DAYFULL[r.day]}, ${date.getDate()}/${String(date.getMonth()+1).padStart(2,'0')}</td><td style="font-weight:500">${r.time}</td><td>${r.name}</td><td><span class="b-cat">${CATLABELS[r.cat]||r.cat}</span></td><td>${r.local}</td><td>${r.aud}</td><td><div class="brand-pills">${brands}</div></td></tr>`;}).join('');
}

/* ── SPONSORS PAGE ── */
function renderSponsors(){
  const filtered=classes.filter(c=>(spWeekFilter==='all'||c.week===parseInt(spWeekFilter))&&(spTypeFilter==='all'||c.sp===spTypeFilter));
  const grid=document.getElementById('sponsorGrid');
  if(spTypeFilter==='open'||spTypeFilter==='all'){
    const open=filtered.filter(c=>c.sp==='open');
    let openHtml=open.length===0?'':(`<div class="no-sp-card"><div class="no-sp-head"><i class="ti ti-circle-dotted" aria-hidden="true"></i>Sem patrocínio (${open.length} aulas)</div>`+open.sort((a,b)=>a.week-b.week||a.day-b.day||a.time.localeCompare(b.time)).map(c=>{const date=new Date(BASE);date.setDate(date.getDate()+c.week*7+c.day);const brands=(BRANDMAP[c.cat]||[]).map(b=>`<span class="bpill">${b}</span>`).join('');return`<div class="sp-class-row"><div class="sp-class-left"><div class="sp-class-name">${c.name}</div><div class="sp-class-meta">${DAYFULL[c.day]} ${date.getDate()}/${String(date.getMonth()+1).padStart(2,'0')} · ${c.time} · ${c.local}</div></div><div class="brand-pills">${brands}</div></div>`;}).join('')+'</div>');
    const brands={};
    filtered.filter(c=>c.sp!=='open'&&c.brand).forEach(c=>{if(!brands[c.brand])brands[c.brand]={name:c.brand,direct:[],incentive:[]};brands[c.brand][c.sp].push(c);});
    const brandCards=Object.values(brands).sort((a,b)=>a.name.localeCompare(b.name)).map(b=>{
      const all=[...b.direct,...b.incentive].sort((x,y)=>x.week-y.week||x.day-y.day||x.time.localeCompare(y.time));
      const pub=all.reduce((s,c)=>s+c.aud,0);
      const rows=all.map(c=>{const date=new Date(BASE);date.setDate(date.getDate()+c.week*7+c.day);return`<div class="sp-class-row"><div class="sp-class-left"><div class="sp-class-name">${c.name}</div><div class="sp-class-meta">${DAYFULL[c.day]} ${date.getDate()}/${String(date.getMonth()+1).padStart(2,'0')} · ${c.time} · ${c.local}</div></div><span class="badge ${c.sp==='direct'?'b-dir':'b-inc'}">${c.sp==='direct'?'Direta':'Incentivo'}</span></div>`;}).join('');
      const initials=b.name.split(' ').map(w=>w[0]).slice(0,2).join('').toUpperCase();
      return`<div class="sp-card"><div class="sp-card-head"><div><div class="sp-card-name" style="display:flex;align-items:center;gap:8px"><div style="width:28px;height:28px;border-radius:7px;background:var(--primary-lt);color:var(--primary);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0">${initials}</div>${b.name}</div><div class="sp-card-seg">${b.direct.length} direta${b.direct.length!==1?'s':''} · ${b.incentive.length} incentivo</div></div></div><div class="sp-card-body">${rows}</div><div class="sp-stat"><span>Público est.: <strong>${pub.toLocaleString('pt-BR')}</strong></span><span>Aulas: <strong>${all.length}</strong></span></div></div>`;
    }).join('');
    grid.innerHTML=`<div class="sp-grid">${brandCards}</div>${openHtml}`;
  } else {
    const brands={};
    filtered.filter(c=>c.brand).forEach(c=>{if(!brands[c.brand])brands[c.brand]={name:c.brand,direct:[],incentive:[]};brands[c.brand][c.sp]&&brands[c.brand][c.sp].push(c);});
    const brandCards=Object.values(brands).sort((a,b)=>a.name.localeCompare(b.name)).map(b=>{
      const all=[...( b.direct||[]),...(b.incentive||[])].sort((x,y)=>x.week-y.week||x.day-y.day);
      const pub=all.reduce((s,c)=>s+c.aud,0);
      const rows=all.map(c=>{const date=new Date(BASE);date.setDate(date.getDate()+c.week*7+c.day);return`<div class="sp-class-row"><div class="sp-class-left"><div class="sp-class-name">${c.name}</div><div class="sp-class-meta">${DAYFULL[c.day]} ${date.getDate()}/${String(date.getMonth()+1).padStart(2,'0')} · ${c.time} · ${c.local}</div></div><span class="badge ${c.sp==='direct'?'b-dir':'b-inc'}">${c.sp==='direct'?'Direta':'Incentivo'}</span></div>`;}).join('');
      const initials=b.name.split(' ').map(w=>w[0]).slice(0,2).join('').toUpperCase();
      return`<div class="sp-card"><div class="sp-card-head"><div><div class="sp-card-name" style="display:flex;align-items:center;gap:8px"><div style="width:28px;height:28px;border-radius:7px;background:var(--primary-lt);color:var(--primary);display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;flex-shrink:0">${initials}</div>${b.name}</div><div class="sp-card-seg">${(b.direct||[]).length} direta${(b.direct||[]).length!==1?'s':''} · ${(b.incentive||[]).length} incentivo</div></div></div><div class="sp-card-body">${rows}</div><div class="sp-stat"><span>Público: <strong>${pub.toLocaleString('pt-BR')}</strong></span><span>Aulas: <strong>${all.length}</strong></span></div></div>`;
    }).join('');
    grid.innerHTML=`<div class="sp-grid">${brandCards}</div>`;
  }
}

document.getElementById('spWeekF').addEventListener('click',e=>{const b=e.target.closest('.fbtn');if(!b)return;spWeekFilter=b.dataset.v;document.querySelectorAll('#spWeekF .fbtn').forEach(x=>x.classList.remove('active'));b.classList.add('active');renderSponsors();});
document.getElementById('spTypeF').addEventListener('click',e=>{const b=e.target.closest('.fbtn');if(!b)return;spTypeFilter=b.dataset.v;document.querySelectorAll('#spTypeF .fbtn').forEach(x=>x.classList.remove('active'));b.classList.add('active');renderSponsors();});

/* ── MODAL ── */
function openEditModal(id){
  const c=classes.find(x=>x.id===id);if(!c)return;
  editingId=id;
  document.getElementById('modalTitle').textContent='Editar patrocínio · '+c.name;
  document.getElementById('fName').value=c.name;
  document.getElementById('fTime').value=c.time;
  document.getElementById('fAud').value=c.aud;
  document.getElementById('fLocal').value=c.local;
  document.getElementById('fSp').value=c.sp;
  document.getElementById('fBrand').value=c.brand||'';
  document.getElementById('overlay').classList.add('open');
}
function closeModal(){document.getElementById('overlay').classList.remove('open');editingId=null;}
async function saveClass(){
  const c=classes.find(x=>x.id===editingId);if(!c)return;
  c.name=document.getElementById('fName').value.trim()||c.name;
  c.time=document.getElementById('fTime').value;
  c.aud=parseInt(document.getElementById('fAud').value)||c.aud;
  c.local=document.getElementById('fLocal').value;
  c.sp=document.getElementById('fSp').value;
  c.brand=document.getElementById('fBrand').value.trim();
  closeModal();await saveClasses();updateAll();showToast('Aula atualizada');
}
function showToast(msg){
  const t=document.getElementById('toast');document.getElementById('toastMsg').textContent=msg;
  t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2800);
}
function updateAll(){updateKPIs();renderGrid();renderOppTable();}

document.getElementById('catF').addEventListener('click',e=>{const b=e.target.closest('.fbtn');if(!b)return;catFilter=b.dataset.v;document.querySelectorAll('#catF .fbtn').forEach(x=>x.classList.remove('active'));b.classList.add('active');renderGrid();});
document.getElementById('spF').addEventListener('click',e=>{const b=e.target.closest('.fbtn');if(!b)return;spFilter=b.dataset.v;document.querySelectorAll('#spF .fbtn').forEach(x=>x.classList.remove('active'));b.classList.add('active');renderGrid();});

/* ── EXCEL IMPORT ── */
const DAY_MAP={'segunda':0,'terca':1,'terça':1,'quarta':2,'quinta':3,'sexta':4,'sabado':5,'sábado':5,'domingo':6};
function normalizeDay(s){return DAY_MAP[s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'')]??0;}

function handleDrop(e){e.preventDefault();document.getElementById('uploadZone').classList.remove('drag');const f=e.dataTransfer.files[0];if(f)handleFile(f);}
function handleFile(file){
  if(!file)return;
  const res=document.getElementById('uploadResult');
  const ext=file.name.split('.').pop().toLowerCase();
  if(!['xlsx','xls','csv'].includes(ext)){res.className='upload-result err';res.innerHTML='<i class="ti ti-x"></i>Formato inválido. Use .xlsx, .xls ou .csv';return;}
  const reader=new FileReader();
  reader.onload=e=>{
    try{
      const wb=XLSX.read(e.target.result,{type:'array'});
      const ws=wb.Sheets[wb.SheetNames[0]];
      const rows=XLSX.utils.sheet_to_json(ws,{defval:''});
      if(!rows.length){res.className='upload-result err';res.innerHTML='<i class="ti ti-x"></i>Planilha vazia ou sem dados.';return;}
      pendingImport=rows.map((r,i)=>({
        id:`import-${Date.now()}-${i}`,
        week:Math.max(0,Math.min(3,(parseInt(r.semana)||1)-1)),
        day:normalizeDay(String(r.dia||'')),
        time:String(r.horario||'07:00'),
        name:String(r.nome||'Aula'),
        cat:String(r.modalidade||'yoga').toLowerCase(),
        local:String(r.local||'Estação Ipanema Norte'),
        sp:['direct','incentive','open'].includes(String(r.patrocinio))? String(r.patrocinio):'open',
        brand:String(r.marca||''),
        aud:parseInt(r.publico)||80,
      }));
      res.className='upload-result ok';res.innerHTML=`<i class="ti ti-check"></i>${rows.length} aulas carregadas. Confirme abaixo para substituir a grade.`;
      document.getElementById('previewSection').style.display='block';
      document.getElementById('previewCount').textContent=pendingImport.length+' aulas na pré-visualização';
      document.getElementById('previewBody').innerHTML=pendingImport.slice(0,30).map(r=>`<tr><td>${r.week+1}</td><td>${DAYFULL[r.day]}</td><td>${r.time}</td><td>${r.name}</td><td><span class="b-cat">${CATLABELS[r.cat]||r.cat}</span></td><td>${r.local}</td><td><span class="badge ${r.sp==='direct'?'b-dir':r.sp==='incentive'?'b-inc':'b-open'}">${SP_LABEL[r.sp]}</span></td><td>${r.brand}</td><td>${r.aud}</td></tr>`).join('')+(pendingImport.length>30?`<tr><td colspan="9" style="text-align:center;color:var(--txf)">… e mais ${pendingImport.length-30} aulas</td></tr>`:'');
    }catch(err){res.className='upload-result err';res.innerHTML='<i class="ti ti-x"></i>Erro ao ler arquivo: '+err.message;}
  };
  reader.readAsArrayBuffer(file);
}
async function applyImport(){
  if(!pendingImport.length)return;
  classes=pendingImport;pendingImport=[];
  await saveClasses();updateAll();
  document.getElementById('previewSection').style.display='none';
  document.getElementById('uploadResult').className='upload-result ok';
  document.getElementById('uploadResult').innerHTML='<i class="ti ti-check"></i>Grade atualizada com sucesso!';
  showToast('Grade importada com sucesso');
  setPage('grade');
}

/* ── CHARTS ── */
function rebuildCharts(){
  const wl=WEEKS_META.map(w=>w.label);
  const openD=[0,1,2,3].map(w=>classes.filter(c=>c.week===w&&c.sp==='open').length);
  const incD=[0,1,2,3].map(w=>classes.filter(c=>c.week===w&&c.sp==='incentive').length);
  const dirD=[0,1,2,3].map(w=>classes.filter(c=>c.week===w&&c.sp==='direct').length);
  const D=id=>{if(charts[id]){charts[id].destroy();delete charts[id];}};
  ['ch1','ch2','ch3','ch4','ch5'].forEach(D);
  charts.ch1=new Chart(document.getElementById('ch1'),{type:'bar',data:{labels:wl,datasets:[{label:'Patrocinada',data:dirD,backgroundColor:'#1D9E75',borderRadius:4},{label:'Via incentivo',data:incD,backgroundColor:'#b87010',borderRadius:4},{label:'Sem patrocínio',data:openD,backgroundColor:'#ed1847',borderRadius:4}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{stacked:true,grid:{display:false}},y:{stacked:true,grid:{color:'rgba(128,128,128,.1)'},ticks:{stepSize:10}}}}});
  charts.ch2=new Chart(document.getElementById('ch2'),{type:'line',data:{labels:wl,datasets:[{label:'Sem patrocínio',data:openD,borderColor:'#ed1847',backgroundColor:'rgba(237,24,71,.08)',fill:true,tension:.4,pointRadius:5,pointBackgroundColor:'#ed1847'},{label:'Meta',data:[15,15,15,15],borderColor:'#1860b8',borderDash:[5,4],borderWidth:1.5,pointRadius:0,fill:false}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{grid:{color:'rgba(128,128,128,.1)'},min:0}}}});
  const cats=Object.keys(CATCOLORS);
  const cc=cats.map(cat=>classes.filter(c=>c.cat===cat&&c.sp==='open').length);
  charts.ch3=new Chart(document.getElementById('ch3'),{type:'doughnut',data:{labels:cats.map(c=>CATLABELS[c]),datasets:[{data:cc,backgroundColor:Object.values(CATCOLORS),borderWidth:2,borderColor:'var(--surf)'}]},options:{responsive:true,maintainAspectRatio:false,cutout:'60%',plugins:{legend:{display:false}}}});
  const dl=document.getElementById('ch3leg');dl.innerHTML='';
  cats.forEach((c,i)=>{dl.innerHTML+=`<div style="display:flex;align-items:center;gap:4px;font-size:10px;color:var(--txm)"><div style="width:8px;height:8px;border-radius:2px;background:${CATCOLORS[c]};flex-shrink:0"></div>${CATLABELS[c]}<span style="margin-left:auto;font-weight:600;color:var(--tx);padding-left:8px">${cc[i]}</span></div>`;});
  const l4=document.getElementById('ch4leg');l4.innerHTML='';
  cats.forEach(c=>{l4.innerHTML+=`<div class="cli"><div class="clsq" style="background:${CATCOLORS[c]}"></div>${CATLABELS[c]}</div>`;});
  charts.ch4=new Chart(document.getElementById('ch4'),{type:'bar',data:{labels:wl,datasets:cats.map(c=>({label:CATLABELS[c],data:[0,1,2,3].map(w=>classes.filter(cl=>cl.week===w&&cl.cat===c&&cl.sp==='open').length),backgroundColor:CATCOLORS[c],borderRadius:3}))},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{grid:{color:'rgba(128,128,128,.1)'},ticks:{stepSize:2}}}}});
  charts.ch5=new Chart(document.getElementById('ch5'),{type:'line',data:{labels:wl,datasets:[{label:'Patrocinada',data:[0,1,2,3].map(w=>classes.filter(c=>c.week===w&&c.sp==='direct').reduce((s,c)=>s+c.aud,0)),borderColor:'#1D9E75',backgroundColor:'rgba(29,158,117,.1)',fill:true,tension:.4,pointRadius:4,pointBackgroundColor:'#1D9E75'},{label:'Via incentivo',data:[0,1,2,3].map(w=>classes.filter(c=>c.week===w&&c.sp==='incentive').reduce((s,c)=>s+c.aud,0)),borderColor:'#b87010',backgroundColor:'rgba(184,112,16,.08)',fill:true,tension:.4,pointRadius:4,pointBackgroundColor:'#b87010'},{label:'Sem patrocínio',data:[0,1,2,3].map(w=>classes.filter(c=>c.week===w&&c.sp==='open').reduce((s,c)=>s+c.aud,0)),borderColor:'#ed1847',backgroundColor:'rgba(237,24,71,.07)',fill:true,tension:.4,pointRadius:4,pointBackgroundColor:'#ed1847'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{grid:{color:'rgba(128,128,128,.1)'},ticks:{callback:v=>v>=1000?(v/1000).toFixed(0)+'k':v}}}}});
  const totalW=[0,1,2,3].map(w=>classes.filter(c=>c.week===w).length);
  const maxOI=openD.indexOf(Math.max(...openD));
  document.getElementById('ins1').textContent=`${WEEKS_META[maxOI].label} (${WEEKS_META[maxOI].range}) tem ${openD[maxOI]} aulas sem patrocínio — maior janela do período.`;
  const cfO=[0,1,2,3].map(w=>classes.filter(c=>c.week===w&&c.cat==='crossfit'&&c.sp==='open').length);
  document.getElementById('ins2').textContent=`CrossFit tem ${Math.max(...cfO)} slots abertos sem patrocínio. Alto público, baixa cobertura.`;
  const bestI=dirD.map((d,i)=>totalW[i]?Math.round(d/totalW[i]*100):0).reduce((bi,v,i,a)=>v>a[bi]?i:bi,0);
  document.getElementById('ins3').textContent=`${WEEKS_META[bestI].label} tem maior cobertura de patrocínio direto (${dirD[bestI]} de ${totalW[bestI]} aulas).`;
  document.getElementById('ins4').textContent=`Yoga tem ${classes.filter(c=>c.cat==='yoga'&&c.sp==='open').length} slots abertos — perfil ideal para Vivo e Danone YoPRO.`;
  const covPct=classes.length?Math.round(classes.filter(c=>c.sp!=='open').length/classes.length*100):0;
  document.getElementById('ins6').textContent=`${covPct}% das aulas têm algum patrocínio. Meta: ≥85%. ${covPct<85?'Ampliar parcerias.':'Acima da meta.'}`;
  document.getElementById('brandRec').innerHTML=[{brand:'Vivo',seg:'Telecom',cats:['yoga','meditacao'],weeks:'2,3,4',type:'Naming'},{brand:'Amstel Ultra',seg:'Bebidas',cats:['crossfit','hiit'],weeks:'1,2',type:'Pós-treino'},{brand:'Danone YoPRO',seg:'Nutrição',cats:['musculacao','pilates'],weeks:'1,3',type:'Sampling'},{brand:'Under Armour',seg:'Moda',cats:['crossfit','danca','hiit'],weeks:'3,4',type:'Kit instrutores'},{brand:'Santander',seg:'Financeiro',cats:['yoga','danca'],weeks:'2,4',type:'Branding'},{brand:'Bradesco Saúde',seg:'Saúde',cats:['meditacao','pilates'],weeks:'1,2,3',type:'Lei Incentivo'}].map(r=>{const slots=r.cats.reduce((s,c)=>s+classes.filter(cl=>cl.cat===c&&cl.sp==='open').length,0);const pub=r.cats.reduce((s,c)=>s+classes.filter(cl=>cl.cat===c&&cl.sp==='open').reduce((ss,cl)=>ss+cl.aud,0),0);return`<tr><td style="font-weight:500">${r.brand}</td><td>${r.seg}</td><td>${r.cats.map(c=>`<span class="b-cat" style="margin-right:3px">${CATLABELS[c]}</span>`).join('')}</td><td>Sem. ${r.weeks}</td><td><span class="badge b-open">${slots} slots</span></td><td>~${(pub/1000).toFixed(0)}k</td><td>${r.type}</td></tr>`;}).join('');
}

async function initApp(){
  initTheme();
  setTodayLabel();
  await loadClasses();
  buildWeekTabs();
  updateAll();
}
checkSession();
</script>
</body>
</html>"""

html = html.replace("LOGO_SRC_PLACEHOLDER", logo_src)

with open("/home/claude/mude-dashboard/index.html", "w") as f:
    f.write(html)

print(f"Done: {len(html)} chars, {html.count(chr(10))} lines")
