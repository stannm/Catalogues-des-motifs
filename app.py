<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Catalogue des motifs – Rouge & Blanc</title>
  <meta name="description" content="Catalogue animé des motifs avec effet néon rouge, zoom au survol, commentaires publics et zone admin (téléchargement + lecture des commentaires)." />
  <style>
    :root{
      --rouge:#e10600; /* rouge principal */
      --rouge-neon:#ff1a3d; /* rouge néon */
      --rouge-dark:#b00500;
      --blanc:#ffffff;
      --fond:#f7f7f8;
      --encre:#161616;
      --muted:#8a8a8a;
    }
    *{box-sizing:border-box}
    html,body{margin:0;padding:0;background:var(--fond);color:var(--encre);font-family:ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,"Apple Color Emoji","Segoe UI Emoji"}

    /* Barre top */
    .topbar{
      position:sticky;top:0;z-index:50;
      display:flex;align-items:center;gap:.75rem;
      padding:.75rem 1rem;background:var(--blanc);
      border-bottom:1px solid #e7e7ea;
    }
    .badge{
      background:var(--rouge);color:var(--blanc);
      padding:.25rem .5rem;border-radius:.5rem;font-weight:600;font-size:.75rem;
      letter-spacing:.02em
    }
    .title{font-size:1.1rem;font-weight:700}
    .spacer{flex:1}
    .btn{appearance:none;border:1px solid #e6e6ea;background:#fff;color:#111;padding:.5rem .75rem;border-radius:.7rem;cursor:pointer;transition:transform .06s ease,box-shadow .2s}
    .btn:hover{box-shadow:0 6px 16px rgba(0,0,0,.08)}
    .btn:active{transform:scale(.98)}
    .btn--primary{background:var(--rouge);color:#fff;border-color:var(--rouge-dark)}
    .btn--primary:hover{box-shadow:0 10px 22px rgba(225,6,0,.25)}
    .admin-chip{display:none;margin-left:.5rem;font-size:.75rem;color:#fff;background:linear-gradient(90deg,var(--rouge),var(--rouge-neon));padding:.25rem .5rem;border-radius:.5rem}

    /* Grille */
    .wrap{max-width:1100px;margin:0 auto;padding:1rem}
    .grid{display:grid;grid-template-columns:repeat(1,minmax(0,1fr));gap:1rem}
    @media(min-width:640px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
    @media(min-width:980px){.grid{grid-template-columns:repeat(3,minmax(0,1fr))}}

    /* Carte image */
    .card{position:relative;background:#fff;border:1px solid #eee;border-radius:16px;overflow:hidden;box-shadow:0 10px 24px rgba(0,0,0,.06)}
    .imgbox{position:relative;overflow:hidden;background:#000}
    .imgbox img{display:block;width:100%;height:280px;object-fit:cover;transition:transform .25s ease, filter .25s ease, box-shadow .25s ease;transform-origin:center}
    /* Néon rouge (glow) */
    .imgbox img.neon{box-shadow:0 0 10px rgba(255,26,61,.6), 0 0 24px rgba(255,26,61,.45), 0 0 48px rgba(255,26,61,.25)}
    .imgbox:hover img{transform:scale(1.12); filter:saturate(1.1) contrast(1.05)}
    /* Curseur zoom */
    .imgbox{cursor:zoom-in}

    .card-body{padding:12px 14px 14px}
    .card-title{font-weight:700}
    .meta{font-size:.82rem;color:var(--muted)}

    .overlay{
      position:absolute;inset:auto .5rem .5rem .5rem;display:flex;gap:.5rem;justify-content:flex-end;align-items:center;
    }
    .tag{position:absolute;top:.5rem;left:.5rem;background:#fff;color:var(--rouge);border-radius:999px;padding:.2rem .55rem;font-size:.75rem;border:1px solid #ffd1d6}

    .pill{display:inline-flex;align-items:center;gap:.35rem;padding:.3rem .55rem;border-radius:.65rem;border:1px solid #eee;background:#fff;color:#111;font-size:.8rem}

    /* Modals */
    .modal-backdrop{position:fixed;inset:0;background:rgba(0,0,0,.46);display:none;align-items:center;justify-content:center;padding:1rem;z-index:100}
    .modal{width:min(680px,95vw);background:#fff;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.35);overflow:hidden}
    .modal-h{display:flex;align-items:center;justify-content:space-between;padding:.9rem 1rem;border-bottom:1px solid #eee}
    .modal-b{padding:1rem}

    label{font-size:.9rem;color:#333}
    input[type="text"], textarea, input[type="password"]{width:100%;padding:.6rem .7rem;border:1px solid #ddd;border-radius:.6rem}
    textarea{min-height:110px}

    .toast{position:fixed;bottom:16px;left:50%;transform:translateX(-50%);background:#111;color:#fff;padding:.6rem .9rem;border-radius:.7rem;box-shadow:0 6px 16px rgba(0,0,0,.2);opacity:0;pointer-events:none;transition:opacity .25s ease;z-index:120}
    .toast.show{opacity:1}

    .footer{padding:3rem 1rem;text-align:center;color:#999}
  </style>
</head>
<body>
  <header class="topbar">
    <span class="badge">ROUGE & BLANC</span>
    <div class="title">Catalogue des motifs</div>
    <div class="spacer"></div>
    <button id="btn-login" class="btn btn--primary">Admin</button>
    <span id="admin-chip" class="admin-chip">admin connecté</span>
  </header>

  <main class="wrap">
    <section id="grid" class="grid"></section>
  </main>

  <div class="footer">JARVIS • Catalogue statique compatible GitHub Pages · © 2025</div>

  <!-- Modal commentaire -->
  <div id="modal-comment" class="modal-backdrop" role="dialog" aria-modal="true">
    <div class="modal">
      <div class="modal-h">
        <strong>Laisser un commentaire</strong>
        <button class="btn" data-close-comment>Fermer</button>
      </div>
      <div class="modal-b">
        <form id="comment-form">
          <div style="display:grid;gap:.75rem">
            <div>
              <label>Votre nom</label>
              <input type="text" id="comment-name" placeholder="Votre nom ou pseudo" required>
            </div>
            <div>
              <label>Commentaire</label>
              <textarea id="comment-text" placeholder="Votre message" required></textarea>
            </div>
            <div style="display:flex;gap:.5rem;justify-content:flex-end">
              <button type="button" class="btn" data-close-comment>Annuler</button>
              <button type="submit" class="btn btn--primary">Publier</button>
            </div>
          </div>
          <input type="hidden" id="comment-imgid" />
        </form>
      </div>
    </div>
  </div>

  <!-- Modal admin (lecture commentaires) -->
  <div id="modal-admin" class="modal-backdrop" role="dialog" aria-modal="true">
    <div class="modal">
      <div class="modal-h">
        <strong>Espace Admin</strong>
        <div style="display:flex;gap:.5rem">
          <button id="btn-logout" class="btn">Se déconnecter</button>
          <button class="btn" data-close-admin>Fermer</button>
        </div>
      </div>
      <div class="modal-b">
        <div id="admin-content"></div>
      </div>
    </div>
  </div>

  <!-- Modal login -->
  <div id="modal-login" class="modal-backdrop" role="dialog" aria-modal="true">
    <div class="modal">
      <div class="modal-h">
        <strong>Connexion Admin</strong>
        <button class="btn" data-close-login>Fermer</button>
      </div>
      <div class="modal-b">
        <div id="login-step">
          <div style="display:grid;gap:.75rem;max-width:420px">
            <div>
              <label>Mot de passe</label>
              <input type="password" id="admin-pass" placeholder="••••••••" autofocus required />
            </div>
            <div style="display:flex;gap:.5rem;justify-content:flex-end">
              <button class="btn" data-close-login>Annuler</button>
              <button id="btn-do-login" class="btn btn--primary">Se connecter</button>
            </div>
            <p style="color:#999;font-size:.85rem">Note : authentification purement <em>front-end</em> pour GitHub Pages (non sécurisée pour contenus sensibles). Pour une vraie sécurité, prévoir un backend (Supabase, Firebase, etc.).</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div id="toast" class="toast">Enregistré ✅</div>

  <script>
    // =========================
    // CONFIG – à personnaliser
    // =========================
    const CONFIG = {
      THEME: { neon: true },
      ADMIN_HASH: '2c39b2465d97f3a8e32f6a42d90d6381c907fd10689d430eb43b34397547f9be', // SHA-256 de "tdi2025!" (changez-le)
      IMAGES: [
        // Remplacez ces images par vos motifs. URLs remotes OK.
        { id: 'motif-01', title: 'Motif géométrique 01', src: 'https://picsum.photos/id/1011/1000/700' },
        { id: 'motif-02', title: 'Motif lignes 02',     src: 'https://picsum.photos/id/1015/1000/700' },
        { id: 'motif-03', title: 'Motif floral 03',     src: 'https://picsum.photos/id/1025/1000/700' },
        { id: 'motif-04', title: 'Motif marbre 04',     src: 'https://picsum.photos/id/1039/1000/700' },
        { id: 'motif-05', title: 'Motif damier 05',     src: 'https://picsum.photos/id/1060/1000/700' },
        { id: 'motif-06', title: 'Motif techno 06',     src: 'https://picsum.photos/id/1074/1000/700' },
      ],
    };

    // Utilitaires
    const $ = (sel, parent=document) => parent.querySelector(sel);
    const $$ = (sel, parent=document) => Array.from(parent.querySelectorAll(sel));
    const show = (el, v=true) => el.style.display = v ? 'flex' : 'none';
    const toast = (msg) => { const t = $('#toast'); t.textContent = msg; t.classList.add('show'); setTimeout(()=>t.classList.remove('show'), 1300); };

    const COMMENTS_KEY = 'catalogue.motifs.comments';
    function readComments(){ try { return JSON.parse(localStorage.getItem(COMMENTS_KEY) || '{}'); } catch(e){ return {}; } }
    function writeComments(obj){ localStorage.setItem(COMMENTS_KEY, JSON.stringify(obj)); }

    function getIsAdmin(){ return sessionStorage.getItem('catalogue.admin') === '1'; }
    function setIsAdmin(v){ v ? sessionStorage.setItem('catalogue.admin','1') : sessionStorage.removeItem('catalogue.admin'); updateAdminUI(); }

    async function sha256Hex(str){
      const enc = new TextEncoder().encode(str);
      const buf = await crypto.subtle.digest('SHA-256', enc);
      return [...new Uint8Array(buf)].map(x=>x.toString(16).padStart(2,'0')).join('');
    }

    function dlFile(url, filename){
      const a = document.createElement('a');
      a.href = url; a.download = filename || '';
      document.body.appendChild(a); a.click(); a.remove();
    }

    // Rendu de la grille
    function renderGrid(){
      const wrap = $('#grid');
      wrap.innerHTML = '';
      CONFIG.IMAGES.forEach(img => {
        const card = document.createElement('article');
        card.className = 'card';
        card.innerHTML = `
          <div class="imgbox">
            <img src="${img.src}" alt="${img.title}" class="neon" data-imgid="${img.id}">
            <span class="tag">${img.id}</span>
            <div class="overlay">
              <button class="pill" data-comment data-id="${img.id}">💬 Commenter</button>
              <button class="pill" data-view-comments data-id="${img.id}" style="display:none">📖 Voir commentaires</button>
              <button class="pill" data-download data-id="${img.id}" data-src="${img.src}" style="display:none">⬇️ Télécharger</button>
            </div>
          </div>
          <div class="card-body">
            <div class="card-title">${img.title}</div>
            <div class="meta">Thème rouge & blanc · effet néon + zoom</div>
          </div>
        `;
        wrap.appendChild(card);

        // Zoom: transform-origin suit la souris
        const imgEl = $('img', card);
        card.querySelector('.imgbox').addEventListener('mousemove', (e)=>{
          const r = imgEl.getBoundingClientRect();
          const x = ((e.clientX - r.left)/r.width)*100;
          const y = ((e.clientY - r.top)/r.height)*100;
          imgEl.style.transformOrigin = `${x}% ${y}%`;
        });
      });
      updateAdminUI();
    }

    function updateAdminUI(){
      const isAdmin = getIsAdmin();
      $$('#grid .card').forEach(card => {
        const btnView = $('[data-view-comments]', card);
        const btnDl = $('[data-download]', card);
        if (btnView) btnView.style.display = isAdmin ? 'inline-flex' : 'none';
        if (btnDl) btnDl.style.display = isAdmin ? 'inline-flex' : 'none';
      });
      $('#admin-chip').style.display = isAdmin ? 'inline-flex' : 'none';
    }

    // Gestion événements globaux
    document.addEventListener('click', (e)=>{
      const t = e.target;
      if (t.matches('[data-close-comment]')) show($('#modal-comment'), false);
      if (t.matches('[data-close-admin]')) show($('#modal-admin'), false);
      if (t.matches('[data-close-login]')) show($('#modal-login'), false);

      if (t.matches('[data-comment]')){
        const id = t.getAttribute('data-id');
        $('#comment-imgid').value = id;
        $('#comment-name').value = '';
        $('#comment-text').value = '';
        show($('#modal-comment'), true);
      }

      if (t.matches('[data-download]')){
        const src = t.getAttribute('data-src');
        const id = t.getAttribute('data-id');
        dlFile(src, id + '.jpg');
      }

      if (t.matches('[data-view-comments]')){
        const id = t.getAttribute('data-id');
        openAdminForImage(id);
      }
    });

    // Form commentaire
    $('#comment-form').addEventListener('submit', (e)=>{
      e.preventDefault();
      const id = $('#comment-imgid').value;
      const name = $('#comment-name').value.trim();
      const text = $('#comment-text').value.trim();
      if (!name || !text) return;
      const all = readComments();
      const list = all[id] || [];
      list.push({ name, text, ts: Date.now() });
      all[id] = list; writeComments(all);
      show($('#modal-comment'), false);
      toast('Commentaire envoyé ✅');
    });

    // Login/logout
    $('#btn-login').addEventListener('click', ()=>{
      if (getIsAdmin()) { // déjà admin → ouvrir modal admin
        buildAdminContent();
        show($('#modal-admin'), true);
      } else {
        show($('#modal-login'), true);
        $('#admin-pass').value = '';
        $('#admin-pass').focus();
      }
    });

    $('#btn-logout').addEventListener('click', ()=>{
      setIsAdmin(false);
      toast('Déconnecté');
    });

    $('#btn-do-login').addEventListener('click', async ()=>{
      const pass = $('#admin-pass').value;
      const hash = await sha256Hex(pass);
      if (hash === CONFIG.ADMIN_HASH){
        setIsAdmin(true);
        show($('#modal-login'), false);
        buildAdminContent();
        show($('#modal-admin'), true);
        toast('Connecté en admin ✅');
      } else {
        toast('Mot de passe incorrect');
      }
    });

    // Admin content
    function buildAdminContent(){
      const box = $('#admin-content');
      const all = readComments();
      const none = Object.keys(all).length === 0 ? '<p style="color:#999">Aucun commentaire pour le moment.</p>' : '';
      let html = '';
      CONFIG.IMAGES.forEach(img => {
        const list = all[img.id] || [];
        html += `
          <article style="display:grid;grid-template-columns:120px 1fr;gap:12px;align-items:flex-start;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #eee">
            <div>
              <img src="${img.src}" alt="${img.title}" style="width:120px;height:80px;object-fit:cover;border-radius:8px;box-shadow:0 6px 14px rgba(0,0,0,.1)">
              <div style="margin-top:.5rem;display:flex;gap:.5rem">
                <button class="btn" onclick="dlFile('${img.src}','${img.id}.jpg')">⬇️ Télécharger</button>
              </div>
            </div>
            <div>
              <strong>${img.title}</strong>
              <div style="font-size:.85rem;color:#999">${img.id}</div>
              <div style="margin-top:.5rem">
                ${list.length===0?'<em style="color:#bbb">Aucun commentaire</em>':''}
                ${list.map(c => `
                  <div style="border:1px solid #eee;border-radius:10px;padding:.6rem .7rem;margin:.5rem 0;background:#fff">
                    <div style="font-size:.85rem;color:#333"><strong>${escapeHtml(c.name)}</strong> · <span style="color:#888">${new Date(c.ts).toLocaleString('fr-FR')}</span></div>
                    <div style="margin-top:.35rem;white-space:pre-wrap;color:#222">${escapeHtml(c.text)}</div>
                  </div>
                `).join('')}
              </div>
            </div>
          </article>
        `;
      });
      box.innerHTML = (none ? none : '') + html;
    }

    function openAdminForImage(id){
      if (!getIsAdmin()){
        toast('Réservé à l\'admin'); return;
      }
      buildAdminContent();
      show($('#modal-admin'), true);
      // scroll vers l'image
      const target = $('#admin-content').querySelector(`img[src*="${CSS.escape(CONFIG.IMAGES.find(x=>x.id===id)?.src || '')}"]`);
      if (target) target.scrollIntoView({behavior:'smooth',block:'start'});
    }

    function escapeHtml(str){
      return String(str).replace(/[&<>"']/g, s=>({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[s]));
    }

    // Init
    renderGrid();
  </script>
</body>
</html>
