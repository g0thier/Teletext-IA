from pathlib import Path
import streamlit as st
import src.custom as my

# Initialisation du state
if "zipped_file" not in st.session_state:
    st.session_state.zipped_file = None
if "last_file_name" not in st.session_state:
    st.session_state.last_file_name = None

# Masquer la previsualisation de fichier
st.markdown("""
<style>
section[data-testid="stFileUploaderDropzone"] + div {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# Interface
st.title("📺 Teletext IA")

selection = st.pills(None, my.options, selection_mode="multi")

uploaded_file = st.file_uploader(
    "Chargez un fichier video ou audio",
    type= my.formats,
    accept_multiple_files= False,
    help="Fichier limité à 200 Mo",
    disabled= len(selection) == 0
)

if uploaded_file is not None:
    # pour éviter les rechargements de page de strealit à chaque interaction, on vérifie si le fichier a changé
    if uploaded_file.name != st.session_state.last_file_name:
        with st.spinner("Conversion en cours..."):
            st.session_state.zipped_file = my.pipeline(uploaded_file, selection)
            st.session_state.last_file_name = uploaded_file.name

    # Affichage du résultat
    if st.session_state.zipped_file is not None:
        st.success("Conversion terminée!")

        base_name = Path(uploaded_file.name).stem

        st.download_button(
            label="Télécharger l'archive ZIP",
            data=st.session_state.zipped_file,
            file_name=f"{base_name}.zip",
            mime="application/zip",
        )
    else:
        st.error("Erreur lors de la conversion du fichier.")