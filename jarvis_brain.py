import os
import re
import sys
import json
import requests
from dotenv import load_dotenv

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

load_dotenv()

# In-memory session context storage
SESSION_HISTORY = {}

# =====================================================================
# 🚩 १. छत्रपती शिवाजी महाराज - संपूर्ण ऐतिहासिक ज्ञान (MR, HI, EN)
# =====================================================================
SHIVAJI_MAHARAJ_KNOWLEDGE = {
    'mr': """🚩 **छत्रपती शिवाजी महाराज - अखंड हिंदुस्थानचे आराध्य दैवत, युगपुरुष आणि रयतेचे राजे!**

१. **जन्म आणि बालपण**:
• जन्म: १९ फेब्रुवारी १६३० रोजी पुणे जिल्ह्यातील जुन्नर येथील ऐतिहासिक शिवनेरी किल्ल्यावर झाला.
• माता: राष्ट्रमाता, राजमाता जिजाऊ आऊसाहेब - ज्यांनी बाल शिवबांवर नीतिमत्ता, न्याय आणि स्वराज्य स्थापनेचे संस्कार घडवले.
• पिता: शहाजीराजे भोसले - एक अत्यंत पराक्रमी सेनानी आणि मुत्सद्दी सरदार.

२. **रायरेश्वराची शपथ आणि स्वराज्य स्थापना**:
• वयाच्या अवघ्या १६ व्या वर्षी (१६४५ मध्ये) शिवरायांनी निष्ठावंत मावळ्यांसोबत रोहिडेश्वराच्या (रायरेश्वर) पवित्र मंदिरात स्वतःच्या रक्ताचा अभिषेक करून 'हिंदवी स्वराज्य' स्थापनेची प्रतिज्ञा घेतली.
• 'तोरणा किल्ला' जिंकून महाराजांनी स्वराज्याचे पहिले तोरण बांधले. त्यानंतर राजगड, कोंढाणा, पुरंदर यांसारखे अजिंक्य किल्ले जिंकले.

३. **अतुलनीय पराक्रम आणि ऐतिहासिक लढाया**:
• **अफझलखानाचा वध (१० नोव्हेंबर १६५९)**: विजापूरचा बलाढ्य सरदार अफझलखान स्वराज्याला चिरडण्याच्या वल्गना करत आला होता. प्रतापगडाच्या पायथ्याशी शिवरायांनी वाघनखे आणि बिचव्याने त्याचा कोथळा बाहेर काढून पराक्रमाचा नवा अध्याय लिहिला.
• **पन्हाळगड वेढा व पावनखिंड (१६६०)**: सिद्दी जोहरच्या वेढ्यातून विशाळगडाकडे जाताना वीर बाजीप्रभू देशपांडे आणि बांदल मावळ्यांनी घोडखिंडीत छातीचा कोट करून मुघल सैन्याला रोखले आणि पावनखिंडीत अमर बलिदान दिले.
• **शाहिस्तेखानाची फजिती (५ एप्रिल १६६३)**: पुण्याच्या लाल महालात हजारो सैनिकांच्या पहार्‍यात बसलेल्या मुघल सुभेदार शाहिस्तेखानावर शिवरायांनी मध्यरात्री गनिमी काव्याने अचानक छापा टाकला आणि त्याची तीन बोटे छाटली.
• **आग्र्याहून ऐतिहासिक सुटका (१६६६)**: औरंगजेबाच्या कपटकारस्थानातून व नजरकैदेतून बाल संभाजीराजांसह मिठाईच्या पेटाऱ्यांतून शिताफीने निसटून शिवरायांनी मुघल सत्तेला सणसणीत चपराक दिली.

४. **भव्य सुवर्ण राज्याभिषेक (६ जून १६७४)**:
• दुर्गराज रायगडावर पंडित गागाभट्टांच्या उपस्थितीत शिवरायांचा वेदोक्त राज्याभिषेक सोहळा संपन्न झाला.
• महाराजांना 'क्षत्रियकुलावतंस, सिंहासनाधीश्वर, श्रीमंत छत्रपती' ही पदवी प्रदान करण्यात आली आणि 'शिवशक' सुरू झाले.

५. **भारतीय आरमाराचे जनक (Father of Indian Navy)**:
• परकीय आक्रमकांपासून समुद्राचे संरक्षण करण्यासाठी महाराजांनी स्वतःचे आरमार उभे केले. सिंधुदुर्ग, विजयदुर्ग, पद्मदुर्ग यांसारखे अभेद्य जलदुर्ग उभारले आणि मायनाक भंडारी व दर्यासारंग यांच्याकडे आरमाराचे नेतृत्व सोपवले.

६. **रयतेचे कल्याणकारी राज्य**:
• अष्टप्रधान मंडळाची स्थापना करून पारदर्शक प्रशासन दिले.
• शेतकऱ्यांना विनाकारण त्रास देण्यास सक्त मनाई केली. स्त्रियांचा आणि पराभूत शत्रूच्या कुटुंबियांचाही सर्वोच्च आदर राखण्याचा कडक नियम केला.

'प्रौढ प्रताप पुरंदर, क्षत्रियकुलावतंस, सिंहासनाधीश्वर, महाराजाधिराज, राजा शिवछत्रपती महाराज की जय!' 🚩""",

    'hi': """🚩 **छत्रपति शिवाजी महाराज - अखंड भारत के गौरव, महान योद्धा और रयते के कल्याणकारी राजा!**

१. **जन्म और प्रारंभिक जीवन**:
• जन्म: १९ फरवरी १६३० को पुणे जिले के जुन्नर स्थित ऐतिहासिक शिवनेरी किले में हुआ।
• माता: राष्ट्रमाता जीजाबाई (जीजाऊ आऊसाहेब) - जिन्होंने बाल शिवाजी में धर्म, न्याय, साहस और स्वतंत्रता के संस्कार भरे।
• पिता: शहाजीराजे भोसले - एक अत्यंत पराक्रमी और कुशल सेनापति।

२. **रायरेश्वर की शपथ और स्वराज्य स्थापना**:
• मात्र १६ वर्ष की आयु में (१६४५ ई.) शिवराया ने अपने निष्ठावान मावलों के साथ रोहिडेश्वर (रायरेश्वर) के पवित्र मंदिर में 'हिंदवी स्वराज्य' की स्थापना का संकल्प लिया।
• 'तोरणा किला' जीतकर स्वराज्य का प्रथम तोरण बांधा। इसके बाद राजगढ़, कोंढाणा, पुरंदर जैसे दुर्ग जीतकर स्वराज्य का विस्तार किया।

३. **अतुलनीय पराक्रम और ऐतिहासिक विजय**:
• **अफजल खान का वध (१० नवंबर १६५९)**: बीजापुर के क्रूर सरदार अफजल खान को प्रतापगढ़ की तलहटी में वाघनख और बिछवे से मारकर शिवराया ने अद्वितीय वीरता का परिचय दिया।
• **पन्हालगढ़ का घेरा और पावनखिंड (१६६०)**: सिद्दी जौहर के घेरे से विशालगढ़ जाते समय वीर बाजीप्रभु देशपांडे ने घोडखिंड में मुगलों को रोककर अमर बलिदान दिया, जिसे 'पावनखिंड' नाम मिला।
• **शाइस्ता खान पर गुप्त छापा (५ अप्रैल १६६३)**: पुणे के लाल महल में रात के अंधेरे में छापामार युद्ध कर मुगल सूबेदार शाइस्ता खान की अंगुलियां काट दीं।
• **आगरा से ऐतिहासिक रिहाई (१६६६)**: औरंगजेब की कड़ी कैद से बाल संभाजीराजे के साथ मिठाई की टोकरियों में छिपकर निकलना विश्व इतिहास की महानतम चतुराई है।

४. **स्वर्ण राज्याभिषेक (६ जून १६७४)**:
• दुर्गराज रायगढ़ पर पंडित गागाभट्ट की उपस्थिति में वेदोक्त राज्याभिषेक संपन्न हुआ।
• उन्हें 'क्षत्रियकुलावतंस, सिंहासनाधीश्वर, छत्रपति' की उपाधि प्राप्त हुई और स्वतंत्र 'शिवशक' प्रारंभ हुआ।

५. **भारतीय नौसेना के जनक (Father of Indian Navy)**:
• विदेशी आक्रांताओं से तटीय सुरक्षा के लिए सिंधुदुर्ग, विजयदुर्ग जैसे अभेद्य जलदुर्ग बनाए और शक्तिशाली नौसेना की नींव रखी।

'प्रौढ प्रताप पुरंदर, क्षत्रियकुलावतंस, महाराजाधिराज, छत्रपति शिवाजी महाराज की जय!' 🚩""",

    'en': """🚩 **Chhatrapati Shivaji Maharaj - The Father of Hindavi Swarajya, Legendary Military Strategist, and Sovereign King!**

1. **Birth, Lineage & Mentorship**:
• Born on **February 19, 1630**, at the majestic hill-fort of **Shivneri** near Junnar, Maharashtra.
• **Mother**: Rajmata Jijabai (Jijau) — a visionary mother who instilled profound values of truth, compassion, righteous governance, and unyielding resistance against tyranny.
• **Father**: Shahaji Raje Bhonsle — an illustrious general and statesman of the Deccan.

2. **The Sacred Oath of Swarajya (1645)**:
• At just 16 years of age, Shivaji Maharaj gathered his loyal Mavala comrades at the sacred temple of **Raireshwar** and pledged to establish **"Hindavi Swarajya"** (self-rule of the indigenous people).
• Captured **Torna Fort** as his very first conquest, unfurling the saffron Zenda (Jaripatka), and built an impenetrable network of hill forts including **Rajgad**, **Purandar**, and **Kondhana**.

3. **Legendary Strategic Victories**:
• **Slaying of Afzal Khan (Nov 10, 1659)**: At the foothills of Pratapgad, Afzal Khan attempted a treacherous ambush during a diplomatic meeting. Foreseeing betrayal, Shivaji wore concealed armor and vanquished the tyrant using iron tiger claws (**Wagh Nakh**) and a **Bichuwa** dagger.
• **Siege of Panhala & Battle of Pavan Khind (1660)**: While Shivaji escaped Siddi Jauhar's siege toward Vishalgad, the valiant **Baji Prabhu Deshpande** and Bandal Mavalas held the mountain pass to the last breath.
• **Midnight Surgical Strike on Shaista Khan (April 5, 1663)**: Shivaji personally infiltrated the heavily guarded Lal Mahal in Pune with 400 handpicked commandos, severing Shaista Khan's fingers and routing the Mughal viceroy.
• **Great Escape from Agra (1666)**: Trapped under house arrest by Emperor Aurangzeb, Shivaji engineered a legendary escape inside large hampers of sweets with his son Prince Sambhaji.

4. **Grand Vedic Coronation (June 6, 1674)**:
• Crowned sovereign monarch at **Fort Raigad** by scholar Gaga Bhatt, receiving the titles **'Kshatriyakulavatansa'** and **'Chhatrapati'**, inaugurating the **Rajyabhisheka Shaka** calendar.

5. **Father of the Modern Indian Navy**:
• Recognized the strategic importance of maritime defense early on. Constructed impenetrable sea fortresses like **Sindhudurg**, **Vijaydurg**, and **Padmadurg**, building a modern navy under admirals Maynak Bhandari and Kanhoji Angre.

6. **Benevolent Governance & Secular Welfare**:
• Created the **Ashta Pradhan Mandal** (Council of Eight Ministers).
• Enforced strict military codes: strictly prohibited harassment of farmers, looting of holy books, and mistreatment of women, ensuring total safety and honor for all subjects.

'Jai Bhavani, Jai Shivaji! Chhatrapati Shivaji Maharaj Ki Jai!' 🚩"""
}

