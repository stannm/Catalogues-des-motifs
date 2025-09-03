import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Catalogue des motifs – SADELA INDUSTRIE", layout="wide")

# ============== CONFIGURATION ==============
ADMIN_PASSWORD = "tdi2025!"  # Change ce mot de passe 
IMAGES = [
    {"id": "motif-01", "title": "Motif géométrique 01", "src": "https://picsum.photos/id/1011/1000/700"},
    {"id": "motif-02", "title": "Motif lignes 02",     "src": "https://picsum.photos/id/1015/1000/700"},
    {"id": "motif-03", "title": "Motif floral 03",     "src": "https://picsum.photos/id/1025/1000/700"},
    {"id": "motif-04", "title": "Motif marbre 04",     "src": "https://picsum.photos/id/1039/1000/700"},
    {"id": "motif-05", "title": "Motif damier 05",     "src": "https://picsum.photos/id/1060/1000/700"},
    {"id": "motif-06", "title": "Motif techno 06",     "src": "https://picsum.photos/id/1074/1000/700"},
]

if "feasibility_comments" not in st.session_state:
    st.session_state.feasibility_comments = {}
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_image_id" not in st.session_state:
    st.session_state.selected_image_id = None
if "delete_comment_trigger" not in st.session_state:
    st.session_state.delete_comment_trigger = None

# ============== CUSTOM CSS FOR ZOOM & NEON ==============
st.markdown("""
    <style>
    .motif-img {
        transition: transform 0.3s cubic-bezier(.25,.8,.25,1), box-shadow 0.2s;
        border-radius: 15px;
        box-shadow: 0 0 0px #e10600;
        border: 2px solid #fff;
        cursor: pointer;
    }
    .motif-img:hover {
        transform: scale(1.07);
        box-shadow: 0 0 22px 4px #e10600, 0 0 2px 1px #fff;
        border: 2px solid #e10600;
        filter: brightness(1.12);
    }
    </style>
""", unsafe_allow_html=True)

# ============== HEADER / ADMIN ==============
col1, col2, col3 = st.columns([2,5,2])
with col2:
    st.markdown("### Catalogue des motifs")
with col3:
    if st.session_state.admin:
        st.markdown('<span style="background:linear-gradient(90deg,#e10600,#ff1a3d);color:white;padding:4px 10px;border-radius:8px;">Admin connecté</span>', unsafe_allow_html=True)
        if st.button("Déconnexion admin"):
            st.session_state.admin = False
            st.success("Déconnecté")
    else:
        if st.button("Espace admin"):
            st.session_state.show_admin_login = True

st.write("---")

# ============== ADMIN LOGIN MODAL ==============
if st.session_state.get("show_admin_login", False):
    with st.form("admin-login"):
        st.write("### Connexion Admin")
        pwd = st.text_input("Mot de passe", type="password")
        ok = st.form_submit_button("Se connecter")
        cancel = st.form_submit_button("Annuler")
        if cancel:
            st.session_state.show_admin_login = False
        elif ok:
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin = True
                st.session_state.show_admin_login = False
                st.success("Connecté en admin ✅")
            else:
                st.error("Mot de passe incorrect")

