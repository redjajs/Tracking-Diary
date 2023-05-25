# Bibliotheken importiert.
import streamlit as st
import pandas as pd
import json
import os
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import time
from jsonbin import load_key, save_key
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
#from pages import Personalien
#from pages import Tipps


# Laden der Personalien Seite aus anderen Python Datei
# def show():
#     Personalien.show()

# if __name__ == "__show__":
#     show()
    
# def show():
#     Tipps.show()

# if __name__ == "__show__":
#     show()
    

# Hintergrundfarbe anpassen
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

    st.markdown(css, unsafe_allow_html=True)

set_blue_background()


# Laden von Secrets für jsonbin.io 
jsonbin_secrets = st.secrets["jsonbin"]
api_key = jsonbin_secrets["api_key"]
bin_id = jsonbin_secrets["bin_id"]
 

# jsonbin_secrets = st.secrets["jsonbin"]
# api_key = jsonbin_secrets["api_key"]
# bin_id_personalien = jsonbin_secrets["bin_id_personalien"]



with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# Login generiert
fullname, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:   # login successful
    authenticator.logout('Logout', 'main')   # show logout button
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()


# st.write(username)
#test = load_key(api_key, bin_id, username)
# st.write(test)

#APP
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




# Benachrichtigung mithilfe einer Checkbox in der Sidebar. 
checkbox = st.sidebar.checkbox("Benachrichtigung")
if checkbox:
    info_banner = st.info("Benachrichtigung aktiviert!")
    start_time = time.time()
    while time.time() - start_time < 1:
        pass
    info_banner.empty()

else:
    info_banner = st.info("Benachrichtigung deaktiviert!")
    start_time = time.time()
    while time.time() - start_time < 1:
        pass
    info_banner.empty()
    
    
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

    
    st.header(':black[TrackingDiary©]')
    
def show_personalien():
    st.title("Dein Profil")
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
        
        jsonbin_secrets = st.secrets["jsonbin"]
        api_key = jsonbin_secrets["api_key"]
        bin_id_personalien = jsonbin_secrets["bin_id_personalien"]

        save_key(api_key, bin_id_personalien, username, data)
  
    #Optik Design
    st.write("---")
    st.text('© 2023 Applaunch Wädenswil ZHAW')

