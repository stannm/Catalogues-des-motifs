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

# ============== PANIER ANIMATION EN HAUT À DROITE ==============
basket_count = len(st.session_state.basket)
custom_css = f"""
<style>
#basket-anim {{
    position: fixed;
    top: 20px;
    right: 30px;
    z-index: 9999;
    background: {st.session_state.theme['primary']};
    color: {st.session_state.theme['secondary']};
    padding: 10px 25px;
    border-radius: 30px;
    font-size: 1.1rem;
    font-weight: bold;
    box-shadow: 0 2px 12px #e1060030;
    transition: transform 0.3s;
    animation: pulse 1.2s infinite;
    border: 2px solid #fff;
}}
@keyframes pulse {{
    0% {{ transform: scale(1); box-shadow: 0 2px 12px #e1060030; }}
    50% {{ transform: scale(1.12); box-shadow: 0 4px 24px #e1060080; }}
    100% {{ transform: scale(1); box-shadow: 0 2px 12px #e1060030; }}
}}
</style>
<div id="basket-anim" onclick="window.location.hash='basket-popup'">
    🛒 Panier : <span style="font-size:1.3rem">{basket_count}</span>
</div>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ============== HEADER / ADMIN ==============
col1, col2, col3 = st.columns([2,5,2])
with col1:
    pass
with col2:
    st.markdown("### Catalogue des motifs")
with col3:
    if st.session_state.admin:
        st.markdown('<span style="background:linear-gradient(90deg,{},{secondary});color:white;padding:4px 10px;border-radius:8px;">Admin connecté</span>'.format(
            st.session_state.theme.get("primary", "#e10600"), secondary=st.session_state.theme.get("secondary", "#fff")), unsafe_allow_html=True)
        if st.button("Déconnexion admin"):
            st.session_state.admin = False
            st.success("Déconnecté")
    else:
        if st.button("Espace admin"):
            st.session_state.show_admin_login = True

st.write("---")

# ============== POPUP FENÊTRE ==============
if st.session_state.show_popup:
    with st.popover("Panier", use_container_width=True):
        st.write("## Vos articles dans le panier")
        basket_imgs = [img for img in IMAGES if img["id"] in st.session_state.basket]
        for img in basket_imgs:
            st.image(img["src"], caption=img["title"], width=140)
            st.markdown(f"<span style='background:{st.session_state.theme['secondary']};color:{st.session_state.theme['primary']};border-radius:999px;padding:2px 15px;border:1px solid #ffd1d6'>{img['id']}</span>", unsafe_allow_html=True)
        if st.button("Fermer", key="close_popup"):
            st.session_state.show_popup = False
        st.write("---")
        st.write(st.session_state.popup_message)
        st.write("Pour passer commande, cliquez sur 'Demande groupée' plus bas.")

# Ajout d'un bouton flottant pour ouvrir le panier (simulateur)
if st.button("👁 Voir le panier", key="basket_popup_btn"):
    st.session_state.show_popup = True
    st.session_state.popup_message = ""

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

# ============== ADMIN ZONE : THEME PERSONNALISATION ==============
if st.session_state.admin:
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

# ============== GRID MOTIFS ==============
st.write("## Motifs")
cols = st.columns(3)
for idx, img in enumerate(IMAGES):
    with cols[idx % 3]:
        in_basket = img["id"] in st.session_state.basket
        if st.session_state.show_add_modal == img["id"]:
            st.write("### Ajouter au panier")
            st.image(img["src"], caption=img["title"], use_container_width=True)
            st.write("Confirmer l'ajout au panier ?")
            confirm = st.button("Oui, ajouter", key=f"confirm_add_{img['id']}")
            cancel = st.button("Annuler", key=f"cancel_add_{img['id']}")
            if confirm:
                st.session_state.basket.append(img["id"])
                st.session_state.show_add_modal = None
                st.session_state.popup_message = f"{img['title']} ajouté au panier !"
                st.session_state.show_popup = True  # Affiche pop-up confirmation
            elif cancel:
                st.session_state.show_add_modal = None
        elif not in_basket:
            if st.button(f"Ajouter au panier : {img['title']}", key=f"basket_add_{img['id']}"):
                st.session_state.show_add_modal = img["id"]
        else:
            if st.button(f"Retirer du panier : {img['title']}", key=f"basket_remove_{img['id']}"):
                st.session_state.basket.remove(img["id"])
                st.info(f"{img['title']} retiré du panier.")
        st.image(img["src"], caption=f"{img['title']} ({img['id']})", use_container_width=True)
        st.write("Thème rouge & blanc · effet néon + zoom")
        st.markdown(f"**{img['title']}**")
        st.markdown(f"<span style='background:{st.session_state.theme['secondary']};color:{st.session_state.theme['primary']};border-radius:999px;padding:2px 15px;border:1px solid #ffd1d6'>{img['id']}</span>", unsafe_allow_html=True)
        if st.session_state.admin:
            st.download_button("⬇️ Télécharger", img["src"], file_name=img["id"] + ".jpg")
        st.write("---")

# ============== PANIER ET DEMANDE GROUPEE ==============
if st.session_state.basket:
    st.write("### Votre panier")
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

st.write("---")
st.write("STANNM • Catalogue statique pour SADELA INDUSTRIE· © 2025")
