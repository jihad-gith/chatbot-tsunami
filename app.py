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
    # ========== DÉFINITION ET CAUSES ==========
    "definition_tsunami": {
        "keywords": {
            "fr": ["définition tsunami", "qu'est-ce qu'un tsunami", "c'est quoi un tsunami", "expliquer tsunami"],
            "en": ["tsunami definition", "what is tsunami", "explain tsunami"],
            "ar": ["تعريف تسونامي", "ما هو تسونامي", "شرح تسونامي"]
        },
        "responses": {
            "fr": """
**🌊 DÉFINITION DU TSUNAMI**

Un tsunami est une série de vagues gigantesques provoquées par un déplacement soudain d'eau, souvent à la suite d'un séisme, d'un glissement de terrain ou d'une éruption volcanique sous-marine.

**Caractéristiques principales :**
- **Vitesse** : 500-800 km/h en eau profonde (comme un avion de ligne)
- **Hauteur** : 30 cm à 1m en mer → 10-30m près des côtes
- **Longueur d'onde** : 100-200 km (vs 100m pour une vague normale)
- **Période** : 10-60 minutes entre les vagues successives

**Mécanisme physique :** Le déplacement vertical du fond marin pousse toute la colonne d'eau, créant des ondes qui se propagent dans toutes les directions.
            """,
            "en": """
**🌊 TSUNAMI DEFINITION**

A tsunami is a series of giant waves caused by sudden displacement of water, often following an earthquake, landslide, or underwater volcanic eruption.

**Key characteristics:**
- **Speed**: 500-800 km/h in deep water (like a jet airliner)
- **Height**: 30 cm to 1m at sea → 10-30m near coasts
- **Wavelength**: 100-200 km (vs 100m for normal wave)
- **Period**: 10-60 minutes between successive waves

**Physical mechanism**: Vertical seabed displacement pushes the entire water column, creating waves that propagate in all directions.
            """,
            "ar": """
**🌊 تعريف التسونامي**

التسونامي هو سلسلة من أمواج عملاقة ناتجة عن الانزياح المفاجئ للماء، غالبًا بعد زلزال أو انهيار أرضي أو ثوران بركاني تحت الماء.

**الخصائص الرئيسية:**
- **السرعة**: 500-800 كم/ساعة في المياه العميقة (مثل الطائرة النفاثة)
- **الارتفاع**: 30 سم إلى 1م في البحر → 10-30م بالقرب من السواحل
- **الطول الموجي**: 100-200 كم (مقابل 100م للموجة العادية)
- **الفترة**: 10-60 دقيقة بين الأمواج المتتالية

**الآلية الفيزيائية**: الانزياح الرأسي لقاع البحر يدفع عمود الماء بالكامل، مكونًا موجات تنتشر في جميع الاتجاهات.
            """
        }
    },
    
    "difference_vague_tsunami": {
        "keywords": {
            "fr": ["différence vague tsunami", "comparaison vague tsunami", "vague normale tsunami"],
            "en": ["difference wave tsunami", "compare wave tsunami", "normal wave tsunami"],
            "ar": ["فرق موجة تسونامي", "مقارنة موجة تسونامي", "موجة عادية تسونامي"]
        },
        "responses": {
            "fr": """
**🌊 DIFFÉRENCE ENTRE TSUNAMI ET VAGUE NORMALE**

| Caractéristique | Vague Normale | Tsunami |
|-----------------|---------------|---------|
| **Cause** | Vent | Séisme/Glissement |
| **Longueur d'onde** | 100-200 m | 100-200 km |
| **Vitesse** | 10-60 km/h | 500-800 km/h |
| **Période** | 5-20 secondes | 10-60 minutes |
| **Énergie** | Surface | Colonne d'eau entière |
| **Comportement** | Brise sur plage | Inonde terres |

**Point crucial :** Les vagues normales sont causées par le vent et sont limitées en taille et énergie. Les tsunamis ont une longueur d'onde très longue, peuvent se déplacer à grande vitesse sur l'océan et déferler avec une énorme énergie sur les côtes.
            """,
            "en": """
**🌊 DIFFERENCE BETWEEN TSUNAMI AND NORMAL WAVE**

| Characteristic | Normal Wave | Tsunami |
|----------------|-------------|---------|
| **Cause** | Wind | Earthquake/Landslide |
| **Wavelength** | 100-200 m | 100-200 km |
| **Speed** | 10-60 km/h | 500-800 km/h |
| **Period** | 5-20 seconds | 10-60 minutes |
| **Energy** | Surface | Entire water column |
| **Behavior** | Breaks on beach | Floods inland |

**Key point:** Normal waves are caused by wind and are limited in size and energy. Tsunamis have very long wavelengths, can travel at high speed across the ocean and break with enormous energy on coasts.
            """,
            "ar": """
**🌊 الفرق بين التسونامي والموجة العادية**

| الخاصية | الموجة العادية | التسونامي |
|----------|----------------|-----------|
| **السبب** | الرياح | الزلزال/الانهيار |
| **الطول الموجي** | 100-200 م | 100-200 كم |
| **السرعة** | 10-60 كم/ساعة | 500-800 كم/ساعة |
| **الفترة** | 5-20 ثانية | 10-60 دقيقة |
| **الطاقة** | السطح | عمود الماء بالكامل |
| **السلوك** | ينكسر على الشاطئ | يغمر اليابسة |

**النقطة الأساسية:** الأمواج العادية تسببها الرياح ومحدودة في الحجم والطاقة. يتميز التسونامي بطول موجي طويل جدًا، ويمكن أن ينتقل بسرعة عالية عبر المحيط وينكسر بطاقة هائلة على السواحل.
            """
        }
    },
    
    "causes_principales": {
        "keywords": {
            "fr": ["causes tsunami", "origines tsunami", "pourquoi tsunami"],
            "en": ["tsunami causes", "tsunami origins", "why tsunami"],
            "ar": ["أسباب تسونامي", "مصادر تسونامي", "لماذا تسونامي"]
        },
        "responses": {
            "fr": """
**📌 CAUSES PRINCIPALES DES TSUNAMIS**

**1. SÉISMES SOUS-MARINS (90% des cas)**
- **Magnitude minimale** : > 6.5 sur l'échelle de Richter
- **Type de faille** : Mouvement vertical essentiellement
- **Exemple** : Japon 2011 (magnitude 9.0), Sumatra 2004 (9.1)

**2. GLISSEMENTS DE TERRAIN SOUS-MARINS (7%)**
- **Volume** : Peut atteindre des kilomètres cubes
- **Localisation** : Pentes continentales, volcans sous-marins
- **Exemple** : Papouasie-Nouvelle-Guinée 1998

**3. ÉRUPTIONS VOLCANIQUES (2%)**
- **Mécanisme** : Effondrement du volcan, entrée de matériaux
- **Exemple** : Krakatoa 1883 (vagues de 40m)

**4. IMPACTS DE MÉTÉORITES (1%)**
- **Rareté** : Événements exceptionnels
- **Énergie** : Extrêmement destructrice

**5. AUTRES CAUSES** : Explosions nucléaires sous-marines, effondrements glaciaires
            """,
            "en": """
**📌 MAIN TSUNAMI CAUSES**

**1. UNDERSEA EARTHQUAKES (90% of cases)**
- **Minimum magnitude**: > 6.5 on Richter scale
- **Fault type**: Primarily vertical movement
- **Example**: Japan 2011 (magnitude 9.0), Sumatra 2004 (9.1)

**2. SUBMARINE LANDSLIDES (7%)**
- **Volume**: Can reach cubic kilometers
- **Location**: Continental slopes, underwater volcanoes
- **Example**: Papua New Guinea 1998

**3. VOLCANIC ERUPTIONS (2%)**
- **Mechanism**: Volcano collapse, material entry
- **Example**: Krakatoa 1883 (40m waves)

**4. METEORITE IMPACTS (1%)**
- **Rarity**: Exceptional events
- **Energy**: Extremely destructive

**5. OTHER CAUSES**: Underwater nuclear explosions, glacial collapses
            """,
            "ar": """
**📌 الأسباب الرئيسية للتسونامي**

**1. الزلازل تحت البحر (90٪ من الحالات)**
- **الحد الأدنى للقوة**: > 6.5 على مقياس ريختر
- **نوع الصدع**: حركة رأسية primarily
- **مثال**: اليابان 2011 (قوة 9.0)، سومطرة 2004 (9.1)

**2. الانهيارات الأرضية تحت البحر (7٪)**
- **الحجم**: يمكن أن يصل إلى كيلومترات مكعبة
- **الموقع**: المنحدرات القارية، البراكين تحت الماء
- **مثال**: بابوا غينيا الجديدة 1998

**3. الثورات البركانية (2٪)**
- **الآلية**: انهيار البركان، دخول المواد
- **مثال**: كراكاتوا 1883 (أمواج 40م)

**4. اصطدام النيازك (1٪)**
- **الندرة**: أحداث استثنائية
- **الطاقة**: مدمرة للغاية

**5. أسباب أخرى**: انفجارات نووية تحت الماء، انهيارات جليدية
            """
        }
    },
    
    "seisme_tsunami": {
        "keywords": {
            "fr": ["séisme provoque tsunami", "comment séisme tsunami", "mécanisme séisme tsunami"],
            "en": ["earthquake causes tsunami", "how earthquake tsunami", "mechanism earthquake tsunami"],
            "ar": ["زلزال يتسبب تسونامي", "كيف زلزال تسونامي", "آلية زلزال تسونامي"]
        },
        "responses": {
            "fr": """
**🔬 COMMENT UN SÉISME PROVOQUE UN TSUNAMI**

**Processus en 4 étapes :**

**1. RUPTURE SOUS-MARINE**
- Faille tectonique se rompt sous l'océan
- Déplacement vertical du plancher océanique (jusqu'à 10m)
- Temps : Quelques secondes à minutes

**2. DÉPLACEMENT D'EAU**
- La colonne d'eau est poussée vers le haut ou tirée vers le bas
- Création d'une "bosse" d'eau à la surface
- Énergie transmise à toute la colonne d'eau

**3. PROPAGATION DES ONDES**
- Ondes se propagent à 800 km/h en eau profonde
- Longue distance avec peu de perte d'énergie
- Amplification près des côtes

**4. DÉFERLEMENT CÔTIER**
- Ralentissement en eau peu profonde
- Amplitude des vagues multipliée par 10-30
- Inondation des terres

**Explication :** Lorsqu'un séisme se produit sous l'océan, il déplace brusquement le plancher océanique. L'eau au-dessus est alors projetée, créant une série de vagues qui se propagent à grande vitesse.
            """,
            "en": """
**🔬 HOW AN EARTHQUAKE CAUSES A TSUNAMI**

**4-step process:**

**1. UNDERSEA RUPTURE**
- Tectonic fault breaks under ocean
- Vertical displacement of ocean floor (up to 10m)
- Time: Few seconds to minutes

**2. WATER DISPLACEMENT**
- Water column pushed upward or pulled downward
- Creation of water "bulge" at surface
- Energy transmitted to entire water column

**3. WAVE PROPAGATION**
- Waves propagate at 800 km/h in deep water
- Long distance with little energy loss
- Amplification near coasts

**4. COASTAL BREAKING**
- Slowing in shallow water
- Wave amplitude multiplied by 10-30
- Land flooding

**Explanation:** When an earthquake occurs under the ocean, it suddenly displaces the ocean floor. The water above is then thrown, creating a series of waves that propagate at high speed.
            """,
            "ar": """
**🔬 كيف يتسبب الزلزال في تسونامي**

**عملية من 4 خطوات:**

**1. تمزق تحت البحر**
- انكسار الصدع التكتوني تحت المحيط
- الانزياح الرأسي لقاع المحيط (حتى 10م)
- الوقت: بضع ثوان إلى دقائق

**2. إزاحة الماء**
- دفع عمود الماء لأعلى أو سحبه لأسفل
- تكوين "انتفاخ" مائي على السطح
- نقل الطاقة إلى عمود الماء بالكامل

**3. انتشار الموج**
- انتشار الأمواج بسرعة 800 كم/ساعة في المياه العميقة
- مسافة طويلة مع فقدان طاقة قليل
- تضخيم بالقرب من السواحل

**4. انكسار ساحلي**
- التباطؤ في المياه الضحلة
- تضخيم سعة الموجة 10-30 مرة
- فيضان اليابسة

**الشرح:** عندما يحدث زلزال تحت المحيط، فإنه يزحزح قاع المحيط فجأة. ثم يتم قذف الماء أعلاه، مكونًا سلسلة من الأمواج التي تنتشر بسرعة عالية.
            """
        }
    },
    
    "volcan_glissement_tsunami": {
        "keywords": {
            "fr": ["volcan tsunami", "glissement terrain tsunami", "éruption tsunami"],
            "en": ["volcano tsunami", "landslide tsunami", "eruption tsunami"],
            "ar": ["بركان تسونامي", "انهيار أرضي تسونامي", "ثوران تسونامي"]
        },
        "responses": {
            "fr": """
**🌋 TSUNAMIS VOLCANIQUES ET PAR GLISSEMENTS**

**TSUNAMIS VOLCANIQUES :**

**Mécanismes :**
1. **Effondrement du volcan** - Flancs qui s'effondrent dans la mer
2. **Pyroclastiques** - Flux de matériaux entrant dans l'eau
3. **Explosions sous-marines** - Vapeur et gaz sous pression

**Exemples célèbres :**
- **Krakatoa 1883** : Vagues de 40m, 36,000 morts
- **Santorin 1600 av.J-C** : Possible fin de la civilisation minoenne

**TSUNAMIS PAR GLISSEMENTS :**

**Types de glissements :**
- **Sous-marins** : Effondrement pentes continentales
- **Aériens** : Roches/glaciers tombant dans fjords/lacs

**Caractéristiques :**
- Plus localisés mais très destructeurs localement
- Peuvent survenir sans séisme préalable
- Difficiles à prévoir

**Exemple :** Baie Lituya 1958 - Vague de 524m (record mondial)

**Réponse :** Oui. Une éruption volcanique peut provoquer l'effondrement d'une partie du volcan sous l'eau, générant un tsunami. Les glissements de terrain massifs dans l'eau ont le même effet.
            """,
            "en": """
**🌋 VOLCANIC AND LANDSLIDE TSUNAMIS**

**VOLCANIC TSUNAMIS:**

**Mechanisms:**
1. **Volcano collapse** - Flanks collapsing into sea
2. **Pyroclastics** - Material flows entering water
3. **Underwater explosions** - Steam and pressurized gas

**Famous examples:**
- **Krakatoa 1883**: 40m waves, 36,000 deaths
- **Santorini 1600 BC**: Possible end of Minoan civilization

**LANDSLIDE TSUNAMIS:**

**Landslide types:**
- **Submarine**: Continental slope collapses
- **Aerial**: Rocks/glaciers falling into fjords/lakes

**Characteristics:**
- More localized but very destructive locally
- Can occur without prior earthquake
- Difficult to predict

**Example:** Lituya Bay 1958 - 524m wave (world record)

**Answer:** Yes. A volcanic eruption can cause the collapse of part of the volcano underwater, generating a tsunami. Massive landslides into water have the same effect.
            """,
            "ar": """
**🌋 تسونامي البراكين والانهيارات**

**تسونامي البراكين:**

**الآليات:**
1. **انهيار البركان** - انهيار الأجنبة في البحر
2. **المواد البركانية** - تدفق المواد إلى الماء
3. **انفجارات تحت الماء** - البخار والغاز المضغوط

**أمثلة مشهورة:**
- **كراكاتوا 1883**: أمواج 40م، 36,000 وفاة
- **سانتوريني 1600 ق.م**: نهاية محتملة للحضارة المينوية

**تسونامي الانهيارات:**

**أنواع الانهيارات:**
- **تحت البحر**: انهيار المنحدرات القارية
- **جوي**: صخور/أنهار جليدية تسقط في المضايق/البحيرات

**الخصائص:**
- أكثر تمركزًا ولكن مدمرة جدًا محليًا
- يمكن أن تحدث بدون زلزال مسبق
- صعبة التنبؤ

**مثال:** خليج ليتويا 1958 - موجة 524م (رقم قياسي عالمي)

**الجواب:** نعم. يمكن أن يتسبب ثوران بركاني في انهيار جزء من البركان تحت الماء، مما يولد تسونامي. الانهيارات الأرضية الضخمة في الماء لها نفس التأثير.
            """
        }
    },
    
    "signes_precurseurs": {
        "keywords": {
            "fr": ["signes précurseurs tsunami", "avant tsunami", "signes avant tsunami"],
            "en": ["tsunami warning signs", "before tsunami", "tsunami signs"],
            "ar": ["علامات إنذار تسونامي", "قبل تسونامي", "علامات تسونامي"]
        },
        "responses": {
            "fr": """
**⚠️ SIGNES PRÉCURSEURS D'UN TSUNAMI**

**SIGNES NATURELS (À CONNAÎTRE ABSOLUMENT) :**

**1. SÉISME FORT ET LONG**
- Durée > 20 secondes
- Impossible de rester debout
- Secousses violentes

**2. RETRAIT SOUDAIN DE LA MER**
- Mer qui se retire anormalement loin
- Fond marin visible sur des centaines de mètres
- **ATTENTION** : Ce n'est pas le moment de prendre des photos !

**3. BRUIT ANORMAL**
- Bruit de locomotive ou d'avion à réaction
- Grondement sourd venant de l'océan

**4. COMPORTEMENT ANIMAL**
- Animaux qui fuient vers les hauteurs
- Oiseaux qui s'envolent en masse

**Réponse :** Oui. Le plus connu est le retrait soudain de l'eau du littoral, laissant apparaître le fond marin. On peut aussi ressentir un séisme ou observer des sons inhabituels venant de l'océan.
            """,
            "en": """
**⚠️ TSUNAMI WARNING SIGNS**

**NATURAL SIGNS (MUST KNOW):**

**1. STRONG, LONG EARTHQUAKE**
- Duration > 20 seconds
- Cannot stand upright
- Violent shaking

**2. SUDDEN SEA RETREAT**
- Sea retreating abnormally far
- Seabed visible for hundreds of meters
- **WARNING**: Not the time for photos!

**3. ABNORMAL NOISE**
- Locomotive or jet engine noise
- Deep roar from ocean

**4. ANIMAL BEHAVIOR**
- Animals fleeing to high ground
- Birds flying away en masse

**Answer:** Yes. The best known is the sudden retreat of water from the shoreline, exposing the seabed. One can also feel an earthquake or observe unusual sounds coming from the ocean.
            """,
            "ar": """
**⚠️ علامات إنذار التسونامي**

**العلامات الطبيعية (يجب معرفتها):**

**1. زلزال قوي وطويل**
- المدة > 20 ثانية
- عدم القدرة على الوقوف
- اهتزازات عنيفة

**2. انسحاب مفاجئ للبحر**
- تراجع البحر بشكل غير طبيعي
- قاع البحر مرئي لمئات الأمتار
- **تحذير**: ليس وقتًا لالتقاط الصور!

**3. ضجيج غير طبيعي**
- ضجيج مثل القطار أو المحرك النفاث
- هدير عميق قادم من المحيط

**4. سلوك الحيوان**
- حيوانات تهرب إلى المرتفعات
- طيور تطير بعيدًا بأعداد كبيرة

**الجواب:** نعم. أشهرها الانسحاب المفاجئ للماء من الخط الساحلي، مما يكشف قاع البحر. يمكن أيضًا الشعور بزلزال أو ملاحظة أصوات غير عادية قادمة من المحيط.
            """
        }
    },
    
    # ========== CONSÉQUENCES ==========
    "consequences_humaines": {
        "keywords": {
            "fr": ["conséquences humaines tsunami", "victimes tsunami", "morts tsunami"],
            "en": ["human consequences tsunami", "tsunami victims", "tsunami deaths"],
            "ar": ["عواقب بشرية تسونامي", "ضحايا تسونامي", "وفيات تسونامي"]
        },
        "responses": {
            "fr": """
**😢 CONSÉQUENCES HUMAINES DES TSUNAMIS**

**IMPACTS IMMÉDIATS :**

**1. MORTS ET BLESSÉS**
- **Noyade** (cause principale de décès)
- **Traumatismes physiques** (fractures, blessures)
- **Hypothermie** en eau froide

**2. DÉPLACEMENTS DE POPULATION**
- Maisons détruites
- Infrastructures endommagées
- Réfugiés environnementaux

**STATISTIQUES :**
- **Tsunami 2004** : 230,000-280,000 morts
- **Japon 2011** : 18,000 morts confirmés
- **Moyenne historique** : Variable selon l'événement

**Conséquences :** Mort, blessures, disparitions, traumatisme psychologique et déplacements massifs de populations.
            """,
            "en": """
**😢 HUMAN CONSEQUENCES OF TSUNAMIS**

**IMMEDIATE IMPACTS:**

**1. DEATHS AND INJURIES**
- **Drowning** (main cause of death)
- **Physical trauma** (fractures, injuries)
- **Hypothermia** in cold water

**2. POPULATION DISPLACEMENT**
- Homes destroyed
- Damaged infrastructure
- Environmental refugees

**STATISTICS:**
- **2004 tsunami**: 230,000-280,000 deaths
- **Japan 2011**: 18,000 confirmed deaths
- **Historical average**: Varies by event

**Consequences:** Death, injuries, disappearances, psychological trauma and massive population displacements.
            """,
            "ar": """
**😢 العواقب البشرية للتسونامي**

**الآثار الفورية:**

**1. الوفيات والإصابات**
- **الغرق** (السبب الرئيسي للوفاة)
- **الصدمات الجسدية** (كسور، إصابات)
- **انخفاض حرارة الجسم** في الماء البارد

**2. نزوح السكان**
- تدمير المنازل
- تلف البنية التحتية
- لاجئون بيئيون

**الإحصائيات:**
- **تسونامي 2004**: 230,000-280,000 وفاة
- **اليابان 2011**: 18,000 وفاة مؤكدة
- **المتوسط التاريخي**: يختلف حسب الحدث

**العواقب:** وفاة، إصابات، اختفاء، صدمة نفسية ونزوح جماعي للسكان.
            """
        }
    },
    
    "impacts_economiques": {
        "keywords": {
            "fr": ["impacts économiques tsunami", "économie tsunami", "coûts tsunami"],
            "en": ["economic impacts tsunami", "tsunami economy", "tsunami costs"],
            "ar": ["آثار اقتصادية تسونامي", "اقتصاد تسونامي", "تكاليف تسونامي"]
        },
        "responses": {
            "fr": """
**💰 IMPACTS ÉCONOMIQUES DES TSUNAMIS**

**DÉGÂTS DIRECTS :**
- **Destruction d'infrastructures** : Routes, ports, ponts
- **Pertes agricoles** : Terres salinisées, cultures détruites
- **Secteur touristique** : Hôtels, plages, attractions détruites

**COÛTS INDIRECTS :**
- **Reconstruction** : Années de travaux, milliards de dollars
- **Perte d'activités économiques** : Chômage, fermeture d'entreprises
- **Dette nationale** : Emprunts pour la reconstruction

**EXEMPLES :**
- **Japon 2011** : 235 milliards USD de dégâts
- **Indonésie 2004** : 4,5 milliards USD (Aceh seulement)

**Impacts :** Destruction d'infrastructures, pertes agricoles, perte d'activités économiques et coûts de reconstruction élevés.
            """,
            "en": """
**💰 ECONOMIC IMPACTS OF TSUNAMIS**

**DIRECT DAMAGE:**
- **Infrastructure destruction**: Roads, ports, bridges
- **Agricultural losses**: Salinized lands, destroyed crops
- **Tourism sector**: Hotels, beaches, attractions destroyed

**INDIRECT COSTS:**
- **Reconstruction**: Years of work, billions of dollars
- **Loss of economic activities**: Unemployment, business closures
- **National debt**: Loans for reconstruction

**EXAMPLES:**
- **Japan 2011**: 235 billion USD damage
- **Indonesia 2004**: 4.5 billion USD (Aceh only)

**Impacts:** Destruction of infrastructure, agricultural losses, loss of economic activities and high reconstruction costs.
            """,
            "ar": """
**💰 الآثار الاقتصادية للتسونامي**

**الضرر المباشر:**
- **تدمير البنية التحتية**: طرق، موانئ، جسور
- **الخسائر الزراعية**: أراضي مملوحة، محاصيل مدمرة
- **قطاع السياحة**: فنادق، شواطئ، معالم مدمرة

**التكاليف غير المباشرة:**
- **إعادة الإعمار**: سنوات من العمل، مليارات الدولارات
- **فقدان الأنشطة الاقتصادية**: بطالة، إغلاق الأعمال
- **الدين الوطني**: قروض لإعادة الإعمار

**أمثلة:**
- **اليابان 2011**: 235 مليار دولار ضرر
- **إندونيسيا 2004**: 4.5 مليار دولار (آتشيه فقط)

**الآثار:** تدمير البنية التحتية، خسائر زراعية، فقدان الأنشطة الاقتصادية وتكاليف إعادة إعمار مرتفعة.
            """
        }
    },
    
    "impact_environnement": {
        "keywords": {
            "fr": ["impact environnemental tsunami", "environnement tsunami", "biodiversité tsunami"],
            "en": ["environmental impact tsunami", "tsunami environment", "tsunami biodiversity"],
            "ar": ["تأثير بيئي تسونامي", "بيئة تسونامي", "تنوع حيوي تسونامي"]
        },
        "responses": {
            "fr": """
**🌿 IMPACT ENVIRONNEMENTAL DES TSUNAMIS**

**DÉGÂTS ÉCOLOGIQUES :**

**1. HABITATS CÔTIERS DÉTRUITS**
- Récifs coralliens brisés
- Mangroves arrachées
- Plages et dunes érodées

**2. SALINISATION DES TERRES**
- Sols agricoles contaminés par le sel
- Nappes phréatiques polluées
- Végétation morte

**3. FAUNE MARINE ET TERRESTRE**
- Mort de poissons et mammifères marins
- Oiseaux et animaux terrestres noyés
- Perturbation des écosystèmes

**4. POLLUTION**
- Débris et déchets dispersés
- Produits chimiques déversés
- Équipements endommagés

**Impact :** Destruction des habitats côtiers, salinisation des terres agricoles, mort de la faune marine et terrestre.
            """,
            "en": """
**🌿 ENVIRONMENTAL IMPACT OF TSUNAMIS**

**ECOLOGICAL DAMAGE:**

**1. COASTAL HABITATS DESTROYED**
- Broken coral reefs
- Uprooted mangroves
- Eroded beaches and dunes

**2. LAND SALINIZATION**
- Agricultural soils contaminated with salt
- Polluted groundwater
- Dead vegetation

**3. MARINE AND TERRESTRIAL WILDLIFE**
- Death of fish and marine mammals
- Drowned birds and land animals
- Ecosystem disruption

**4. POLLUTION**
- Scattered debris and waste
- Spilled chemicals
- Damaged equipment

**Impact:** Destruction of coastal habitats, salinization of agricultural lands, death of marine and terrestrial wildlife.
            """,
            "ar": """
**🌿 التأثير البيئي للتسونامي**

**الضرر البيئي:**

**1. تدمير الموائل الساحلية**
- تكسير الشعاب المرجانية
- اقتلاع أشجار المانغروف
- تآكل الشواطئ والكثبان الرملية

**2. تمليح الأراضي**
- تربة زراعية ملوثة بالملح
- تلوث المياه الجوفية
- نباتات ميتة

**3. الحياة البحرية والبرية**
- موت الأسماك والثدييات البحرية
- غرق الطيور والحيوانات البرية
- اضطراب النظام البيئي

**4. التلوث**
- حطام ونفايات متناثرة
- انسكاب المواد الكيميائية
- معدات تالفة

**التأثير:** تدمير الموائل الساحلية، تمليح الأراضي الزراعية، موت الحياة البحرية والبرية.
            """
        }
    },
    
    "exemples_importants": {
        "keywords": {
            "fr": ["exemples tsunami", "tsunami 2004", "tsunami japon 2011", "tsunami historique"],
            "en": ["tsunami examples", "2004 tsunami", "japan 2011 tsunami", "historical tsunami"],
            "ar": ["أمثلة تسونامي", "تسونامي 2004", "تسونامي اليابان 2011", "تسونامي تاريخي"]
        },
        "responses": {
            "fr": """
**📜 TSUNAMIS HISTORIQUES IMPORTANTS**

**1. OCÉAN INDIEN 2004 🌊**
- **Cause** : Séisme magnitude 9.1 au large de Sumatra
- **Pays touchés** : Indonésie, Thaïlande, Sri Lanka, Inde, etc.
- **Bilan** : 230,000+ morts
- **Particularité** : Un des tsunamis les plus meurtriers de l'histoire

**2. JAPON 2011 🇯🇵**
- **Cause** : Séisme magnitude 9.0
- **Hauteur vagues** : 10+ mètres
- **Bilan** : 18,000+ morts
- **Conséquence** : Catastrophe nucléaire de Fukushima

**3. KRAKATOA 1883 🌋**
- **Cause** : Éruption volcanique
- **Hauteur vagues** : 40 mètres
- **Bilan** : 36,000 morts
- **Particularité** : Vagues entendues à 5000 km

**4. CHILI 2010 🇨🇱**
- **Cause** : Séisme magnitude 8.8
- **Bilan** : 500+ morts
- **Dégâts** : Infrastructure massive détruite

**Tsunamis les plus meurtriers :**
1. 2004 - Océan Indien (~230,000 morts)
2. 1883 - Krakatoa (~36,000 morts) 
3. 2011 - Japon (~18,000 morts)
            """,
            "en": """
**📜 IMPORTANT HISTORICAL TSUNAMIS**

**1. INDIAN OCEAN 2004 🌊**
- **Cause**: Magnitude 9.1 earthquake off Sumatra
- **Affected countries**: Indonesia, Thailand, Sri Lanka, India, etc.
- **Death toll**: 230,000+
- **Particularity**: One of the deadliest tsunamis in history

**2. JAPON 2011 🇯🇵**
- **Cause**: Magnitude 9.0 earthquake
- **Wave height**: 10+ meters
- **Death toll**: 18,000+
- **Consequence**: Fukushima nuclear disaster

**3. KRAKATOA 1883 🌋**
- **Cause**: Volcanic eruption
- **Wave height**: 40 meters
- **Death toll**: 36,000
- **Particularity**: Waves heard 5000 km away

**4. CHILE 2010 🇨🇱**
- **Cause**: Magnitude 8.8 earthquake
- **Death toll**: 500+
- **Damage**: Massive infrastructure destruction

**Deadliest tsunamis:**
1. 2004 - Indian Ocean (~230,000 deaths)
2. 1883 - Krakatoa (~36,000 deaths)
3. 2011 - Japan (~18,000 deaths)
            """,
            "ar": """
**📜 تسوناميات تاريخية مهمة**

**1. المحيط الهندي 2004 🌊**
- **السبب**: زلزال قوة 9.1 قبالة سومطرة
- **الدول المتضررة**: إندونيسيا، تايلاند، سريلانكا، الهند، إلخ
- **الضحايا**: 230,000+
- **الخصوصية**: أحد أكثر تسوناميات التاريخ دموية

**2. اليابان 2011 🇯🇵**
- **السبب**: زلزال قوة 9.0
- **ارتفاع الأمواج**: 10+ أمتار
- **الضحايا**: 18,000+
- **النتيجة**: كارثة فوكوشيما النووية

**3. كراكاتوا 1883 🌋**
- **السبب**: ثوران بركاني
- **ارتفاع الأمواج**: 40 مترًا
- **الضحايا**: 36,000
- **الخصوصية**: أمواج مسموعة على بعد 5000 كم

**4. تشيلي 2010 🇨🇱**
- **السبب**: زلزال قوة 8.8
- **الضحايا**: 500+
- **الضرر**: تدمير هائل للبنية التحتية

**أكثر تسوناميات دموية:**
1. 2004 - المحيط الهندي (~230,000 وفاة)
2. 1883 - كراكاتوا (~36,000 وفاة)
3. 2011 - اليابان (~18,000 وفاة)
            """
        }
    },
    
    "effets_long_terme": {
        "keywords": {
            "fr": ["effets long terme tsunami", "conséquences durables tsunami", "après tsunami"],
            "en": ["long term effects tsunami", "lasting consequences tsunami", "after tsunami"],
            "ar": ["آثار طويلة المدى تسونامي", "عواقب دائمة تسونامي", "بعد تسونامي"]
        },
        "responses": {
            "fr": """
**⏳ EFFETS À LONG TERME SUR LES POPULATIONS**

**IMPACTS DURABLES :**

**1. DÉPLACEMENT PROLONGÉ**
- Populations ne pouvant retourner chez elles
- Camps de réfugiés pendant des années
- Perte de terres ancestrales

**2. TRAUMATISME PSYCHOLOGIQUE**
- Syndrome de stress post-traumatique
- Dépression et anxiété
- Deuil collectif

**3. PERTE DE REVENUS**
- Destruction des moyens de subsistance
- Chômage de longue durée
- Appauvrissement

**4. RECONSTRUCTION LENTE**
- Années pour reconstruire les infrastructures
- Dette nationale accrue
- Dépendance à l'aide internationale

**5. VULNÉRABILITÉ ACCRUE**
- Peur persistante des tsunamis
- Sensibilisation accrue mais anxiété
- Préparation future améliorée

**Effets :** Déplacement prolongé, perte de revenus, reconstruction lente, traumatisme psychologique et vulnérabilité accrue aux catastrophes futures.
            """,
            "en": """
**⏳ LONG-TERM EFFECTS ON POPULATIONS**

**LASTING IMPACTS:**

**1. PROLONGED DISPLACEMENT**
- Populations unable to return home
- Refugee camps for years
- Loss of ancestral lands

**2. PSYCHOLOGICAL TRAUMA**
- Post-traumatic stress disorder
- Depression and anxiety
- Collective grief

**3. LOSS OF INCOME**
- Destruction of livelihoods
- Long-term unemployment
- Impoverishment

**4. SLOW RECONSTRUCTION**
- Years to rebuild infrastructure
- Increased national debt
- Dependence on international aid

**5. INCREASED VULNERABILITY**
- Persistent fear of tsunamis
- Increased awareness but anxiety
- Improved future preparation

**Effects:** Prolonged displacement, loss of income, slow reconstruction, psychological trauma and increased vulnerability to future disasters.
            """,
            "ar": """
**⏳ الآثار طويلة المدى على السكان**

**آثار دائمة:**

**1. نزوح مطول**
- سكان غير قادرين على العودة إلى ديارهم
- مخيمات لاجئين لسنوات
- فقدان الأراضي ancestral

**2. صدمة نفسية**
- اضطراب ما بعد الصدمة
- اكتئاب وقلق
- حزن جماعي

**3. فقدان الدخل**
- تدمير سبل العيش
- بطالة طويلة الأمد
- إفقار

**4. إعادة إعمار بطيئة**
- سنوات لإعادة بناء البنية التحتية
- زيادة الدين الوطني
- الاعتماد على المساعدة الدولية

**5. زيادة الضعف**
- خوف مستمر من التسونامي
- زيادة الوعي ولكن القلق
- تحسين الاستعداد المستقبلي

**الآثار:** نزوح مطول، فقدان الدخل، إعادة إعمار بطيئة، صدمة نفسية وزيادة الضعف للكوارث المستقبلية.
            """
        }
    },
    
    "mortalite_moyenne": {
        "keywords": {
            "fr": ["mortalité tsunami", "combien morts tsunami", "statistiques mortalité tsunami"],
            "en": ["tsunami mortality", "how many tsunami deaths", "tsunami death statistics"],
            "ar": ["وفيات تسونامي", "كم وفاة تسونامي", "إحصائيات وفيات تسونامي"]
        },
        "responses": {
            "fr": """
**📊 MORTALITÉ MOYENNE LORS DES TSUNAMIS**

**VARIABILITÉ IMPORTANTE :**

**FACTEURS INFLUENÇANT LA MORTALITÉ :**
- **Densité population côtière**
- **Heure de la journée** (nuit = plus dangereux)
- **Systèmes d'alerte** en place
- **Éducation** de la population
- **Topographie** côtière

**EXEMPLES DE BILANS :**
- **Tsunami 2004** : 230,000-280,000 morts
- **Japon 2011** : 18,000 morts
- **Papouasie 1998** : 2,200 morts
- **Chili 2010** : 500 morts

**MOYENNE :** Cela varie beaucoup selon la zone et les mesures de prévention : quelques dizaines dans des régions bien préparées, plusieurs milliers dans des zones densément peuplées et vulnérables.

**RÉDUCTION GRÂCE À :**
- Systèmes d'alerte précoces
- Éducation et exercices
- Planification de l'évacuation
- Règlementation de construction
            """,
            "en": """
**📊 AVERAGE MORTALITY IN TSUNAMIS**

**SIGNIFICANT VARIABILITY:**

**FACTORS INFLUENCING MORTALITY:**
- **Coastal population density**
- **Time of day** (night = more dangerous)
- **Warning systems** in place
- **Population education**
- **Coastal topography**

**EXAMPLES OF DEATH TOLLS:**
- **2004 tsunami**: 230,000-280,000 deaths
- **Japan 2011**: 18,000 deaths
- **Papua 1998**: 2,200 deaths
- **Chile 2010**: 500 deaths

**AVERAGE:** This varies greatly depending on the area and prevention measures: a few dozen in well-prepared regions, several thousand in densely populated and vulnerable areas.

**REDUCTION THROUGH:**
- Early warning systems
- Education and drills
- Evacuation planning
- Construction regulations
            """,
            "ar": """
**📊 متوسط الوفيات في التسونامي**

**تغير كبير:**

**العوامل المؤثرة على الوفيات:**
- **كثافة السكان الساحليين**
- **وقت اليوم** (الليل = أكثر خطورة)
- **أنظمة الإنذار** الموجودة
- **تثقيف السكان**
- **طبوغرافيا الساحل**

**أمثلة على أعداد الضحايا:**
- **تسونامي 2004**: 230,000-280,000 وفاة
- **اليابان 2011**: 18,000 وفاة
- **بابوا 1998**: 2,200 وفاة
- **تشيلي 2010**: 500 وفاة

**المتوسط:** هذا يختلف كثيرًا حسب المنطقة وإجراءات الوقاية: بضع عشرات في المناطق المستعدة جيدًا، عدة آلاف في المناطق المكتظة بالسكان والضعيفة.

**الخفض من خلال:**
- أنظمة الإنذار المبكر
- التعليم والتدريبات
- تخطيط الإخلاء
- لوائح البناء
            """
        }
    }
}

