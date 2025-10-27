import streamlit as st
import random
import requests
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import time

# Configuration de la page avec design moderne
st.set_page_config(
    page_title="🌊 Tsunami Guard", 
    page_icon="🌊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== STYLE CSS MODERNE ====================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1e88e5, #0d47a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .chat-container {
        background: white;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .sidebar-content {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 4px solid #1e88e5;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .emergency-box {
        background: linear-gradient(135deg, #ff5252, #d32f2f);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 6px 20px rgba(255,82,82,0.3);
    }
    .question-btn {
        background: linear-gradient(135deg, #4caf50, #2e7d32);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 12px;
        margin: 6px 0;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s;
        font-weight: 600;
        font-size: 0.9em;
    }
    .question-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(76,175,80,0.4);
    }
    .arabic-text {
        direction: rtl;
        text-align: right;
        font-size: 1.1em;
        line-height: 1.8;
        font-family: 'Arial', sans-serif;
    }
    .keyword-tag {
        display: inline-block;
        background: #e3f2fd;
        color: #1565c0;
        padding: 4px 12px;
        border-radius: 20px;
        margin: 2px;
        font-size: 0.8em;
        font-weight: 500;
    }
    .language-selector {
        background: #f5f5f5;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SYSTÈME MULTILINGUE ====================

LANGUAGES = {
    "🇫🇷 Français": "fr",
    "🇬🇧 English": "en", 
    "🇸🇦 العربية": "ar"
}

# ==================== GÉNÉRATION D'IMAGES RÉALISTES ====================

def create_realistic_tsunami_image(category, language):
    """Crée une image réaliste de tsunami selon la catégorie"""
    # Créer une image haute qualité
    img = Image.new('RGB', (800, 500), color=(240, 245, 249))
    d = ImageDraw.Draw(img)
    
    try:
        # Essayer de charger des polices plus grandes
        font_large = ImageFont.load_default()
        font_title = ImageFont.load_default()
    except:
        font_large = ImageFont.load_default()
        font_title = ImageFont.load_default()
    
    # Couleurs modernes
    primary_blue = (30, 136, 229)
    danger_red = (229, 57, 53)
    success_green = (67, 160, 71)
    dark_text = (33, 33, 33)
    light_bg = (250, 250, 250)
    
    # En-tête avec dégradé simulé
    d.rectangle([0, 0, 800, 80], fill=primary_blue)
    
    # Titres par catégorie
    titles = {
        "definition": {
            "fr": "🌊 PHÉNOMÈNE TSUNAMI", 
            "en": "🌊 TSUNAMI PHENOMENON", 
            "ar": "🌊 ظاهرة التسونامي"
        },
        "causes": {
            "fr": "📌 ORIGINES DU TSUNAMI", 
            "en": "📌 TSUNAMI ORIGINS", 
            "ar": "📌 مصادر التسونامي"
        },
        "consequences": {
            "fr": "💥 IMPACTS DÉVASTATEURS", 
            "en": "💥 DEVASTATING IMPACTS", 
            "ar": "💥 الآثار المدمرة"
        },
        "safety": {
            "fr": "🛡️ GUIDE DE SURVIE", 
            "en": "🛡️ SURVIVAL GUIDE", 
            "ar": "🛡️ دليل النجاة"
        },
        "reaction": {
            "fr": "🚨 URGENCE: QUE FAIRE?", 
            "en": "🚨 EMERGENCY: WHAT TO DO?", 
            "ar": "🚨 الطوارئ: ماذا أفعل؟"
        }
    }
    
    title = titles[category][language]
    d.text((400, 40), title, fill=(255, 255, 255), anchor="mm", font=font_title)
    
    # Contenu visuel selon la catégorie
    if category == "definition":
        # Diagramme scientifique réaliste
        # Océan
        d.rectangle([50, 150, 750, 300], fill=(33, 150, 243, 100), outline=primary_blue, width=3)
        
        # Vague tsunami
        wave_points = [(50, 250), (200, 180), (400, 160), (600, 190), (750, 250)]
        d.line(wave_points, fill=danger_red, width=4)
        
        # Flèches explicatives
        d.line((400, 160, 400, 120), fill=dark_text, width=2)
        d.text((410, 110), "30m", fill=danger_red)
        
        d.line((50, 350, 750, 350), fill=dark_text, width=2)
        d.text((400, 370), "200 km", fill=primary_blue)
        
    elif category == "causes":
        # Visualisation des causes
        causes = [
            ("SÉISME\n90%", 150, 180),
            ("GLISSEMENT\n5%", 350, 180), 
            ("VOLCAN\n4%", 550, 180),
            ("MÉTÉORITE\n1%", 400, 300)
        ]
        
        for text, x, y in causes:
            d.ellipse([x-60, y-60, x+60, y+60], outline=primary_blue, width=3)
            d.text((x, y), text, fill=dark_text, anchor="mm", font=font_large)
            
    elif category == "consequences":
        # Icônes d'impacts
        impacts = [
            ("🏠", "Destruction", 200, 180),
            ("👥", "Victimes", 400, 180),
            ("💰", "Coût économique", 600, 180),
            ("🌍", "Pollution", 300, 300),
            ("😔", "Traumatisme", 500, 300)
        ]
        
        for emoji, text, x, y in impacts:
            d.text((x, y-30), emoji, fill=dark_text, anchor="mm", font=font_large)
            d.text((x, y+20), text, fill=dark_text, anchor="mm", font=font_large)
            
    elif category == "safety" or category == "reaction":
        # Étapes de sécurité
        steps = [
            ("1. S'ÉLOIGNER", "Du rivage", 200, 160),
            ("2. MONTER", "> 15m altitude", 400, 160),
            ("3. ALERTER", "Les autres", 600, 160),
            ("4. NE PAS PRENDRE", "La voiture", 300, 280),
            ("5. RESTER INFORMÉ", "Médias officiels", 500, 280)
        ]
        
        for step, detail, x, y in steps:
            d.rectangle([x-80, y-40, x+80, y+40], fill=light_bg, outline=success_green, width=2)
            d.text((x, y-15), step, fill=dark_text, anchor="mm", font=font_large)
            d.text((x, y+15), detail, fill=primary_blue, anchor="mm", font=font_large)
    
    # Pied de page
    d.rectangle([0, 450, 800, 500], fill=(66, 66, 66))
    d.text((400, 475), "Tsunami Guard - Sécurité & Prévention", 
          fill=(255, 255, 255), anchor="mm", font=font_large)
    
    # Convertir en base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG", quality=95)
    return base64.b64encode(buffered.getvalue()).decode()

def display_image(base64_string, caption):
    """Affiche une image avec le bon paramètre"""
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption=caption, use_container_width=True)
    except:
        st.info("🖼️ Illustration générée")

# ==================== BASE DE CONNAISSANCES COMPLÈTE ====================

KNOWLEDGE_BASE = {
    "definition": {
        "keywords": {
            "fr": ["définition", "qu'est-ce", "c'est quoi", "explique", "définir", "quoi", "tsunami"],
            "en": ["definition", "what is", "explain", "define", "what", "tsunami"],
            "ar": ["تعريف", "ما هو", "شرح", "ماهو", "ما", "تسونامي"]
        },
        "responses": {
            "fr": """
**🌊 COMPRENDRE LE TSUNAMI**

Un tsunami est une série de vagues océaniques extrêmement longues générées par le déplacement soudain d'un grand volume d'eau.

**📊 CARACTÉRISTIQUES CLÉS :**
- **Vitesse** : 500-800 km/h (comme un avion)
- **Hauteur** : 1m en mer → 10-30m sur les côtes  
- **Longueur** : 100-200 km (vs 100m vague normale)
- **Énergie** : Équivalente à des milliers de bombes atomiques

**⚠️ CE N'EST PAS :** Une simple grosse vague, mais le mouvement de TOUTE la colonne d'eau.
            """,
            "en": """
**🌊 UNDERSTANDING TSUNAMI**

A tsunami is a series of extremely long ocean waves generated by the sudden displacement of a large volume of water.

**📊 KEY CHARACTERISTICS:**
- **Speed**: 500-800 km/h (like a jet)
- **Height**: 1m at sea → 10-30m on coasts
- **Length**: 100-200 km (vs 100m normal wave)  
- **Energy**: Equivalent to thousands of atomic bombs

**⚠️ IT IS NOT:** Just a big wave, but movement of the ENTIRE water column.
            """,
            "ar": """
**🌊 فهم التسونامي**

التسونامي هو سلسلة من أمواج المحيط الطويلة جدًا الناتجة عن الانزياح المفاجئ لحجم كبير من الماء.

**📊 الخصائص الرئيسية:**
- **السرعة**: 500-800 كم/ساعة (مثل الطائرة)
- **الارتفاع**: 1م في البحر → 10-30م على السواحل
- **الطول**: 100-200 كم (مقابل 100م موجة عادية)
- **الطاقة**: تعادل آلاف القنابل الذرية

**⚠️ ليس مجرد:** موجة كبيرة، ولكن حركة عمود الماء بالكامل.
            """
        }
    },
    
    "causes": {
        "keywords": {
            "fr": ["cause", "provoque", "origine", "pourquoi", "séisme", "tremblement", "volcan", "glissement"],
            "en": ["cause", "causes", "why", "origin", "earthquake", "volcano", "landslide", "trigger"],
            "ar": ["سبب", "أسباب", "لماذا", "مصدر", "زلزال", "بركان", "انهيار", "يتسبب"]
        },
        "responses": {
            "fr": """
**📌 ORIGINES PRINCIPALES :**

1. **SÉISMES SOUS-MARINS** (90% des cas)
   - Magnitude > 7.0 nécessaire
   - Mouvement vertical des failles
   - Exemple : Japon 2011 (magnitude 9.0)

2. **GLISSEMENTS DE TERRAIN** 
   - Effondrement de sédiments sous-marins  
   - Volumes énormes (km³)

3. **ÉRUPTIONS VOLCANIQUES**
   - Effondrement de volcans sous-marins
   - Projections dans l'océan

4. **IMPACTS EXTRATERRESTRES**
   - Météorites (très rare)

**🔬 MÉCANISME :** Déplacement eau → Ondes → Amplification côtière
            """,
            "en": """
**📌 MAIN ORIGINS:**

1. **UNDERSEA EARTHQUAKES** (90% of cases)
   - Magnitude > 7.0 required
   - Vertical fault movement  
   - Example: Japan 2011 (magnitude 9.0)

2. **SUBMARINE LANDSLIDES**
   - Underwater sediment collapse
   - Huge volumes (km³)

3. **VOLCANIC ERUPTIONS** 
   - Underwater volcano collapse
   - Ocean projections

4. **EXTRATERRESTRIAL IMPACTS**
   - Meteorites (very rare)

**🔬 MECHANISM:** Water displacement → Waves → Coastal amplification
            """,
            "ar": """
**📌 المصادر الرئيسية:**

1. **الزلازل تحت البحر** (90٪ من الحالات)
   - требуется قوة أكبر من 7.0
   - حركة الصدوع العمودية
   - مثال: اليابان 2011 (قوة 9.0)

2. **الانهيارات الأرضية تحت البحر**
   - انهيار الرواسب تحت الماء
   - أحجام هائلة (كم³)

3. **الثورات البركانية**
   - انهيار البراكين تحت الماء
   - القذف في المحيط

4. **التأثيرات خارج الأرض**
   - النيازك (نادر جدًا)

**🔬 الآلية:** إزاحة الماء → موج → تضخيم ساحلي
            """
        }
    },
    
    "consequences": {
        "keywords": {
            "fr": ["conséquence", "impact", "effet", "dégât", "destruction", "victime", "dévastation"],
            "en": ["consequence", "impact", "effect", "damage", "destruction", "victim", "devastation"],
            "ar": ["عاقبة", "تأثير", "أثر", "ضرر", "دمار", "ضحية", "تدمير"]
        },
        "responses": {
            "fr": """
**💥 IMPACTS DÉVASTATEURS :**

**IMMÉDIATS :**
- **Humain** : Noyades, traumatismes physiques
- **Matériel** : Infrastructure côtière détruite
- **Économique** : Pertes milliardaires

**À LONG TERME :**
- **Environnement** : Pollution, salinisation sols
- **Social** : Déplacement populations, traumatismes
- **Sanitaire** : Maladies, eau contaminée

**📈 EXEMPLES HISTORIQUES :**
- 2004 Océan Indien : 230,000 morts
- 2011 Japon : 18,000 morts + Fukushima
            """,
            "en": """
**💥 DEVASTATING IMPACTS:**

**IMMEDIATE:**
- **Human**: Drowning, physical trauma  
- **Material**: Coastal infrastructure destroyed
- **Economic**: Billion-dollar losses

**LONG-TERM:**
- **Environment**: Pollution, soil salinization
- **Social**: Population displacement, trauma
- **Health**: Diseases, contaminated water

**📈 HISTORICAL EXAMPLES:**
- 2004 Indian Ocean: 230,000 deaths
- 2011 Japan: 18,000 deaths + Fukushima
            """,
            "ar": """
**💥 الآثار المدمرة:**

**فورية:**
- **بشرية**: غرق، صدمات جسدية
- **مادية**: تدمير البنية التحتية الساحلية
- **اقتصادية**: خسائر بمليارات الدولارات

**طويلة الأمد:**
- **بيئية**: تلوث، تمليح التربة
- **اجتماعية**: نزوح السكان، صدمات
- **صحية**: أمراض، مياه ملوثة

**📈 أمثلة تاريخية:**
- 2004 المحيط الهندي: 230,000 وفاة
- 2011 اليابان: 18,000 وفاة + فوكوشيما
            """
        }
    },
    
    "reaction": {
        "keywords": {
            "fr": ["réagir", "faire", "danger", "urgence", "évacuer", "alerte", "protéger", "survie", "sauver"],
            "en": ["react", "do", "danger", "emergency", "evacuate", "alert", "protect", "survival", "save"],
            "ar": ["يتفاعل", "افعل", "خطر", "طوارئ", "إخلاء", "إنذار", "حماية", "نجاة", "أنقذ"]
        },
        "responses": {
            "fr": """
**🚨 GUIDE DE SURVIE IMMÉDIAT :**

**SIGNES D'ALERTE :**
- Séisme prolongé (>20 secondes)
- Retrait soudain de la mer
- Bruit de locomotive

**ACTION IMMÉDIATE :**
1. 🏃 **FUYEZ** vers l'intérieur des terres
2. ⬆️ **MONTEZ** > 15m d'altitude
3. 📢 **ALERTEZ** les personnes autour
4. 🚫 **NE PRENEZ PAS** votre voiture
5. 📱 **SUIVEZ** les consignes officielles

**⏱️ TEMPS CRITIQUE :** 5-30 minutes pour évacuer
**📞 URGENCE :** 112 / 911 / 999
            """,
            "en": """
**🚨 IMMEDIATE SURVIVAL GUIDE:**

**WARNING SIGNS:**
- Prolonged earthquake (>20 seconds)  
- Sudden sea retreat
- Locomotive-like noise

**IMMEDIATE ACTION:**
1. 🏃 **RUN** inland
2. ⬆️ **CLIMB** > 15m elevation  
3. 📢 **ALERT** people around
4. 🚫 **DON'T TAKE** your car
5. 📱 **FOLLOW** official instructions

**⏱️ CRITICAL TIME:** 5-30 minutes to evacuate
**📞 EMERGENCY:** 112 / 911 / 999
            """,
            "ar": """
**🚨 دليل النجاة الفوري:**

**علامات التحذير:**
- زلزال طويل الأمد (>20 ثانية)
- انسحاب مفاجئ للبحر
- ضجيج مثل القطار

**الإجراءات الفورية:**
1. 🏃 **اهرب** إلى الداخل
2. ⬆️ **اصعد** > 15م ارتفاعًا
3. 📢 **حذر** الأشخاص حولك
4. 🚫 **لا تأخذ** سيارتك
5. 📱 **اتبع** التعليمات الرسمية

**⏱️ الوقت الحرج:** 5-30 دقيقة للإخلاء
**📞 الطوارئ:** 112 / 911 / 999
            """
        }
    }
}

# ==================== SYSTÈME DE RECHERCHE INTELLIGENT ====================

def find_response(user_input, language):
    """Trouve la réponse la plus pertinente"""
    user_input_lower = user_input.lower()
    
    # Détection de demande d'image
    image_words = ["image", "photo", "diagramme", "schéma", "illustration", "صورة", "رسم", "مخطط"]
    wants_image = any(word in user_input_lower for word in image_words)
    
    # Recherche par catégorie
    for category, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"][language]:
            if keyword in user_input_lower:
                image_data = create_realistic_tsunami_image(category, language) if wants_image else None
                return data["responses"][language], image_data, category
    
    # Réponse par défaut
    default_responses = {
        "fr": "🤖 **Tsunami Guard** - Posez-moi sur : définition, causes, conséquences, ou comment réagir. Utilisez des mots-clés !",
        "en": "🤖 **Tsunami Guard** - Ask me about: definition, causes, consequences, or how to react. Use keywords!",
        "ar": "🤖 **حارس التسونامي** - اسألني عن: التعريف، الأسباب، العواقب، أو كيفية التفاعل. استخدم الكلمات المفتاحية!"
    }
    return default_responses[language], None, None

def display_text(text, language):
    """Affiche le texte avec la bonne direction"""
    if language == "ar":
        st.markdown(f'<div class="arabic-text">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(text)

# ==================== INTERFACE STREAMLIT ====================

# Header épuré
st.markdown('<div class="main-header">🌊 Tsunami Guard</div>', unsafe_allow_html=True)

# Sidebar moderne
with st.sidebar:
    st.markdown('<div class="language-selector">', unsafe_allow_html=True)
    st.markdown("### 🌍 Choisir la langue")
    selected_language = st.radio("", list(LANGUAGES.keys()), label_visibility="collapsed")
    current_lang = LANGUAGES[selected_language]
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 💡 Questions types")
    
    sample_questions = {
        "fr": [
            "Définition d'un tsunami",
            "Causes principales",
            "Conséquences et impacts", 
            "Comment réagir face à un tsunami",
            "Image d'un tsunami"
        ],
        "en": [
            "Tsunami definition",
            "Main causes",
            "Consequences and impacts",
            "How to react to tsunami", 
            "Tsunami image"
        ],
        "ar": [
            "تعريف التسونامي",
            "الأسباب الرئيسية",
            "العواقب والآثار",
            "كيفية التفاعل مع التسونامي",
            "صورة تسونامي"
        ]
    }
    
    for question in sample_questions[current_lang]:
        if st.button(question, key=f"q_{question}"):
            st.session_state.auto_question = question
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 🔍 Mots-clés utiles")
    
    keyword_examples = {
        "fr": ["définition", "causes", "conséquences", "réagir", "image"],
        "en": ["definition", "causes", "consequences", "react", "image"],
        "ar": ["تعريف", "أسباب", "عواقب", "يتفاعل", "صورة"]
    }
    
    keywords_html = " ".join([f'<span class="keyword-tag">{kw}</span>' for kw in keyword_examples[current_lang]])
    st.markdown(f'<div>{keywords_html}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="emergency-box">', unsafe_allow_html=True)
    st.markdown("### 🚨 URGENCE")
    st.markdown("**Éloignement immédiat du rivage**")
    st.markdown("**112 • 911 • 999**")
    st.markdown("</div>", unsafe_allow_html=True)

# Zone de chat principale
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Historique de conversation
if "messages" not in st.session_state:
    welcome_messages = {
        "fr": "🌊 **Bonjour ! Je suis Tsunami Guard.** Posez-moi vos questions sur les tsunamis : définition, causes, conséquences, ou comment réagir. Utilisez des mots-clés pour des réponses précises !",
        "en": "🌊 **Hello! I'm Tsunami Guard.** Ask me your questions about tsunamis: definition, causes, consequences, or how to react. Use keywords for precise answers!",
        "ar": "🌊 **مرحبًا! أنا حارس التسونامي.** اسألني أسئلتك عن التسونامي: التعريف، الأسباب، العواقب، أو كيفية التفاعل. استخدم الكلمات المفتاحية لإجابات دقيقة!"
    }
    st.session_state.messages = [
        {"role": "assistant", "content": welcome_messages[current_lang], "image_data": None}
    ]

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        display_text(message["content"], current_lang)
        if message.get("image_data"):
            captions = {
                "definition": {"fr": "Phénomène tsunami", "en": "Tsunami phenomenon", "ar": "ظاهرة التسونامي"},
                "causes": {"fr": "Origines du tsunami", "en": "Tsunami origins", "ar": "مصادر التسونامي"},
                "consequences": {"fr": "Impacts du tsunami", "en": "Tsunami impacts", "ar": "آثار التسونامي"},
                "reaction": {"fr": "Guide de survie", "en": "Survival guide", "ar": "دليل النجاة"}
            }
            caption = captions.get(message.get("category", ""), {}).get(current_lang, "Illustration")
            display_image(message["image_data"], caption)

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
    st.session_state.messages.append({"role": "user", "content": prompt, "image_data": None})
    
    # Génération de la réponse
    with st.spinner("🔍 Recherche en cours..."):
        time.sleep(0.3)
        response, image_data, category = find_response(prompt, current_lang)
        
        # Ajout de la réponse
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "image_data": image_data,
            "category": category
        })
        
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