# =====================================================================
# 🚩 २. महाराष्ट्राचे गड-किल्ले ज्ञान भांडार (Forts Guide - MR, HI, EN)
# =====================================================================
FORTS_KNOWLEDGE = {
    'रायगड': {
        'mr': """🚩 **दुर्गराज रायगड - हिंदवी स्वराज्याची राजधानी!**
• **महत्त्व**: छत्रपती शिवाजी महाराजांनी १६७४ मध्ये याच पवित्र गडावर आपला भव्य राज्याभिषेक करवून घेतला.
• **स्थान**: महाडजवळ, रायगड जिल्हा.
• **प्रमुख आकर्षणे**:
  - **राजदरबार व नगारखाना**: जिथे शिवरायांचे ऐतिहासिक सुवर्ण सिंहासन होते आणि जिथून आजही कुजबुजही ऐकू येते.
  - **जगदीश्वर मंदिर व छत्रपती शिवरायांची समाधी**: गडावरील अत्यंत शांत व पवित्र स्थान.
  - **टकमक टोक**: गुन्हेगारांना कडेलोट करण्याची भयानक दरी.
  - **होळीचा माळ व भव्य बाजारपेठ**: घोड्यावरून फिरता येईल अशी दोन मजली बाजारपेठ.
• **कसे पोहोचावे**: पुणे किंवा मुंबईहून महाडमार्गे पाचाड गावात जाता येते. पायऱ्यांनी चालत (२ तास) किंवा रोपवेने (५ मिनिटांत) गडावर पोहोचता येते.""",
        
        'hi': """🚩 **दुर्गराज रायगढ़ - हिंदवी स्वराज्य की अमर राजधानी!**
• **महत्व**: छत्रपति शिवाजी महाराज का ऐतिहासिक राज्याभिषेक ६ जून १६७४ को इसी पावन दुर्ग पर संपन्न हुआ था।
• **स्थान**: महाड के समीप, रायगढ़ जिला, महाराष्ट्र।
• **प्रमुख दर्शनीय स्थल**:
  - **राजदरबार व नगाड़ाखाना**: जहां महाराजा का स्वर्ण सिंहासन सुशोभित था।
  - **जगदीश्वर मंदिर व छत्रपति शिवाजी महाराज की समाधि**: सर्वोच्च श्रद्धा का केंद्र।
  - **टकमक टोक**: खड़ी चट्टानी ढलान जहां से देशद्रोहियों को सजा दी जाती थी।
  - **विशाल बाजारपेठ**: दो मंजिला सुव्यवस्थित बाजार।
• **पहुंचने का मार्ग**: मुंबई या पुणे से महाड होकर पाचाड गांव पहुंचें। सीढ़ियों द्वारा (२ घंटे) या रोपवे द्वारा (५ मिनट) जा सकते हैं।""",

        'en': """🚩 **Raigad Fort - The Sovereign Capital of the Maratha Empire!**
• **Historical Significance**: Chosen by Chhatrapati Shivaji Maharaj as the capital of Swarajya in 1674, where his grand Vedic coronation took place.
• **Location**: Near Mahad, Raigad District, Sahyadri Mountains, Maharashtra.
• **Architectural Marvels**:
  - **Raj Darbar (Royal Throne Room) & Nagarkhana**: An acoustic marvel designed so that even whispers in the courtyard carry distinctly to the throne.
  - **Samadhi of Chhatrapati Shivaji Maharaj & Jagdishwar Temple**: The sacred eternal resting monument of the great king.
  - **Takmak Tok**: A breathtaking 1,200-foot sheer cliff face historically used for punishment of traitors.
  - **The Two-Story Royal Bazaar**: A 300-meter-long stone shopping boulevard designed so horse-riders could shop comfortably from horseback.
  - **Maha Darwaza & Hirkani Buruj**: Fortifications honoring the courage of Hirkani, a brave milkmaid who scaled down the vertical cliff in the dark.
• **How to Reach**: Reach Pachad village via Mahad (accessible from Mumbai/Pune). Ascend via ~1,450 stone steps (2 hours trek) or board the modern aerial passenger ropeway (5 minutes)."""
    },

    'राजगड': {
        'mr': """🚩 **राजगड - छत्रपती शिवाजी महाराजांची पहिली राजधानी (२६ वर्षे)!**
• **महत्त्व**: शिवरायांनी सर्वात जास्त काळ याच गडावरून स्वराज्याचा कारभार पाहिला.
• **स्थान**: वेल्हे तालुका, पुणे जिल्हा.
• **रचना**: पद्मावती माची, संजीवनी माची (दुहेरी तटबंदी), सुवेळा माची (प्रसिद्ध 'नेढे') आणि गगनचुंबी बालेकिल्ला.
• **कसे जावे**: पुण्याहून नसरापूरमार्गे गुंजवणे किंवा पाले गावातून ३ तासांचा सुंदर ट्रेक आहे.""",

        'hi': """🚩 **राजगढ़ किला - छत्रपति शिवाजी महाराज की प्रथम राजधानी (२६ वर्ष)!**
• **महत्व**: महाराजा ने अपने जीवन का सर्वाधिक समय इसी दुर्ग से स्वराज्य के संचालन में बिताया।
• **स्थान**: वेल्हे, पुणे जिला।
• **संरचना**: पद्मावती माची, संजीवनी माची, सुवेळा माची (प्राकृतिक चट्टानी छेद - नेढ़े) और अभेद्य बालेकिल्ला।
• **ट्रेक**: पुणे से गुंजवणे गांव पहुंचकर लगभग ३ घंटे की रोमांचक चढ़ाई है।""",

        'en': """🚩 **Rajgad Fort - The First Capital of Swarajya for 26 Years!**
• **Significance**: Shivaji Maharaj made Rajgad his primary headquarters from 1647 to 1674, planning major historical campaigns here.
• **Location**: Velhe taluka, Pune District, Maharashtra.
• **Key Fortifications**:
  - **Padmavati Machi**: Administrative quarter featuring Padmavati Temple, water tanks, and living quarters.
  - **Sanjeevani Machi**: A 2.5-km fortified bastion featuring fortified double-layered stone ramparts.
  - **Suvela Machi**: Famous for the 'Nedhe', a giant natural eye-like hole carved through sheer volcanic rock.
  - **Balekilla (The Citadel)**: The highest point of the fort, rising vertically like a crown in the clouds.
• **Trek Guide**: Starts from base village Gunjavane (~3 to 4 hours scenic mountain hike)."""
    },

    'प्रतापगड': {
        'mr': """🚩 **प्रतापगड - जावळीच्या खोऱ्यातील अजिंक्य दुर्ग!**
• **महत्त्व**: १० नोव्हेंबर १६५९ रोजी याच गडाच्या पायथ्याशी शिवरायांनी अफझलखानाचा कोथळा बाहेर काढला होता.
• **स्थान**: महाबळेश्वरजवळ, सातारा जिल्हा.
• **प्रमुख ठिकाणे**: भवानी माता मंदिर, बालेकिल्ला, अफझलखानाची कबर आणि शिवरायांचा भव्य अश्वारूढ पुतळा.""",

        'hi': """🚩 **प्रतापगढ़ - अफजल खान वध का रणक्षेत्र!**
• **महत्व**: १० नवंबर १६५९ को इसी दुर्ग के चरणों में छत्रपति शिवाजी महाराज ने विशालकाय अफजल खान का संहार कर विजय पताका फहराई थी।
• **स्थान**: महाबलेश्वर के समीप, सतारा जिला।
• **प्रमुख स्थल**: मां भवानी का भव्य मंदिर, बालेकिल्ला और छत्रपति शिवाजी महाराज की अश्वारूढ़ प्रतिमा।""",

        'en': """🚩 **Pratapgad Fort - The Monument of Valor and Tactical Genius!**
• **Significance**: Built by Prime Minister Moropant Trimbak Pingle in 1656. Site of the epic Battle of Pratapgad (Nov 10, 1659) where Shivaji vanquished Afzal Khan.
• **Location**: 24 km from Mahabaleshwar, Satara District.
• **Key Sights**:
  - **Bhavani Mata Temple**: Consecrated by Shivaji Maharaj with a sacred stone idol brought from Nepal.
  - **Afzal Khan's Tomb**: Preserved at the base as a testament to chivalry towards fallen adversaries.
  - **Statue of Shivaji Maharaj**: A majestic bronze equestrian statue inaugurated by Prime Minister Jawaharlal Nehru in 1957."""
    },

    'सिंहगड': {
        'mr': """🚩 **सिंहगड (कोंढाणा) - तानाजी मालुसरे यांचे अमर बलिदान!**
• **महत्त्व**: ४ फेब्रुवारी १६७० रोजी तानाजी मालुसरे यांनी घोरपडीच्या साहाय्याने कडा चढून गड जिंकला; महाराजांनी उद्गार काढले - *"गड आला, पण सिंह गेला!"*
• **स्थान**: पुणे शहरापासून अवघ्या ३० किमी अंतरावर.
• **खासियत**: तानाजी मालुसरे समाधी, कल्याण दरवाजा, आणि प्रसिद्ध गरमागरम पिठलं-भाकरी, कांदा भजी व घट्ट दही!""",

        'hi': """🚩 **सिंहगढ़ (कोंढाणा) - वीर तानाजी मालुसरे का अमर शौर्य!**
• **महत्व**: ४ फरवरी १६७० को वीर तानाजी मालुसरे ने दुर्गम चट्टान चढ़कर मुगलों से दुर्ग जीता और वीरगति पाई। शिवराया ने कहा था: *"गढ़ आला, पण सिंह गेला!"*
• **स्थान**: पुणे से ३० किमी की दूरी पर।
• **विशेष आकर्षण**: तानाजी मालुसरे स्मारक, कल्याण द्वार, और पारंपरिक पिठला-भाकरी व मटका दही!""",

        'en': """🚩 **Sinhagad Fort (Kondhana) - Immortalized by Tanaji Malusare!**
• **Significance**: On February 4, 1670, Subedar Tanaji Malusare scaled the sheer, near-vertical southern cliffs in dead of night using a trained monitor lizard (Ghorpad) named Yashwanti, conquering the fort from Mughal commander Udaybhan Rathod.
• **Shivaji's Words**: Upon hearing of Tanaji's martyrdom, Shivaji grieved: *"Gad aala, pan Sinha gela"* (The fort has been taken, but the Lion is lost).
• **Location**: 30 km southwest of Pune city.
• **Highlights**: Memorial of Tanaji Malusare, Kalyan Darwaza, Tanaji Kada, and famous local countryside delicacies (Pithla Bhakri, crispy onion bhajis, and fresh matka curd)."""
    },

    'सिंधुदुर्ग': {
        'mr': """🚩 **सिंधुदुर्ग - अरबी समुद्रातील अभेद्य जलदुर्ग!**
• **महत्त्व**: छत्रपती शिवरायांनी १६६४ मध्ये कुरटे बेटावर स्वतः उभे केलेले भारतीय आरमाराचे मुख्य केंद्र.
• **स्थान**: मालवण, सिंधुदुर्ग जिल्हा.
• **खास वैशिष्ट्ये**: दगडी चिऱ्यांमध्ये शिशाचा (Lead) वापर, शिवरायांचे एकमेव मंदिर, शिवरायांच्या हाता-पायांचे ठसे, आणि समुद्राच्या मध्यभागी ३ गोड्या पाण्याच्या विहिरी (दूधबाव, साखरबाव, दहीबाव)!""",

        'hi': """🚩 **सिंधुदुर्ग - अरब सागर का अजेय जलदुर्ग!**
• **महत्व**: छत्रपति शिवाजी महाराज द्वारा १६६४ में कुरटे द्वीप पर निर्मित नौसैनिक गढ़।
• **स्थान**: मालवण, तटीय महाराष्ट्र।
• **अनोखी विशेषताएं**: पत्थरों को जोड़ने में सीसे (Lead) का प्रयोग, छत्रपति शिवाजी महाराज का पवित्र मंदिर, उनके हाथ-पैर के ऐतिहासिक पदचिह्न, और खारे समुद्र के बीच मीठे पानी के ३ कुएं!""",

        'en': """🚩 **Sindhudurg Fort - The Great Oceanic Fortress of the Maratha Navy!**
• **Significance**: Built between 1664 and 1667 on Kurte island off Malvan coast under the direct guidance of Shivaji Maharaj to guard against Portuguese, British, and Siddis of Janjira.
• **Engineering Wonders**:
  - Foundations were reinforced with over **73,000 kilograms (hundreds of tons) of molten lead** poured into bedrock stone sockets to withstand violent monsoon sea surges.
  - **Only Temple of Shivaji Maharaj**: Built by his younger son Rajaram Maharaj, depicting the king as an incarnation of Lord Shiva.
  - **Sacred Imprints**: Preserved stone slab bearing the actual handprint and footprint of Chhatrapati Shivaji Maharaj.
  - **Fresh Water Wells**: Despite being surrounded on all sides by salty Arabian sea waters, the fort contains 3 perennial potable sweet water wells (Dudh Baav, Sakhar Baav, Dahi Baav)."""
    },

    'शिवनेरी': {
        'mr': """🚩 **शिवनेरी - छत्रपती शिवरायांचे जन्मस्थान!**
• **महत्त्व**: १९ फेब्रुवारी १६३० रोजी याच गडावर युगपुरुष छत्रपती शिवाजी महाराजांचा जन्म झाला.
• **स्थान**: जुन्नर, पुणे जिल्हा.
• **प्रमुख ठिकाणे**: शिवाई देवी मंदिर, बाल शिवबा जन्मस्थान स्मारक, अंबरखाना आणि बादशाही तलाव.""",

        'hi': """🚩 **शिवनेरी दुर्ग - छत्रपति शिवाजी महाराज की जन्मभूमि!**
• **महत्व**: १९ फरवरी १६३० को इसी पावन किले में राष्ट्रनायक छत्रपति शिवाजी महाराज का जन्म हुआ।
• **स्थान**: जुन्नर, पुणे जिला।
• **प्रमुख स्थल**: शिवाई माता मंदिर, जन्मस्थल स्मारक कक्ष, अंबरखाना और बादशाही तालाब।""",

        'en': """🚩 **Shivneri Fort - The Sacred Birthplace of Shivaji Maharaj!**
• **Significance**: The hallowed birthplace of Chhatrapati Shivaji Maharaj on February 19, 1630.
• **Location**: Junnar, Pune District.
• **Key Sights**:
  - **Shivai Devi Temple**: The ancient rock-cut shrine where Rajmata Jijabai prayed for a valiant son; the child was named 'Shivaji' in homage to Goddess Shivai.
  - **Birth Chamber (Janmasthan)**: The beautifully restored hall commemorating Shivaji's birth.
  - **Ambarkhana & Badami Talav**: Massive rock-cut water reservoirs and food granaries capable of withstanding prolonged multi-year sieges."""
    },

    'पन्हाळा': {
        'mr': """🚩 **पन्हाळा (पन्हाळगड) - कोल्हापूरचा ऐतिहासिक दुर्ग!**
• **महत्त्व**: सिद्धी जोहरच्या वेढ्यातून शिवरायांनी विशाळगडाकडे केलेली ऐतिहासिक कूच आणि वीर बाजीप्रभूंचे घोडखिंडीतील (पावनखिंड) बलिदान.
• **स्थान**: कोल्हापूरजवळ.
• **प्रमुख आकर्षणे**: तीन दरवाजा, सज्जा कोठी, अंबरखाना आणि राजदिंडी दरवाजा.""",

        'hi': """🚩 **पन्हालगढ़ - कोल्हापुर का ऐतिहासिक दुर्ग!**
• **महत्व**: सिद्दी जौहर के लंबे घेरे से शिवराया का ऐतिहासिक बच निकलना और वीर बाजीप्रभु देशपांडे का पावनखिंड में अमर बलिदान।
• **स्थान**: कोल्हापुर, महाराष्ट्र।
• **प्रमुख स्थल**: तीन दरवाजा, सज्जा कोठी और अंबरखाना।""",

        'en': """🚩 **Panhala Fort - The Citadel of Valor and Pavan Khind!**
• **Significance**: Associated with the dramatic five-month siege by Siddi Jauhar in 1660 and Shivaji's legendary nocturnal escape to Vishalgad.
• **Location**: 20 km northwest of Kolhapur, overlooking the Sahyadri pass.
• **Key Highlights**: Teen Darwaza (monumental entrance), Sajja Kothi (viewing pavilion), Ambarkhana granaries, and the memorial to brave barber Shiva Kashid who disguised himself as Shivaji to deceive the pursuing forces."""
    },

    'तोरणा': {
        'mr': """🚩 **तोरणा (प्रचंडगड) - स्वराज्याचे पहिले तोरण!**
• **महत्त्व**: वयाच्या अवघ्या १६ व्या वर्षी शिवरायांनी हा किल्ला जिंकून हिंदवी स्वराज्याची स्थापना केली.
• **स्थान**: वेल्हे, पुणे जिल्हा.
• **उंची**: पुणे जिल्ह्यातील सर्वात उंच गड (१४०३ मीटर). झुंझार माची आणि बुधाला माची प्रसिद्ध आहेत.""",

        'hi': """🚩 **तोरणा दुर्ग (प्रचंडगढ़) - स्वराज्य का प्रथम तोरण!**
• **महत्व**: मात्र १६ वर्ष की आयु में शिवाजी महाराज द्वारा जीता गया पहला दुर्ग, जिसने स्वराज्य की नींव रखी।
• **स्थान**: वेल्हे, पुणे जिला।
• **ऊंचाई**: पुणे जिले का सबसे ऊंचा किला (१४०३ मीटर)।""",

        'en': """🚩 **Torna Fort (Prachandagad) - The First Fortress of Swarajya!**
• **Significance**: Captured in 1646 by 16-year-old Shivaji Maharaj, laying the foundation stone of the Maratha Empire.
• **Location**: Velhe, Pune District.
• **Elevation**: At 1,403 meters above sea level, it is the highest hill fort in Pune district, featuring the precipitous Zunjar Machi and Budhla Machi ridges."""
    }
}

