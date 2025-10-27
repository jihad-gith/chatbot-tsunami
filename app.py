import streamlit as st
import random
import requests
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import time
import re

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
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        border: 2px solid #e0e0e0;
    }
    .sidebar-content {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #1f77b4;
    }
    .emergency-box {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .question-btn {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        margin: 8px 0;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s;
        font-weight: bold;
    }
    .question-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .response-box {
        background: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .arabic-text {
        direction: rtl;
        text-align: right;
        font-size: 1.1em;
        line-height: 1.8;
    }
    .image-container {
        text-align: center;
        margin: 20px 0;
        padding: 15px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==================== SYSTÈME MULTILINGUE ====================

LANGUAGES = {
    "🇫🇷 Français": "fr",
    "🇬🇧 English": "en", 
    "🇸🇦 العربية": "ar"
}

# ==================== FONCTIONS POUR IMAGES AMÉLIORÉES ====================

def create_educational_image(category, language):
    """Crée une image éducative de haute qualité"""
    # Créer une image plus grande et détaillée
    img = Image.new('RGB', (600, 400), color=(240, 245, 249))
    d = ImageDraw.Draw(img)
    
    try:
        # Essayer de charger une police, sinon utiliser la police par défaut
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Couleurs
    primary_color = (41, 128, 185)  # Bleu
    secondary_color = (231, 76, 60)   # Rouge
    accent_color = (46, 204, 113)     # Vert
    text_color = (44, 62, 80)         # Gris foncé
    
    # Dessiner un en-tête
    d.rectangle([0, 0, 600, 60], fill=primary_color)
    
    # Textes selon la catégorie et la langue
    titles = {
        "definition": {
            "fr": "🌊 DIAGRAMME DU TSUNAMI", 
            "en": "🌊 TSUNAMI DIAGRAM", 
            "ar": "🌊 مخطط التسونامي"
        },
        "causes": {
            "fr": "📌 CAUSES DU TSUNAMI", 
            "en": "📌 TSUNAMI CAUSES", 
            "ar": "📌 أسباب التسونامي"
        },
        "consequences": {
            "fr": "💥 CONSÉQUENCES DU TSUNAMI", 
            "en": "💥 TSUNAMI CONSEQUENCES", 
            "ar": "💥 عواقب التسونامي"
        },
        "safety": {
            "fr": "🛡️ SÉCURITÉ TSUNAMI", 
            "en": "🛡️ TSUNAMI SAFETY", 
            "ar": "🛡️ سلامة التسونامي"
        }
    }
    
    # Dessiner le titre
    title = titles[category][language]
    d.text((300, 30), title, fill=(255, 255, 255), anchor="mm", font=font_large)
    
    # Dessiner des éléments éducatifs détaillés selon la catégorie
    if category == "definition":
        # Diagramme de vague tsunami
        d.rectangle([100, 100, 500, 250], outline=primary_color, width=3)
        
        # Ligne d'eau
        d.line([100, 175, 500, 175], fill=primary_color, width=2)
        d.text((80, 170), "Niveau mer", fill=text_color, anchor="rm")
        
        # Flèche de hauteur
        d.line([150, 175, 150, 120], fill=secondary_color, width=2)
        d.line([145, 125, 150, 120], fill=secondary_color, width=2)
        d.line([155, 125, 150, 120], fill=secondary_color, width=2)
        d.text((170, 145), "Hauteur vague\n30m max", fill=secondary_color)
        
        # Flèche de longueur
        d.line([100, 280, 500, 280], fill=accent_color, width=2)
        d.line([495, 275, 500, 280], fill=accent_color, width=2)
        d.line([495, 285, 500, 280], fill=accent_color, width=2)
        d.text((300, 300), "Longueur d'onde: 100-200km", fill=accent_color, anchor="mm")
        
    elif category == "causes":
        # Diagramme des causes
        y_positions = [120, 180, 240, 300]
        causes = [
            ("Séisme sous-marin", "90%"),
            ("Glissement terrain", "5%"),
            ("Éruption volcanique", "4%"),
            ("Impact météorite", "1%")
        ]
        
        for i, (cause, percentage) in enumerate(causes):
            x_start = 150
            bar_width = int(300 * (int(percentage.strip('%')) / 100))
            
            # Barre de pourcentage
            d.rectangle([x_start, y_positions[i], x_start + bar_width, y_positions[i] + 30], 
                       fill=primary_color, outline=text_color, width=1)
            
            # Texte
            d.text((x_start - 10, y_positions[i] + 15), cause, fill=text_color, anchor="rm")
            d.text((x_start + bar_width + 10, y_positions[i] + 15), percentage, 
                  fill=secondary_color, anchor="lm")
        
    elif category == "consequences":
        # Icônes des conséquences
        consequences = [
            ("👥 Victimes", "230k (2004)"),
            ("🏠 Destructions", "Infrastructures"),
            ("💰 Coût", "Milliards $"),
            ("🌍 Environnement", "Pollution")
        ]
        
        for i, (consequence, detail) in enumerate(consequences):
            x = 150 + (i % 2) * 200
            y = 120 + (i // 2) * 100
            
            # Cercle avec icône
            d.ellipse([x-30, y-30, x+30, y+30], outline=secondary_color, width=2)
            d.text((x, y-5), consequence.split()[0], fill=text_color, anchor="mm")
            d.text((x, y+40), detail, fill=text_color, anchor="mm", font=font_medium)
            
    elif category == "safety":
        # Étapes de sécurité
        steps = [
            ("1. S'éloigner", "Du rivage"),
            ("2. Monter", "> 15m hauteur"),
            ("3. Alerter", "Les personnes"),
            ("4. Ne pas prendre", "La voiture")
        ]
        
        for i, (step, detail) in enumerate(steps):
            x = 150
            y = 120 + i * 70
            
            # Numéro dans un cercle
            d.ellipse([x-25, y-25, x+25, y+25], fill=accent_color, outline=accent_color)
            d.text((x, y), str(i+1), fill=(255, 255, 255), anchor="mm", font=font_large)
            
            # Texte de l'étape
            d.text((x+50, y-10), step, fill=text_color, anchor="lm", font=font_large)
            d.text((x+50, y+10), detail, fill=text_color, anchor="lm", font=font_medium)
    
    # Pied de page
    d.rectangle([0, 370, 600, 400], fill=(52, 73, 94))
    d.text((300, 385), "Tsunami AI Expert - Illustration Éducative", 
          fill=(255, 255, 255), anchor="mm", font=font_medium)
    
    # Convertir en base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG", quality=95)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str

def display_base64_image(base64_string, caption):
    """Affiche une image encodée en base64 - CORRIGÉ avec use_container_width"""
    try:
        # Décoder l'image base64
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        
        # Afficher l'image avec Streamlit - CORRECTION APPLIQUÉE
        st.image(image, caption=caption, use_container_width=True)  # use_container_width au lieu de use_column_width
    except Exception as e:
        # En cas d'erreur, afficher un message
        st.info("🖼️ *Illustration éducative générée*")

# ==================== BASE DE CONNAISSANCES AVANCÉE ====================

KNOWLEDGE_BASE = {
    "definition": {
        "keywords": {
            "fr": ["définition", "qu'est-ce", "c'est quoi", "explique", "définir", "quoi", "image", "diagramme", "schéma"],
            "en": ["definition", "what is", "explain", "define", "what", "image", "diagram", "schema"],
            "ar": ["تعريف", "ما هو", "شرح", "ماهو", "ما", "صورة", "مخطط", "رسم"]
        },
        "responses": {
            "fr": """
🌊 **DÉFINITION DU TSUNAMI**

**Un tsunami** est une série de vagues océaniques extrêmement longues générées par le déplacement soudain d'un grand volume d'eau.

**Caractéristiques principales :**
• Longueur d'onde : 100-200 km (vs 100m pour vagues normales)
• Vitesse : 500-800 km/h en eau profonde
• Hauteur : 1m en mer → 10-30m près des côtes
• Période : 10-60 minutes entre vagues

**Différence avec une vague normale :**
Ce n'est PAS une simple grosse vague, mais un mouvement de toute la colonne d'eau du fond à la surface.
            """,
            "en": """
🌊 **TSUNAMI DEFINITION**

**A tsunami** is a series of extremely long ocean waves generated by the sudden displacement of a large volume of water.

**Key characteristics:**
• Wavelength: 100-200 km (vs 100m for normal waves)
• Speed: 500-800 km/h in deep water
• Height: 1m at sea → 10-30m near coasts
• Period: 10-60 minutes between waves

**Difference from normal waves:**
It is NOT just a big wave, but movement of the entire water column from bottom to surface.
            """,
            "ar": """
🌊 **تعريف التسونامي**

**التسونامي** هو سلسلة من أمواج المحيط الطويلة جدًا الناتجة عن الانزياح المفاجئ لحجم كبير من الماء.

**الخصائص الرئيسية:**
• الطول الموجي: 100-200 كم (مقابل 100م للأمواج العادية)
• السرعة: 500-800 كم/ساعة في المياه العميقة
• الارتفاع: 1م في البحر → 10-30م بالقرب من السواحل
• الفترة: 10-60 دقيقة بين الأمواج

**الفرق عن الموج العادي:**
ليس مجرد موجة كبيرة، ولكن حركة عمود الماء بالكامل من القاع إلى السطح.
            """
        }
    },
    
    "causes": {
        "keywords": {
            "fr": ["cause", "provoque", "origine", "pourquoi", "séisme", "tremblement", "volcan", "image causes"],
            "en": ["cause", "causes", "why", "origin", "earthquake", "volcano", "trigger", "cause image"],
            "ar": ["سبب", "أسباب", "لماذا", "مصدر", "زلزال", "بركان", "يتسبب", "صورة أسباب"]
        },
        "responses": {
            "fr": """
📌 **CAUSES DES TSUNAMIS**

**Principales causes (par ordre de fréquence) :**

1. **Séismes sous-marins (90% des cas)**
   • Magnitude > 7.0 sur l'échelle de Richter
   • Mouvement vertical des failles
   • Exemple : Japon 2011 (magnitude 9.0)

2. **Glissements de terrain sous-marins**
   • Effondrement de sédiments
   • Volumes pouvant atteindre des km³

3. **Éruptions volcaniques**
   • Effondrement de volcans sous-marins
   • Pyroclastiques entrant dans l'eau

4. **Impacts de météorites**
   • Événements rares mais dévastateurs

**Mécanisme :** Déplacement vertical du fond marin → Déplacement de la colonne d'eau → Formation d'ondes.
            """,
            "en": """
📌 **TSUNAMI CAUSES**

**Main causes (by frequency order):**

1. **Undersea earthquakes (90% of cases)**
   • Magnitude > 7.0 on Richter scale
   • Vertical fault movement
   • Example: Japan 2011 (magnitude 9.0)

2. **Submarine landslides**
   • Sediment collapse
   • Volumes up to km³

3. **Volcanic eruptions**
   • Underwater volcano collapse
   • Pyroclastics entering water

4. **Meteorite impacts**
   • Rare but devastating events

**Mechanism:** Vertical seabed displacement → Water column displacement → Wave formation.
            """,
            "ar": """
📌 **أسباب التسونامي**

**الأسباب الرئيسية (حسب الترتيب التكراري):**

1. **الزلازل تحت البحر (90٪ من الحالات)**
   • قوة أكبر من 7.0 على مقياس ريختر
   • حركة الصدوع العمودية
   • مثال: اليابان 2011 (قوة 9.0)

2. **الانهيارات الأرضية تحت البحر**
   • انهيار الرواسب
   • أحجام تصل إلى كيلومترات مكعبة

3. **الثورات البركانية**
   • انهيار البراكين تحت الماء
   • دخول المواد البركانية إلى الماء

4. **اصطدام النيازك**
   • أحداث نادرة ولكن مدمرة

**الآلية:** الانزياح الرأسي لقاع البحر → إزاحة عمود الماء → تكوين الموج.
            """
        }
    },
    
    "consequences": {
        "keywords": {
            "fr": ["conséquence", "impact", "effet", "dégât", "destruction", "victime", "image impacts"],
            "en": ["consequence", "impact", "effect", "damage", "destruction", "victim", "impact image"],
            "ar": ["عاقبة", "تأثير", "أثر", "ضرر", "دمار", "ضحية", "صورة تأثيرات"]
        },
        "responses": {
            "fr": """
💥 **CONSÉQUENCES DES TSUNAMIS**

**Impacts immédiats :**
• **Humain :** Milliers de victimes par noyade, traumatismes
• **Matériel :** Destruction complète des infrastructures côtières
• **Économique :** Pertes de plusieurs milliards de dollars

**Impacts à long terme :**
• **Environnemental :** Salinisation des terres, pollution
• **Social :** Déplacement de populations, traumatismes psychologiques
• **Sanitaire :** Risques d'épidémies, eau contaminée

**Exemples historiques :**
• 2004 Océan Indien : 230,000 victimes
• 2011 Japon : 18,000 victimes + catastrophe nucléaire
            """,
            "en": """
💥 **TSUNAMI CONSEQUENCES**

**Immediate impacts:**
• **Human:** Thousands of victims by drowning, trauma
• **Material:** Complete destruction of coastal infrastructure
• **Economic:** Losses of several billion dollars

**Long-term impacts:**
• **Environmental:** Land salinization, pollution
• **Social:** Population displacement, psychological trauma
• **Health:** Epidemic risks, contaminated water

**Historical examples:**
• 2004 Indian Ocean: 230,000 victims
• 2011 Japan: 18,000 victims + nuclear disaster
            """,
            "ar": """
💥 **عواقب التسونامي**

**الآثار الفورية:**
• **البشرية:** آلاف الضحايا بسبب الغرق والصدمات
• **المادية:** تدمير كامل للبنية التحتية الساحلية
• **الاقتصادية:** خسائر بمليارات الدولارات

**الآثار طويلة المدى:**
• **البيئية:** تمليح الأراضي، التلوث
• **الاجتماعية:** نزوح السكان، الصدمات النفسية
• **الصحية:** مخاطر الأوبئة، تلوث المياه

**أمثلة تاريخية:**
• 2004 المحيط الهندي: 230,000 ضحية
• 2011 اليابان: 18,000 ضحية + كارثة نووية
            """
        }
    },
    
    "safety": {
        "keywords": {
            "fr": ["sécurité", "danger", "que faire", "évacuer", "alerte", "protéger", "survie", "image sécurité"],
            "en": ["safety", "danger", "what to do", "evacuate", "alert", "protect", "survival", "safety image"],
            "ar": ["أمان", "خطر", "ماذا أفعل", "إخلاء", "إنذار", "حماية", "نجاة", "صورة سلامة"]
        },
        "responses": {
            "fr": """
🛡️ **SÉCURITÉ - RÈGLES VITALES**

**Signes d'alerte naturels :**
• Séisme prolongé (>20 secondes)
• Retrait soudain et inhabituel de la mer
• Bruit rugissant venant de l'océan

**Actions IMMÉDIATES :**
1. 🏃 **Éloignez-vous du rivage** - Ne restez pas pour observer
2. ⬆️ **Gagnez les hauteurs** - Minimum 15m, idéalement 30m
3. 🚫 **Ne prenez pas votre voiture** - Elle crée des embouteillages mortels
4. 📞 **Alertez les personnes autour** - Criez pour prévenir
5. 📱 **Restez informé** - Suivez les consignes officielles

**Numéros d'urgence :** 112 (Europe) • 911 (USA) • 999 (UK)
            """,
            "en": """
🛡️ **SAFETY - VITAL RULES**

**Natural warning signs:**
• Prolonged earthquake (>20 seconds)
• Sudden unusual sea retreat
• Roaring noise from ocean

**IMMEDIATE actions:**
1. 🏃 **Move away from shore** - Don't stay to observe
2. ⬆️ **Reach high ground** - Minimum 15m, ideally 30m
3. 🚫 **Don't take your car** - Creates deadly traffic jams
4. 📞 **Alert people around** - Shout to warn
5. 📱 **Stay informed** - Follow official instructions

**Emergency numbers:** 112 (Europe) • 911 (USA) • 999 (UK)
            """,
            "ar": """
🛡️ **السلامة - قواعد حيوية**

**علامات التحذير الطبيعية:**
• زلزال طويل الأمد (>20 ثانية)
• انسحاب مفاجئ وغير عادي للبحر
• ضجيج هدير قادم من المحيط

**الإجراءات الفورية:**
1. 🏃 **ابتعد عن الشاطئ** - لا تبقى للمراقبة
2. ⬆️ **اتجه إلى المرتفعات** - 15 متر كحد أدنى، 30 متر بشكل مثالي
3. 🚫 **لا تستخدم سيارتك** - تسبب اختناقات مرورية مميتة
4. 📞 **حذر الأشخاص حولك** - اصرخ للتحذير
5. 📱 **ابق على اطلاع** - اتبع التعليمات الرسمية

**أرقام الطوارئ:** 112 (أوروبا) • 911 (الولايات المتحدة) • 999 (المملكة المتحدة)
            """
        }
    }
}

# ==================== SYSTÈME INTELLIGENT DE RECHERCHE ====================

def find_best_response(user_input, language):
    """Trouve la meilleure réponse basée sur les mots-clés dans toutes les langues"""
    user_input_lower = user_input.lower()
    
    # Vérifier d'abord les demandes explicites d'images
    image_keywords = {
        "fr": ["image", "photo", "diagramme", "schéma", "illustration", "montre", "voir"],
        "en": ["image", "picture", "diagram", "schema", "illustration", "show", "see"],
        "ar": ["صورة", "رسم", "مخطط", "توضيح", "أرني", "عرض"]
    }
    
    has_image_request = any(keyword in user_input_lower for keyword in image_keywords[language])
    
    # Recherche dans la langue actuelle pour chaque catégorie
    for category, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"][language]:
            if keyword.lower() in user_input_lower:
                # Générer une image pour cette catégorie
                image_base64 = create_educational_image(category, language)
                return data["responses"][language], image_base64, category
    
    # Si demande d'image explicite mais pas de catégorie trouvée
    if has_image_request:
        # Générer une image générale
        image_base64 = create_educational_image("definition", language)
        default_image_responses = {
            "fr": "🖼️ **Voici une illustration éducative sur les tsunamis.**\n\nPosez une question plus spécifique comme 'image causes tsunami' ou 'diagramme sécurité' pour des illustrations ciblées.",
            "en": "🖼️ **Here's an educational illustration about tsunamis.**\n\nAsk a more specific question like 'tsunami causes image' or 'safety diagram' for targeted illustrations.",
            "ar": "🖼️ **ها هي رسم توضيحي تعليمي عن التسونامي.**\n\nاطرح سؤالاً أكثر تحديداً مثل 'صورة أسباب التسونامي' أو 'مخطط السلامة' للحصول على رسوم توضيحية مستهدفة."
        }
        return default_image_responses[language], image_base64, "definition"
    
    # Si aucune correspondance, réponse par défaut
    default_responses = {
        "fr": "🤖 **Assistant Tsunami:** Posez-moi sur : définition, causes, conséquences ou sécurité. Essayez 'définition tsunami' ou 'image sécurité tsunami'",
        "en": "🤖 **Tsunami Assistant:** Ask me about: definition, causes, consequences or safety. Try 'tsunami definition' or 'tsunami safety image'",
        "ar": "🤖 **مساعد التسونامي:** اسألني عن: التعريف، الأسباب، العواقب أو السلامة. جرب 'تعريف التسونامي' أو 'صورة سلامة التسونامي'"
    }
    
    return default_responses[language], None, None

def display_text_with_direction(text, language):
    """Affiche le texte avec la bonne direction (RTL pour l'arabe)"""
    if language == "ar":
        st.markdown(f'<div class="arabic-text">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(text)

# ==================== INTERFACE STREAMLIT ====================

# Header personnalisé
st.markdown('<div class="main-header">🚨 Tsunami AI Expert</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Système Expert Multilingue • Génération d\'Images • Réponses Intelligentes</div>', unsafe_allow_html=True)

# Sidebar moderne
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    st.markdown("### 🌍 Sélection de la Langue")
    selected_language = st.radio("", list(LANGUAGES.keys()))
    current_lang = LANGUAGES[selected_language]
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 🎯 Questions Rapides")
    
    quick_questions = {
        "fr": [
            "Image définition tsunami",
            "Diagramme causes tsunami", 
            "Illustration conséquences",
            "Schéma sécurité tsunami"
        ],
        "en": [
            "Tsunami definition image",
            "Tsunami causes diagram",
            "Consequences illustration", 
            "Tsunami safety schema"
        ],
        "ar": [
            "صورة تعريف التسونامي",
            "مخطط أسباب التسونامي",
            "رسم عواقب التسونامي",
            "رسم سلامة التسونامي"
        ]
    }
    
    for question in quick_questions[current_lang]:
        if st.button(question, key=f"btn_{question}"):
            st.session_state.auto_question = question
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="emergency-box">', unsafe_allow_html=True)
    st.markdown("### 🚨 URGENCE")
    st.markdown("**Éloignez-vous du rivage IMMÉDIATEMENT!**")
    st.markdown("112 • 911 • 999")
    st.markdown("</div>", unsafe_allow_html=True)

# Zone de chat principale
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Historique de conversation
if "messages" not in st.session_state:
    welcome_messages = {
        "fr": "🤖 **Bienvenue!** Je suis votre expert Tsunami. Demandez-moi des informations ou générez des images éducatives en utilisant des mots comme 'image', 'diagramme' ou 'illustration'.",
        "en": "🤖 **Welcome!** I'm your Tsunami expert. Ask me for information or generate educational images using words like 'image', 'diagram' or 'illustration'.",
        "ar": "🤖 **أهلاً وسهلاً!** أنا خبير التسونامي الخاص بك. اسألني عن المعلومات أو أنشئ صورًا تعليمية باستخدام كلمات مثل 'صورة' أو 'مخطط' أو 'رسم'."
    }
    st.session_state.messages = [
        {"role": "assistant", "content": welcome_messages[current_lang], "image_data": None, "category": None}
    ]

# Affichage de l'historique
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        display_text_with_direction(message["content"], current_lang)
        
        if message.get("image_data"):
            captions = {
                "definition": {"fr": "Diagramme explicatif du tsunami", "en": "Tsunami explanatory diagram", "ar": "مخطط توضيحي للتسونامي"},
                "causes": {"fr": "Illustration des causes du tsunami", "en": "Tsunami causes illustration", "ar": "رسم توضيحي لأسباب التسونامي"},
                "consequences": {"fr": "Impacts et conséquences du tsunami", "en": "Tsunami impacts and consequences", "ar": "تأثيرات وعواقب التسونامي"},
                "safety": {"fr": "Règles de sécurité tsunami", "en": "Tsunami safety rules", "ar": "قواعد سلامة التسونامي"}
            }
            
            caption = captions.get(message.get("category", ""), {}).get(current_lang, "Illustration éducative")
            display_base64_image(message["image_data"], caption)

# Gestion des questions automatiques
if "auto_question" in st.session_state:
    prompt = st.session_state.auto_question
    del st.session_state.auto_question
else:
    prompt = None

# Input utilisateur
if prompt or (user_input := st.chat_input("💬 Tapez votre question ou 'image' pour générer...")):
    
    if not prompt:
        prompt = user_input
    
    # Ajout du message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt, "image_data": None, "category": None})
    
    # Simulation de chargement
    with st.spinner("🎨 Génération de l'image et de la réponse..."):
        time.sleep(0.5)
        
        # Recherche intelligente
        response, image_data, category = find_best_response(prompt, current_lang)
        
        # Ajout de la réponse
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response,
            "image_data": image_data,
            "category": category
        })
        
        # Rechargement
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Footer informatif
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🎯 Mots-clés Images**")
    st.markdown("image • diagramme • illustration • schéma")
with col2:
    st.markdown("**🌍 Multilingue**") 
    st.markdown("Français • English • العربية")
with col3:
    st.markdown("**🖼️ Génération auto**")
    st.markdown("Images éducatives • Temps réel")
