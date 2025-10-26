import streamlit as st
import random
import requests
from PIL import Image
import io

# Configuration de la page
st.set_page_config(page_title="🌍 TsunamiGuard Pro", page_icon="🌊", layout="wide")

# ==================== SYSTÈME MULTILINGUE ====================

LANGUAGES = {
    "Français": "fr",
    "English": "en", 
    "العربية": "ar"
}

# Dictionnaire avec URLs d'images réelles
KNOWLEDGE_BASE = {
    "tsunami": {
        "keywords": ["tsunami", "موجة", "wave", "تسونامي", "image", "photo", "صورة"],
        "responses": {
            "fr": "🌊 **Un tsunami** est une série de vagues océaniques extrêmement longues. Voici une illustration :",
            "en": "🌊 **A tsunami** is a series of extremely long ocean waves. Here's an illustration:",
            "ar": "🌊 **تسونامي** هو سلسلة من أمواج المحيط الطويلة جدًا. إليك رسم توضيحي:"
        },
        "image_url": "https://www.noaa.gov/sites/default/files/styles/scale_crop_1120x490/public/2023-04/tsunami-diagram-1120x490.png"
    },
    "causes": {
        "keywords": ["cause", "provoque", "سبب", "origin", "why", "لماذا", "séisme", "earthquake", "زلزال"],
        "responses": {
            "fr": "📌 **Causes principales :**\n• Séismes sous-marins (90%)\n• Glissements de terrain\n• Éruptions volcaniques",
            "en": "📌 **Main causes:**\n• Undersea earthquakes (90%)\n• Landslides\n• Volcanic eruptions",
            "ar": "📌 **الأسباب الرئيسية:**\n• الزلازل تحت البحر (90٪)\n• الانهيارات الأرضية\n• الثورات البركانية"
        },
        "image_url": "https://i0.wp.com/www.geologyin.com/wp-content/uploads/2015/03/How-tsunamis-work-01.jpg"
    },
    "safety": {
        "keywords": ["sécurité", "safety", "أمان", "danger", "خطر", "que faire", "what to do", "ماذا أفعل", "évacuer", "evacuate", "إخلاء"],
        "responses": {
            "fr": "🛡️ **5 RÈGLES D'OR :**\n1. Éloignez-vous du rivage\n2. Gagnez les hauteurs (>15m)\n3. Ne prenez pas la voiture\n4. Ne retournez pas\n5. Restez informé",
            "en": "🛡️ **5 GOLDEN RULES:**\n1. Move away from shore\n2. Reach high ground (>15m)\n3. Don't take car\n4. Don't go back\n5. Stay informed", 
            "ar": "🛡️ **5 قواعد ذهبية:**\n1. ابتعد عن الشاطئ\n2. اتجه إلى المرتفعات (>15م)\n3. لا تستخدم السيارة\n4. لا تعود\n5. ابق على اطلاع"
        },
        "image_url": "https://www.weather.gov/images/safety/tsunami-route-signs.jpg"
    },
    "geomatics": {
        "keywords": ["géomatique", "geomatics", "جيوماتكس", "SIG", "GIS", "cartographie", "mapping", "خرائط", "carte", "map"],
        "responses": {
            "fr": "🗺️ **Rôle de la géomatique :**\n• Cartographie des risques\n• Modélisation SIG\n• Plans d'évacuation\n• Surveillance temps réel",
            "en": "🗺️ **Geomatics role:**\n• Risk mapping\n• GIS modeling\n• Evacuation plans\n• Real-time monitoring",
            "ar": "🗺️ **دور الجيوماتكس:**\n• رسم خرائط المخاطر\n• نمذجة نظم المعلومات الجغرافية\n• خطط الإخلاء\n• المراقبة في الوقت الحقيقي"
        },
        "image_url": "https://www.researchgate.net/profile/M-Hammoud-2/publication/349072898/figure/fig1/AS:990412897329153@1613390069448/GIS-map-showing-tsunami-hazard-zones-in-the-coastal-area-of-Chabahar-Bay-Iran.png"
    },
    "hauteur": {
        "keywords": ["hauteur", "height", "ارتفاع", "15m", "15 mètres", "hauteur vague", "wave height"],
        "responses": {
            "fr": "📏 **Hauteur des vagues :** Les tsunamis peuvent atteindre 30m de haut. Voici une comparaison :",
            "en": "📏 **Wave height:** Tsunamis can reach 30m high. Here's a comparison:",
            "ar": "📏 **ارتفاع الموج:** يمكن أن تصل أمواج التسونامي إلى 30 مترًا. إليك مقارنة:"
        },
        "image_url": "https://www.shutterstock.com/image-vector/tsunami-wave-size-scale-measurement-600nw-2178811233.jpg"
    }
}

# ==================== FONCTIONS INTELLIGENTES ====================