# ==================== FONCTION DE RECHERCHE AMÉLIORÉE ====================

def find_response(user_input, language):
    """Trouve la réponse la plus pertinente avec reconnaissance améliorée"""
    user_input_lower = user_input.lower().strip()
    
    # Nettoyer l'input
    words = user_input_lower.split()
    
    # Recherche exacte d'abord
    best_match = None
    best_score = 0
    
    for category, data in KNOWLEDGE_BASE.items():
        score = 0
        keywords = data["keywords"][language]
        
        # Vérifier chaque mot-clé
        for keyword in keywords:
            # Si le mot-clé est une phrase complète dans l'input
            if keyword in user_input_lower:
                score += 3  # Score élevé pour correspondance exacte
            # Sinon vérifier les mots individuels
            else:
                keyword_words = keyword.split()
                for kw in keyword_words:
                    if kw in words:
                        score += 1
        
        if score > best_score:
            best_score = score
            best_match = category
    
    # Seuil minimum pour éviter les mauvaises correspondances
    if best_score >= 2:
        return KNOWLEDGE_BASE[best_match]["responses"][language]
    
    # Recherche de secours avec correspondance partielle
    if best_score >= 1:
        return KNOWLEDGE_BASE[best_match]["responses"][language]
    
    # Réponse par défaut
    default_responses = {
        "fr": """
🤖 **Expert Tsunami** - Je n'ai pas bien compris votre question. 

Voici ce que je peux vous expliquer :
• **Définition** : Qu'est-ce qu'un tsunami ?
• **Causes** : Séismes, volcans, glissements
• **Différence** : Tsunami vs vague normale  
• **Signes** : Précurseurs d'un tsunami
• **Conséquences** : Humaines, économiques, environnementales
• **Exemples** : Tsunamis historiques importants

Utilisez les boutons à gauche ou reformulez votre question !
        """,
        "en": """
🤖 **Tsunami Expert** - I didn't fully understand your question.

Here's what I can explain:
• **Definition**: What is a tsunami?
• **Causes**: Earthquakes, volcanoes, landslides
• **Difference**: Tsunami vs normal wave
• **Warning signs**: Tsunami precursors
• **Consequences**: Human, economic, environmental
• **Examples**: Important historical tsunamis

Use the buttons on the left or rephrase your question!
        """,
        "ar": """
🤖 **خبير التسونامي** - لم أفهم سؤالك بالكامل.

إليك ما يمكنني شرحه:
• **التعريف**: ما هو التسونامي؟
• **الأسباب**: زلازل، براكين، انهيارات
• **الفرق**: تسونامي مقابل موجة عادية
• **علامات الإنذار**: مؤشرات التسونامي
• **العواقب**: بشرية، اقتصادية، بيئية
• **أمثلة**: تسوناميات تاريخية مهمة

استخدم الأزرار على اليسار أو أعد صياغة سؤالك!
        """
    }
    return default_responses[language]

