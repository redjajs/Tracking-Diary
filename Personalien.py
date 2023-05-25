# #Personalien
import streamlit as st
import json
import os
from jsonbin import save_key

# Funktion zum Laden der Daten aus der JSON-Datei
def load_data(filename):
    if os.path.isfile(filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = []
    return data

# Funktion zum Speichern der Daten in der JSON-Datei
def save_data(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
        
jsonbin_secrets = st.secrets["jsonbin"]
api_key = jsonbin_secrets["api_key"]
bin_id_personalien = jsonbin_secrets["bin_id_personalien"]


save_key(api_key, bin_id_personalien)


def set_blue_background():
    bg_color = "background-color: lightsteelblue;"
    text_color = "color: black;"
    padding = "padding: 10px;"

    # Benutzerdefinierten CSS-Code generieren
    css = f"""
        <style>
        body {{
            {bg_color}
        }}

        .stApp {{
            {bg_color}
            {text_color}
            {padding}
        }}
        </style>
    """

    # CSS-Code mithilfe von st.markdown() einfügen
    st.markdown(css, unsafe_allow_html=True)
st.title("Dein Profil")

# Beispielanwendung
set_blue_background()

st.header(':black[TrackingDiary©]')

# Eingabefelder für Personalien
firstname = st.text_input("Vorname")
lastname = st.text_input("Nachname")
age = st.number_input("Alter", min_value=0, max_value=150)

# Button zum Absenden der Daten
if st.button("Daten absenden"):
    # Lade vorhandene Daten aus der JSON-Datei
    filename = "Personalien.json"
    existing_data = load_data(filename)

    # Neues Dictionary mit den eingegebenen Daten erstellen
    data = {
        "Vorname": firstname,
        "Nachname": lastname,
        "Alter": age
    }

    # Konvertiere vorhandene Daten in eine Liste, wenn es sich um ein einzelnes Dictionary handelt
    if isinstance(existing_data, dict):
        existing_data = [existing_data]

    # Füge das neue Dictionary der vorhandenen Datenliste hinzu
    existing_data.append(data)

    # Speichere die aktualisierten Daten in der JSON-Datei
    save_data(existing_data, filename)

    st.success("Daten wurden gespeichert")

# import streamlit as st
# import json

# # Dictionary mit den Personalien

# def set_blue_background():
#     bg_color = "background-color: lightsteelblue;"
#     text_color = "color: black;"
#     padding = "padding: 10px;"

#     # Benutzerdefinierten CSS-Code generieren
#     css = f"""
#         <style>
#         body {{
#             {bg_color}
#         }}

#         .stApp {{
#             {bg_color}
#             {text_color}
#             {padding}
#         }}
#         </style>
#     """

#     # CSS-Code mithilfe von st.markdown() einfügen
#     st.markdown(css, unsafe_allow_html=True)

# # Beispielanwendung
# set_blue_background()

# st.header(':black[TrackingDiary©]')

# #def show_personalien_page():
# st.title("Personalien erfassen")
    
# # Eingabefelder für Personalien
# firstname = st.text_input("Vorname")
# lastname = st.text_input("Nachname")
# age = st.number_input("Alter", min_value=0, max_value=150, value=30)
    
#     # Button zum Absenden der Daten
# if st.button("Daten absenden"):
#         # Datenverarbeitung oder -speicherung hier durchführen
#         st.success("Daten erfolgreich gesendet!")
        
# data = {
#         "Vorname": firstname,
#         "Nachname": lastname,
#         "Alter": age
#         }

# # JSON-Datei erstellen und Daten speichern
# with open("Personalien.json", "w") as json_file:
#             json.dump(data, json_file)

#Optik Design
st.write("---")
st.text('© 2023 Applaunch Wädenswil ZHAW')