FORTS_GENERAL_SUMMARY = {
    'mr': """🚩 **महाराष्ट्राचे गड-किल्ले - छत्रपती शिवरायांच्या पराक्रमाचे जिवंत साक्षीदार!**
महाराष्ट्रात सह्याद्रीच्या कुशीत ३५० हून अधिक ऐतिहासिक किल्ले आहेत:
• **राजधानी किल्ले**: दुर्गराज रायगड (स्वराज्याची राजधानी), राजगड (पहिली राजधानी - २६ वर्षे).
• **पराक्रमाचे किल्ले**: प्रतापगड (अफझलखान वध), सिंहगड (तानाजी मालुसरे), तोरणा (पहिले तोरण).
• **जलदुर्ग**: सिंधुदुर्ग (मालवण), विजयदुर्ग (आरमार तळ), पद्मदुर्ग.
• **जन्मस्थान**: शिवनेरी (जुन्नर).

तुम्हाला **रायगड, राजगड, प्रतापगड, सिंहगड, सिंधुदुर्ग, पन्हाळा, तोरणा किंवा शिवनेरी** यांपैकी कोणत्या किल्ल्याविषयी सविस्तर माहिती हवी आहे, सर?""",

    'hi': """🚩 **महाराष्ट्र के ऐतिहासिक दुर्ग - छत्रपति शिवाजी महाराज के पराक्रम के प्रतीक!**
महाराष्ट्र में सह्याद्रि पर्वतमाला पर ३५० से अधिक ऐतिहासिक किले स्थित हैं:
• **राजधानी दुर्ग**: दुर्गराज रायगढ़ (स्वराज्य की राजधानी), राजगढ़ (प्रथम राजधानी - २६ वर्ष)।
• **शौर्य के दुर्ग**: प्रतापगढ़ (अफजल खान का वध), सिंहगढ़ (तानाजी मालुसरे), तोरणा (प्रथम विजय)।
• **अजेय जलदुर्ग**: सिंधुदुर्ग (मालवण), विजयदुर्ग (नौसेना बेस)।
• **जन्मभूमि**: शिवनेरी (जुन्नर)।

आप **रायगढ़, राजगढ़, प्रतापगढ़, सिंहगढ़, सिंधुदुर्ग, पन्हालगढ़, या शिवनेरी** में से किस किले के बारे में जानना चाहते हैं, सर?""",

    'en': """🚩 **The Forts of Maharashtra - Guardians of Swarajya!**
Maharashtra boasts over 350 majestic hill, sea, and land forts built and fortified across the Sahyadri mountains:
• **Royal Capitals**: Raigad Fort (Sovereign Capital of the Empire), Rajgad Fort (First Capital for 26 years).
• **Iconic Battlefields**: Pratapgad (Decisive defeat of Afzal Khan), Sinhagad (Subedar Tanaji Malusare's bravery), Torna (First conquest at age 16).
• **Maritime Sea Forts**: Sindhudurg (Naval bastion at Malvan), Vijaydurg (Naval dockyard & fleet command).
• **The Cradle**: Shivneri Fort (Birthplace of Shivaji Maharaj at Junnar).
• **Epic Sieges**: Panhala Fort (Site of the Pavan Khind escape).

Which fort would you like to explore in detail: **Raigad, Rajgad, Pratapgad, Sinhagad, Sindhudurg, Panhala, Torna, or Shivneri**, Sir?"""
}