# ============== ADMIN ZONE ==============
if st.session_state.admin:
    st.write("## Espace Admin")
    for img in IMAGES:
        feasibility = st.session_state.feasibility_comments.get(img["id"], [])
        col_img, col_info = st.columns([1,2])
        with col_img:
            st.markdown(f'<img src="{img["src"]}" class="motif-img" width="220px" style="margin-bottom:6px;" />', unsafe_allow_html=True)
            st.download_button("Télécharger l'image", img["src"], file_name=img["id"] + ".jpg")
        with col_info:
            st.markdown(f"**{img['title']}** ({img['id']})")
            # Afficher commentaires de faisabilité (privés)
            if feasibility:
                st.markdown("#### Demandes de faisabilité (privées)")
                for idx, f in enumerate(feasibility):
                    delete_key = f"delcomment_{img['id']}_{idx}"
                    st.markdown(
                        f"""
                        <div style="border:1px solid #e10600;border-radius:10px;padding:.6rem .7rem;margin:.5rem 0;background:#fff">
                        <strong>{f['name']}</strong> · <span style='color:#888'>{f['ts']}</span>
                        <div style="margin-top:.35rem;white-space:pre-wrap;color:#e10600">{f['text']}</div>
                        <div style="font-size:80%;color:#888">Email: {f['email']} · Téléphone: {f['phone']}</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                    # Bouton pour supprimer le commentaire
                    if st.button("🗑️ Supprimer ce commentaire", key=delete_key):
                        st.session_state.delete_comment_trigger = (img["id"], idx)
                        st.experimental_rerun()
            else:
                st.markdown("<em style='color:#bbb'>Aucune demande de faisabilité</em>", unsafe_allow_html=True)
    st.write("---")

# ======= SUPPRESSION DES COMMENTAIRES ADMIN =======
# Ce bloc doit être placé après la zone admin pour que le bouton fonctionne correctement
if st.session_state.delete_comment_trigger:
    img_id, comm_idx = st.session_state.delete_comment_trigger
    feas_list = st.session_state.feasibility_comments.get(img_id, [])
    if 0 <= comm_idx < len(feas_list):
        feas_list.pop(comm_idx)
        st.session_state.feasibility_comments[img_id] = feas_list
    st.session_state.delete_comment_trigger = None
    st.experimental_rerun()

# ============== BARRE DE RECHERCHE ==============
search_query = st.text_input("🔎 Rechercher un motif...", "")
filtered_images = [img for img in IMAGES if search_query.lower() in img["title"].lower() or search_query.lower() in img["id"].lower()]

# ============== GRID MOTIFS ==============
st.write("## Motifs")
cols = st.columns(3)
for idx, img in enumerate(filtered_images):
    with cols[idx % 3]:
        # Sélection par image (bouton ou clickable avec Streamlit)
        if st.button(f"Sélectionner {img['title']}", key=f"select_{img['id']}"):
            st.session_state.selected_image_id = img["id"]
        st.markdown(f'<img src="{img["src"]}" class="motif-img" width="100%" style="margin-bottom:6px;" />', unsafe_allow_html=True)
        st.write("Thème rouge & blanc · effet néon + zoom")
        st.markdown(f"**{img['title']}**")
        st.markdown(f"<span style='background:#fff;color:#e10600;border-radius:999px;padding:2px 15px;border:1px solid #ffd1d6'>{img['id']}</span>", unsafe_allow_html=True)
        # Bouton Télécharger uniquement pour admin
        if st.session_state.admin:
            st.download_button("⬇️ Télécharger", img["src"], file_name=img["id"] + ".jpg")
        st.write("---")

# ============== FAISABILITÉ & COMMENTAIRE ==============
selected_id = st.session_state.selected_image_id
if selected_id:
    selected_img = next((img for img in IMAGES if img["id"] == selected_id), None)
    st.write(f"### Demander la faisabilité pour : {selected_img['title']}")
    with st.form(f"feasibility_form_{selected_id}"):
        name = st.text_input("Votre nom", key=f"feas_name_{selected_id}")
        email = st.text_input("Votre email", key=f"feas_email_{selected_id}")
        phone = st.text_input("Votre téléphone", key=f"feas_phone_{selected_id}")
        text = st.text_area("Votre demande / commentaire", key=f"feas_text_{selected_id}")
        submit = st.form_submit_button("Envoyer la demande")
        cancel = st.form_submit_button("Annuler la sélection")
        if cancel:
            st.session_state.selected_image_id = None
        elif submit:
            if not name or not email or not phone or not text:
                st.warning("Tous les champs sont obligatoires.")
            else:
                feas_list = st.session_state.feasibility_comments.get(selected_id, [])
                feas_list.append({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "text": text,
                    "ts": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })
                st.session_state.feasibility_comments[selected_id] = feas_list
                st.success("Demande envoyée ✅")
                st.session_state.selected_image_id = None

st.write("---")
st.write("STANNM • Catalogue statique pour SADELA INDUSTRIE · v0.11 © 2025")
