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



tips = {
    "hoher Blutdruck": [
        "Vermeide salzhaltige Nahrung",
        "Vermeide Koffein",
        "Vermeide k\u00f6rperliche Anstrengung in der n\u00e4chsten Stunde",
        "Trinke Zitronenwasser",
        "Achten Sie auf eine ausgewogene Ern\u00e4hrung mit viel Obst und Gem\u00fcse."
    ],
    "Niedriger Blutdruck": [
        "Konsumiere salzhaltige Nahrung",
        "Konsumiere Koffein",
        " Vermeiden Sie pl\u00f6tzliches Aufstehen, um Schwindelgef\u00fchle zu vermeiden.",
        "Tragen Sie Kompressionsstr\u00fcmpfe, um den Blutfluss zu verbessern.",
        "Trinken Sie viel, um Ihren Fl\u00fcssigkeitshaushalt aufrechtzuerhalten."
    ]
}







# -------- load secrets for jsonbin.io --------
jsonbin_secrets = st.secrets["jsonbin"]
api_key = jsonbin_secrets["api_key"]
bin_id = jsonbin_secrets["bin_id"]

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

fullname, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == True:   # login successful
    authenticator.logout('Logout', 'main')   # show logout button
elif authentication_status == False:
    st.error('Username/password is incorrect')
    st.stop()
elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.stop()

# data = loak_key(api_key, bin_id, username)
# res = save_key(api_key, bin_id, username, data)

st.write(username)
test = load_key(api_key, bin_id, username)
st.write(test)

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

# Daten werden geladen und ins DataFrame konvertiert.
#tracked_data = load_data("blutdruck.json")
tracked_data = load_key(api_key, bin_id, username)
tracked_data = pd.DataFrame(tracked_data)

# Benachrichtigung mithilfe einer Checkbox in der Sidebar. Die Benachrichtigung soll nicht länger als 3 sekunden eingeblendet werden.
checkbox = st.sidebar.checkbox("Benachrichtigung")
if checkbox:
    info_banner = st.info("Benachrichtigung aktiviert!")
    start_time = time.time()
    while time.time() - start_time < 3:
        pass
    info_banner.empty()

else:
    info_banner = st.info("Benachrichtigung deaktiviert!")
    start_time = time.time()
    while time.time() - start_time < 3:
        pass
    info_banner.empty()


# Titel und Untertitel der App
st.title(':blue[TrackingDiary©]')
st.subheader('_Dein täglicher Begleiter._')
st.write("---")
string=("Mit der Tracking App kannst du deinen täglichen Blutdruck schnell und simpel erfassen und sie bietet dir einen Überblick über deine Messdaten.")
st.markdown(string)
st.write("---")

# Tabs wurden definiert.
tab1, tab2, tab3 = st.tabs(["Tracking", "Tagebuch", "Tipps"])

# Erste Seite der App: Tracking, hier werden die Werte eingetragen.
# Datum und Zeit wurden in einen String verwandelt, damit die Werte im JSON Format gespeichert werden können. 
# Alle values der Key-value Paare wurden als Liste umgewandelt, damit ein DataFrame erstellt werden kann.
with tab1:
    st.subheader("_:orange[Tracking]_:pencil2:")

    # Eingabefelder wurden hinzugefügt.
    date = st.date_input("Datum", value=pd.Timestamp.now().date())
    time = st.time_input("Uhrzeit", value=pd.Timestamp.now().time())
    systole = st.number_input("Systole", min_value=0, max_value=300, value=0, step=1)
    diastole = st.number_input("Diastole", min_value=0, max_value=300, value=0, step=1)
    if st.button('Speichern'):
        if systole >= 130 or diastole >= 89:
            st.error("Dein Blutdruck ist zu hoch.")
        elif systole <= 90 or diastole <= 59:
                st.error("Dein Blutdruck ist zu niedrig.")
                st.info("Die Daten wurden gespeichert.")
        else:
            st.success("Dein Blutdruck ist optimal.")
        # Neue eingetragene Werte werden gespeichert.
        new_data = {'Date': [str(date)], 
                    'Time': [str(time)],
                    'Systole': [systole],
                    'Diastole': [diastole]}
        new_data = pd.DataFrame(new_data)
        # Pandas wurde benutzt, um die neuen daten an bestehende Daten als neue Zeile anzuhängen.
        df = pd.concat([tracked_data, new_data], ignore_index=True)
        df = df.fillna('')
        # Umwandlung zurück zu Dictionary
        data_dict = df.to_dict(orient="records")
        save_key(api_key, bin_id, username, data_dict)
        #save_data(data_dict, "blutdruck.json")
        st.info("Die Daten wurden gespeichert.")

