import streamlit as st
import random
import re

# Configuration de la page
st.set_page_config(page_title="Expert TsunamiGuard", page_icon="🌊", layout="wide")

# Base de connaissances AVANCÉE sur les tsunamis
knowledge_base = {
    "tsunami": {
        "definition": "🌊 **Un tsunami** est une série de vagues océaniques extrêmement longues générées par le déplacement soudain d'un grand volume d'eau, pas une simple grosse vague.",
        "details": "Les tsunamis peuvent voyager à 800 km/h en eau profonde et atteindre 30m de haut près des côtes."
    },
    "causes": {
        "principales": "📌 **Causes principales :**\n• Séismes sous-marins (≈90% des cas)\n• Glissements de terrain sous-marins\n• Éruptions volcaniques\n• Impacts de météorites",
        "exemple": "Le tsunami de 2004 (Océan Indien) fut causé par un séisme de magnitude 9.1-9.3."
    },
    "signes": {
        "naturels": "🚨 **Signes d'alerte naturels :**\n• Séisme prolongé (>20 sec)\n• Retrait soudain et inhabituel de la mer\n• Bruit rugissant venant de l'océan\n• Comportement étrange des animaux",
        "officiels": "📢 **Alertes officielles :** Sirènes, SMS d'urgence, médias"
    },
    "sécurité": {
        "règles": "🛡️ **5 RÈGLES D'OR :**\n1. S'éloigner IMMÉDIATEMENT du rivage\n2. Gagner les hauteurs (>15m idéal)\n3. NE PAS prendre sa voiture\n4. NE PAS retourner chercher ses affaires\n5. Rester informé et attentif aux répliques",
        "urgence": "⏱️ **Temps de réaction :** Vous avez quelques minutes seulement. Ne perdez pas de temps !"
    },
    "géomatique": {
        "applications": "🗺️ **Rôle de la géomatique :**\n• Cartographie des zones à risque via MNT\n• Modélisation des impacts avec SIG\n• Planification des itinéraires d'évacuation\n• Surveillance en temps réel",
        "expertise": "Nous utilisons des Modèles Numériques de Terrain pour prédire les zones inondables."
    },
    "statistiques": {
        "fréquence": "📊 **Quelques chiffres :**\n• 80% des tsunamis se produisent dans le Pacifique\n• 5-10 tsunamis majeurs par siècle\n• Vitesse : 500-800 km/h en eau profonde\n• Longueur d'onde : jusqu'à 200 km"
    }
}

# Fonction de recherche intelligente
def find_best_response(user_input):
    user_input = user_input.lower().strip()
    
    # Détection des intentions avec mots-clés
    if any(word in user_input for word in ["quoi", "qu'est", "définition", "définir", "c'est quoi"]):
        if "tsunami" in user_input:
            return knowledge_base["tsunami"]["definition"]
    
    if any(word in user_input for word in ["cause", "provoque", "origine", "pourquoi"]):
        return knowledge_base["causes"]["principales"] + "\n\n" + knowledge_base["causes"]["exemple"]
    
    if any(word in user_input for word in ["signe", "reconnaître", "alerte", "avant"]):
        return knowledge_base["signes"]["naturels"] + "\n\n" + knowledge_base["signes"]["officiels"]
    
    if any(word in user_input for word in ["faire", "sécurité", "danger", "urgence", "évacuer"]):
        return knowledge_base["sécurité"]["règles"] + "\n\n" + knowledge_base["sécurité"]["urgence"]
    
    if any(word in user_input for word in ["géomatique", "sig", "cart", "donnée", "ingénieur"]):
        return knowledge_base["géomatique"]["applications"] + "\n\n" + knowledge_base["géomatique"]["expertise"]
    
    if any(word in user_input for word in ["stat", "chiffre", "fréquence", "combien"]):
        return knowledge_base["statistiques"]["fréquence"]
    
    # Recherche par mots-clés dans toute la base
    for category, content in knowledge_base.items():
        if category in user_input:
            if isinstance(content, dict):
                return "\n\n".join(content.values())
            return content
    
    # Réponses par défaut plus intelligentes
    default_responses = [
        "🌊 Je suis Expert TsunamiGuard. Posez-moi des questions sur : causes, signes avant-coureurs, consignes de sécurité, ou le rôle de la géomatique !",
        "🤔 Pour une réponse précise, essayez : 'Que faire en cas de tsunami ?' ou 'Quelles sont les causes ?'",
        "🎯 Je peux vous expliquer les aspects techniques des tsunamis et comment la géomatique aide à sauver des vies."
    ]
    
    return random.choice(default_responses)

# Interface améliorée
st.title("🌊 Expert TsunamiGuard - Chatbot Spécialisé")
st.markdown("**Votre assistant expert en tsunamis, sécurité civile et géomatique**")

# Sidebar avec informations utiles
with st.sidebar:
    st.header("💡 Questions suggérées")
    st.markdown("""
    - Qu'est-ce qu'un tsunami ?
    - Quelles sont les causes ?
    - Comment reconnaître les signes ?
    - Que faire en cas d'alerte ?
    - Rôle de la géomatique ?
    - Statistiques importantes
    """)
    
    st.header("📞 Urgence")
    st.markdown("En situation réelle : **Composez le 112**")

# Historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🌊 Bonjour ! Je suis Expert TsunamiGuard. Je peux vous renseigner sur les tsunamis, la sécurité et l'apport de la géomatique. Comment puis-je vous aider ?"}
    ]

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie
if prompt := st.chat_input("Posez votre question sur les tsunamis..."):
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Génération de la réponse intelligente
    response = find_best_response(prompt)
    
    # Ajout de la réponse de l'assistant
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Footer informatif
st.markdown("---")
st.markdown("🔬 *Développé par des étudiants en géoinformatique - Outil pédagogique*")
