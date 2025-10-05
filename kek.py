import streamlit as st
import random
import os
from pathlib import Path

def main():
    st.set_page_config(page_title="Foto-Karten Ziehen", page_icon="🎴", layout="wide")
    
    # Titel und Beschreibung
    st.title("🎴 Foto-Karten Ziehen 🎴")
    st.markdown("*Ziehe 5 zufällige Karten aus deinen Fotos*")
    
    # Pfad zum Bilder-Ordner
    image_folder = "cards"  # Ordner wo deine Fotos liegen
    
    # Unterstützte Bildformate
    supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    # Prüfe ob Ordner existiert
    if not os.path.exists(image_folder):
        st.warning(f"⚠️ Der Ordner '{image_folder}' existiert nicht!")
        st.info("""
        **So richtest du die App ein:**
        
        1. Erstelle einen Ordner namens `cards` im gleichen Verzeichnis wie diese App
        2. Lege deine Fotos in diesen Ordner (JPG, PNG, GIF, WebP)
        3. Benenne die Fotos nach deinen Karten (z.B. `karte1.jpg`, `karte2.png`)
        4. Starte die App neu
        """)
        return
    
    # Lade alle Bilddateien aus dem Ordner
    image_files = []
    for ext in supported_formats:
        image_files.extend(list(Path(image_folder).glob(f'*{ext}')))
        image_files.extend(list(Path(image_folder).glob(f'*{ext.upper()}')))
    
    if len(image_files) == 0:
        st.warning(f"⚠️ Keine Bilder im Ordner '{image_folder}' gefunden!")
        st.info("Lege mindestens 5 Fotos in den 'cards' Ordner.")
        return
    
    if len(image_files) < 5:
        st.warning(f"⚠️ Nur {len(image_files)} Bild(er) gefunden. Du brauchst mindestens 5 Fotos!")
        return
    
    # Zeige Info über gefundene Karten
    st.success(f"✅ {len(image_files)} Karten gefunden!")
    
    # Session State initialisieren
    if 'drawn_cards' not in st.session_state:
        st.session_state.drawn_cards = []
    
    # Zieh-Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🎴 Ziehe 5 Karten", use_container_width=True, type="primary"):
            # Wähle 5 zufällige Karten
            st.session_state.drawn_cards = random.sample(image_files, 5)
    
    # Zeige die gezogenen Karten an
    if st.session_state.drawn_cards:
        st.markdown("---")
        st.subheader("Deine gezogenen Karten:")
        
        # Zeige die Karten in 5 Spalten nebeneinander
        cols = st.columns(5)
        
        for idx, (col, card_path) in enumerate(zip(cols, st.session_state.drawn_cards)):
            with col:
                # Zeige das Foto als Karte
                st.image(str(card_path), use_container_width=True)
                # Zeige den Dateinamen unter der Karte (ohne Dateierweiterung)
                card_name = card_path.stem
                st.markdown(f"**{card_name}**")
        
        st.markdown("---")
        
        # Noch einmal ziehen Button
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔄 Noch einmal ziehen", use_container_width=True):
                st.rerun()
    
    # Sidebar mit Infos
    with st.sidebar:
        st.header("ℹ️ Anleitung")
        st.markdown(f"""
        ### Setup:
        1. Erstelle einen Ordner `cards`
        2. Lege deine Fotos hinein
        3. Klicke auf "Ziehe 5 Karten"
        
        ### Gefundene Karten:
        **{len(image_files)} Karten verfügbar**
        
        ### Kartenformat:
        - JPG, PNG, GIF, WebP
        - Beliebige Auflösung
        
        ### Tipp:
        Benenne deine Fotos sinnvoll - 
        der Dateiname wird unter der 
        Karte angezeigt!
        """)
        
        # Zeige Liste aller verfügbaren Karten
        if st.checkbox("Alle Karten anzeigen"):
            st.markdown("### 📋 Verfügbare Karten:")
            for img_file in sorted(image_files):
                st.caption(f"• {img_file.stem}")

if __name__ == "__main__":
    main()
