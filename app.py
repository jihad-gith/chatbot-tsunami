import streamlit as st
import random

# Configuration de la page
st.set_page_config(page_title="Chatbot Tsunami", page_icon="🌊")

# Base de connaissances sur les tsunamis
knowledge_base = {
    "tsunami": "Un tsunami est une série de vagues océaniques très longues générées par le déplacement soudain d'un grand volume d'eau.",
    "causes": "Les causes principales sont : séismes sous-marins (90%), glissements de terrain, éruptions volcaniques, ou impacts de météorites.",
    "signes": "Signes avant-coureurs : séisme prolongé, retrait soudain de la mer, bruit rugissant venant de l'océan.",
    "sécurité": "Consignes de sécurité : s'éloigner du rivage, gagner les hauteurs (>10m), ne pas prendre sa voiture, ne pas retourner chercher ses affaires.",
    "hauteur": "Une hauteur de 10-15 mètres est généralement suffisante, mais plus on s'éloigne du rivage, mieux c'est.",
    "géomatique": "La géomatique aide à cartographier les zones à risque, modéliser l'impact, et planifier les évacuations via les SIG.",
    "durée": "Un tsunami peut durer plusieurs heures, avec des vagues successives. La première vague n'est pas toujours la plus dangereuse.",
}

# Fonction pour trouver la meilleure réponse
def get_response(message):
    message = message.lower()
    
    # Recherche de correspondance
    for key, value in knowledge_base.items():
        if key in message:
            return value
    
    # Réponses par défaut
    default_responses = [
        "Je suis spécialisé dans les tsunamis. Posez-moi une question sur les causes, la sécurité ou la prévention!",
        "Je peux vous parler des tsunamis : causes, signes avant-coureurs, consignes de sécurité...",
        "Question intéressante ! En tant qu'expert tsunamis, je peux vous aider sur les aspects sécurité, prévention ou géomatique."
    ]
    
    return random.choice(default_responses)

# Interface Streamlit
st.title("🌊 Chatbot Expert Tsunami")
st.write("Bonjour ! Je suis votre assistant spécialisé sur les tsunamis. Posez-moi vos questions !")

# Historique du chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Votre question sur les tsunamis..."):
    # Ajouter le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Générer la réponse
    response = get_response(prompt)
    
    # Ajouter la réponse de l'assistant
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)
