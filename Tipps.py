# tips
import streamlit as st

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

# Beispielanwendung
set_blue_background()


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