# Zweite Seite der App: Tagebuch, hier werden die Messwerte gespeichert.
with tab2:
    st.header('_:orange[Tagebuch]_:book:')
    st.subheader('Deine Messwerte')
 # Daten werden aus JSON-Datei geladen und ein DataFrame wird aus der JSON-Datei erstellt.
    data = load_data(api_key, bin_id, username)
    if not data:
        st.warning("Es wurden noch keine Daten gespeichert.")
    else:
        df = pd.DataFrame(data)
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

# Dritte Seite der App: Hier werden Empfehlungen für den User vorgeschlagen.
with tab3:
    st.header('_:orange[Tipps]_:bulb:')
    st.write(tips)
    
    # # Tipps aus JSON-Datei laden
    # tips_data = load_data('tips.json')
    # if tips_data:
    #     for key, value in tips_data.items():
    #         st.subheader(key)
    #         for tip in value:
    #             st.write(f"- {tip}")

# # Tipps für einen zu hohen Blutdruck
# if 'Too High Blood Pressure' in tips_data:
#     tips_data['Too High Blood Pressure'] = ['Vermeide salzhaltige Nahrung', 'Vermeide Koffein','Vermeide körperliche Anstrengung in der nächsten Stunde','Trinke Zitronenwasser','Achten Sie auf eine ausgewogene Ernährung mit viel Obst und Gemüse.']


# # Schreiben der modifizierten JSON-Daten in die Datei.
# with open('tips.json', 'w') as json_file:
#     json.dump(tips_data, json_file, indent=4)
    
    
# with open('tips.json', 'r') as json_file:
#     tips_data = json.load(json_file)

# # Laden der JSON-Daten
# # Tipps für einen niedrigen Blutdruck
# if 'Too Low Blood Pressure' in tips_data:
#     tips_data['Too Low Blood Pressure'] = ['Konsumiere salzhaltige Nahrung', 'Konsumiere Koffein',' Vermeiden Sie plötzliches Aufstehen, um Schwindelgefühle zu vermeiden.', 'Tragen Sie Kompressionsstrümpfe, um den Blutfluss zu verbessern.','Trinken Sie viel, um Ihren Flüssigkeitshaushalt aufrechtzuerhalten.']


# # Schreiben der modifizierten JSON-Daten in die Datei
# with open('tips.json', 'w') as json_file:
#     json.dump(tips_data, json_file, indent=4)

# # Laden der JSON-Daten
# with open('tips.json', 'r') as json_file:
#     tips_data = json.load(json_file)


# #Titel des JSON Inhalts wird geändert.
# # JSON-Datei laden
# with open('tips.json', 'r') as json_file:
#     tips_data = json.load(json_file)


# # Titel ändern 1: von ,,Too High Blood Pressure'' zu ,,Hoher Blutdruck''.
# if 'Too High Blood Pressure' in tips_data:
#     tips_data['hoher Blutdruck'] = tips_data.pop('Too High Blood Pressure')
#     # Hier wird der Titel von 'Too High Blood Pressure' zu 'Hoher Blutdruck' geändert.

# # Modifizierte JSON-Datei wird gespeichert.
# with open('tips.json', 'w') as json_file:
#     json.dump(tips_data, json_file, indent=4)



# #Titel ändern 2 von ,,Too Low Blood Pressure'' zu ,,Niederiger Blutdruck''.
# if 'Too Low Blood Pressure' in tips_data:
#     tips_data['Niedriger Blutdruck'] = tips_data.pop('Too Low Blood Pressure')
#     # Hier wird der Titel von 'Too Low Blood Pressure' zu 'Niedriger BLutdruck' geändert.


# # Modifizierte JSON-Datei wird gespeichert.
# with open('tips.json', 'w') as json_file:
#     json.dump(tips_data, json_file, indent=4)


#Optik Design
st.write("---")
st.text('© 2023 Applaunch Wädenswil ZHAW')



