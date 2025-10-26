import streamlit as st
import random
import requests
import io
import base64
from PIL import Image
import time

# Configuration de la page avec design premium
st.set_page_config(
    page_title="🚨 Tsunami AI Expert", 
    page_icon="🌊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLE CSS PERSONNALISÉ ====================
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    .sidebar-content {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .emergency-box {
        background: #ff4444;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    }
    .question-btn {
        background: #4CAF50;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 25px;
        margin: 5px 0;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s;
    }
    .question-btn:hover {
        background: #45a049;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ==================== SYSTÈME MULTILINGUE ====================

LANGUAGES = {
    "🇫🇷 Français": "fr",
    "🇬🇧 English": "en", 
    "🇸🇦 العربية": "ar"
}

# ==================== GÉNÉRATION D'IMAGES AI ====================

def generate_ai_image(prompt, language):
    """Génère une image AI basée sur le prompt"""
    
    # Mappage des prompts aux images prédéfinies (simulation d'AI)
    image_prompts = {
        "tsunami": {
            "fr": "Diagramme scientifique d'un tsunami montrant les vagues et la propagation",
            "en": "Scientific diagram of tsunami showing waves and propagation", 
            "ar": "مخطط علمي للتسونامي يظهر الأمواج والانتشار"
        },
        "causes": {
            "fr": "Illustration éducative des causes des tsunamis: séismes, glissements de terrain",
            "en": "Educational illustration of tsunami causes: earthquakes, landslides",
            "ar": "رسم توضيحي تعليمي لأسباب التسونامي: الزلازل، الانهيارات الأرضية"
        },
        "safety": {
            "fr": "Infographie de sécurité montrant les règles d'évacuation tsunami",
            "en": "Safety infographic showing tsunami evacuation rules", 
            "ar": "إنفوجرافيك سلامة يظهر قواعد إخلاء التسونامي"
        },
        "geomatics": {
            "fr": "Carte géomatique montrant les zones à risque de tsunami",
            "en": "Geomatic map showing tsunami risk zones",
            "ar": "خريطة جيوماتيكية تظهر مناطق خطر التسونامي"
        },
        "hauteur": {
            "fr": "Comparaison visuelle de la hauteur des vagues de tsunami",
            "en": "Visual comparison of tsunami wave heights",
            "ar": "مقارنة بصرية لارتفاعات أمواج التسونامي"
        }
    }
    
    # URLs d'images éducatives de haute qualité
    image_urls = {
        "tsunami": "https://www.noaa.gov/sites/default/files/2023-04/tsunami-diagram-1120x490.png",
        "causes": "https://www.usgs.gov/sites/default/files/2021-09/tsunami-generation-diagram.gif",
        "safety": "https://www.weather.gov/images/safety/tsunami-brochure-2.png",
        "geomatics": "https://i.ytimg.com/vi/TRDpTEjumdo/maxresdefault.jpg",
        "hauteur": "https://www.shutterstock.com/image-vector/tsunami-wave-size-scale-measurement-600nw-2178811233.jpg",
        "evacuation": "https://www.oregon.gov/oem/Documents/Tsunami_Evac_Brochure.jpg"
    }
    
    # Trouver la catégorie la plus proche
    for category, prompts in image_prompts.items():
        if any(keyword in prompt.lower() for keyword in [category] + list(image_prompts.keys())):
            return image_urls.get(category, image_urls["tsunami"]), prompts[language]
    
    return image_urls["tsunami"], "Image éducative générée"

# ==================== BASE DE CONNAISSANCES INTELLIGENTE ====================

def get_ai_response(user_input, language):
    """Réponse AI avancée avec génération d'images"""
    
    user_input_lower = user_input.lower()
    
    # Détection intelligente du contexte
    if any(word in user_input_lower for word in ["image", "photo", "photo", "صورة", "montre", "show", "أرني", "voir"]):
        image_url, description = generate_ai_image(user_input, language)
        
        responses = {
            "fr": f"🖼️ **Voici une image générée pour vous:**\n\n*{description}*",
            "en": f"🖼️ **Here's a generated image for you:**\n\n*{description}*", 
            "ar": f"🖼️ **ها هي صورة تم إنشاؤها لك:**\n\n*{description}*"
        }
        return responses[language], image_url
    
    elif any(word in user_input_lower for word in ["tsunami", "تسونامي", "wave", "موجة"]):
        image_url, description = generate_ai_image("tsunami", language)
        responses = {
            "fr": "🌊 **Tsunami - Phénomène océanique:**\n• Série de vagues longue période\n• Vitesse: 800 km/h\n• Hauteur: jusqu'à 30m\n• Énergie massive",
            "en": "🌊 **Tsunami - Ocean phenomenon:**\n• Long-period wave series\n• Speed: 800 km/h\n• Height: up to 30m\n• Massive energy",
            "ar": "🌊 **تسونامي - ظاهرة محيطية:**\n• سلسلة أمواج طويلة المدى\n• السرعة: 800 كم/ساعة\n• الارتفاع: حتى 30 مترًا\n• طاقة هائلة"
        }
        return responses[language], image_url
    
    elif any(word in user_input_lower for word in ["sécurité", "safety", "أمان", "danger", "خطر", "faire", "do", "أفعل"]):
        image_url, description = generate_ai_image("safety", language)
        responses = {
            "fr": "🛡️ **Protection Tsunami - Règles Vitales:**\n\n🚨 **ÉVACUATION IMMÉDIATE:**\n• Montez > 15m altitude\n• Éloignez-vous du rivage\n• À PIED uniquement\n• Ne retournez pas\n\n📞 **Urgence: 112**",
            "en": "🛡️ **Tsunami Protection - Vital Rules:**\n\n🚨 **IMMEDIATE EVACUATION:**\n• Go above > 15m elevation\n• Move away from shore\n• On FOOT only\n• Don't go back\n\n📞 **Emergency: 112**",
            "ar": "🛡️ **حماية التسونامي - قواعد حيوية:**\n\n🚨 **الإخلاء الفوري:**\n• اصعد > 15م ارتفاع\n• ابتعد عن الشاطئ\n• على الأقدام فقط\n• لا تعود\n\n📞 **الطوارئ: 112**"
        }
        return responses[language], image_url
    
    elif any(word in user_input_lower for word in ["géomatique", "geomatics", "جيوماتكس", "sig", "gis", "carte", "map", "خريطة"]):
        image_url, description = generate_ai_image("geomatics", language)
        responses = {
            "fr": "🗺️ **Géomatique Appliquée - Notre Expertise:**\n\n📊 **Technologies:**\n• Systèmes d'Information Géographique (SIG)\n• Modèles Numériques de Terrain (MNT)\n• Télédétection satellite\n• Analyse spatiale avancée\n\n🎯 **Applications:**\n• Cartographie des risques\n• Modélisation d'impact\n• Plans d'évacuation optimisés",
            "en": "🗺️ **Applied Geomatics - Our Expertise:**\n\n📊 **Technologies:**\n• Geographic Information Systems (GIS)\n• Digital Terrain Models (DTM)\n• Satellite remote sensing\n• Advanced spatial analysis\n\n🎯 **Applications:**\n• Risk mapping\n• Impact modeling\n• Optimized evacuation plans",
            "ar": "🗺️ **الجيوماتكس التطبيقية - تخصصنا:**\n\n📊 **التقنيات:**\n• نظم المعلومات الجغرافية\n• النماذج الرقمية للتضاريس\n• الاستشعار عن بعد بالأقمار الصناعية\n• التحليل المكاني المتقدم\n\n🎯 **التطبيقات:**\n• رسم خرائط المخاطر\n• نمذجة التأثير\n• خطط الإخلاء المحسنة"
        }
        return responses[language], image_url
    
    # Réponse par défaut
    default_responses = {
        "fr": ["🤖 **Assistant AI Tsunami:**\nPosez-moi des questions sur les tsunamis, la sécurité, ou demandez-moi de générer des images éducatives!",
               "💡 **Conseil:** Dites 'montre-moi une image de...' pour des visuels explicatifs"],
        "en": ["🤖 **Tsunami AI Assistant:**\nAsk me about tsunamis, safety, or request educational image generation!",
               "💡 **Tip:** Say 'show me an image of...' for explanatory visuals"],
        "ar": ["🤖 **مساعد الذكاء الاصطناعي للتسونامي:**\nاسألني عن التسونامي، السلامة، أو اطلب إنشاء صور تعليمية!",
               "💡 **نصيحة:** قل 'أرني صورة...' للرسوم التوضيحية التفسيرية"]
    }
    
    return random.choice(default_responses[language]), None

# ==================== INTERFACE STREAMLIT AMÉLIORÉE ====================

# Header personnalisé
st.markdown('<div class="main-header">🚨 Tsunami AI Expert</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Assistant Intelligent Multilingue • Génération d\'Images • Expertise Géomatique</div>', unsafe_allow_html=True)

# Sidebar moderne
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    st.markdown("### 🌍 Sélection de la Langue")
    selected_language = st.radio("", list(LANGUAGES.keys()))
    current_lang = LANGUAGES[selected_language]
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 🧪 Questions de Test")
    
    test_questions = {
        "fr": [
            "🎨 Génère une image de tsunami",
            "🛡️ Montre les règles de sécurité", 
            "🗺️ Carte des risques tsunami",
            "🌊 Explique le phénomène tsunami",
            "📐 Hauteur des vagues tsunami"
        ],
        "en": [
            "🎨 Generate tsunami image",
            "🛡️ Show safety rules",
            "🗺️ Tsunami risk map", 
            "🌊 Explain tsunami phenomenon",
            "📐 Tsunami wave height"
        ],
        "ar": [
            "🎨 أنشئ صورة تسونامي",
            "🛡️ أظهر قواعد السلامة",
            "🗺️ خريطة خطر التسونامي",
            "🌊 اشرح ظاهرة التسونامي", 
            "📐 ارتفاع موجة التسونامي"
        ]
    }
    
    for question in test_questions[current_lang]:
        if st.button(question, key=question):
            st.session_state.auto_question = question
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="emergency-box">', unsafe_allow_html=True)
    st.markdown("### 🚨 URGENCE")
    st.markdown("**112** • **911** • **999**")
    st.markdown("Éloignez-vous du rivage immédiatement!")
    st.markdown("</div>", unsafe_allow_html=True)

# Zone de chat principale avec design amélioré
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Historique de conversation
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "🤖 **Bienvenue!** Je suis votre expert AI Tsunami. Demandez-moi des informations ou générez des images éducatives!", "image_url": None}
    ]

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if current_lang == "ar":
            st.markdown(f"<div dir='rtl' style='text-align: right;'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(message["content"])
        
        if message.get("image_url"):
            try:
                response = requests.get(message["image_url"], timeout=10)
                image = Image.open(io.BytesIO(response.content))
                st.image(image, use_column_width=True, caption="🖼️ Image éducative générée")
            except:
                st.warning("📡 Chargement de l'image...")

# Gestion des questions
if "auto_question" in st.session_state:
    prompt = st.session_state.auto_question
    del st.session_state.auto_question
else:
    prompt = None

# Input utilisateur
if prompt or (user_input := st.chat_input("💬 Posez votre question...")):

    if not prompt:
        prompt = user_input
    
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt, "image_url": None})
    
    # Simulation de chargement AI
    with st.spinner("🤖 AI en cours de génération..."):
        time.sleep(1)
        
        # Génération de la réponse AI
        response, image_url = get_ai_response(prompt, current_lang)
        
        # Ajout de la réponse
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "image_url": image_url
        })
        
        # Rechargement pour affichage
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Footer premium
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🔬 Projet Éducatif**")
    st.markdown("Géoinformatique Avancée")
with col2:
    st.markdown("**🤖 AI Powered**") 
    st.markdown Génération Intelligente")
with col3:
    st.markdown("**🌍 Multilingue**")
    st.markdown("Accessibilité Globale")