def get_best_response(user_input, language):
    """Trouve la meilleure réponse basée sur les mots-clés"""
    user_input = user_input.lower()
    
    # Recherche par mots-clés
    for topic, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            if keyword.lower() in user_input:
                return data["responses"][language], data.get("image_url")
    
    # Réponses par défaut selon la langue
    default_responses = {
        "fr": [
            "🌊 Posez-moi des questions sur: causes, sécurité, ou géomatique!",
            "🤔 Essayez: 'Que faire en cas de tsunami?' ou 'Rôle de la géomatique?'"
        ],
        "en": [
            "🌊 Ask me about: causes, safety, or geomatics!",
            "🤔 Try: 'What to do in tsunami?' or 'Geomatics role?'"
        ],
        "ar": [
            "🌊 اسألني عن: الأسباب، السلامة، أو الجيوماتكس!",
            "🤔 جرب: 'ماذا أفعل في التسونامي؟' أو 'دور الجيوماتكس؟'"
        ]
    }
    
    return random.choice(default_responses[language]), None

def display_image_from_url(image_url):
    """Affiche une image à partir d'une URL"""
    try:
        response = requests.get(image_url, timeout=10)
        image = Image.open(io.BytesIO(response.content))
        st.image(image, use_column_width=True)
    except:
        st.warning("🖼️ Image non disponible - Source externe")
        st.markdown(f"*Lien vers l'image: {image_url}*")

def get_suggested_questions(language):
    """Retourne les questions suggérées selon la langue"""
    questions = {
        "fr": [
            "Montre-moi une image de tsunami",
            "Quelle est la hauteur d'un tsunami?",
            "Que faire en cas d'alerte?",
            "Rôle de la géomatique?",
            "Causes principales?",
            "Donne-moi une carte des risques"
        ],
        "en": [
            "Show me a tsunami image",
            "What is tsunami height?",
            "What to do in alert?",
            "Geomatics role?",
            "Main causes?",
            "Give me a risk map"
        ],
        "ar": [
            "أرني صورة لتسونامي",
            "ما هو ارتفاع التسونامي؟",
            "ماذا أفعل في حالة الإنذار؟",
            "دور الجيوماتكس؟",
            "الأسباب الرئيسية؟",
            "أعطني خريطة المخاطر"
        ]
    }
    return questions[language]

# ==================== INTERFACE STREAMLIT ====================

# Sidebar pour la sélection de langue
with st.sidebar:
    st.header("🌍 Language / اللغة")
    selected_language = st.radio("Choisir la langue / Select language / اختر اللغة", 
                               list(LANGUAGES.keys()))
    
    current_lang = LANGUAGES[selected_language]
    
    st.header("💡 Questions de test / Test Questions / أسئلة اختبار")
    for question in get_suggested_questions(current_lang):
        if st.button(question):
            # Simule une question cliquée
            st.session_state.auto_question = question

# Interface principale
st.title("🌍 TsunamiGuard Pro - Multilingual Expert")
st.markdown("**Chatbot expert avec images - Testez avec les questions dans la sidebar!**")

# Gestion des questions automatiques
if "auto_question" in st.session_state:
    prompt = st.session_state.auto_question
    del st.session_state.auto_question
else:
    prompt = None

# Historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🌊 Bonjour ! Je suis Expert TsunamiGuard. Posez-moi des questions et je fournirai des images explicatives!"}
    ]

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if current_lang == "ar":
            st.markdown(f"<div dir='rtl' style='text-align: right;'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(message["content"])
        
        # Afficher l'image si elle existe dans le message
        if "image_url" in message and message["image_url"]:
            display_image_from_url(message["image_url"])

# Zone de saisie ou question automatique
if prompt or (user_input := st.chat_input(f"Posez votre question / Ask your question / اطرح سؤالك...")):
    
    if not prompt:
        prompt = user_input
    
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        if current_lang == "ar":
            st.markdown(f"<div dir='rtl' style='text-align: right;'>{prompt}</div>", unsafe_allow_html=True)
        else:
            st.markdown(prompt)
    
    # Génération de la réponse intelligente
    response, image_url = get_best_response(prompt, current_lang)
    
    # Ajout de la réponse
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response,
        "image_url": image_url
    })
    
    with st.chat_message("assistant"):
        if current_lang == "ar":
            st.markdown(f"<div dir='rtl' style='text-align: right;'>{response}</div>", unsafe_allow_html=True)
        else:
            st.markdown(response)
        
        # Afficher l'image si disponible
        if image_url:
            display_image_from_url(image_url)

# Footer informatif
st.markdown("---")
st.markdown("🔬 *Développé par des étudiants en géoinformatique - Projet éducatif*")

# Section d'information
st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Testez le chatbot avec:**\n"
    "'image tsunami', 'hauteur vague', 'carte risques', 'sécurité'"
)
