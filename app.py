import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Catalogue des motifs – Rouge & Blanc", layout="wide")

# ============== CONFIGURATION ==============
ADMIN_PASSWORD = "tdi2025!"  # Change ce mot de passe !
IMAGES = [
    {"id": "motif-01", "title": "Motif géométrique 01", "src": "https://picsum.photos/id/1011/1000/700"},
    {"id": "motif-02", "title": "Motif lignes 02",     "src": "https://picsum.photos/id/1015/1000/700"},
    {"id": "motif-03", "title": "Motif floral 03",     "src": "https://picsum.photos/id/1025/1000/700"},
    {"id": "motif-04", "title": "Motif marbre 04",     "src": "https://picsum.photos/id/1039/1000/700"},
    {"id": "motif-05", "title": "Motif damier 05",     "src": "https://picsum.photos/id/1060/1000/700"},
    {"id": "motif-06", "title": "Motif techno 06",     "src": "https://picsum.photos/id/1074/1000/700"},
]

# ============== SESSION STATE INIT ==============
if "comments" not in st.session_state:
    st.session_state.comments = {}
if "feasibility_comments" not in st.session_state:
    st.session_state.feasibility_comments = {}
if "admin" not in st.session_state:
    st.session_state.admin = False
if "selected_image_id" not in st.session_state:
    st.session_state.selected_image_id = None
if "basket" not in st.session_state:
    st.session_state.basket = []
if "show_admin_login" not in st.session_state:
    st.session_state.show_admin_login = False
if "theme" not in st.session_state:
    st.session_state.theme = {"primary": "#e10600", "secondary": "#fff"}  # Valeur par défaut
if "show_add_modal" not in st.session_state:
    st.session_state.show_add_modal = None  # id de l'image à ajouter
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False
if "popup_message" not in st.session_state:
    st.session_state.popup_message = ""

# ============== SIDEBAR : NAVIGATION & PANIER ==============
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Aller à",
    ["Accueil", "Motifs", "Panier", "Espace Admin" if st.session_state.admin else "Connexion admin"]
)
basket_count = len(st.session_state.basket)
st.sidebar.markdown("---")
st.sidebar.markdown(f"## 🛒 Panier ({basket_count})")
if st.session_state.basket:
    for img_id in st.session_state.basket:
        img = next((i for i in IMAGES if i["id"] == img_id), None)
        if img:
            st.sidebar.image(img["src"], width=80)
            st.sidebar.markdown(f"{img['title']}")
    if st.sidebar.button("Voir le panier complet"):
        page = "Panier"
else:
    st.sidebar.markdown("*Votre panier est vide*")

st.sidebar.markdown("---")
st.sidebar.write("STANNM • SADELA INDUSTRIE © 2025")

# ============== HEADER ==============
col1, col2, col3 = st.columns([2,5,2])
with col2:
    st.markdown("<h1 style='text-align:center;margin-bottom:0;'>Catalogue des motifs</h1>", unsafe_allow_html=True)
with col3:
    if st.session_state.admin:
        st.markdown('<span style="background:linear-gradient(90deg,{},{secondary});color:white;padding:4px 10px;border-radius:8px;">Admin connecté</span>'.format(
            st.session_state.theme.get("primary", "#e10600"), secondary=st.session_state.theme.get("secondary", "#fff")), unsafe_allow_html=True)

st.write("---")

# ============== PAGE ACCUEIL ==============
if page == "Accueil":
    st.markdown("## Bienvenue !")
    st.markdown("Découvrez notre sélection de motifs Rouge & Blanc. Utilisez le menu à gauche pour naviguer.")

# ============== PAGE MOTIFS ==============
if page == "Motifs":
    st.write("### Motifs disponibles")
    # Responsive grid : 1 colonne sur mobile, 3 sur desktop
    import streamlit as st
    import sys
    width = st.experimental_get_query_params().get("width",[1200])
    try:
        width = int(width[0])
    except Exception:
        width = 1200
    n_cols = 1 if width < 600 else 3

    cols = st.columns(n_cols)
    for idx, img in enumerate(IMAGES):
        with cols[idx % n_cols]:
            in_basket = img["id"] in st.session_state.basket
            st.image(img["src"], caption=img["title"], use_container_width=True)
            st.markdown(f"**{img['title']}**")
            if st.session_state.admin:
                st.download_button("⬇️ Télécharger", img["src"], file_name=img["id"] + ".jpg")
            if st.session_state.show_add_modal == img["id"]:
                st.write("Confirmer l'ajout au panier ?")
                confirm = st.button("Oui, ajouter", key=f"confirm_add_{img['id']}")
                cancel = st.button("Annuler", key=f"cancel_add_{img['id']}")
                if confirm:
                    st.session_state.basket.append(img["id"])
                    st.session_state.show_add_modal = None
                    st.session_state.popup_message = f"{img['title']} ajouté au panier !"
                    st.session_state.show_popup = True
                elif cancel:
                    st.session_state.show_add_modal = None
            elif not in_basket:
                if st.button(f"Ajouter au panier", key=f"basket_add_{img['id']}"):
                    st.session_state.show_add_modal = img["id"]
            else:
                if st.button(f"Retirer du panier", key=f"basket_remove_{img['id']}"):
                    st.session_state.basket.remove(img["id"])
                    st.info(f"{img['title']} retiré du panier.")