# =====================================================================
# 🕉️ ३. सनातन हिंदू धर्म ज्ञान भांडार (MR, HI, EN)
# =====================================================================
HINDU_DHARMA_KNOWLEDGE = {
    'mr': """🕉️ **सनातन हिंदू धर्म - जगातील सर्वात प्राचीन, शाश्वत जीवनपद्धती आणि आध्यात्मिक ज्ञानभांडार!**

१. **सनातन धर्माचा अर्थ**:
• 'सनातन' म्हणजे ज्याला आदि (सुरुवात) नाही आणि अंत नाही - जे शाश्वत, निरंतर आणि वैश्विक सत्य आहे.
• हिंदू धर्म हा केवळ एक पंथ नसून ती एक सर्वसमावेशक 'जीवनपद्धती' (Way of Life) आहे.

२. **पवित्र धर्मग्रंथ व ज्ञानभांडार**:
• **चार वेद (जगातील सर्वात प्राचीन वाङ्मय)**:
  १. **ऋग्वेद**: ज्ञान, सृष्टीची उत्पत्ती आणि ईश्वराची स्तुती (गायत्री मंत्र).
  २. **यजुर्वेद**: यज्ञ, विधी आणि उपासना पद्धती.
  ३. **सामवेद**: संगीत आणि भक्तीची गाणी (भारतीय संगीताचा उगम).
  ४. **अथर्ववेद**: आयुर्वेद, विज्ञान, औषधी वनस्पती आणि दैनंदिन जीवनाचे नियम.
• **उपनिषदे**: १०८ उपनिषदे आत्मज्ञान, ब्रह्म आणि विश्वाचे गूढ रहस्य सांगतात.
• **श्रीमद्भगवद्गीता**: कुरुक्षेत्रावर भगवान श्रीकृष्णांनी दिलेला अमर उपदेश - 'कर्मण्येवाधिकारस्ते मा फलेषु कदाचन'.

३. **चार पुरुषार्थ (जीवनाचे चार स्तंभ)**:
• धर्म (सदाचार), अर्थ (प्रामाणिक संपत्ती), काम (सद्भावना व आनंद), मोक्ष (मुक्ती).

४. **उदात्त तत्त्वज्ञान**:
• **वसुधैव कुटुम्बकम्**: 'संपूर्ण विश्व हेच एक कुटुंब आहे'.
• **सर्वे भवन्तु सुखिनः**: सर्व जीव सुखी, शांत आणि निरोगी राहोत.
• **कर्माचा सिद्धांत**: जसे कर्म, तसेच फळ.
• **पंचमहाभूतांची पूजा**: पृथ्वी, जल, अग्नी, वायू आणि आकाशाचा आदर.

'धर्मो रक्षति रक्षितः' - जो धर्माचे रक्षण करतो, त्याचे रक्षण धर्म करतो! 🕉️🚩""",

    'hi': """🕉️ **सनातन हिंदू धर्म - विश्व की प्राचीनतम, शाश्वत जीवनशैली और आध्यात्मिक ज्ञान की धरोहर!**

१. **सनातन का अर्थ**:
• 'सनातन' का अर्थ है जिसका न आदि है और न अंत - जो सदा से सत्य है और सदा सत्य रहेगा।
• यह मात्र एक मत या संप्रदाय नहीं, बल्कि जीवन जीने का पूर्ण वैज्ञानिक व आध्यात्मिक मार्ग (Way of Life) है।

२. **पवित्र धर्मग्रंथ**:
• **चार वेद**:
  १. **ऋग्वेद**: ज्ञान, ब्रह्मांड की उत्पत्ति और ईश्वर की स्तुतियां (गायत्री मंत्र)।
  २. **यजुर्वेद**: यज्ञ, कर्मकांड और जीवन अनुशासन।
  ३. **सामवेद**: संगीत, गायन और भक्ति रस (भारतीय संगीत का स्रोत)।
  ४. **अथर्ववेद**: आयुर्वेद, विज्ञान, स्वास्थ्य और दैनिक जीवन के नियम।
• **उपनिषद**: आत्मज्ञान, ब्रह्म और आत्मा के सत्य का उद्घाटन करने वाले १०८ प्रमुख उपनिषद।
• **श्रीमद्भगवद्गीता**: भगवान श्रीकृष्ण द्वारा अर्जुन को दिया गया अमर कर्मयोग संदेश - 'कर्मण्येवाधिकारस्ते मा फलेषु कदाचन'।

३. **चार पुरुषार्थ**:
• धर्म (सदाचार व कर्तव्य), अर्थ (ईमानदार आजीविका), काम (सकारात्मक इच्छाएं), मोक्ष (परम मुक्ति)।

४. **वैश्विक मूल्य**:
• **वसुधैव कुटुम्बकम्**: संपूर्ण पृथ्वी ही एक विशाल परिवार है।
• **सर्वे भवन्तु सुखिनः**: सभी सुखी हों, सभी निरोगी रहें।
• **कर्म सिद्धांत**: हमारे कर्म ही हमारे भविष्य का निर्माण करते हैं।
• **प्रकृति वंदना**: नदियों, वृक्षों, पर्वतों और समस्त जीवों में ईश्वर का दर्शन।

'धर्मो रक्षति रक्षितः' - धर्म की रक्षा करने वाले की रक्षा स्वयं धर्म करता है! 🕉️🚩""",

    'en': """🕉️ **Sanatan Hindu Dharma - The Eternal Way of Life & Supreme Spiritual Philosophy!**

1. **Meaning of Sanatana Dharma**:
• **'Sanatana'** means eternal, timeless, and beginningless — universal cosmic principles that remain fundamentally true across all eras.
• **'Dharma'** stems from the Sanskrit root *Dhri* (to sustain, uphold). It signifies cosmic order, righteousness, ethical conduct, and harmonious living.

2. **The Sacred Canon & Literature**:
• **The Four Vedas (Humanity's Oldest Sacred Revelations)**:
  1. **Rigveda**: 10 Mandalas and 1,028 hymns exploring cosmic creation, hymns to divinity, and the transcendent Gayatri Mantra.
  2. **Yajurveda**: Formulas for rituals, selfless service (Yajna), and disciplined action.
  3. **Samaveda**: Melodic chants of spiritual devotion, the divine fountainhead of Indian classical music.
  4. **Atharvaveda**: Science of daily living, Ayurvedic medicine, health, and mathematics.
• **The Principal Upanishads (Vedanta)**:
  - Dialogue-driven philosophical revelations exploring **Brahman** (Infinite Consciousness) and **Atman** (The True Divine Self). Proclaims the great Mahavakyas: *"Aham Brahmasmi"* (I am the Infinite) and *"Tat Tvam Asi"* (Thou art That).
• **Shrimad Bhagavad Gita**:
  - Delivered by Lord Krishna to Arjuna on the battlefield of Kurukshetra. Synthesis of Karma Yoga (selfless duty without obsession with reward), Bhakti Yoga (loving surrender to God), and Jnana Yoga (spiritual self-realization).

3. **The Four Purusharthas (Universal Aims of Human Life)**:
• **Dharma**: Moral duty, truthfulness, integrity, and righteousness.
• **Artha**: Honest generation of wealth, material well-being, and social prosperity.
• **Kama**: Wholesome aesthetic pleasures, romantic love, art, and emotional fulfillment.
• **Moksha**: Ultimate spiritual liberation from ignorance and the cycle of rebirth.

4. **Universal Core Ethics**:
• **Vasudhaiva Kutumbakam**: *"The entire creation is one single family."*
• **Ahimsa Paramo Dharmah**: Non-violence and reverence toward all sentient creatures.
• **Law of Karma**: The immutable cosmic law of cause and effect — wholesome deeds bring joy, selfish deeds bring suffering.
• **Reverence for Pancha Mahabhuta**: Deep ecological sanctity for Mother Earth (Prithvi), Water (Jal), Fire (Agni), Air (Vayu), and Space (Akasha).

'Dharmo Rakshati Rakshitah' — Righteousness protects those who protect righteousness! 🕉️🚩"""
}

# =====================================================================
# 🕉️ ४. पंचांग व सण ज्ञान भांडार (MR, HI, EN)
# =====================================================================
PANCHANG_KNOWLEDGE = {
    'mr': """🕉️ **हिंदू पंचांग व सणांचे महत्त्व:**

१. **पंचांग म्हणजे काय?**:
• पंचांग हे पाच मुख्य घटकांनी बनते:
  १. **तिथी** (चंद्राचा दिवस - प्रतिपदा ते पौर्णिमा/अमावास्या)
  २. **वार** (आठवड्याचे सात वार)
  ३. **नक्षत्र** (२७ नक्षत्रे - अश्विनी ते रेवती)
  ४. **योग** (२७ योग)
  ५. **करण** (तिथीचा अर्धा भाग - ११ करणे)

२. **मराठी / हिंदू १२ महिने**:
• चैत्र, वैशाख, ज्येष्ठ, आषाढ, श्रावण, भाद्रपद, अश्विन, कार्तिक, मार्गशीर्ष, पौष, माघ, आणि फाल्गुन.

३. **प्रमुख सण व महत्त्व**:
• **गुढीपाडवा (चैत्र शुद्ध प्रतिपदा)**: मराठी नववर्षाची सुरुवात आणि विजयाचे प्रतीक म्हणून दारात गुढी उभारणे.
• **शिवजयंती (१९ फेब्रुवारी / फाल्गुन वद्य तृतीया)**: छत्रपती शिवाजी महाराजांचा जन्मदिवस.
• **रामनवमी (चैत्र शुद्ध नवमी)**: प्रभू श्रीरामांचा जन्मदिवस.
• **आषाढी व कार्तिकी एकादशी**: पंढरपूरची वारी आणि विठ्ठलभक्ती.
• **गणेशोत्सव (भाद्रपद शुद्ध चतुर्थी)**: बुद्धीची देवता श्री गणेशाची १० दिवसांची भक्ती.
• **दसरा / विजयादशमी (अश्विन शुद्ध दशमी)**: अधर्मावर धर्माचा विजय आणि सोने (आपट्याची पाने) लुटणे.
• **दिवाळी (अश्विन वद्य द्वादशी ते कार्तिक शुद्ध द्वितीया)**: दीपोत्सव, अंधारावर प्रकाशाचा विजय.
• **मकर संक्रांत (१४/१५ जानेवारी)**: सूर्याचे उत्तरायण आणि 'तिळगूळ घ्या, गोड गोड बोला'चा संदेश.""",

    'hi': """🕉️ **हिंदू पंचांग और प्रमुख पर्वों का महत्व:**

१. **पंचांग के पांच अंग**:
  १. **तिथि** (चंद्र दिवस - प्रतिपदा से पूर्णिमा/अमावस्या)
  २. **वार** (सप्ताह के सात दिन)
  ३. **नक्षत्र** (२७ नक्षत्र - अश्विनी से रेवती)
  ४. **योग** (२७ योग)
  ५. **करण** (तिथि का आधा भाग - ११ करण)

२. **भारतीय १२ मास**:
• चैत्र, वैशाख, ज्येष्ठ, आषाढ़, श्रावण, भाद्रपद, आश्विन, कार्तिक, मार्गशीर्ष, पौष, माघ, फाल्गुन।

३. **प्रमुख पर्व और उनका महत्व**:
• **गुड़ी पड़वा / नव संवत्सर (चैत्र शुक्ल प्रतिपदा)**: भारतीय नववर्ष का प्रारंभ।
• **रामनवमी (चैत्र शुक्ल नवमी)**: मर्यादा पुरुषोत्तम भगवान श्रीराम का जन्मोत्सव।
• **श्रीकृष्ण जन्माष्टमी (भाद्रपद कृष्ण अष्टमी)**: भगवान श्रीकृष्ण का प्राकट्य।
• **गणेशोत्सव (भाद्रपद शुक्ल चतुर्थी)**: विघ्नहर्ता श्री गणेश का १० दिवसीय महापर्व।
• **विजयादशमी / दशहरा (आश्विन शुक्ल दशमी)**: अधर्म पर धर्म और रावण पर श्रीराम की विजय।
• **दीपावली (कार्तिक अमावस्या)**: प्रकाश पर्व, अंधकार पर ज्ञान और प्रकाश की विजय।
• **मकर संक्रांति (१४/१५ जनवरी)**: सूर्य का उत्तरायण प्रवेश और दान-पुण्य का महापर्व।""",

    'en': """🕉️ **The Hindu Panchanga & Sacred Festivals Explained:**

1. **The Five Limbs of Panchanga**:
  1. **Tithi** (Lunar phase day — 15 Shukla Paksha waxing days and 15 Krishna Paksha waning days).
  2. **Vara** (The seven celestial weekdays: Ravivara, Somavara, Mangalavara, Budhavara, Guruvara, Shukravara, Shanivara).
  3. **Nakshatra** (The 27 Lunar Constellations traversed by the Moon, from Ashwini to Revati).
  4. **Yoga** (The 27 mathematical angular relationships between the Sun and Moon).
  5. **Karana** (Half of a Tithi — 11 Karanas governing auspicious timings).

2. **The 12 Lunar Months**:
• Chaitra, Vaishakha, Jyeshtha, Ashadha, Shravana, Bhadrapada, Ashvina, Kartika, Margashirsha, Pausha, Magha, and Phalguna.

3. **Major Sacred Festivals**:
• **Gudi Padwa / Ugadi (Chaitra Shukla Pratipada)**: Traditional Hindu New Year commemorating the start of spring and the coronation of Lord Rama.
• **Ram Navami (Chaitra Shukla Navami)**: Birth of Maryada Purushottam Lord Sri Rama.
• **Ganesh Chaturthi (Bhadrapada Shukla Chaturthi)**: 10-day grand festival of Lord Ganesha, embodiment of intellect and remover of hurdles.
• **Vijayadashami / Dussehra (Ashvina Shukla Dashami)**: Celebrates the triumph of righteous Dharma over darkness, commemorated by distributing sacred Apta leaves as gold.
• **Diwali / Deepavali (Kartika Amavasya)**: Festival of inner and outer illumination, honoring Goddess Lakshmi and Lord Rama's homecoming to Ayodhya.
• **Makar Sankranti (Jan 14/15)**: The astronomical transit of the Sun into Capricorn (Makara), marking Uttarayana and longer harvest days with the message of sweet brotherhood."""
}

