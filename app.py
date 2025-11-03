import streamlit as st
import random
import base64
from PIL import Image, ImageDraw
import io
import time

# Configuration de la page
st.set_page_config(
    page_title="🌊 Tsunami Expert", 
    page_icon="🌊", 
    layout="wide"
)

# ==================== STYLE MODERNE ====================
st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .chat-container {
        background: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .sidebar-content {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        margin: 12px 0;
        border-left: 4px solid #1e88e5;
    }
    .emergency-box {
        background: linear-gradient(135deg, #ff5252, #d32f2f);
        color: white;
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
    }
    .question-btn {
        background: linear-gradient(135deg, #4caf50, #2e7d32);
        color: white;
        border: none;
        padding: 12px 18px;
        border-radius: 10px;
        margin: 6px 0;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s;
        font-weight: 600;
        font-size: 0.9em;
        text-align: left;
    }
    .question-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(76,175,80,0.3);
    }
    .arabic-text {
        direction: rtl;
        text-align: right;
        line-height: 1.8;
        font-size: 1.05em;
    }
    .category-header {
        color: #1e88e5;
        border-bottom: 2px solid #1e88e5;
        padding-bottom: 8px;
        margin-top: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==================== SYSTÈME MULTILINGUE ====================

LANGUAGES = {
    "🇫🇷 Français": "fr",
    "🇬🇧 English": "en", 
    "🇸🇦 العربية": "ar"
}

# ==================== BASE DE CONNAISSANCES COMPLÈTE ET CORRIGÉE ====================

KNOWLEDGE_BASE = {
    "effets_long_terme": {
        "keywords": {
            "fr": ["effets à long terme", "effets long terme", "conséquences long terme", "impact long terme", "populations touchées"],
            "en": ["long term effects", "long-term effects", "long term consequences", "long-term impact", "affected populations"],
            "ar": ["الآثار طويلة المدى", "عواقب طويلة المدى", "تأثير طويل المدى", "المتضررين", "السكان المتأثرين"]
        },
        "responses": {
            "fr": """
**🌊 EFFETS À LONG TERME SUR LES POPULATIONS TOUCHÉES**

**SANTÉ MENTALE :**
• **SSPT** : 60-70% des survivants développent un trouble de stress post-traumatique
• **Dépression** : Taux 3 fois plus élevé que la normale
• **Anxiété chronique** : Particulièrement lors d'alertes météo
• **Deuil compliqué** : Difficulté à faire le deuil des disparus

**SANTÉ PHYSIQUE :**
• **Maladies chroniques** : Problèmes respiratoires dus aux moisissures
• **Handicaps permanents** : Blessures non traitées correctement
• **Problèmes de santé reproductive** : Stress affectant la fertilité

**IMPACT ÉCONOMIQUE :**
• **Pauvreté durable** : Perte de moyens de subsistance
• **Chômage prolongé** : Destruction des entreprises locales
• **Dettes importantes** : Reconstruction sans assurances adequates

**DÉPLACEMENTS PERMANENTS :**
• **Relocalisation** : Communautés dispersées
• **Perte du patrimoine** : Sites culturels et historiques détruits
• **Changements démographiques** : Jeunes quittant les zones touchées

**RÉSILIENCE COMMUNAUTAIRE :**
• **Renforcement des liens** : Solidarité accrue dans certaines communautés
• **Systèmes d'alerte améliorés** : Meilleure préparation aux futurs risques
• **Reconstruction plus sûre** : Normes de construction renforcées
            """,
            "en": """
**🌊 LONG-TERM EFFECTS ON AFFECTED POPULATIONS**

**MENTAL HEALTH:**
• **PTSD**: 60-70% of survivors develop post-traumatic stress disorder
• **Depression**: Rates 3 times higher than normal
• **Chronic anxiety**: Especially during weather alerts
• **Complicated grief**: Difficulty mourning the missing

**PHYSICAL HEALTH:**
• **Chronic diseases**: Respiratory problems due to mold
• **Permanent disabilities**: Injuries not properly treated
• **Reproductive health issues**: Stress affecting fertility

**ECONOMIC IMPACT:**
• **Lasting poverty**: Loss of livelihoods
• **Prolonged unemployment**: Destruction of local businesses
• **Significant debt**: Reconstruction without adequate insurance

**PERMANENT DISPLACEMENT:**
• **Relocation**: Dispersed communities
• **Loss of heritage**: Destroyed cultural and historical sites
• **Demographic changes**: Young people leaving affected areas

**COMMUNITY RESILIENCE:**
• **Strengthened bonds**: Increased solidarity in some communities
• **Improved warning systems**: Better preparation for future risks
• **Safer reconstruction**: Strengthened building standards
            """,
            "ar": """
**🌊 الآثار طويلة المدى على السكان المتضررين**

**الصحة النفسية:**
• **اضطراب ما بعد الصدمة**: 60-70% من الناجين يصابون باضطراب ما بعد الصدمة
• **الاكتئاب**: معدلات أعلى بثلاث مرات من الطبيعي
• **القلق المزمن**: خاصة أثناء تنبيهات الطقس
• **حزن معقد**: صعوبة في حداد المفقودين

**الصحة البدنية:**
• **أمراض مزمنة**: مشاكل تنفسية due to mold
• **إعاقات دائمة**: إصابات لم تعالج بشكل صحيح
• **مشاكل الصحة الإنجابية**: الإجهاد يؤثر على الخصوبة

**التأثير الاقتصادي:**
• **فقر دائم**: فقدان سبل العيش
• **بطالة مطولة**: تدمير الشركات المحلية
• **ديون كبيرة**: إعادة بناء without adequate insurance

**النزوح الدائم:**
• **إعادة التوطين**: مجتمعات مشتتة
• **فقدان التراث**: مواقع ثقافية وتاريخية مدمرة
• **تغيرات ديموغرافية**: شباب يغادرون المناطق المتضررة

**مرونة المجتمع:**
• **تعزيز الروابط**: تضامن متزايد في بعض المجتمعات
• **أنظمة إنذار محسنة**: استعداد أفضل للمخاطر المستقبلية
• **إعادة بناء أكثر أمانًا**: معايير بناء معززة
            """
        }
    },

    "mortalite_moyenne": {
        "keywords": {
            "fr": ["mortalité moyenne", "moyenne morts", "combien meurent", "nombre morts", "victimes moyenne"],
            "en": ["average mortality", "average deaths", "how many die", "number of deaths", "average victims"],
            "ar": ["متوسط الوفيات", "متوسط الوفيات", "كم يموت", "عدد الوفيات", "ضحايا متوسط"]
        },
        "responses": {
            "fr": """
**🌊 MORTALITÉ MOYENNE LORS DES TSUNAMIS**

**STATISTIQUES GLOBALES :**
• **Moyenne historique** : 500-2,000 morts par tsunami majeur
• **Variabilité extrême** : De 0 à 280,000 morts
• **Facteur principal** : Densité population côtière + système d'alerte

**TSUNANIS LES PLUS MEURTRIERS :**

**1. OCÉAN INDIEN 2004**
• **Morts** : 230,000 - 280,000
• **Pays** : Indonésie, Sri Lanka, Inde, Thaïlande
• **Cause** : Absence système d'alerte

**2. JAPON 2011**
• **Morts** : 15,897 confirmés
• **Disparus** : 2,533
• **Cause principale** : Tsunami (92% des morts)

**3. MESSINE 1908**
• **Morts** : 80,000 - 100,000
• **Lieu** : Italie
• **Cause** : Séisme + tsunami

**FACTEURS INFLUENÇANT LA MORTALITÉ :**

**1. HEURE DE LA JOURNÉE**
• **Nuit** : +300% mortalité (difficulté évacuation)
• **Saison touristique** : Population multipliée

**2. SYSTÈME D'ALERTE**
• **Avec alerte** : Réduction 50-80% mortalité
• **Sans alerte** : Catastrophes massives

**3. TOPOGRAPHIE CÔTIÈRE**
• **Plates** : Zones inondables étendues
• **Falaises** : Protection naturelle

**TENDANCE MODERNE :**
• **Diminution mortalité** : Grâce aux systèmes d'alerte
• **Augmentation coûts** : Croissance zones côtières
            """,
            "en": """
**🌊 AVERAGE MORTALITY IN TSUNAMIS**

**GLOBAL STATISTICS:**
• **Historical average**: 500-2,000 deaths per major tsunami
• **Extreme variability**: From 0 to 280,000 deaths
• **Main factor**: Coastal population density + warning system

**DEADLIEST TSUNAMIS:**

**1. INDIAN OCEAN 2004**
• **Deaths**: 230,000 - 280,000
• **Countries**: Indonesia, Sri Lanka, India, Thailand
• **Cause**: Lack of warning system

**2. JAPAN 2011**
• **Deaths**: 15,897 confirmed
• **Missing**: 2,533
• **Main cause**: Tsunami (92% of deaths)

**3. MESSINA 1908**
• **Deaths**: 80,000 - 100,000
• **Location**: Italy
• **Cause**: Earthquake + tsunami

**FACTORS INFLUENCING MORTALITY:**

**1. TIME OF DAY**
• **Night**: +300% mortality (evacuation difficulty)
• **Tourist season**: Multiplied population

**2. WARNING SYSTEM**
• **With warning**: 50-80% mortality reduction
• **Without warning**: Massive disasters

**3. COASTAL TOPOGRAPHY**
• **Flat**: Extensive floodable areas
• **Cliffs**: Natural protection

**MODERN TREND:**
• **Decreasing mortality**: Thanks to warning systems
• **Increasing costs**: Coastal zone growth
            """,
            "ar": """
**🌊 متوسط الوفيات في التسونامي**

**الإحصائيات العالمية:**
• **المتوسط التاريخي**: 500-2,000 قتيل لكل تسونامي رئيسي
• **تغيرية شديدة**: من 0 إلى 280,000 قتيل
• **العامل الرئيسي**: كثافة السكان الساحليين + نظام الإنذار

**أخطر التسوناميات:**

**1. المحيط الهندي 2004**
• **الوفيات**: 230,000 - 280,000
• **الدول**: إندونيسيا، سريلانكا، الهند، تايلاند
• **السبب**: عدم وجود نظام إنذار

**2. اليابان 2011**
• **الوفيات**: 15,897 مؤكد
• **مفقودون**: 2,533
• **السبب الرئيسي**: التسونامي (92% من الوفيات)

**3. ميسينا 1908**
• **الوفيات**: 80,000 - 100,000
• **الموقع**: إيطاليا
• **السبب**: زلزال + تسونامي

**العوامل المؤثرة على الوفيات:**

**1. وقت اليوم**
• **الليل**: +300% وفيات (صعوبة الإخلاء)
• **موسم السياحة**: تضاعف السكان

**2. نظام الإنذار**
• **مع إنذار**: تخفيض 50-80% في الوفيات
• **بدون إنذار**: كوارث ضخمة

**3. تضاريس الساحل**
• **مسطحة**: مناطق قابلة للفيضان واسعة
• **منحدرات**: حماية طبيعية

**الاتجاه الحديث:**
• **انخفاض الوفيات**: بفضل أنظمة الإنذار
• **زيادة التكاليف**: نمو المناطق الساحلية
            """
        }
    },

    "definition_tsunami": {
        "keywords": {
            "fr": ["qu'est ce qu'un tsunami", "définition tsunami", "définition d'un tsunami", "c'est quoi un tsunami", "tsunami définition"],
            "en": ["what is a tsunami", "tsunami definition", "definition of tsunami", "what's a tsunami"],
            "ar": ["ما هو التسونامي", "تعريف التسونامي", "ماهو التسونامي", "تعريف تسونامي"]
        },
        "responses": {
            "fr": """
**🌊 QU'EST-CE QU'UN TSUNAMI ?**

**DÉFINITION :**
Un tsunami est une série de vagues océaniques extrêmement longues et puissantes, générées par des perturbations soudaines du fond marin. Contrairement aux vagues normales créées par le vent, les tsunamis transportent une énergie colossale sur de grandes distances.

**CARACTÉRISTIQUES PRINCIPALES :**

**• Longueur d'onde** : 100-300 km (vs 100-200 m pour vagues normales)
**• Période** : 10-60 minutes entre les vagues
**• Vitesse** : 500-800 km/h en eau profonde
**• Amplitude** : Faible en mer (quelques cm), énorme près des côtes

**ÉTYMOLOGIE :**
Mot japonais : "tsu" (port) + "nami" (vague) = "vague de port"
            """,
            "en": """
**🌊 WHAT IS A TSUNAMI?**

**DEFINITION:**
A tsunami is a series of extremely long and powerful ocean waves generated by sudden disturbances of the seabed. Unlike normal waves created by wind, tsunamis carry colossal energy over great distances.

**MAIN CHARACTERISTICS:**

**• Wavelength**: 100-300 km (vs 100-200 m for normal waves)
**• Period**: 10-60 minutes between waves
**• Speed**: 500-800 km/h in deep water
**• Amplitude**: Low at sea (few cm), huge near coasts

**ETYMOLOGY:**
Japanese word: "tsu" (harbor) + "nami" (wave) = "harbor wave"
            """,
            "ar": """
**🌊 ما هو التسونامي؟**

**التعريف:**
التسونامي هو سلسلة من أمواج المحيط الطويلة والقوية بشكل استثنائي، generated by sudden disturbances of the seabed. على عكس الأمواج العادية الناتجة عن الرياح، يحمل التسونامي طاقة هائلة عبر مسافات كبيرة.

**الخصائص الرئيسية:**

**• الطول الموجي**: 100-300 كم (مقابل 100-200 م للأمواج العادية)
**• الفترة**: 10-60 دقيقة بين الأمواج
**• السرعة**: 500-800 كم/ساعة في المياه العميقة
**• السعة**: منخفضة في البحر (بضعة سم)، هائلة بالقرب من السواحل

**أصل الكلمة:**
كلمة يابانية: "تسو" (ميناء) + "نامي" (موجة) = "موجة الميناء"
            """
        }
    },

    "causes_principales": {
        "keywords": {
            "fr": ["causes principales", "causes tsunamis", "origine tsunamis", "quoi cause tsunami", "quelles causes"],
            "en": ["main causes", "tsunami causes", "what causes tsunami", "origin tsunami", "what causes"],
            "ar": ["الأسباب الرئيسية", "أسباب التسونامي", "ماذا يسبب التسونامي", "أصل التسونامي", "ما الأسباب"]
        },
        "responses": {
            "fr": """
**🌊 CAUSES PRINCIPALES DES TSUNAMIS**

**1. SÉISMES SOUS-MARINS (88%)**
• **Magnitude** : ≥ 7.0 généralement
• **Type** : Subduction (mouvement vertical du fond marin)
• **Exemple** : Japon 2011 (magnitude 9.0)

**2. GLISSEMENTS DE TERRAIN (7%)**
• **Lieux** : Fjords, volcans, pentes raides
• **Volume** : Millions de m³ nécessaires
• **Exemple** : Baie Lituya 1958 (524m vague)

**3. ÉRUPTIONS VOLCANIQUES (5%)**
• **Mécanismes** : Effondrement, explosion, pyroclastiques
• **Exemple** : Krakatoa 1883 (vagues 40m)

**4. IMPACTS MÉTÉORITIQUES (rare)**
• **Diamètre** : > 1km nécessaire
• **Énergie** : Équivalent millions bombes atomiques

**AUTRES CAUSES :**
• **Effondrements glaciers**
• **Explosions nucléaires** (théorique)
            """,
            "en": """
**🌊 MAIN TSUNAMI CAUSES**

**1. UNDERSEA EARTHQUAKES (88%)**
• **Magnitude**: ≥ 7.0 generally
• **Type**: Subduction (vertical seabed movement)
• **Example**: Japan 2011 (magnitude 9.0)

**2. LANDSLIDES (7%)**
• **Locations**: Fjords, volcanoes, steep slopes
• **Volume**: Millions of m³ required
• **Example**: Lituya Bay 1958 (524m wave)

**3. VOLCANIC ERUPTIONS (5%)**
• **Mechanisms**: Collapse, explosion, pyroclastic flows
• **Example**: Krakatoa 1883 (40m waves)

**4. METEORITE IMPACTS (rare)**
• **Diameter**: > 1km required
• **Energy**: Equivalent millions atomic bombs

**OTHER CAUSES:**
• **Glacier collapses**
• **Nuclear explosions** (theoretical)
            """,
            "ar": """
**🌊 الأسباب الرئيسية للتسونامي**

**1. الزلازل تحت البحر (88%)**
• **القوة**: ≥ 7.0 عادة
• **النوع**: اندساس (حركة رأسية لقاع البحر)
• **مثال**: اليابان 2011 (قوة 9.0)

**2. الانهيارات الأرضية (7%)**
• **المواقع**: المضايق، البراكين، المنحدرات الشديدة
• **الحجم**: ملايين الأمتار المكعبة مطلوبة
• **مثال**: خليج ليتويا 1958 (موجة 524م)

**3. الثورات البركانية (5%)**
• **الآليات**: الانهيار، الانفجار، تدفقات pyroclastic
• **مثال**: كراكاتوا 1883 (أمواج 40م)

**4. اصطدام النيازك (نادر)**
• **القطر**: > 1كم مطلوب
• **الطاقة**: تعادل ملايين القنابل الذرية

**أسباب أخرى:**
• **انهيارات الجليد**
• **الانفجارات النووية** (نظري)
            """
        }
    }
}

# ==================== FONCTION DE RECHERCHE AMÉLIORÉE ====================

def find_response(user_input, language):
    """Trouve la réponse la plus pertinente avec reconnaissance améliorée"""
    user_input_lower = user_input.lower().strip()
    
    # Nettoyer l'entrée utilisateur
    import re
    user_input_clean = re.sub(r'[^\w\s]', '', user_input_lower)
    
    # Recherche améliorée avec pondération
    best_match = None
    best_score = 0
    
    for category, data in KNOWLEDGE_BASE.items():
        score = 0
        keywords = data["keywords"][language]
        
        # Vérifier chaque mot-clé
        for keyword in keywords:
            # Correspondance exacte du mot-clé
            if keyword in user_input_clean:
                score += 3
            # Correspondance partielle
            elif any(word in user_input_clean for word in keyword.split()):
                score += 1
        
        # Vérifier les mots individuels
        user_words = user_input_clean.split()
        for word in user_words:
            if any(word in keyword for keyword in keywords):
                score += 1
            if any(keyword in word for keyword in keywords):
                score += 1
        
        if score > best_score:
            best_score = score
            best_match = category
    
    # Seuil minimum pour éviter les mauvaises correspondances
    if best_score >= 2:
        return KNOWLEDGE_BASE[best_match]["responses"][language]
    
    # Réponse par défaut avec suggestions
    default_responses = {
        "fr": """
🤖 **Expert Tsunami** - Je n'ai pas trouvé de réponse précise à votre question. 

**Questions que je peux traiter :**
• Effets à long terme sur les populations
• Mortalité moyenne lors des tsunamis  
• Définition et causes des tsunamis
• Différence avec les vagues normales
• Systèmes de détection et prévention

Utilisez les boutons sur le côté ou reformulez votre question !
        """,
        "en": """
🤖 **Tsunami Expert** - I didn't find a precise answer to your question.

**Questions I can handle:**
• Long-term effects on populations
• Average tsunami mortality
• Definition and causes of tsunamis
• Difference with normal waves
• Detection and prevention systems

Use the buttons on the side or rephrase your question!
        """,
        "ar": """
🤖 **خبير التسونامي** - لم أجد إجابة دقيقة لسؤالك.

**الأسئلة التي يمكنني معالجتها:**
• الآثار طويلة المدى على السكان
• متوسط وفيات التسونامي
• تعريف وأسباب التسونامي
• الفرق مع الأمواج العادية
• أنظمة الكشف والوقاية

استخدم الأزرار على الجانب أو أعد صياغة سؤالك!
        """
    }
    return default_responses[language]

def display_text(text, language):
    """Affiche le texte avec la bonne direction"""
    if language == "ar":
        st.markdown(f'<div class="arabic-text">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(text)

# ==================== INTERFACE COMPLÈTE ====================

# Titre
st.markdown('<div class="main-header">🌊 Expert Tsunami</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🌍 Langue")
    selected_language = st.radio("", list(LANGUAGES.keys()), label_visibility="collapsed")
    current_lang = LANGUAGES[selected_language]
    
    # Toutes les catégories de questions
    categories = {
        "fr": {
            "definition": "📚 Définition et Causes",
            "consequences": "💥 Conséquences", 
            "historique": "📅 Exemples Historiques",
            "prevention": "🛡️ Prévention et Solutions",
            "science": "🔬 Science et Géographie",
            "curiosites": "🔍 Curiosités et Études"
        },
        "en": {
            "definition": "📚 Definition and Causes",
            "consequences": "💥 Consequences",
            "historique": "📅 Historical Examples", 
            "prevention": "🛡️ Prevention and Solutions",
            "science": "🔬 Science and Geography",
            "curiosites": "🔍 Curiosities and Studies"
        },
        "ar": {
            "definition": "📚 التعريف والأسباب",
            "consequences": "💥 العواقب",
            "historique": "📅 أمثلة تاريخية",
            "prevention": "🛡️ الوقاية والحلول", 
            "science": "🔬 العلم والجغرافيا",
            "curiosites": "🔍 فضوليات ودراسات"
        }
    }
    
    # Toutes les questions organisées par catégorie
    questions_by_category = {
        "consequences": {
            "fr": [
                "Effets à long terme sur les populations touchées",
                "Mortalité moyenne lors des tsunamis"
            ],
            "en": [
                "Long-term effects on affected populations",
                "Average mortality in tsunamis"
            ],
            "ar": [
                "الآثار طويلة المدى على السكان المتضررين",
                "متوسط الوفيات في التسونامي"
            ]
        },
        "definition": {
            "fr": [
                "Qu'est-ce qu'un tsunami ?",
                "Causes principales des tsunamis"
            ],
            "en": [
                "What is a tsunami?",
                "Main causes of tsunamis"
            ],
            "ar": [
                "ما هو التسونامي؟",
                "الأسباب الرئيسية للتسونامي"
            ]
        }
    }
    
    # Affichage de toutes les catégories
    for category_key, category_name in categories[current_lang].items():
        if category_key in questions_by_category:
            st.markdown(f'<div class="category-header">{category_name}</div>', unsafe_allow_html=True)
            for question in questions_by_category[category_key][current_lang]:
                if st.button(question, key=f"{category_key}_{question}"):
                    st.session_state.auto_question = question
    
    st.markdown("---")
    st.markdown("### 🚨 Urgence")
    emergency_text = {
        "fr": "**Éloignement immédiat**\n\n**112 • 911 • 999**\n\nEn cas de séisme côtier ou retrait de la mer, évacuez immédiatement vers les hauteurs !",
        "en": "**Immediate evacuation**\n\n**112 • 911 • 999**\n\nDuring coastal earthquake or sea retreat, evacuate immediately to high ground!",
        "ar": "**إخلاء فوري**\n\n**112 • 911 • 999**\n\nأثناء الزلزال الساحلي أو انسحاب البحر، اخل فورًا إلى المرتفعات!"
    }
    st.markdown(f'<div class="emergency-box">{emergency_text[current_lang]}</div>', unsafe_allow_html=True)

# Zone de chat principale
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Historique de conversation
if "messages" not in st.session_state:
    welcome_messages = {
        "fr": "🌊 **Expert Tsunami** - Je peux répondre à vos questions sur les effets à long terme, la mortalité moyenne, les causes et définitions des tsunamis. Utilisez les boutons ou tapez vos questions !",
        "en": "🌊 **Tsunami Expert** - I can answer your questions about long-term effects, average mortality, causes and definitions of tsunamis. Use buttons or type your questions!", 
        "ar": "🌊 **خبير التسونامي** - يمكنني الإجابة على أسئلتك حول الآثار طويلة المدى، متوسط الوفيات، أسباب وتعريفات التسونامي. استخدم الأزرار أو اكتب أسئلتك!"
    }
    st.session_state.messages = [
        {"role": "assistant", "content": welcome_messages[current_lang]}
    ]

# Affichage de l'historique des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        display_text(message["content"], current_lang)

# Gestion des questions automatiques depuis les boutons
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
    
    with st.chat_message("user"):
        display_text(prompt, current_lang)
    
    # Génération de la réponse
    with st.chat_message("assistant"):
        with st.spinner("Recherche de la réponse..."):
            response = find_response(prompt, current_lang)
            display_text(response, current_lang)
    
    # Ajout de la réponse à l'historique
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response
    })

st.markdown('</div>', unsafe_allow_html=True)

# Pied de page
st.markdown("---")
footer_text = {
    "fr": "🌊 **Expert Tsunami** - Application éducative créée pour informer et sensibiliser sur les risques de tsunamis. Les informations fournies sont à but éducatif uniquement.",
    "en": "🌊 **Tsunami Expert** - Educational application created to inform and raise awareness about tsunami risks. Provided information is for educational purposes only.",
    "ar": "🌊 **خبير التسونامي** - تطبيق تعليمي تم إنشاؤه لإعلام والتوعية بمخاطر التسونامي. المعلومات المقدمة لأغراض تعليمية فقط."
}
st.markdown(f'<div style="text-align: center; color: #666; font-size: 0.9em;">{footer_text[current_lang]}</div>', unsafe_allow_html=True)