test = pd.DataFrame()
def show_startseite():  
# Tabs wurden definiert.
    tab1, tab2, tab3 = st.tabs(["Über uns","Tracking", "Tagebuch"])

    
    with tab1:
        st.title(':black[TrackingDiary©]')
        st.subheader('_Dein täglicher Begleiter._')
        st.write("---")
        string=("Mit der Tracking App kannst du deinen täglichen Blutdruck schnell und simpel erfassen und sie bietet dir einen Überblick über deine Messdaten.")
        st.markdown(string)
        # st.write("---")
    
    # Erste Seite der App: Tracking, hier werden die Werte eingetragen.
    # Datum und Zeit wurden in einen String verwandelt, damit die Werte im JSON Format gespeichert werden können. 
    # Alle values der Key-value Paare wurden als Liste umgewandelt, damit ein DataFrame erstellt werden kann.
    with tab2:
        st.subheader("_:black[Tracking]_:pencil2:")
    # Daten werden geladen und ins DataFrame konvertiert.
        # Eingabefelder wurden hinzugefügt.
        date = st.date_input("Datum", value=pd.Timestamp.now(tz='Europe/Zurich').date())
        time = st.time_input("Uhrzeit", value=pd.Timestamp.now(tz='Europe/Zurich').time())
        systole = st.number_input("Systole", min_value=0, max_value=300, value=0, step=1)
        diastole = st.number_input("Diastole", min_value=0, max_value=300, value=0, step=1)
        if st.button('Speichern'):
            if systole >= 130 or diastole >= 89:
                st.error("Dein Blutdruck ist zu hoch.")
            elif systole <= 90 or diastole <= 59:
                    st.error("Dein Blutdruck ist zu niedrig.")
                    #st.info("Die Daten wurden gespeichert.")
            else:
                st.success("Dein Blutdruck ist optimal.")
            # Neue eingetragene Werte werden gespeichert.
            new_data = {'Date': [str(date)], 
                        'Time': [str(time)],
                        'Systole': [systole],
                        'Diastole': [diastole]}
            new_data = pd.DataFrame(new_data)
            # Pandas wurde benutzt, um die neuen daten an bestehende Daten als neue Zeile anzuhängen.
            df = pd.concat([test, new_data], ignore_index=True)
            df = df.fillna('')
            # Umwandlung zurück zu Dictionary
            data_dict = df.to_dict(orient="records")
            save_key(api_key, bin_id, username, data_dict)
            #save_data(data_dict, "blutdruck.json")
            st.info("Die Daten wurden gespeichert.")
    
    # Zweite Seite der Startseite: Tagebuch, hier werden die Messwerte gespeichert.
    with tab3:
        st.header('_:orange[Tagebuch]_:book:')
        st.subheader('Deine Messwerte')
     # Daten werden aus JSON-Datei geladen und ein DataFrame wird aus der JSON-Datei erstellt.
        test1 = load_key(api_key, bin_id, username, test)
        
        if not test1:
            st.warning("Es wurden noch keine Daten gespeichert.")
        else:
            df = pd.DataFrame(test1)
            st.write(df)
            
            
        # Konvertierung 'Date' und 'Time' in einen DateTime-Datentyp
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
        
        # DateTime' wird als Index eingesetzt.
            df = df.set_index('DateTime')
        
        # Es wurde ein Plot aus dem DataFrame erstellt.
            fig, ax = plt.subplots()
            ax.plot(df.index, df["Systole"], label="Systole")
            ax.plot(df.index, df["Diastole"], label="Diastole")
            ax.set_xlabel("Datum und Uhrzeit")
            ax.set_ylabel("mmHg / bpm")
            ax.set_title("Blutdruckverlauf")
            ax.legend()
        
        # Verwendung von DateFormatter für die X-Achse.
            date_form = DateFormatter("%d.%m.%y %H:%M") 
            ax.xaxis.set_major_formatter(date_form)
            plt.xticks(rotation=45)
    
    # Plot wird auf Streamlit angezeigt.
            st.subheader("Blutdruckverlauf")
            st.pyplot(fig)
            
                    
    
    #Optik Design
    st.write("---")
    st.text('© 2023 Applaunch Wädenswil ZHAW')

def show_tipps():
    
    st.header(':black[TrackingDiary©]')

    tips = {
        "Hoher Blutdruck": [
            "Vermeide salzhaltige Nahrung",
            "Vermeide Koffein",
            "Vermeide körperliche Anstrengung in der nächsten Stunde",
            "Trinke Zitronenwasser",
            "Achten Sie auf eine ausgewogene Ernährung mit viel Obst und Gemüse."
        ],
        "Niedriger Blutdruck": [
            "Konsumiere salzhaltige Nahrung",
            "Konsumiere Koffein",
            "Vermeiden Sie plötzliches Aufstehen, um Schwindelgefühle zu vermeiden.",
            "Tragen Sie Kompressionsstrümpfe, um den Blutfluss zu verbessern.",
            "Trinken Sie viel, um Ihren Flüssigkeitshaushalt aufrechtzuerhalten."
        ]
    }

    st.title(':black[Tipps für den Blutdruck]')

    for category, tips_list in tips.items():
        st.subheader(category)
        for tip in tips_list:
            st.write("- " + tip)


    #Optik Design
    st.write("---")
    st.text('© 2023 Applaunch Wädenswil ZHAW')
    
    
    # Sidebar-Navigation
pages = {
    "Startseite": show_startseite,
    "Personalien": show_personalien,
    "Tipps": show_tipps
}

# Seiten in der Sidebar anzeigen
selected_page = st.sidebar.radio("", list(pages.keys()))

# Ausgewählte Seite anzeigen
pages[selected_page]()