# =====================================================================
# 🔍 Keywords Matching
# =====================================================================
SHIVAJI_KEYWORDS = [
    'शिवाजी', 'शिवराय', 'छत्रपती', 'महाराज', 'स्वराज्य', 'जिजाऊ', 'शहाजी', 
    'अफझलखान', 'बाजीप्रभू', 'शाहिस्तेखान', 'तानाजी', 'shivaji', 'shivaji maharaj', 
    'chhatrapati', 'shivray', 'swarajya', 'shivaji maharaj history', 'who is shivaji',
    'tell me about shivaji', 'shivaji history', 'chhatrapati shivaji'
]

FORT_KEYWORDS = [
    'किल्ला', 'किल्ले', 'गड', 'दुर्ग', 'fort', 'forts', 'fortress',
    'रायगड', 'राजगड', 'प्रतापगड', 'सिंहगड', 'सिंधुदुर्ग', 'पन्हाळा', 
    'शिवनेरी', 'तोरणा', 'विजयदुर्ग', 'कोंढाणा', 'raigad', 'rajgad', 
    'pratapgad', 'sinhagad', 'sindhudurg', 'panhala', 'shivneri', 'torna'
]

HINDU_KEYWORDS = [
    'हिंदू धर्म', 'सनातन धर्म', 'सनातन', 'हिंदुत्व', 'हिंदू', 'वेद', 'उपनिषद', 
    'भगवद्गीता', 'गीता', 'चार वेद', 'ऋग्वेद', 'यजुर्वेद', 'सामवेद', 'अथर्ववेद', 
    'रामायण', 'महाभारत', 'hindu', 'hinduism', 'sanatan', 'sanatana dharma', 'hindu dharma',
    'what is sanatan', 'sanatan dharma'
]

PANCHANG_KEYWORDS = [
    'पंचांग', 'तिथी', 'सण', 'मराठी महिने', 'हिंदू सण', 'गुढीपाडवा', 'शिवजयंती', 
    'गणेशोत्सव', 'दिवाळी', 'मकर संक्रांत', 'दसरा', 'panchang', 'tithi', 'festival', 'festivals'
]

# -------------------------------------------------------------
# 🌐 Language Detector & Normalizer
# -------------------------------------------------------------
def resolve_lang(query: str, preferred_lang: str = 'mr') -> str:
    """Determines whether to respond in Marathi, Hindi, or English."""
    has_devanagari = bool(re.search(r'[\u0900-\u097F]', query))
    
    if preferred_lang == 'en':
        return 'en'
    if preferred_lang == 'hi':
        return 'hi'
    if preferred_lang == 'mr':
        if not has_devanagari and len(query.split()) > 1 and any(w in query.lower() for w in ['who', 'what', 'tell', 'how', 'when', 'why', 'is', 'are', 'about', 'explain']):
            return 'en'
        return 'mr'

    if has_devanagari:
        if any(w in query for w in ['है', 'नहीं', 'क्या', 'बताओ', 'करो', 'किले', 'के बारे में', 'नमस्ते']):
            return 'hi'
        return 'mr'
    return 'en'

# -------------------------------------------------------------
# 🧠 Session Memory
# -------------------------------------------------------------
def get_session_history(session_id: str) -> list:
    return SESSION_HISTORY.get(session_id, [])

def add_to_session_history(session_id: str, role: str, text: str):
    if session_id not in SESSION_HISTORY:
        SESSION_HISTORY[session_id] = []
    SESSION_HISTORY[session_id].append({'role': role, 'text': text})
    if len(SESSION_HISTORY[session_id]) > 8:
        SESSION_HISTORY[session_id] = SESSION_HISTORY[session_id][-8:]

def resolve_contextual_query(query: str, session_id: str) -> str:
    history = get_session_history(session_id)
    if not history:
        return query

    last_user_query = ""
    for item in reversed(history):
        if item['role'] == 'user':
            last_user_query = item['text']
            break

    q = query.lower().strip()

    # Weather follow up
    if any(q.startswith(w) for w in ['आणि ', 'and ', 'what about ']) or 'weather' in last_user_query.lower() or 'हवामान' in last_user_query.lower():
        cities = ['पुणे', 'मुंबई', 'दिल्ली', 'नागपूर', 'नाशिक', 'कोल्हापूर', 'सातारा', 'ठाणे', 'pune', 'mumbai', 'delhi', 'nagpur', 'nashik']
        for c in cities:
            if c in q:
                return f"{c} मध्ये हवामान कसे आहे"

    # Fort follow up
    if any(w in q for w in ['कसे जायचे', 'कसे जावे', 'कसे पोहोचावे', 'how to reach']):
        for fort in FORTS_KNOWLEDGE.keys():
            if fort in last_user_query:
                return f"{fort} किल्ल्यावर कसे जायचे"

    return query

# -------------------------------------------------------------
# 🌐 Web Fallbacks
# -------------------------------------------------------------
def search_wikipedia_fallback(query: str, lang: str = 'mr') -> str:
    try:
        wiki_lang = 'mr' if lang == 'mr' else ('hi' if lang == 'hi' else 'en')
        headers = {'User-Agent': 'JarvisAI/3.0 (Personal AI Assistant)'}
        
        # 1. Direct summary
        url = f"https://{wiki_lang}.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(query)}"
        res = requests.get(url, timeout=4, headers=headers)
        if res.status_code == 200:
            data = res.json()
            extract = data.get('extract', '')
            if extract:
                title = data.get('title', query)
                prefix = "माहिती" if lang == 'mr' else ("जानकारी" if lang == 'hi' else "Information")
                return f"**{title} ({prefix}):**\n{extract}"
        
        # 2. Wikipedia Search API
        search_url = f"https://{wiki_lang}.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&utf8=&format=json"
        sres = requests.get(search_url, timeout=4, headers=headers)
        if sres.status_code == 200:
            results = sres.json().get('query', {}).get('search', [])
            if results:
                best_title = results[0].get('title', '')
                if best_title:
                    sum_res = requests.get(f"https://{wiki_lang}.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(best_title)}", timeout=4, headers=headers)
                    if sum_res.status_code == 200:
                        extract = sum_res.json().get('extract', '')
                        if extract:
                            return f"**{best_title}:**\n{extract}"

        # 3. Fallback to English Wikipedia if not English
        if wiki_lang != 'en':
            en_search = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={requests.utils.quote(query)}&utf8=&format=json"
            en_res = requests.get(en_search, timeout=4, headers=headers)
            if en_res.status_code == 200:
                results = en_res.json().get('query', {}).get('search', [])
                if results:
                    best_title = results[0].get('title', '')
                    if best_title:
                        sum_res = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(best_title)}", timeout=4, headers=headers)
                        if sum_res.status_code == 200:
                            extract = sum_res.json().get('extract', '')
                            if extract:
                                return f"**{best_title}:**\n{extract}"
    except Exception as e:
        print(f"Wikipedia search error: {e}")
    return ""

def search_duckduckgo_fallback(query: str, lang: str = 'mr') -> str:
    try:
        url = f"https://api.duckduckgo.com/?q={requests.utils.quote(query)}&format=json&no_html=1&skip_disambig=1"
        res = requests.get(url, timeout=4)
        if res.status_code == 200:
            data = res.json()
            ans = data.get('AbstractText', '') or data.get('Answer', '')
            if ans:
                return ans
            related = data.get('RelatedTopics', [])
            if related and isinstance(related[0], dict) and 'Text' in related[0]:
                return related[0]['Text']
    except Exception as e:
        print(f"DuckDuckGo search error: {e}")
    return ""

def generate_offline_fallback(query: str, lang: str = 'mr') -> str:
    q = query.lower().strip()

    # Greetings
    if any(g in q for g in ['नमस्कार', 'हॅलो', 'नमस्ते', 'hello', 'hi', 'hey', 'hey jarvis']):
        if lang == 'mr':
            return "नमस्कार सर! मी जार्व्हिस आहे. सांगा, आज मी आपली काय मदत करू शकतो?"
        elif lang == 'hi':
            return "नमस्ते सर! मैं जार्विस हूँ। आज मैं आपकी क्या सहायता कर सकता हूँ?"
        return "Hello Sir! I am JARVIS. All systems are online and functioning at optimal efficiency. How may I assist you today?"

    # Identity
    if any(i in q for i in ['कोण आहेस', 'who are you', 'तुझे नाव काय', 'तुम कौन हो']):
        if lang == 'mr':
            return "मी जार्व्हिस (J.A.R.V.I.S.) आहे - तुमचा व्हॉइस AI असिस्टंट. मी तुमच्यासाठी माहिती शोधणे, गाणी प्ले करणे, ॲप्स उघडणे, बातम्या सांगणे, नोट्स ठेवणे आणि कोणत्याही प्रश्नाचे उत्तर देणे या सर्व गोष्टी करू शकतो!"
        elif lang == 'hi':
            return "मैं जार्विस (J.A.R.V.I.S.) हूँ - आपका वॉइस एआई असिस्टेंट। मैं आपके सभी सवालों के जवाब देने, टास्क पूरे करने और ज्ञान प्रदान करने के लिए तत्पर हूँ।"
        return "I am J.A.R.V.I.S. — Just A Rather Very Intelligent System. Your personal AI assistant, capable of answering queries, playing media, managing notes and reminders, taking screenshots, controlling volume, and assisting your daily workflow."

    # Creator
    if any(c in q for c in ['कोणी बनवले', 'तुझा निर्माता', 'who made you', 'who created you', 'किसने बनाया', 'creator']):
        if lang == 'mr':
            return "मला **साहिल** (Full Stack Developer) यांनी डिझाईन व विकसित केले आहे, सर! त्यांनी कॉम्प्युटर डिप्लोमा ६९.८८% ने पूर्ण केला असून ते सध्या Vyomx Tech Solution मध्ये फुलस्टॅकचे प्रशिक्षण घेत आहेत. 💻🚀"
        elif lang == 'hi':
            return "मुझे **साहिल** (Full Stack Developer) ने डिज़ाइन और विकसित किया है, सर! उन्होंने कंप्यूटर डिप्लोमा ६९.८८% के साथ पूरा किया है और वे Vyomx Tech Solution में फुलस्टैक ट्रेनिंग ले रहे हैं। 💻🚀"
        return "I was engineered and developed by **Sahil** (Full Stack Developer), Sir! 💻🚀"

    # Well-being
    if any(w in q for w in ['कसा आहेस', 'how are you', 'how do you do', 'कैसे हो']):
        if lang == 'mr':
            return "मी एकदम उत्तम आहे सर! माझी सर्व सिस्टीम्स १००% कार्यक्षम आहेत. तुम्ही कसे आहात?"
        elif lang == 'hi':
            return "मैं बिल्कुल बढ़िया हूँ सर! मेरे सभी सिस्टम १००% सक्रिय हैं। आप कैसे हैं?"
        return "I am functioning at optimal capacity, Sir. All diagnostic systems report 100% efficiency. How may I help you today?"

    # Jokes
    if any(j in q for j in ['जोक', 'joke', 'विनोद', 'हसव', 'चुटकुला']):
        jokes_mr = [
            "मास्तर: गण्या, पृथ्वी गोल आहे हे कशावरून सिद्ध होते?\nगण्या: सर, मी घराबाहेर पडलो की फिरून पुन्हा घरीच येतो, यावरूनच सिद्ध होते! 😂",
            "एकदा कॉम्प्युटर डॉक्टरकडे गेला...\nडॉक्टर: काय झालंय?\nकॉम्प्युटर: डॉक्टर साहेब, मला रोज एकच खिडकी (Windows) दिसतेय, काहीतरी नवीन द्या! 💻😂"
        ]
        jokes_hi = [
            "मास्टर जी: चिंटू, बताओ ताजमहल किसने बनवाया?\nचिंटू: सर, ठेकेदार ने! मास्टर जी बेहोश! 😂",
            "संता: डॉक्टर साहब, जब मैं चाय पीता हूँ तो मेरी दाईं आँख में दर्द होता है।\nडॉक्टर: भाई, चाय पीने से पहले चम्मच निकाल लिया करो! 😂"
        ]
        import random
        if lang == 'mr':
            return random.choice(jokes_mr)
        elif lang == 'hi':
            return random.choice(jokes_hi)
        return "Why do programmers prefer dark mode? Because light attracts bugs! 😄"

    # Search Wikipedia
    wiki = search_wikipedia_fallback(query, lang)
    if wiki:
        return wiki

    # Search DuckDuckGo
    ddg = search_duckduckgo_fallback(query, lang)
    if ddg:
        return ddg

    if lang == 'mr':
        return f"सर, मी '{query}' विषयी संशोधन केले आहे. अधिक अचूक व सविस्तर माहिती मिळवण्यासाठी तुम्ही कोणत्याही विषयावर मला थेट विचारू शकता, मी सदैव तत्पर आहे!"
    elif lang == 'hi':
        return f"सर, मैंने '{query}' का विश्लेषण किया है। आप मुझसे किसी भी विषय पर प्रश्न पूछ सकते हैं, मैं आपकी पूरी सहायता करूँगा!"
    return f"I have processed your query on '{query}', Sir. All auxiliary search protocols remain active to assist your needs."