# ============== PAGE PANIER ==============
if page == "Panier":
    st.write("## Votre panier")
    if not st.session_state.basket:
        st.warning("Votre panier est vide.")
    else:
        basket_imgs = [img for img in IMAGES if img["id"] in st.session_state.basket]
        cols_basket = st.columns(len(basket_imgs))
        for i, img in enumerate(basket_imgs):
            with cols_basket[i]:
                st.image(img["src"], caption=img["title"], width=180)
                st.markdown(f"<span style='background:{st.session_state.theme['secondary']};color:{st.session_state.theme['primary']};border-radius:999px;padding:2px 15px;border:1px solid #ffd1d6'>{img['id']}</span>", unsafe_allow_html=True)

        with st.form("basket_form"):
            st.write("#### Vos coordonnées")
            name = st.text_input("Votre nom", key="basket_name")
            email = st.text_input("Votre email", key="basket_email")
            message = st.text_area("Votre demande ou commentaire global", key="basket_msg")
            comment = st.text_area("Commentaire (visible uniquement pour l'admin)", key="basket_admin_comment")
            submit = st.form_submit_button("Envoyer la demande groupée")
            cancel = st.form_submit_button("Vider le panier")
            if cancel:
                st.session_state.basket = []
                st.info("Panier vidé.")
            elif submit:
                if not name or not email or not message:
                    st.warning("Veuillez remplir tous les champs pour envoyer la demande.")
                else:
                    for img_id in st.session_state.basket:
                        feas_list = st.session_state.feasibility_comments.get(img_id, [])
                        feas_list.append({
                            "name": name,
                            "email": email,
                            "text": message,
                            "ts": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        })
                        st.session_state.feasibility_comments[img_id] = feas_list
                        if comment:
                            comments = st.session_state.comments.get(img_id, [])
                            comments.append({
                                "name": name,
                                "text": comment,
                                "ts": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                            })
                            st.session_state.comments[img_id] = comments
                    st.success("Votre demande groupée a bien été envoyée ✅")
                    st.session_state.basket = []
                    st.session_state.show_popup = True
                    st.session_state.popup_message = "Demande groupée envoyée avec succès !"

# ============== ADMIN LOGIN / ZONE ==============
if page == "Connexion admin" and not st.session_state.admin:
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
                st.success("Connecté en admin ✅")
            else:
                st.error("Mot de passe incorrect")

if page == "Espace Admin" and st.session_state.admin:
    st.write("## Espace Admin")
    with st.expander("🎨 Personnaliser le thème pour tous"):
        primary = st.color_picker("Couleur principale", value=st.session_state.theme.get("primary", "#e10600"))
        secondary = st.color_picker("Couleur secondaire", value=st.session_state.theme.get("secondary", "#fff"))
        if st.button("Appliquer le thème"):
            st.session_state.theme = {"primary": primary, "secondary": secondary}
            st.success("Thème mis à jour !")
    for img in IMAGES:
        comments = st.session_state.comments.get(img["id"], [])
        feasibility = st.session_state.feasibility_comments.get(img["id"], [])
        col_img, col_info = st.columns([1,2])
        with col_img:
            st.image(img["src"], width=220, caption=img["title"])
            st.download_button("Télécharger l'image", img["src"], file_name=img["id"] + ".jpg")
        with col_info:
            st.markdown(f"**{img['title']}** ({img['id']})")
            if comments:
                st.markdown("#### Commentaires (admin uniquement)")
                for idx, c in enumerate(comments):
                    st.markdown(
                        f"""
                        <div style="border:1px solid #eee;border-radius:10px;padding:.6rem .7rem;margin:.5rem 0;background:{st.session_state.theme['secondary']}">
                        <strong>{c['name']}</strong> · <span style='color:#888'>{c['ts']}</span>
                        <div style="margin-top:.35rem;white-space:pre-wrap;color:#222">{c['text']}</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                    if st.button(f"🗑️ Supprimer commentaire {idx+1}", key=f"del_pub_{img['id']}_{idx}"):
                        st.session_state.comments[img["id"]].pop(idx)
                        st.experimental_rerun()
            else:
                st.markdown("<em style='color:#bbb'>Aucun commentaire</em>", unsafe_allow_html=True)
            if feasibility:
                st.markdown("#### Demandes de faisabilité (privées)")
                for idx, f in enumerate(feasibility):
                    st.markdown(
                        f"""
                        <div style="border:1px solid {st.session_state.theme['primary']};border-radius:10px;padding:.6rem .7rem;margin:.5rem 0;background:{st.session_state.theme['secondary']}">
                        <strong>{f['name']}</strong> · <span style='color:#888'>{f['ts']}</span>
                        <div style="margin-top:.35rem;white-space:pre-wrap;color:{st.session_state.theme['primary']}">{f['text']}</div>
                        </div>
                        """, unsafe_allow_html=True
                    )
                    if st.button(f"🗑️ Supprimer faisabilité {idx+1}", key=f"del_feas_{img['id']}_{idx}"):
                        st.session_state.feasibility_comments[img["id"]].pop(idx)
                        st.experimental_rerun()
            else:
                st.markdown("<em style='color:#bbb'>Aucune demande de faisabilité</em>", unsafe_allow_html=True)
    st.write("---")

# ============== POPUP CONFIRMATION ==============
if st.session_state.show_popup:
    st.success(st.session_state.popup_message)
    st.session_state.show_popup = False
