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

# ==================== BASE DE CONNAISSANCES COMPLÈTE ====================

KNOWLEDGE_BASE = {
    # ... (toutes les entrées précédentes restent les mêmes jusqu'à "vague_plus_haute")
    
    "vague_plus_haute": {
        "keywords": {
            "fr": ["vague plus haute", "record hauteur", "plus haute vague", "vague maximale"],
            "en": ["highest wave", "height record", "highest wave", "maximum wave"],
            "ar": ["أعلى موجة", "رقم قياسي ارتفاع", "أعلى موجة", "الموجة القصوى"]
        },
        "responses": {
            "fr": """
**🌊 RECORDS DE HAUTEUR DE VAGUES DE TSUNAMI**

**RECORD ABSOLU : BAIE LITUYA 1958**

**Caractéristiques :**
- **Hauteur** : 524 mètres (1,720 pieds)
- **Lieu** : Alaska, États-Unis
- **Cause** : Glissement terrain massif (30 millions m³)
- **Mécanisme** : Roche tombant dans fjord étroit

**Détails :**
- **Énergie** : Équivalent 30 millions tonnes TNT
- **Survivants** : 2 bateaux (miraculeusement)
- **Forêt** : Arbres arrachés jusqu'à 524m d'altitude

**AUTRES RECORDS NOTABLES :**

**1. JAPON 2011**
- **Hauteur** : 40.5 mètres
- **Lieu** : Miyako, Iwate
- **Cause** : Séisme magnitude 9.0

**2. INDONÉSIE 2004**
- **Hauteur** : 30 mètres
- **Lieu** : Banda Aceh
- **Cause** : Séisme magnitude 9.1

**3. ALASKA 1964**
- **Hauteur** : 67 mètres
- **Lieu** : Valdez Inlet
- **Cause** : Séisme magnitude 9.2
            """,
            "en": """
**🌊 TSUNAMI WAVE HEIGHT RECORDS**

**ABSOLUTE RECORD: LITUYA BAY 1958**

**Characteristics:**
- **Height**: 524 meters (1,720 feet)
- **Location**: Alaska, USA
- **Cause**: Massive landslide (30 million m³)
- **Mechanism**: Rock falling into narrow fjord

**Details:**
- **Energy**: Equivalent to 30 million tons TNT
- **Survivors**: 2 boats (miraculously)
- **Forest**: Trees uprooted up to 524m altitude

**OTHER NOTABLE RECORDS:**

**1. JAPAN 2011**
- **Height**: 40.5 meters
- **Location**: Miyako, Iwate
- **Cause**: Magnitude 9.0 earthquake

**2. INDONESIA 2004**
- **Height**: 30 meters
- **Location**: Banda Aceh
- **Cause**: Magnitude 9.1 earthquake

**3. ALASKA 1964**
- **Height**: 67 meters
- **Location**: Valdez Inlet
- **Cause**: Magnitude 9.2 earthquake
            """,
            "ar": """
**🌊 أرقام قياسية لارتفاع أمواج التسونامي**

**الرقم القياسي المطلق: خليج ليتويا 1958**

**الخصائص:**
- **الارتفاع**: 524 متر (1,720 قدم)
- **الموقع**: ألاسكا، الولايات المتحدة
- **السبب**: انهيار أرضي هائل (30 مليون م³)
- **الآلية**: صخور تسقط في مضيق ضيق

**التفاصيل:**
- **الطاقة**: تعادل 30 مليون طن من TNT
- **الناجون**: قاربان (بمعجزة)
- **الغابة**: أشجار اقتلعت حتى ارتفاع 524م

**أرقام قياسية أخرى ملحوظة:**

**1. اليابان 2011**
- **الارتفاع**: 40.5 متر
- **الموقع**: مياكو، إواتي
- **السبب**: زلزال قوة 9.0

**2. إندونيسيا 2004**
- **الارتفاع**: 30 متر
- **الموقع**: باندا آتشيه
- **السبب**: زلزال قوة 9.1

**3. ألاسكا 1964**
- **الارتفاع**: 67 متر
- **الموقع**: مضيق فالديز
- **السبب**: زلزال قوة 9.2
            """
        }
    },

    "tsunami_lacs_rivieres": {
        "keywords": {
            "fr": ["lacs", "rivières", "lac tsunami", "rivière tsunami", "eau douce"],
            "en": ["lakes", "rivers", "lake tsunami", "river tsunami", "freshwater"],
            "ar": ["بحيرات", "أنهار", "تسونامي بحيرة", "تسونامي نهر", "ماء عذب"]
        },
        "responses": {
            "fr": """
**🏞️ TSUNAMIS DANS LES LACS ET RIVIÈRES**

**POSSIBILITÉ : OUI, MAIS DIFFÉRENTS**

**CAUSES SPÉCIFIQUES :**

**1. GLISSEMENTS DE TERRAIN**
- **Fjords norvégiens** : Fréquents
- **Lacs alpins** : Instabilité des pentes
- **Exemple** : Lac Léman 563 ap.J-C

**2. EFFONDREMENTS GLACIAIRES**
- **Icebergs** : Vêlage massif
- **Langues glaciaires** : Effondrement soudain
- **Exemple** : Groenland 2017

**3. SÉISMES LACUSTRES**
- **Failles actives** : Sous les lacs
- **Sédiments** : Liquéfaction possible
- **Exemple** : Lac Tahoe (USA)

**CARACTÉRISTIQUES :**

**DIFFÉRENCES AVEC OCEAN :**
- **Échelle réduite** : Mais tout aussi dangereux localement
- **Confinement** : Amplification par résonance
- **Durée** : Oscillations prolongées

**EXEMPLES HISTORIQUES :**

**LAC LÉMAN 563 :**
- **Hauteur vague** : 8-13 mètres
- **Cause** : Glissement terrain Tauredunum
- **Dégâts** : Villages riverains détruits

**FJORD NORVÉGIEN 1934 :**
- **Hauteur** : 62 mètres
- **Cause** : Glissement rocheux
- **Morts** : 40 personnes

**RISQUES ACTUELS :**
- **Lac Léman** : Études en cours
- **Lacs artificiels** : Barrages préoccupants
- **Tourisme** : Populations exposées
            """,
            "en": """
**🏞️ TSUNAMIS IN LAKES AND RIVERS**

**POSSIBILITY: YES, BUT DIFFERENT**

**SPECIFIC CAUSES:**

**1. LANDSLIDES**
- **Norwegian fjords**: Frequent
- **Alpine lakes**: Slope instability
- **Example**: Lake Geneva 563 AD

**2. GLACIAL COLLAPSES**
- **Icebergs**: Massive calving
- **Glacial tongues**: Sudden collapse
- **Example**: Greenland 2017

**3. LACUSTRINE EARTHQUAKES**
- **Active faults**: Under lakes
- **Sediments**: Possible liquefaction
- **Example**: Lake Tahoe (USA)

**CHARACTERISTICS:**

**DIFFERENCES WITH OCEAN:**
- **Reduced scale**: But equally dangerous locally
- **Confinement**: Amplification by resonance
- **Duration**: Prolonged oscillations

**HISTORICAL EXAMPLES:**

**LAKE GENEVA 563:**
- **Wave height**: 8-13 meters
- **Cause**: Tauredunum landslide
- **Damage**: Riverside villages destroyed

**NORWEGIAN FJORD 1934:**
- **Height**: 62 meters
- **Cause**: Rock landslide
- **Deaths**: 40 people

**CURRENT RISKS:**
- **Lake Geneva**: Ongoing studies
- **Artificial lakes**: Concerning dams
- **Tourism**: Exposed populations
            """,
            "ar": """
**🏞️ تسونامي في البحيرات والأنهار**

**الإمكانية: نعم، ولكن مختلفة**

**أسباب محددة:**

**1. الانهيارات الأرضية**
- **المضايق النرويجية**: متكررة
- **البحيرات الجبلية**: عدم استقرار المنحدرات
- **مثال**: بحيرة جنيف 563 م

**2. الانهيارات الجليدية**
- **الجبال الجليدية**: انفصال هائل
- **الألسنة الجليدية**: انهيار مفاجئ
- **مثال**: جرينلاند 2017

**3. زلازل البحيرات**
- **الصدوع النشطة**: تحت البحيرات
- **الرواسب**: تميع محتمل
- **مثال**: بحيرة تاهو (الولايات المتحدة)

**الخصائص:**

**الاختلافات مع المحيط:**
- **نطاق مصغر**: ولكن بنفس الخطورة محليًا
- **الحصر**: تضخيم بالرنين
- **المدة**: تذبذبات مطولة

**أمثلة تاريخية:**

**بحيرة جنيف 563:**
- **ارتفاع الموجة**: 8-13 متر
- **السبب**: انهيار أرضي في توريدونوم
- **الأضرار**: تدمير القرى النهرية

**مضيق نرويجي 1934:**
- **الارتفاع**: 62 متر
- **السبب**: انهيار صخري
- **الوفيات**: 40 شخصًا

**المخاطر الحالية:**
- **بحيرة جنيف**: دراسات مستمرة
- **البحيرات الاصطناعية**: سدود مقلقة
- **السياحة**: سكان معرضون للخطر
            """
        }
    },

    "prevoir_taille_tsunami": {
        "keywords": {
            "fr": ["prévoir taille", "prédire taille", "estimer taille", "prévision taille"],
            "en": ["predict size", "forecast size", "estimate size", "size prediction"],
            "ar": ["التنبؤ بالحجم", "توقع الحجم", "تقدير الحجم", "تنبؤ الحجم"]
        },
        "responses": {
            "fr": """
**📊 PRÉVOIR LA TAILLE D'UN TSUNAMI**

**DIFFICULTÉS MAJEURES :**

**1. VARIABLES MULTIPLES**
- **Magnitude séisme** : Corrélation imprécise
- **Topographie fond marin** : Effets complexes
- **Géographie côtière** : Amplification variable

**2. INCERTITUDES**
- **Mécanisme faille** : Pas toujours connu
- **Glissements secondaires** : Imprévisibles
- **Interaction vagues** : Non linéaire

**MÉTHODES ACTUELLES :**

**1. MODÈLES NUMÉRIQUES**
- **Données sismiques** : Paramètres instantanés
- **Bathymétrie** : Cartes détaillées
- **Simulations** : Scénarios multiples

**2. DONNÉES TEMPS RÉEL**
- **Buoys DART** : Mesures directes
- **Satellites** : Altimétrie océanique
- **Marégraphes** : Confirmation côtière

**PRÉCISION ACTUELLE :**

**HEURE D'ARRIVÉE :**
- **Précision** : ± 5-10 minutes
- **Distance** : Fonction de la propagation

**HAUTEUR DES VAGUES :**
- **Estimation** : ± 30-50% d'erreur
- **Facteurs locaux** : Difficiles à modéliser

**LIMITATIONS :**
- **Premières minutes** : Données limitées
- **Événements complexes** : Multi-sources
- **Extrapolation** : Incertitudes cumulées
            """,
            "en": """
**📊 PREDICTING TSUNAMI SIZE**

**MAJOR DIFFICULTIES:**

**1. MULTIPLE VARIABLES**
- **Earthquake magnitude**: Imprecise correlation
- **Seabed topography**: Complex effects
- **Coastal geography**: Variable amplification

**2. UNCERTAINTIES**
- **Fault mechanism**: Not always known
- **Secondary landslides**: Unpredictable
- **Wave interaction**: Non-linear

**CURRENT METHODS:**

**1. NUMERICAL MODELS**
- **Seismic data**: Instant parameters
- **Bathymetry**: Detailed maps
- **Simulations**: Multiple scenarios

**2. REAL-TIME DATA**
- **DART buoys**: Direct measurements
- **Satellites**: Ocean altimetry
- **Tide gauges**: Coastal confirmation

**CURRENT ACCURACY:**

**ARRIVAL TIME:**
- **Accuracy**: ± 5-10 minutes
- **Distance**: Function of propagation

**WAVE HEIGHT:**
- **Estimation**: ± 30-50% error
- **Local factors**: Difficult to model

**LIMITATIONS:**
- **First minutes**: Limited data
- **Complex events**: Multi-source
- **Extrapolation**: Cumulative uncertainties
            """,
            "ar": """
**📊 التنبؤ بحجم التسونامي**

**صعوبات كبيرة:**

**1. متغيرات متعددة**
- **قوة الزلزال**: ارتباط غير دقيق
- **تضاريس قاع البحر**: تأثيرات معقدة
- **جغرافيا السواحل**: تضخيم متغير

**2. عدم اليقين**
- **آلية الصدع**: غير معروفة دائمًا
- **انهيارات ثانوية**: غير متوقعة
- **تفاعل الأمواج**: غير خطي

**الطرق الحالية:**

**1. النماذج العددية**
- **البيانات الزلزالية**: معلمات فورية
- **قياس الأعماق**: خرائط مفصلة
- **المحاكاة**: سيناريوهات متعددة

**2. بيانات الوقت الحقيقي**
- **عوامات DART**: قياسات مباشرة
- **الأقمار الصناعية**: قياس الارتفاع المحيطي
- **مقاييس المد**: تأكيد ساحلي

**الدقة الحالية:**

**وقت الوصول:**
- **الدقة**: ± 5-10 دقائق
- **المسافة**: دالة الانتشار

**ارتفاع الموجة:**
- **التقدير**: ± 30-50٪ خطأ
- **العوامل المحلية**: صعبة النمذجة

**القيود:**
- **الدقائق الأولى**: بيانات محدودة
- **أحداث معقدة**: متعددة المصادر
- **الاستقراء**: عدم اليقين التراكمي
            """
        }
    },

    "technologies_futures": {
        "keywords": {
            "fr": ["technologies futures", "innovations", "protection future", "nouvelles technologies"],
            "en": ["future technologies", "innovations", "future protection", "new technologies"],
            "ar": ["تقنيات مستقبلية", "ابتكارات", "حماية مستقبلية", "تقنيات جديدة"]
        },
        "responses": {
            "fr": """
**🚀 TECHNOLOGIES FUTURES CONTRE LES TSUNAMIS**

**INNOVATIONS EN DÉVELOPPEMENT :**

**1. SYSTÈMES D'ALERTE AVANCÉS**
- **IA et Machine Learning** : Prédiction améliorée
- **Réseaux de capteurs** : Couverture dense
- **Satellites nouvelle génération** : Surveillance globale

**2. CAPTEURS NOVATEURS**
- **Fibre optique sous-marine** : Détection précoce
- **Radars haute fréquence** : Mesure vagues
- **Drones sous-marins** : Surveillance mobile

**3. PROTECTIONS INNOVANTES**

**STRUCTURES INTELLIGENTES :**
- **Digues adaptatives** : Hauteur variable
- **Portes anti-tsunami** : Fermeture automatique
- **Bâtiments flottants** : Résistance aux inondations

**SOLUTIONS NATURELLES AMPLIFIÉES :**
- **Récifs artificiels** : Conception optimisée
- **Mangroves génétiquement adaptées** : Croissance rapide
- **Systèmes dunes intelligents** : Auto-réparation

**4. COMMUNICATION DU FUTUR**

**ALERTES PERSONNALISÉES :**
- **Géolocalisation précise** : Messages ciblés
- **Réalité augmentée** : Itinéraires d'évacuation visuels
- **IoT grand public** : Appareils connectés

**RÉSEAUX ROBUSTES :**
- **Satellite direct** : Bypass réseaux terrestres
- **Systèmes mesh** : Communication pair-à-pair
- **Batteries longue durée** : Fonctionnement secours

**RECHERCHE PROMETTEUSE :**

**1. MODÉLISATION QUANTIQUE**
- **Calcul haute performance** : Simulations complexes
- **Prévision probabiliste** : Incertitudes quantifiées

**2. MATÉRIAUX NOVATEURS**
- **Métamatériaux** : Déviation des vagues
- **Alliances intelligentes** : Absorption d'énergie
- **Auto-cicatrisation** : Réparation automatique

**3. SYSTÈMES INTÉGRÉS**
- **Villes résilientes** : Conception globale
- **Infrastructures adaptatives** : Réponse dynamique
- **Gestion crise IA** : Coordination optimisée
            """,
            "en": """
**🚀 FUTURE TECHNOLOGIES AGAINST TSUNAMIS**

**INNOVATIONS IN DEVELOPMENT:**

**1. ADVANCED WARNING SYSTEMS**
- **AI and Machine Learning**: Improved prediction
- **Sensor networks**: Dense coverage
- **Next-generation satellites**: Global monitoring

**2. INNOVATIVE SENSORS**
- **Submarine fiber optics**: Early detection
- **High-frequency radars**: Wave measurement
- **Underwater drones**: Mobile surveillance

**3. INNOVATIVE PROTECTIONS**

**SMART STRUCTURES:**
- **Adaptive seawalls**: Variable height
- **Anti-tsunami gates**: Automatic closure
- **Floating buildings**: Flood resistance

**AMPLIFIED NATURAL SOLUTIONS:**
- **Artificial reefs**: Optimized design
- **Genetically adapted mangroves**: Rapid growth
- **Smart dune systems**: Self-repair

**4. FUTURE COMMUNICATION**

**PERSONALIZED ALERTS:**
- **Precise geolocation**: Targeted messages
- **Augmented reality**: Visual evacuation routes
- **Consumer IoT**: Connected devices

**ROBUST NETWORKS:**
- **Direct satellite**: Bypass ground networks
- **Mesh systems**: Peer-to-peer communication
- **Long-lasting batteries**: Backup operation

**PROMISING RESEARCH:**

**1. QUANTUM MODELING**
- **High-performance computing**: Complex simulations
- **Probabilistic forecasting**: Quantified uncertainties

**2. INNOVATIVE MATERIALS**
- **Metamaterials**: Wave deflection
- **Smart alloys**: Energy absorption
- **Self-healing**: Automatic repair

**3. INTEGRATED SYSTEMS**
- **Resilient cities**: Global design
- **Adaptive infrastructure**: Dynamic response
- **AI crisis management**: Optimized coordination
            """,
            "ar": """
**🚀 تقنيات مستقبلية ضد التسونامي**

**ابتكارات قيد التطوير:**

**1. أنظمة إنذار متقدمة**
- **الذكاء الاصطناعي والتعلم الآلي**: تنبؤ محسن
- **شبكات المستشعرات**: تغطية كثيفة
- **أقمار صناعية الجيل التالي**: مراقبة عالمية

**2. مستشعرات مبتكرة**
- **الألياف البصرية تحت البحر**: كشف مبكر
- **رادارات عالية التردد**: قياس الأمواج
- **طائرات بدون طيار تحت الماء**: مراقبة متنقلة

**3. حمايات مبتكرة**

**هياكل ذكية:**
- **أسوار بحرية متكيفة**: ارتفاع متغير
- **بوابات مضادة للتسونامي**: إغلاق تلقائي
- **مباني عائمة**: مقاومة الفيضانات

**حلول طبيعية معززة:**
- **شعاب مرجانية اصطناعية**: تصميم مُحسَّن
- **أشجار مانغروف متكيفة وراثيًا**: نمو سريع
- **أنظمة كثبان ذكية**: إصلاح ذاتي

**4. اتصالات المستقبل**

**تنبيهات مخصصة:**
- **تحديد جغرافي دقيق**: رسائل مستهدفة
- **الواقع المعزز**: طرق إخلاء بصرية
- **إنترنت الأشياء للمستهلكين**: أجهزة متصلة

**شبكات قوية:**
- **قمر صناعي مباشر**: تجاوز الشبكات الأرضية
- **أنظمة شبكية**: اتصال نظير إلى نظير
- **بطاريات طويلة الأمد**: تشغيل احتياطي

**بحث واعد:**

**1. النمذجة الكمية**
- **الحوسبة عالية الأداء**: محاكاة معقدة
- **التنبؤ الاحتمالي**: عدم اليقين المُقَدَّر

**2. مواد مبتكرة**
- **ما بعد المواد**: انحراف الموجة
- **سبائك ذكية**: امتصاص الطاقة
- **الشفاء الذاتي**: إصلاح تلقائي

**3. أنظمة متكاملة**
- **مدن مرنة**: تصميم شامل
- **بنية تحتية متكيفة**: استجابة ديناميكية
- **إدارة الأزمات بالذكاء الاصطناعي**: تنسيق مُحسَّن
            """
        }
    }
}