def display_text(text, language):
    """Affiche le texte avec la bonne direction"""
    if language == "ar":
        st.markdown(f'<div class="arabic-text">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(text)

# ==================== INTERFACE ====================

# Titre
st.markdown('<div class="main-header">🌊 Expert Tsunami</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🌍 Langue")
    selected_language = st.radio("", list(LANGUAGES.keys()), label_visibility="collapsed")
    current_lang = LANGUAGES[selected_language]
    
    # Questions par catégorie
    categories = {
        "fr": {
            "definition": "📚 Définition et Causes",
            "consequences": "💥 Conséquences",
            "historique": "📜 Exemples Historiques"
        },
        "en": {
            "definition": "📚 Definition and Causes", 
            "consequences": "💥 Consequences",
            "historique": "📜 Historical Examples"
        },
        "ar": {
            "definition": "📚 التعريف والأسباب",
            "consequences": "💥 العواقب",
            "historique": "📜 أمثلة تاريخية"
        }
    }
    
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
                "Impact environnemental",
                "Effets à long terme",
                "Mortalité moyenne"
            ],
            "en": [
                "Human consequences", 
                "Economic impacts",
                "Environmental impact",
                "Long term effects",
                "Average mortality"
            ],
            "ar": [
                "العواقب البشرية",
                "الآثار الاقتصادية",
                "التأثير البيئي",
                "الآثار طويلة المدى",
                "متوسط الوفيات"
            ]
        },
        "historique": {
            "fr": [
                "Exemples historiques importants",
                "Tsunami 2004 Océan Indien",
                "Tsunami Japon 2011"
            ],
            "en": [
                "Important historical examples",
                "2004 Indian Ocean tsunami",
                "2011 Japan tsunami"
            ],
            "ar": [
                "أمثلة تاريخية مهمة",
                "تسونامي المحيط الهندي 2004",
                "تسونامي اليابان 2011"
            ]
        }
    }
    
    for category_key, category_name in categories[current_lang].items():
        st.markdown(f'<div class="category-header">{category_name}</div>', unsafe_allow_html=True)
        for question in questions_by_category[category_key][current_lang]:
            if st.button(question, key=f"{category_key}_{question}"):
                st.session_state.auto_question = question
    
    st.markdown("---")
    st.markdown("### 🚨 Urgence")
    st.markdown("**Éloignement immédiat**")
    st.markdown("**112 • 911 • 999**")

# Zone de chat
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Historique de conversation
if "messages" not in st.session_state:
    welcome_messages = {
        "fr": "🌊 **Expert Tsunami** - Je peux répondre à vos questions sur : définition, causes, conséquences des tsunamis. Utilisez les boutons ou tapez vos questions !",
        "en": "🌊 **Tsunami Expert** - I can answer your questions about: definition, causes, consequences of tsunamis. Use buttons or type your questions!", 
        "ar": "🌊 **خبير التسونامي** - يمكنني الإجابة على أسئلتك عن: تعريف، أسباب، عواقب التسونامي. استخدم الأزرار أو اكتب أسئلتك!"
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

st.markdown('</div>', unsafe_allow_html=True)