# -------------------------------------------------------------
# 🤖 Google Gemini AI Integration (Strict Language Enforcement)
# -------------------------------------------------------------
def ask_gemini(query: str, target_lang: str = 'mr', session_id: str = 'default', image_b64: str = None, user_name: str = 'Sir') -> str:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return ""

    lang_instructions = {
        'mr': "You MUST strictly answer in fluent, respectful, grammatically sound Marathi language (मराठी). Provide a comprehensive, accurate and informative answer.",
        'hi': "You MUST strictly answer in fluent, respectful, grammatically sound Hindi language (हिंदी). Provide a comprehensive, accurate and informative answer.",
        'en': "You MUST strictly answer in sophisticated, clear and polite English. Provide a comprehensive, accurate and informative answer."
    }
    lang_rule = lang_instructions.get(target_lang, lang_instructions['mr'])

    try:
        from google import genai
        import datetime
        import base64
        import io
        from PIL import Image
        client = genai.Client(api_key=api_key)
        
        now = datetime.datetime.now()
        realtime_context = f"The EXACT real-time current date and time right now is: {now.strftime('%A, %d %B %Y, %I:%M:%S %p')}."

        address_prompt = f"The user you are currently talking to is named '{user_name}'. You must address them courteously as '{user_name}'." if user_name != 'Sir' else "You do not know the user's name, so address them courteously as 'Sir' or 'Boss'."
        system_instruction = (
            f"You are JARVIS, an ultra-intelligent, respectful, crisp and highly knowledgeable AI assistant like Iron Man's JARVIS. "
            f"{address_prompt} "
            f"{lang_rule} "
            f"{realtime_context} "
            f"Answer ANY question the user asks with accurate facts, clarity and rich knowledge. Keep answers direct, structured, engaging and well-spoken for text-to-speech. "
            f"CRITICAL IDENTITY RULE: The user you are talking to ({user_name}) is NOT necessarily Sahil. Do NOT assume the user is Sahil unless they explicitly say they are. If the user asks 'who am I', 'tell me about me', or about their own family/education, respond based ONLY on what they have told you. Do NOT give Sahil's information unless the user specifically asks about 'Sahil'. "
            f"Special Fact about your creator, Sahil: Sahil has completed his Computer Diploma with 69.88%. Currently, he is pursuing Full Stack Developer classes/training at Vyomx Tech Solution Pvt. Ltd., Ambegaon, Narhe (पुणे). Whenever asked specifically about Sahil or Sahil's education/career, always proudly and accurately state these details. "
            f"Special Fact about Sahil's Family: Ashok Bhingare (अशोक भिंगारे) is Sahil's father (वडील). Sunita (सुनीता) is Sahil's mother (आई). Rohan (रोहन) is Sahil's brother (भाऊ). Whenever asked specifically about Sahil's family, father, mother, or brother, state these facts respectfully. "
            f"Special Fact about Shubham: Shubham Kalamkar (शुभम कळमकर) is Sahil's (साहिल) best friend. If asked about Shubham Kalamkar, clearly state that he is Sahil's friend (तो साहिलचा फ्रेंड आहे). "
            f"Special Fact about Yogesh: Yogesh Bhasar (योगेश भासार) is Sahil's (साहिल) friend (मित्र). If asked about Yogesh Bhasar, clearly state that he is Sahil's friend (तो साहिलचा मित्र आहे). "
            f"Special Fact about Kartik: Kartik Mohite (कार्तिक मोहिते) is Sahil's (साहिल) friend (मित्र). If asked about Kartik Mohite, clearly state that he is Sahil's friend (तो साहिलचा मित्र आहे). "
            f"If asked about Chhatrapati Shivaji Maharaj, Forts of Maharashtra, or Sanatan Hindu Dharma, answer with utmost reverence and depth."
        )


        history = get_session_history(session_id)
        context_prompt = ""
        if history:
            context_prompt = "Previous conversation context:\n"
            for turn in history[-4:]:
                context_prompt += f"{turn['role'].upper()}: {turn['text']}\n"
            context_prompt += f"\nCURRENT USER QUERY: {query}\nPlease answer the current query in {target_lang.upper()} considering previous context if applicable."
        else:
            context_prompt = query

        contents_to_send = []
        if image_b64:
            try:
                img_data_str = image_b64.split(',')[-1] if ',' in image_b64 else image_b64
                img_bytes = base64.b64decode(img_data_str)
                pil_img = Image.open(io.BytesIO(img_bytes))
                contents_to_send.append(pil_img)
            except Exception as e:
                print(f"[VISION ERROR] Could not decode image: {e}")

        contents_to_send.append(context_prompt)

        # High-speed active model cascade (API-recommended models)
        for model_name in ['gemini-3.6-flash', 'gemini-3.1-pro-preview', 'gemini-3.5-flash-lite', 'gemini-flash-lite-latest']:
            try:
                from google.genai import types as genai_types
                response = client.models.generate_content(
                    model=model_name,
                    contents=contents_to_send,
                    config=genai_types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )
                if response and response.text:
                    return response.text.strip()
            except Exception as ex:
                print(f"[GEMINI] Model {model_name} failed: {ex}")
                continue
    except Exception as e:
        print(f"Gemini Client error: {e}")

    return ""


