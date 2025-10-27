import streamlit as st
import random
import base64
from PIL import Image, ImageDraw
import io
import time

# Configuration de la page
st.set_page_config(
    page_title="🌊 Tsunami Guard", 
    page_icon="🌊", 
    layout="wide"
)

# ==================== STYLE SIMPLE ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .chat-container {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }
    .sidebar-content {
        background: #f8f9fa;
        padding: 15px;
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
        border-radius: 8px;
        margin: 5px 0;
        width: 100%;
        cursor: pointer;
    }
    .arabic-text {
        direction: rtl;
        text-align: right;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SYSTÈME MULTILINGUE ====================

LANGUAGES = {
    "🇫🇷 Français": "fr",
    "🇬🇧 English": "en", 
    "🇸🇦 العربية": "ar"
}

# ==================== BASE DE CONNAISSANCES SIMPLE ====================

KNOWLEDGE_BASE = {
    "definition": {
        "keywords": {
            "fr": ["définition", "qu'est-ce", "c'est quoi", "explique", "définir"],
            "en": ["definition", "what is", "explain", "define"],
            "ar": ["تعريف", "ما هو", "شرح"]
        },
        "responses": {
            "fr": """
**🌊 DÉFINITION DU TSUNAMI**

Un tsunami est une série de vagues océaniques géantes causées par le déplacement soudain d'un grand volume d'eau.

**Caractéristiques :**
• Vitesse : 500-800 km/h
• Hauteur : jusqu'à 30 mètres
• Longueur d'onde : 100-200 km

**Attention :** Ce n'est pas une vague normale, mais un mouvement de toute la colonne d'eau.
            """,
            "en": """
**🌊 TSUNAMI DEFINITION**

A tsunami is a series of giant ocean waves caused by the sudden displacement of a large volume of water.

**Characteristics:**
• Speed: 500-800 km/h
• Height: up to 30 meters  
• Wavelength: 100-200 km

**Warning:** It's not a normal wave, but movement of the entire water column.
            """,
            "ar": """
**🌊 تعريف التسونامي**

التسونامي هو سلسلة من أمواج المحيط العملاقة الناتجة عن الانزياح المفاجئ لحجم كبير من الماء.

**الخصائص:**
• السرعة: 500-800 كم/ساعة
• الارتفاع: حتى 30 مترًا
• الطول الموجي: 100-200 كم

**تحذير:** ليس موجة عادية، ولكن حركة عمود الماء بالكامل.
            """
        }
    },
    
    "causes": {
        "keywords": {
            "fr": ["cause", "provoque", "origine", "pourquoi", "séisme"],
            "en": ["cause", "causes", "why", "origin", "earthquake"],
            "ar": ["سبب", "أسباب", "لماذا", "مصدر", "زلزال"]
        },
        "responses": {
            "fr": """
**📌 CAUSES DES TSUNAMIS**

**Principales causes :**

1. **Séismes sous-marins** (90%)
   - Magnitude > 7.0
   - Mouvement vertical des failles

2. **Glissements de terrain sous-marins**
   - Effondrement de sédiments

3. **Éruptions volcaniques**
   - Volcans sous-marins

4. **Impacts de météorites** (rares)
            """,
            "en": """
**📌 TSUNAMI CAUSES**

**Main causes:**

1. **Undersea earthquakes** (90%)
   - Magnitude > 7.0
   - Vertical fault movement

2. **Submarine landslides** 
   - Sediment collapse

3. **Volcanic eruptions**
   - Underwater volcanoes

4. **Meteorite impacts** (rare)
            """,
            "ar": """
**📌 أسباب التسونامي**

**الأسباب الرئيسية:**

1. **الزلازل تحت البحر** (90٪)
   - قوة أكبر من 7.0
   - حركة الصدوع العمودية

2. **الانهيارات الأرضية تحت البحر**
   - انهيار الرواسب

3. **الثورات البركانية**
   - البراكين تحت الماء

4. **اصطدام النيازك** (نادر)
            """
        }
    },
    
    "consequences": {
        "keywords": {
            "fr": ["conséquence", "impact", "effet", "dégât", "destruction"],
            "en": ["consequence", "impact", "effect", "damage", "destruction"],
            "ar": ["عاقبة", "تأثير", "أثر", "ضرر", "دمار"]
        },
        "responses": {
            "fr": """
**💥 CONSÉQUENCES DES TSUNAMIS**

**Impacts immédiats :**
• Victimes par noyade
• Destruction des infrastructures
• Pertes économiques énormes

**Impacts à long terme :**
• Pollution environnementale
• Déplacement des populations
• Traumatismes psychologiques

**Exemples :**
• 2004 : 230,000 morts
• 2011 : 18,000 morts
            """,
            "en": """
**💥 TSUNAMI CONSEQUENCES**

**Immediate impacts:**
• Drowning victims
• Infrastructure destruction
• Huge economic losses

**Long-term impacts:**
• Environmental pollution
• Population displacement
• Psychological trauma

**Examples:**
• 2004: 230,000 deaths
• 2011: 18,000 deaths
            """,
            "ar": """
**💥 عواقب التسونامي**

**الآثار الفورية:**
• ضحايا الغرق
• تدمير البنية التحتية
• خسائر اقتصادية هائلة

**الآثار طويلة المدى:**
• تلوث بيئي
• نزوح السكان
• صدمات نفسية

**أمثلة:**
• 2004: 230,000 وفاة
• 2011: 18,000 وفاة
            """
        }
    },
    
    "reaction": {
        "keywords": {
            "fr": ["réagir", "faire", "danger", "urgence", "évacuer", "alerte"],
            "en": ["react", "do", "danger", "emergency", "evacuate", "alert"],
            "ar": ["يتفاعل", "افعل", "خطر", "طوارئ", "إخلاء", "إنذار"]
        },
        "responses": {
            "fr": """
**🚨 QUE FAIRE FACE À UN TSUNAMI ?**

**Signes d'alerte :**
• Séisme prolongé
• Retrait de la mer
• Bruit fort

**Actions immédiates :**
1. Éloignez-vous du rivage
2. Montez en hauteur (>15m)
3. N'utilisez pas votre voiture
4. Alertez les autres
5. Suivez les consignes officielles

**Urgence : 112 / 911 / 999**
            """,
            "en": """
**🚨 WHAT TO DO DURING TSUNAMI?**

**Warning signs:**
• Prolonged earthquake
• Sea retreat
• Loud noise

**Immediate actions:**
1. Move away from shore
2. Go to high ground (>15m)
3. Don't use your car
4. Alert others
5. Follow official instructions

**Emergency: 112 / 911 / 999**
            """,
            "ar": """
**🚨 ماذا أفعل أثناء التسونامي؟**

**علامات التحذير:**
• زلزال طويل
• انسحاب البحر
• ضجيج عال

**الإجراءات الفورية:**
1. ابتعد عن الشاطئ
2. اصعد إلى مكان مرتفع (>15م)
3. لا تستخدم سيارتك
4. حذر الآخرين
5. اتبع التعليمات الرسمية

**الطوارئ: 112 / 911 / 999**
            """
        }
    }
}

# ==================== FONCTION DE RECHERCHE SIMPLE ====================

def find_response(user_input, language):
    """Trouve la réponse la plus pertinente"""
    user_input_lower = user_input.lower()
    
    # Recherche simple par mots-clés
    for category, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"][language]:
            if keyword in user_input_lower:
                return data["responses"][language]
    
    # Réponse par défaut
    default_responses = {
        "fr": "Posez-moi une question sur : définition, causes, conséquences, ou comment réagir face à un tsunami.",
        "en": "Ask me about: definition, causes, consequences, or how to react to tsunami.",
        "ar": "اسألني عن: التعريف، الأسباب، العواقب، أو كيفية التفاعل مع التسونامي."
    }
    return default_responses[language]

def display_text(text, language):
    """Affiche le texte avec la bonne direction"""
    if language == "ar":
        st.markdown(f'<div class="arabic-text">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(text)

# ==================== INTERFACE SIMPLE ====================

# Titre simple
st.markdown('<div class="main-header">🌊 Tsunami Guard</div>', unsafe_allow_html=True)

# Sidebar simple
with st.sidebar:
    st.markdown("### 🌍 Langue")
    selected_language = st.radio("", list(LANGUAGES.keys()), label_visibility="collapsed")
    current_lang = LANGUAGES[selected_language]
    
    st.markdown("### 💡 Questions types")
    
    sample_questions = {
        "fr": [
            "Définition tsunami",
            "Causes tsunami",
            "Conséquences tsunami", 
            "Que faire tsunami"
        ],
        "en": [
            "Tsunami definition",
            "Tsunami causes",
            "Tsunami consequences",
            "What to do tsunami"
        ],
        "ar": [
            "تعريف تسونامي",
            "أسباب تسونامي",
            "عواقب تسونامي",
            "ماذا أفعل تسونامي"
        ]
    }
    
    for question in sample_questions[current_lang]:
        if st.button(question, key=question):
            st.session_state.auto_question = question
    
    st.markdown("### 🚨 Urgence")
    st.markdown("**Éloignez-vous du rivage**")
    st.markdown("**112 • 911 • 999**")

# Zone de chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Historique de conversation
if "messages" not in st.session_state:
    welcome_messages = {
        "fr": "🌊 **Tsunami Guard** - Posez-moi vos questions sur les tsunamis.",
        "en": "🌊 **Tsunami Guard** - Ask me your questions about tsunamis.", 
        "ar": "🌊 **حارس التسونامي** - اسألني أسئلتك عن التسونامي."
    }
    st.session_state.messages = [
        {"role": "assistant", "content": welcome_messages[current_lang]}
    ]

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        display_text(message["content"], current_lang)

# Gestion des questions automatiques
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
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Génération de la réponse
    response = find_response(prompt, current_lang)
    
    # Ajout de la réponse
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response
    })
    
    st.rerun()