# ==================== FONCTION DE RECHERCHE AMÉLIORÉE ====================

def find_response(user_input, language):
    """Trouve la réponse la plus pertinente avec reconnaissance améliorée"""
    user_input_lower = user_input.lower()
    
    # Recherche améliorée - vérifie chaque mot-clé individuellement
    best_match = None
    best_score = 0
    
    for category, data in KNOWLEDGE_BASE.items():
        score = 0
        for keyword in data["keywords"][language]:
            if keyword in user_input_lower:
                score += 1
        
        if score > best_score:
            best_score = score
            best_match = category
    
    # Si on a trouvé une bonne correspondance
    if best_score >= 1:
        return KNOWLEDGE_BASE[best_match]["responses"][language]
    
    # Recherche de secours avec mots individuels
    for category, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"][language]:
            # Vérifie si des mots individuels correspondent
            words = user_input_lower.split()
            for word in words:
                if word in keyword or keyword in word:
                    return data["responses"][language]
    
    # Réponse par défaut
    default_responses = {
        "fr": "🤖 **Expert Tsunami** - Je n'ai pas compris votre question. Essayez avec : définition, causes, séisme, volcan, conséquences, signes avant-coureurs, protection, ou exemples historiques.",
        "en": "🤖 **Tsunami Expert** - I didn't understand your question. Try with: definition, causes, earthquake, volcano, consequences, warning signs, protection, or historical examples.",
        "ar": "🤖 **خبير التسونامي** - لم أفهم سؤالك. جرب مع: تعريف، أسباب، زلزال، بركان، عواقب، علامات إنذار، حماية، أو أمثلة تاريخية."
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
        "definition": {
            "fr": [
                "Qu'est-ce qu'un tsunami ?",
                "Différence avec vague normale",
                "Causes principales", 
                "Comment un séisme provoque un tsunami",
                "Tsunamis volcaniques et glissements",
                "Signes avant-coureurs"
            ],
            "en": [
                "What is a tsunami?",
                "Difference with normal wave",
                "Main causes",
                "How earthquake causes tsunami", 
                "Volcanic and landslide tsunamis",
                "Warning signs"
            ],
            "ar": [
                "ما هو التسونامي؟",
                "الفرق مع الموجة العادية",
                "الأسباب الرئيسية",
                "كيف يتسبب الزلزال في تسونامي",
                "تسونامي البراكين والانهيارات", 
                "علامات الإنذار"
            ]
        },
        "consequences": {
            "fr": [
                "Conséquences humaines",
                "Impacts économiques",
                "Impact environnement et biodiversité",
                "Exemples de tsunamis dévastateurs",
                "Effets à long terme sur les populations", 
                "Mortalité moyenne lors des tsunamis"
            ],
            "en": [
                "Human consequences",
                "Economic impacts", 
                "Environmental impact and biodiversity",
                "Examples of devastating tsunamis",
                "Long-term effects on populations",
                "Average mortality in tsunamis"
            ],
            "ar": [
                "العواقب البشرية",
                "الآثار الاقتصادية",
                "التأثير البيئي والتنوع البيولوجي", 
                "أمثلة على تسوناميات مدمرة",
                "الآثار طويلة المدى على السكان",
                "متوسط الوفيات في التسونامي"
            ]
        },
        "historique": {
            "fr": [
                "Tsunami de 2004 dans l'océan Indien",
                "Tsunami du Japon en 2011",
                "Tsunamis les plus meurtriers de l'histoire",
                "Pays affectés par des tsunamis célèbres"
            ],
            "en": [
                "2004 Indian Ocean tsunami", 
                "2011 Japan tsunami",
                "Deadliest tsunamis in history",
                "Countries affected by famous tsunamis"
            ],
            "ar": [
                "تسونامي المحيط الهندي 2004",
                "تسونامي اليابان 2011",
                "أخطر التسوناميات في التاريخ", 
                "الدول المتضررة من تسوناميات مشهورة"
            ]
        },
        "prevention": {
            "fr": [
                "Systèmes de détection des tsunamis",
                "Protection au Japon et au Chili",
                "Mesures pour réduire les pertes humaines",
                "Sensibilisation de la population", 
                "Efficacité des digues et barrières",
                "Rôle des alertes précoces et exercices"
            ],
            "en": [
                "Tsunami detection systems",
                "Protection in Japan and Chile", 
                "Measures to reduce human losses",
                "Population awareness",
                "Effectiveness of seawalls and barriers",
                "Role of early warnings and drills"
            ],
            "ar": [
                "أنظمة كشف التسونامي",
                "الحماية في اليابان وتشيلي",
                "إجراءات لتقليل الخسائر البشرية", 
                "توعية السكان",
                "فعالية الأسوار البحرية والحواجز",
                "دور الإنذارات المبكرة والتمارين"
            ]
        },
        "science": {
            "fr": [
                "Zones les plus fréquentes des tsunamis",
                "Profondeur minimale pour la formation",
                "Mouvement des tsunamis dans l'océan",
                "Tsunamis toujours après séisme ?", 
                "Influence de la géographie côtière"
            ],
            "en": [
                "Most frequent tsunami zones",
                "Minimum depth for formation", 
                "Tsunami movement in the ocean",
                "Tsunamis always after earthquake?",
                "Influence of coastal geography"
            ],
            "ar": [
                "أكثر مناطق التسونامي تكرارًا",
                "الحد الأدنى للعمق للتكوين",
                "حركة التسونامي في المحيط", 
                "هل التسونامي دائمًا بعد الزلزال؟",
                "تأثير الجغرافيا الساحلية"
            ]
        },
        "curiosites": {
            "fr": [
                "Temps d'atteinte de la côte",
                "Vague la plus haute enregistrée", 
                "Tsunamis dans lacs ou rivières",
                "Prévoir la taille d'un tsunami",
                "Technologies futures de protection"
            ],
            "en": [
                "Time to reach the coast",
                "Highest recorded wave",
                "Tsunamis in lakes or rivers", 
                "Predicting tsunami size",
                "Future protection technologies"
            ],
            "ar": [
                "وقت الوصول إلى الساحل",
                "أعلى موجة مسجلة",
                "تسونامي في البحيرات أو الأنهار", 
                "التنبؤ بحجم التسونامي",
                "تقنيات الحماية المستقبلية"
            ]
        }
    }
    
    # Affichage de toutes les catégories
    for category_key, category_name in categories[current_lang].items():
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
        "fr": "🌊 **Expert Tsunami** - Je peux répondre à toutes vos questions sur les tsunamis : définition, causes, conséquences, prévention, science et exemples historiques. Utilisez les boutons ou tapez vos questions !",
        "en": "🌊 **Tsunami Expert** - I can answer all your questions about tsunamis: definition, causes, consequences, prevention, science and historical examples. Use buttons or type your questions!", 
        "ar": "🌊 **خبير التسونامي** - يمكنني الإجابة على جميع أسئلتك عن التسونامي: تعريف، أسباب، عواقب، وقاية، علم وأمثلة تاريخية. استخدم الأزرار أو اكتب أسئلتك!"
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
    
    # Génération de la réponse
    response = find_response(prompt, current_lang)
    
    # Ajout de la réponse
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response
    })
    
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Pied de page
st.markdown("---")
footer_text = {
    "fr": "🌊 **Expert Tsunami** - Application éducative créée pour informer et sensibiliser sur les risques de tsunamis. Les informations fournies sont à but éducatif uniquement.",
    "en": "🌊 **Tsunami Expert** - Educational application created to inform and raise awareness about tsunami risks. Provided information is for educational purposes only.",
    "ar": "🌊 **خبير التسونامي** - تطبيق تعليمي تم إنشاؤه لإعلام والتوعية بمخاطر التسونامي. المعلومات المقدمة لأغراض تعليمية فقط."
}
st.markdown(f'<div style="text-align: center; color: #666; font-size: 0.9em;">{footer_text[current_lang]}</div>', unsafe_allow_html=True)