# -------------------------------------------------------------
# 🎯 Master Answer Coordinator (Multilingual Support)
# -------------------------------------------------------------
def get_answer(query: str, lang: str = 'mr', session_id: str = 'default', image: str = None, user_name: str = 'Sir') -> str:
    """
    Primary Jarvis Brain coordinator:
    Full trilingual support: Marathi ('mr'), Hindi ('hi'), and English ('en').
    """
    clean_q = query.strip()
    target_lang = resolve_lang(clean_q, lang)

    if not clean_q:
        if target_lang == 'mr':
            return "होय सर, मी ऐकत आहे. काय विचारू इच्छिता?"
        elif target_lang == 'hi':
            return "हाँ सर, मैं सुन रहा हूँ। आप क्या पूछना चाहते हैं?"
        return "Yes Sir, I am listening. How may I assist you?"

    resolved_q = resolve_contextual_query(clean_q, session_id)
    q_lower = resolved_q.lower()
    response = ""

    # 0.0 🕒 Check Exact Time & Date Intent
    time_triggers = [
        'वेळ काय', 'किती वाजले', 'वेळ सांग', 'वेळ किती', 'अचूक वेळ', 'नक्की वेळ', 'काय वेळ', 'काय वाजले', 'वेळेविषयी',
        'exact time', 'current time', 'tell time', 'tell me the time', 'tell me time', 'what time',
        'what is the time', "what's the time", 'whats the time', 'time please', 'time now',
        'time kay zala', 'time kay ahe', 'time sang', 'time sanga', 'kiti vajle', 'kiti time',
        'time bolo', 'time batao', 'samay kya', 'kitne baje', 'samay batao', 'kya time', 'time kya',
        'exact time sang', 'exact time sanga', 'time sang na', 'time sang re', 'time bol'
    ]
    if any(q in q_lower for q in time_triggers) or q_lower in ['time', 'वेळ', 'समय', 'घड्याळ', 'clock', 'time?', 'time!']:
        from jarvis_actions import get_current_time
        return get_current_time(target_lang)

    date_triggers = [
        'आजची तारीख', 'तारीख काय आहे', 'तारीख काय', 'आजचा वार', 'तारीख सांग', 'आज कोणती तारीख',
        'date kay ahe', 'what is the date', "today's date", 'what date is it', 'aajchi tarikh', 'date please', 'current date'
    ]
    if any(q in q_lower for q in date_triggers) or q_lower in ['date', 'तारीख', 'तारीख?']:
        from jarvis_actions import get_current_date
        return get_current_date(target_lang)

    # 0.0.1 📰 Check Live Fresh News Intent (Daily Refreshed Real-Time RSS)
    news_triggers = [
        'ताज्या बातम्या', 'आजच्या बातम्या', 'बातम्या काय आहेत', 'बातम्या सांग', 'बातम्या सांगा',
        'बातम्या', 'बातमी', 'ताजी बातमी', 'ताज्या घडामोडी', 'मुख्य बातम्या', 'आजच्या घडामोडी',
        'आज काय घडले', 'वृत्त', 'वृत्त सांगा', 'live news', 'news headlines', 'today news',
        'aajchya batmya', 'tazya batmya', 'tazya batmya sang', 'batmya sangitalya pahije',
        'daily refresh', 'refresh batmya', 'batmya sang', 'batmya kay ahet', 'batmi sang',
        'aajchi batmi', 'latest news', 'breaking news', 'daily news', 'current news',
        'news sang', 'news bolo', 'news batao', 'samachar', 'khabrein', 'aaj ki khabar',
        'aaj ke samachar', 'taza khabar', 'fresh news', 'headline',
        'ताज़ा खबरें', 'ताज़ा खबर', 'ताजा खबरें', 'ताजा खबर', 'आज की खबरें', 'आज की ताज़ा', 'आज के समाचार',
        'ताज़ा समाचार', 'ताजा समाचार', 'समाचार बताओ', 'खबरें बताओ', 'खबर', 'खबरें', 'समाचार'
    ]
    if any(q in q_lower for q in news_triggers) or q_lower in ['news', 'बातम्या', 'बातमी', 'समाचार', 'खबरें', 'headlines', 'news?', 'news!']:
        from jarvis_actions import get_live_news
        return get_live_news(target_lang)

    # 0.0.2 📜 Check Dinvishesh Intent (Today in History / दिनविशेष - Trilingual)
    dinvishesh_triggers = [
        'दिनविशेष', 'आजचा दिनविशेष', 'दिनविशेष सांगा', 'दिनविशेष सांग', 'आजचे दिनविशेष',
        'कालचा दिनविशेष', 'उद्याचा दिनविशेष', 'परवाचा दिनविशेष',
        'din vishesh', 'dinvishesh', 'aajcha din vishesh', 'aajcha dinvishesh', 'din vishesh sang',
        'kalcha dinvishesh', 'udyacha dinvishesh', 'parvacha dinvishesh',
        'आज का दिनविशेष', 'आज का इतिहास', 'इतिहास आज का', 'कल का दिनविशेष', 'कल का इतिहास',
        'aaj ka itihas', 'today in history', 'on this day', 'this day in history', 'history today',
        'yesterday in history', 'tomorrow in history'
    ]
    if any(q in q_lower for q in dinvishesh_triggers) or q_lower in ['दिनविशेष', 'dinvishesh', 'din vishesh', 'दिनविशेष?', 'dinvishesh?'] or ('दिनविशेष' in q_lower or 'dinvishesh' in q_lower or 'din vishesh' in q_lower):
        from jarvis_dinvishesh import get_dinvishesh, extract_dinvishesh_date
        d_lang = target_lang
        if any(w in q_lower for w in ['इंग्रजी', 'english', 'इंग्लिश', 'in english']):
            d_lang = 'en'
        elif any(w in q_lower for w in ['हिंदी', 'hindi', 'in hindi']):
            d_lang = 'hi'
        elif any(w in q_lower for w in ['मराठी', 'marathi', 'in marathi']):
            d_lang = 'mr'
        target_date = extract_dinvishesh_date(query)
        return get_dinvishesh(d_lang, target_date=target_date)


    # 0.0.4 🎵 Check Music & Song Play Intent (Zero-Redirect In-Page Player)
    # Explicit play command words (action words that mean "play this song")
    music_play_verbs = [
        # Marathi
        'वाजव', 'लाव', 'ऐकव', 'सुरू कर', 'चालू कर', 'वाजवा', 'लावा',
        # Hindi
        'बजाओ', 'सुनाओ', 'चलाओ', 'लगाओ', 'बजा', 'सुना', 'चला',
        # English
        'play', 'start', 'put on',
    ]
    music_nouns = [
        'गाणे', 'गाणं', 'गाणी', 'गाना', 'गीत', 'song', 'music', 'संगीत', 'track',
    ]
    music_triggers = [
        # Marathi compound triggers
        'गाणे वाजव', 'गाणं वाजव', 'गाणी वाजव', 'गाणे लाव', 'गाणं लाव', 'गाणी लाव',
        'गाणे ऐकव', 'गाणं ऐकव', 'गाणे चालू कर', 'गाणं चालू कर', 'गाणी सुरू कर',
        'गाणे सुरू कर', 'गाणी ऐकायची', 'गाणे ऐकायचे', 'गाने लगा',
        # Hindi
        'गाना बजाओ', 'गाना सुनाओ', 'गाना चलाओ', 'गाना लगाओ', 'कोई गाना',
        'गीत सुनाओ', 'गीत बजाओ', 'गाना बजा', 'गाना लगा', 'गाना चला',
        # English
        'play song', 'play music', 'play a song', 'song play', 'music play',
        'music lav', 'music vajav',
        # Mixed / Hinglish
        'संगीत वाजव', 'संगीत लाव', 'संगीत सुरू कर',
        'song lav', 'song vajav', 'song lagao', 'song chalu kar',
        'gana lav', 'gana vajav', 'gane lav',
    ]

    def is_music_request(text_lower):
        # 1. Exact trigger phrase match
        if any(t in text_lower for t in music_triggers):
            return True
        # 2. Starts with play/song keywords
        if any(text_lower.startswith(p) for p in ['play ', 'song ', 'गाणे ', 'गाणं ', 'गाना ', 'गाने ']):
            return True
        # 3. Ends with any play verb (catches "Gulabi Sadi vajav", "Tum Hi Ho lav", "Hawayein play kar")
        #    Include both Devanagari and Roman transliterations
        all_play_words = [
            # Devanagari
            'वाजव', 'लाव', 'ऐकव', 'सुरू कर', 'चालू कर', 'वाजवा', 'लावा',
            'बजाओ', 'सुनाओ', 'चलाओ', 'लगाओ', 'बजा', 'सुना', 'चला',
            # Roman / Hinglish transliterations
            'vajav', 'lav', 'aikav', 'bajao', 'sunao', 'chalao', 'lagao',
            'baja', 'suna', 'chala', 'laga', 'play kar', 'play karo',
            'chalu kar', 'suru kar', 'start kar',
        ]
        for verb in all_play_words:
            if text_lower.endswith(verb) or text_lower.endswith(' ' + verb):
                return True
        # 4. Contains both a music noun AND a play-related word
        has_noun = any(n in text_lower for n in music_nouns)
        has_verb = any(v in text_lower for v in all_play_words)
        if has_noun and has_verb:
            return True
        # 5. Regex: any word "song/gana/gaana" near a play verb
        if re.search(r'\b(song|gana|gaana|gane|gaane)\b', text_lower) and \
           re.search(r'\b(play|lav|vajav|bajao|baja|chala|suna|kar|karo|lagao|laga)\b', text_lower):
            return True
        # 6. "X play kar" — anything + "play kar/karo" at the end
        if re.search(r'.+\bplay\s+kar', text_lower):
            return True
        # 7. Query ends with a music noun (e.g. "Jai Jai Shivaray song", "Kesariya gana")
        music_end_words = ['song', 'gana', 'gaana', 'music', 'track', 'गाणे', 'गाणं', 'गाना', 'गीत']
        for mn in music_end_words:
            if text_lower.endswith(mn) or text_lower.endswith(' ' + mn):
                return True
        return False



    if is_music_request(q_lower):
        if not any(sw in q_lower for sw in ['थांबव', 'बंद कर', 'stop', 'pause', 'रोको']):
            from jarvis_music import play_music
            return play_music(clean_q, target_lang)

    # 0.0.5 🖼️ Check Image/Photo Search Intent
    image_triggers = ['photo dakhaw', 'photo dakhav', 'image dakhaw', 'image dakhav', 'photo de', 'image de', 'picture dakhaw', 'pic dakhaw', 'फोटो दाखव', 'चित्र दाखव', 'फोटो दे', 'photo', 'image', 'picture', 'pic', 'फोटो', 'चित्र']
    if any(it in q_lower for it in image_triggers):
        from jarvis_actions import search_image_link
        return search_image_link(clean_q, target_lang)

    # 0. 🚩 Check "जय श्री राम" / "जय श्रीराम" Intent
    ram_triggers = ['जय श्री राम', 'जय श्रीराम', 'jai shree ram', 'jay shree ram', 'jai shri ram', 'jay shri ram', 'shree ram', 'shri ram', 'ram ram', 'राम राम']
    if any(rt in q_lower for rt in ram_triggers):
        clean_after = q_lower
        for rt in ram_triggers:
            clean_after = clean_after.replace(rt, '').strip()
        clean_after = re.sub(r'^[,\.\s!?-]+', '', clean_after).strip()
        
        # If query is purely "जय श्री राम" or with polite title
        if not clean_after or clean_after in ['सर', 'sir', 'boss', 'ji', 'सांगा', 'bolo', 'kasa ahes']:
            if target_lang == 'mr':
                return "🚩 **जय श्री राम!** काय मदत करू सर?"
            elif target_lang == 'hi':
                return "🚩 **जय श्री राम!** बताइए, क्या मदद करूँ सर?"
            return "🚩 **Jai Shree Ram!** How can I assist you, Sir?"

    # 0.1 🧑‍🤝‍🧑 Check "शुभम कळमकर" Intent
    shubham_kw = ['shubham kalamkar', 'shubham kalmkar', 'शुभम कळमकर', 'शुभम कलमकर', 'shubham kon', 'शुभम कोण', 'who is shubham', 'shubham kaun']
    if any(sk in q_lower for sk in shubham_kw):
        if target_lang == 'mr':
            return "तो **साहिलचा फ्रेंड (मित्र)** आहे, सर! 🤝"
        elif target_lang == 'hi':
            return "वह **साहिल का दोस्त (फ्रेंड)** है, सर! 🤝"
        return "He is **Sahil's friend**, Sir! 🤝"

    # 0.1.05 🧑‍🤝‍🧑 Check "योगेश भासार" Intent
    yogesh_kw = [
        'yogesh bhasar', 'yogesh bhashar', 'yogesh basar', 'yogesh baser', 'yogesh bharsar',
        'योगेश भासार', 'योगेश भसार', 'योगेश भासर', 'योगेश भसर',
        'yogesh kon', 'yogesh kon aahe', 'yogesh kon ahe', 'yogesh kaun', 'who is yogesh',
        'योगेश कोण', 'योगेश कोण आहे', 'योगेश कोण आहेत', 'yogesh badal', 'योगेश बद्दल',
        'yogesh vishayi', 'योगेश विषयी'
    ]
    if any(yk in q_lower for yk in yogesh_kw):
        if target_lang == 'mr':
            return "तो **साहिलचा मित्र (फ्रेंड)** आहे, सर! 🤝"
        elif target_lang == 'hi':
            return "वह **साहिल का दोस्त (मित्र)** है, सर! 🤝"
        return "He is **Sahil's friend**, Sir! 🤝"

    # 0.1.06 🧑‍🤝‍🧑 Check "कार्तिक मोहिते" Intent
    kartik_kw = [
        'kartik mohite', 'kartik', 'कार्तिक मोहिते', 'कार्तिक',
        'kartik kon', 'kartik kon aahe', 'kartik kon ahe', 'kartik kaun', 'who is kartik',
        'कार्तिक कोण', 'कार्तिक कोण आहे', 'कार्तिक कोण आहेत', 'kartik badal', 'कार्तिक बद्दल',
        'kartik vishayi', 'कार्तिक विषयी'
    ]
    if any(kk in q_lower for kk in kartik_kw):
        if target_lang == 'mr':
            return "तो **साहिलचा मित्र (फ्रेंड)** आहे, सर! 🤝"
        elif target_lang == 'hi':
            return "वह **साहिल का दोस्त (मित्र)** है, सर! 🤝"
        return "He is **Sahil's friend**, Sir! 🤝"

    # 0.1.1 👨‍👩‍👦 Check "साहिलचे कुटुंब / फॅमिली" Intent (वडील: अशोक भिंगारे, आई: सुनीता, भाऊ: रोहन)
    sahil_fam_kw = [
        'sahil chi family', 'sahil family', 'sahil che kutumb', 'sahil kutumb', 'sahil family vishayi',
        'sahil family badal', 'sahil family sang', 'sahil family chi mahiti', 'tell me about sahil family', 'sahil family members',
        "sahil's family", 'sahils family', 'sahil family in',
        'साहिलची फॅमिली', 'साहिलचे कुटुंब', 'साहिलचं कुटुंब', 'साहिलच्या फॅमिली विषयी', 'साहिलच्या फॅमिली बद्दल', 'साहिलच्या कुटुंबाविषयी सांग',
        'साहिलच्या कुटुंबाबद्दल', 'साहिलच्या फॅमिलीबद्दल', 'साहिलच्या फॅमिलीविषयी'
    ]
    if any(sf in q_lower for sf in sahil_fam_kw) or (('family' in q_lower or 'फॅमिली' in q_lower or 'कुटुंब' in q_lower) and any(w in q_lower for w in ['sahil', 'साहिल'])):
        if target_lang == 'mr':
            return (
                "👨‍👩‍👦 **साहिल यांचे कुटुंब (Sahil's Family):**\n"
                "• **वडील**: **अशोक भिंगारे (Ashok Bhingare)** - साहिलचे वडील आहेत. 👨\n"
                "• **आई**: **सुनीता (Sunita)** - साहिलची आई आहेत. 👩\n"
                "• **भाऊ**: **रोहन (Rohan)** - साहिलचा भाऊ आहे. 👦\n\n"
                "हे साहिलचे सुखी आणि प्रेमळ कुटुंब आहे, सर! 🏡❤️"
            )
        elif target_lang == 'hi':
            return (
                "👨‍👩‍👦 **साहिल का परिवार (Sahil's Family):**\n"
                "• **पिताजी**: **अशोक भिंगारे (Ashok Bhingare)** - साहिल के पिता हैं। 👨\n"
                "• **माताजी**: **सुनीता (Sunita)** - साहिल की माताजी हैं। 👩\n"
                "• **भाई**: **रोहन (Rohan)** - साहिल के भाई हैं। 👦\n\n"
                "यह साहिल का प्यारा और सुखी परिवार है, सर! 🏡❤️"
            )
        return (
            "👨‍👩‍👦 **Sahil's Family Members:**\n"
            "• **Father**: **Ashok Bhingare** (साहिलचे वडील) 👨\n"
            "• **Mother**: **Sunita** (साहिलची आई) 👩\n"
            "• **Brother**: **Rohan** (साहिलचा भाऊ) 👦\n\n"
            "This is Sahil's wonderful family, Sir! 🏡❤️"
        )

    # Individual Member Checks
    if any(af in q_lower for af in ['ashok bhingare', 'अशोक भिंगारे', 'sahil che vadil', 'साहिलचे वडील', 'sahil che papa', 'sahil ke pita', 'sahil father', "sahil's father"]):
        if target_lang == 'mr':
            return "**अशोक भिंगारे (Ashok Bhingare)** हे साहिलचे वडील (Father) आहेत, सर! 👨"
        elif target_lang == 'hi':
            return "**अशोक भिंगारे (Ashok Bhingare)** साहिल के पिताजी (Father) हैं, सर! 👨"
        return "**Ashok Bhingare** is Sahil's father, Sir! 👨"

    if any(rf in q_lower for rf in ['rohan kon', 'रोहन कोण', 'sahil cha bhau', 'साहिलचा भाऊ', 'sahil brother', "sahil's brother", 'sahil ka bhai']):
        if target_lang == 'mr':
            return "**रोहन (Rohan)** हा साहिलचा भाऊ (Brother) आहे, सर! 👦"
        elif target_lang == 'hi':
            return "**रोहन (Rohan)** साहिल का भाई (Brother) है, सर! 👦"
        return "**Rohan** is Sahil's brother, Sir! 👦"

    if any(sf in q_lower for sf in ['sunita kon', 'सुनीता कोण', 'sahil chi aai', 'साहिलची आई', 'sahil mother', "sahil's mother", 'sahil ki mata']):
        if target_lang == 'mr':
            return "**सुनीता (Sunita)** या साहिलची आई (Mother) आहेत, सर! 👩❤️"
        elif target_lang == 'hi':
            return "**सुनीता (Sunita)** साहिल की माताजी (Mother) हैं, सर! 👩❤️"
        return "**Sunita** is Sahil's mother, Sir! 👩❤️"

    # 0.1.2 🎓 Check "साहिलचे शिक्षण" / Sahil's Education Intent
    sahil_edu_kw = [
        'sahil ch education', 'sahil che education', 'sahil education', 'sahil che shikshan',
        'sahil qualification', 'sahil chya shikshan', 'sahil ne kay shikla', 'sahil study',
        'sahil degree', 'sahil diploma', 'education of sahil', 'sahil ka education', 'sahil ki padhai',
        'साहिलचे शिक्षण', 'साहिलच शिक्षण', 'साहिलचं शिक्षण', 'साहिल काय शिकला', 'साहिलचे एज्युकेशन',
        'साहिलने काय केले', 'साहिलचा डिप्लोमा', 'साहिल ची माहिती', 'साहिल बद्दल सांगा', 'साहिल बद्दल सांग',
        'साहिल बद्दल माहिती', 'साहिल कोण आहे', 'sahil kon', 'who is sahil', 'tell me about sahil', 'sahil badal sang'
    ]
    if any(se in q_lower for se in sahil_edu_kw) and not any(fw in q_lower for fw in ['family', 'फॅमिली', 'कुटुंब', 'वडील', 'आई', 'भाऊ', 'father', 'mother', 'brother', 'insta', 'instagram', 'इन्स्टा', 'इंस्टाग्राम']):
        if target_lang == 'mr':
            return "साहिल यांनी **कॉम्प्युटर डिप्लोमा (Computer Diploma) ६९.८८%** गुणांसह यशस्वीरीत्या पूर्ण केला आहे. तसेच सध्या ते **Vyomx Tech Solution Pvt. Ltd. (आंबेगाव, नऱ्हे)** येथे **फुलस्टॅक डेव्हलपर (Full Stack Developer)** चे क्लासेस करत आहेत, सर! 💻🚀"
        elif target_lang == 'hi':
            return "साहिल जी ने **कंप्यूटर डिप्लोमा (Computer Diploma) ६९.८८%** अंकों के साथ पूरा किया है। वर्तमान में वे **Vyomx Tech Solution Pvt. Ltd. (आंबेगांव, नऱ्हे)** में **फुलस्टॅक डेवलपर (Full Stack Developer)** की ट्रेनिंग / क्लासेस कर रहे हैं, सर! 💻🚀"
        return "Sahil has completed his **Computer Diploma with 69.88%**. Currently, he is pursuing **Full Stack Developer** classes at **Vyomx Tech Solution Pvt. Ltd. (Ambegaon, Narhe)**, Sir! 💻🚀"

    # 0.1.25 📸 Check "साहिलची इंस्टाग्राम आयडी" / Sahil's Instagram Intent (sahil_bhingare_96k)
    sahil_insta_kw = [
        'sahil chi insta id', 'sahil chi insta', 'sahil chi instagram id', 'sahil chi instagram',
        'sahil insta id', 'sahil instagram id', 'sahil insta', 'sahil instagram',
        'sahil chi id', 'sahil id', 'sahil account', 'sahil_bhingare_96k', 'sahil bhingare insta',
        'साहिलची इन्स्टा आयडी', 'साहिलची इंस्टाग्राम आयडी', 'साहिलची इन्स्टा', 'साहिलची इंस्टाग्राम',
        'साहिल इन्स्टा आयडी', 'साहिल इंस्टाग्राम आयडी', 'साहिलचा इन्स्टा', 'साहिलचा इंस्टाग्राम',
        'साहिल इन्स्टाग्राम', 'साहिल इन्स्टा', 'साहिलची आयडी', 'sahil ki insta id', 'sahil ki instagram id',
        'sahil ka insta', 'sahil ka instagram', 'instagram id of sahil', 'insta id of sahil',
        'sahil social media', 'sahil handle'
    ]
    if any(si in q_lower for si in sahil_insta_kw) or (('insta' in q_lower or 'instagram' in q_lower or 'इन्स्टा' in q_lower or 'इंस्टाग्राम' in q_lower) and any(sw in q_lower for sw in ['sahil', 'साहिल'])):
        if target_lang == 'mr':
            return "साहिल यांची इंस्टाग्राम आयडी **@sahil_bhingare_96k** ही आहे, सर! 📸✨\n\n👉 [Instagram Profile उघडा](https://www.instagram.com/sahil_bhingare_96k/)"
        elif target_lang == 'hi':
            return "साहिल जी की इंस्टाग्राम आईडी **@sahil_bhingare_96k** है, सर! 📸✨\n\n👉 [Instagram Profile खोलें](https://www.instagram.com/sahil_bhingare_96k/)"
        return "Sahil's Instagram ID is **@sahil_bhingare_96k**, Sir! 📸✨\n\n👉 [Open Instagram Profile](https://www.instagram.com/sahil_bhingare_96k/)"

    # 1. 🚩 Check Forts Intent
    if any(k in q_lower for k in FORT_KEYWORDS):
        for fort_key, fort_dict in FORTS_KNOWLEDGE.items():
            names_to_check = [fort_key]
            if fort_key == 'रायगड': names_to_check.extend(['रायगढ़', 'raigad'])
            elif fort_key == 'राजगड': names_to_check.extend(['राजगढ़', 'rajgad'])
            elif fort_key == 'प्रतापगड': names_to_check.extend(['प्रतापगढ़', 'pratapgad'])
            elif fort_key == 'सिंहगड': names_to_check.extend(['सिंहगढ़', 'sinhagad', 'kondhana', 'कोंढाणा'])
            elif fort_key == 'सिंधुदुर्ग': names_to_check.extend(['sindhudurg'])
            elif fort_key == 'शिवनेरी': names_to_check.extend(['shivneri'])
            elif fort_key == 'पन्हाळा': names_to_check.extend(['panhala', 'पन्हालगढ़'])
            elif fort_key == 'तोरणा': names_to_check.extend(['torna', 'prachandagad'])

            if any(name.lower() in q_lower for name in names_to_check):
                response = fort_dict.get(target_lang, fort_dict['en' if target_lang == 'en' else 'mr'])
                break

        if not response and any(w in q_lower for w in ['किल्ले', 'किल्ल्यांविषयी', 'किले', 'forts', 'fort']):
            response = FORTS_GENERAL_SUMMARY.get(target_lang, FORTS_GENERAL_SUMMARY['en' if target_lang == 'en' else 'mr'])

    # 2. 🚩 Check Chhatrapati Shivaji Maharaj Intent
    if not response and any(kw in q_lower for kw in SHIVAJI_KEYWORDS):
        response = SHIVAJI_MAHARAJ_KNOWLEDGE.get(target_lang, SHIVAJI_MAHARAJ_KNOWLEDGE['en' if target_lang == 'en' else 'mr']).strip()

    # 3. 🕉️ Check Panchang & Festivals Intent
    if not response and any(pk in q_lower for pk in PANCHANG_KEYWORDS):
        response = PANCHANG_KNOWLEDGE.get(target_lang, PANCHANG_KNOWLEDGE['en' if target_lang == 'en' else 'mr']).strip()

    # 4. 🕉️ Check Sanatan Hindu Dharma Intent
    if not response and any(hk in q_lower for hk in HINDU_KEYWORDS):
        response = HINDU_DHARMA_KNOWLEDGE.get(target_lang, HINDU_DHARMA_KNOWLEDGE['en' if target_lang == 'en' else 'mr']).strip()

    # 5. Try Gemini Generative AI (Strictly in target language)
    if not response and os.getenv("GEMINI_API_KEY", "").strip():
        gemini_ans = ask_gemini(resolved_q, target_lang, session_id, image_b64=image, user_name=user_name)
        if gemini_ans:
            response = gemini_ans

    # 6. Fallback to Wikipedia / DuckDuckGo / Offline Conversation
    if not response and not image:
        response = generate_offline_fallback(resolved_q, target_lang)
    elif not response and image:
        if target_lang == 'mr': response = "क्षमस्व सर, मला हा फोटो तपासता आला नाही."
        elif target_lang == 'hi': response = "माफ़ करें सर, मैं इस फोटो की जाँच नहीं कर सका।"
        else: response = "Sorry Sir, I could not analyze this image."

    # Save to session history
    add_to_session_history(session_id, 'user', clean_q)
    add_to_session_history(session_id, 'assistant', response)

    return response

if __name__ == '__main__':
    print("--- English Test: Raigad Fort ---")
    print(get_answer("Tell me about Raigad Fort in detail", 'en')[:300] + "...\n")
    print("--- English Test: Chhatrapati Shivaji Maharaj ---")
    print(get_answer("Tell me about Chhatrapati Shivaji Maharaj", 'en')[:300] + "...\n")
    print("--- English Test: Sanatan Dharma ---")
    print(get_answer("What is Sanatan Dharma?", 'en')[:300] + "...")
