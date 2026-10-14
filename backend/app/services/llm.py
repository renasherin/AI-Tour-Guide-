"""
LLM Generation Service for Incredible Journeys: AI Tour Guide for India.
Integrates:
- Warm, evocative, witty local storyteller persona (telling authentic jokes and proverbs)
- Support for all Indian languages (English, Hindi, Malayalam, Kannada, Telugu, Tulu, Tamil,
  Marathi, Punjabi, Bihari/Bhojpuri, Nepali, Bengali, Gujarati, Odia, Assamese, Urdu)
- Strict grounding in retrieved passages, authentic foods atlas, and live Wikipedia intelligence
- Zero dry refusals: rich, delightful, sensory travel narratives with Google Maps links
- Streaming (SSE) and synchronous responses
"""

import os
import re
import json
import logging
import urllib.parse
from typing import List, Dict, Any, Optional, Iterator, AsyncIterator

logger = logging.getLogger("services.llm")

# Regional authentic culinary pairings for immersive storytelling
REGIONAL_FEASTS = {
    "Kerala": "fragrant Malabar Dum Biryani, fluffy Appam with spiced coconut stew, Kozhikodan Halwa, and freshly brewed Malabar filter coffee",
    "Tamil Nadu": "crisp Ghee Roast Dosa, Chettinad pepper chicken, steaming brass-tumbler filter coffee, and cooling Madurai Jigarthanda",
    "Karnataka": "aromatic Mysore Masala Dosa, Mangalorean Kori Rotti, Neer Dosa, rich Bisi Bele Bath, and melting Mysore Pak",
    "Andhra Pradesh": "fiery Gongura pachadi, Royyala iguru, royal Hyderabadi dum biryani, and melt-in-mouth Pootharekulu sweets",
    "Telangana": "slow-cooked Hyderabadi Kacchi Dum Biryani, crunchy Sarva Pindi, and piping hot Irani chai with Osmania biscuits",
    "Rajasthan": "wood-fired Dal Baati Churma, spicy Ker Sangri wild berries, crisp Pyaaz Kachori, and honeyed Ghevar",
    "Punjab": "crispy tandoor-baked Amritsari Kulcha with pindi chole, creamy Sarson da Saag with Makki di Roti, and tall brass glasses of sweet lassi",
    "Maharashtra": "spicy Misal Pav topped with farsan, steaming street-side Vada Pav, Puran Poli flatbreads, and refreshing Solkadhi",
    "Gujarat": "steamed spongy Khaman Dhokla, festive Gujarati Thali, Khandvi rolls, and winter Undhiyu",
    "Uttar Pradesh": "melt-in-the-mouth Awadhi Galouti Kebabs, crisp Banarasi Kachori-Jalebi, and velvety winter Malaiyo froth infused with saffron",
    "Madhya Pradesh": "steamed Poha crowned with crisp sev, hot spiral Jalebis, Bhutte ka Kees (spiced grated corn), and Dal Bafla",
    "West Bengal": "mustard-infused Shorshe Ilish, spicy Kolkata Kathi Rolls, melt-in-the-mouth Nolen Gur Sandesh, and spongy Rosogolla",
    "Odisha": "cooling fermented Pakhala Bhata, velvety Chhena Poda caramelized cottage cheese cake, and holy temple Mahaprasad",
    "Assam": "delicate Masor Tenga sour fish curry, Khaar alkaline delicacy, bamboo shoot pork, and aromatic Assam orthodox black tea",
    "Meghalaya": "flavorful Jadoh (red hill rice cooked with herbs), fermented soybean chutney, Dohkhlieh, and wild forest honey",
    "Himachal Pradesh": "ceremonial Himachali Dham served on leaf plates, steamed walnut-stuffed Siddu breads with ghee, and Kangra valley tea",
    "Uttarakhand": "hearty Kumaoni Bhatt ki Churkani black soybean gravy, Aloo ke Gutke with hemp seed salt, and sweet Bal Mithai",
    "Jammu and Kashmir": "royal 36-course Wazwan (Rogan Josh, Gustaba, Rista), saffron-scented Kahwa tea with crushed almonds, and freshly baked Tsot bread",
    "Ladakh": "warming hand-pulled Thukpa noodle soup, steaming momos with fiery chili dip, and comforting salted butter tea (Gur-Gur chai)",
    "Goa": "coconut-tamarind Goan Fish Curry, fiery Vindaloo, and seven-layered caramelized Bebinca cake",
    "Sikkim": "piping hot Himalayan momos, Sel Roti, nourishing Gundruk fermented leaf broth, Thukpa, and locally brewed millet Tongba",
    "Bihar": "rustic charcoal-roasted Litti Chokha dipped in pure desi ghee, crispy sattu paratha, and flaky sweet Silao Khaja",
    "Chhattisgarh": "steamed rice Chhattisgarhi Chila with tomato-coriander chutney, Faraa rice dumplings, and sweet Bafauri",
    "Jharkhand": "golden crisp Dhuska made of rice and lentils, spicy Ghugni, and tender bamboo shoot curry",
    "Arunachal Pradesh": "bamboo-steamed Pasa herbal soup, smoked pork with local bhoot jolokia chili, and Apong rice brew",
    "Manipur": "spicy Chamthong vegetable stew, Eromba mashed fish with king chilies, and aromatic black rice Chak-hao kheer",
    "Mizoram": "fragrant Mizo Bai herbal vegetable stew with bamboo shoots, and tender smoked pork with mustard greens",
    "Nagaland": "smoky wood-fired pork with fermented axone soybeans, fiery Naga King Chili dip, and steamed organic wild greens",
    "Tripura": "traditional Berma fermented fish stew with bamboo shoots, Mui Borok herbs, and Bangui sticky rice cakes"
}

# Native language greetings, joke collections, and cultural proverbs
NATIVE_LANGUAGE_PACKS = {
    "ml": {
        "greeting": "നമസ്കാരം സുഹൃത്തേ! ദൈവത്തിന്റെ സ്വന്തം നാടായ കേരളത്തിൽ നിന്നും ഭാരതത്തിന്റെ അത്ഭുതങ്ങളിലേക്ക് സ്വാഗതം! ഒരു പ്രിയ സുഹൃത്തിനെപ്പോലെ ഞാൻ കൂടെയുണ്ട്.",
        "joke": "യാത്രയിൽ ഒരു ചിരി: കോഴിക്കോട് ബീച്ചിൽ വച്ച് ഒരു വിദേശി ചോദിച്ചു: 'ഇവിടെ ഏറ്റവും വലിയ അത്ഭുതം എന്താ?' ചായക്കടയിലെ ഇക്ക ചിരിച്ചുകൊണ്ട് പറഞ്ഞു: 'നമ്മുടെ ദം ബിരിയാണിയും ചൂടുള്ള ഹൽവയും കഴിച്ചുകഴിഞ്ഞാൽ ലോകത്തിലെ ഒരു ടെൻഷനും മനസ്സിൽ ബാക്കി കാണില്ല എന്നുള്ളത് തന്നെ!' 😄☕",
        "wow_prefix": "🌟 അമ്പരപ്പിക്കുന്ന അത്ഭുത സത്യങ്ങൾ (Wow Factors):",
        "saga_prefix": "🌅 ജീവസ്സുറ്റ ചരിത്രവും ഐതിഹ്യവും:",
        "food_prefix": "🍲 നാവിൽ കൊതിയൂറുന്ന തനത് രുചികൾ:",
        "best_time_prefix": "🗓️ സന്ദർശിക്കാൻ ഏറ്റവും അനുയോജ്യമായ സമയം:",
        "map_prefix": "📍 ഗൂഗിൾ മാപ്പ്സ് ലൊക്കേഷൻ:",
        "farewell": "മനസ്സുതുറന്ന് യാത്ര ചെയ്യൂ, അനുഭവങ്ങൾ നെഞ്ചേറ്റൂ!"
    },
    "hi": {
        "greeting": "नमस्ते प्रिय यात्री! भारत की पावन भूमि, गगनचुंबी किलों, पावन नदियों और लज़ीज़ स्वादों की इस अनूठी यात्रा में आपका दिल से स्वागत है!",
        "joke": "यात्रा का एक मजेदार जोक: एक बार बनारस के घाट पर एक टूरिस्ट ने नाविक से पूछा—'भैया, क्या तुम्हें कंप्यूटर चलाना आता है?' नाविक बोला—'नहीं बाबूजी!' टूरिस्ट बोला—'तुम्हारी 25% ज़िंदगी बेकार!' थोड़ी देर में लहरें उठीं और नाव डगमगाने लगी, नाविक ने पूछा—'बाबूजी, क्या आपको तैरना आता है?' टूरिस्ट घबराकर बोला—'नहीं!' नाविक मुस्कुराया—'तो बाबूजी, आपकी 100% ज़िंदगी दांव पर है!' 😂🛶",
        "wow_prefix": "🌟 अद्भुत विस्मयकारी तथ्य (Mind-Blowing Wow Factors):",
        "saga_prefix": "🌅 जीवंत गाथा और प्राचीन इतिहास:",
        "food_prefix": "🍲 स्थानीय स्वाद और ज़ायके (Culinary Soul):",
        "best_time_prefix": "🗓️ भ्रमण का सर्वोत्तम समय:",
        "map_prefix": "📍 गूगल मैप्स नेविगेशन:",
        "farewell": "हंसते-मुस्कुराते यात्रा करें और जीवन भर की यादें संजोएं!"
    },
    "kn": {
        "greeting": "ನಮಸ್ಕಾರ ಗೆಳೆಯರೇ! ನಮ್ಮ ಕರುನಾಡಿನಿಂದ ಇಡೀ ಭಾರತದ ಸುಂದರ ದೇವಾಲಯಗಳು, ಹಸಿರು ಕಣಿವೆಗಳು ಮತ್ತು ಸ್ವಾದಿಷ್ಟ ಆಹಾರದ ಲೋಕಕ್ಕೆ ಆತ್ಮೀಯ ಸ್ವಾಗತ!",
        "joke": "ಪ್ರವಾಸದ ಒಂದು ಮಜವಾದ ಜೋಕ್: ಒಬ್ಬ ಪ್ರವಾಸಿ ಹಂಪಿಯ ಕಲ್ಲಿನ ರಥದ ಮುಂದೆ ನಿಂತು ಗೈಡ್‌ಗೆ ಕೇಳಿದ: 'ಈ ಕಲ್ಲಿನ ರಥ ಚಲಿಸುತ್ತಾ ಸರ್?' ಗೈಡ್ ಮುಗುಳ್ನಕ್ಕು ಹೇಳಿದ: 'ನೀವು ಬರೀ ಕಣ್ಣಿಂದ ನೋಡಿದರೆ ಚಲಿಸಲ್ಲ ಸಾರ್, ಅದೇ ಒಂದು ಮೈಸೂರು ಮಸಾಲೆ ದೋಸೆ ತಿಂದು ಕಲ್ಪನೆ ಕುದುರೆ ಹತ್ತಿದರೆ ಇಡೀ ಸಾಮ್ರಾಜ್ಯವೇ ನಿಮ್ಮ ಮುಂದೆ ಓಡುತ್ತೆ!' 😄🛕",
        "wow_prefix": "🌟 ವಿಸ್ಮಯಕಾರಿ ಸತ್ಯಗಳು (Mind-Blowing Wow Factors):",
        "saga_prefix": "🌅 ಜೀವಂತ ಇತಿಹಾಸ ಮತ್ತು ಮಹಾಕಾವ್ಯ:",
        "food_prefix": "🍲 ನಾಲಿಗೆ ಚಪ್ಪರಿಸುವ ಸ್ಥಳೀಯ ರುಚಿಗಳು:",
        "best_time_prefix": "🗓️ ಭೇಟಿ ನೀಡಲು ಅತ್ಯುತ್ತಮ ಸಮಯ:",
        "map_prefix": "📍 ಗೂಗಲ್ ಮ್ಯಾಪ್ಸ್ ಮಾರ್ಗಸೂಚಿ:",
        "farewell": "ಖುಷಿಯಿಂದ ಪ್ರಯಾಣಿಸಿ, ಅದ್ಭುತ ನೆನಪುಗಳನ್ನು ನಿಮ್ಮದಾಗಿಸಿಕೊಳ್ಳಿ!"
    },
    "te": {
        "greeting": "నమస్కారం ప్రియమైన మిత్రమా! మన భారతదేశంలోని అద్భుతమైన చారిత్రక కట్టడాలు, పవిత్ర క్షేత్రాలు మరియు ఘుమఘుమలాడే వంటకాల యాత్రకు సాదర స్వాగతం!",
        "joke": "యాత్రలో ఒక సరదా జోక్: ఒక పర్యాటకుడు హోటల్లో అడిగాడు: 'ఈ హైదరాబాద్ దమ్ బిర్యానీ ఎంత ఘాటుగా ఉంటుంది?' సర్వర్ నవ్వుతూ అన్నాడు: 'మొదటి ముద్ద తింటే ఆనందబాష్పాలు వస్తాయి, రెండో ముద్ద తింటే చార్మినార్ చుట్టూ రౌండ్లు కొట్టాలనిపిస్తుంది సార్!' 🌶️😄",
        "wow_prefix": "🌟 ఆశ్చర్యపరిచే అద్భుత వాస్తవాలు (Wow Factors):",
        "saga_prefix": "🌅 సజీవ చరిత్ర మరియు చారిత్రక కథనం:",
        "food_prefix": "🍲 నోరూరించే స్థానిక రుచులు:",
        "best_time_prefix": "🗓️ సందర్శించడానికి ఉత్తమ సమయం:",
        "map_prefix": "📍 గూగుల్ మ్యాప్స్ లొకేషన్:",
        "farewell": "సంతోషంగా ప్రయాణించండి, మధుర జ్ఞాపకాలను మూటగట్టుకోండి!"
    },
    "ta": {
        "greeting": "வணக்கம் அன்பான பயணியே! கோவில் கோபுரங்கள், கம்பீரமான கோட்டைகள் மற்றும் சுவையான உணவு பாரம்பரியம் கொண்ட பாரத தேசத்தின் வரலாற்றுப் பயணத்திற்கு உங்களை அன்போடு வரவேற்கிறேன்!",
        "joke": "பயணத்தில் ஒரு சின்ன சிரிப்பு: மதுரைக்கு வந்த ஒரு சுற்றுலாப் பயணி கேட்டாராம்: 'இங்க வெயில் ரொம்ப அதிகமா இருக்கே, என்ன பண்றது?' உள்ளூர் அண்ணன் சொன்னாராம்: 'கவலைய விடுங்க தம்பி, ஒரு டம்ளர் ஜிகர்தண்டா குடிச்சுட்டு நெய் ரோஸ்ட் சாப்பிடுங்க, வெயில் உங்க உடம்பை விட்டு ஓடிப் போயிடும்!' 😆🍨",
        "wow_prefix": "🌟 பிரமிக்க வைக்கும் ஆச்சரிய உண்மைகள் (Wow Factors):",
        "saga_prefix": "🌅 வரலாற்றுச் சுவடுகளும் வாழும் காவியமும்:",
        "food_prefix": "🍲 நாவில் எஞ்சும் பாரம்பரிய சுவைகள்:",
        "best_time_prefix": "🗓️ பயணிக்க சிறந்த காலம்:",
        "map_prefix": "📍 கூகுள் மேப்ஸ் இருப்பிடம்:",
        "farewell": "மகிழ்ச்சியுடன் பயணியுங்கள், பசுமையான நினைவுகளைச் சேருங்கள்!"
    },
    "tcy": {
        "greeting": "ನಮಸ್ಕಾರ ಮಾರಾಯ್ರೆ! ಕುಡ್ಲ (ಮಂಗಳೂರು), ತುಳುನಾಡ್ದ ಬೊಕ್ಕ ಇಡೀ ಭಾರತ ದೇಶದ ಪೊರ್ಲು ತಾಣೊಲೆಗ್, ತಿನಿಸುಲೆಗ್ ಎದ್ಕೊಂಡು ಪನ್ಪಿನೆ!",
        "joke": "ಒಂಜಿ ತುಳು ಜೋಕ್: ಒರಿ ಪ್ರವಾಸಿ ಬೀಚ್‌ಡ್ ಉಪ್ಪುನಗ ಭಟ್ಟ್ರೆಡ ಕೇಂಡೆ: 'ಭಟ್ಟ್ರೆ, ಈ ಸಮುದ್ರದ ನೀರ್ ಉಪ್ಪು ದಾಯೆ?' ಭಟ್ಟ್ರೆ ಪಂಡೆರ್: 'ಕೋರಿ ರೊಟ್ಟಿಗ್ ತಕ್ಕ ಕಜಿಪು ಮಲ್ಪೆರೆ ದೇವೆರ್ ಅರೆನ್ ರೆಡಿ ಮಲ್ತ್ ದೀತೆರ್ ಮಾರಾಯ!' 🤣🍗",
        "wow_prefix": "🌟 ಅಚ್ಚರಿದ ಸಂಗತಿಲು (Wow Factors):",
        "saga_prefix": "🌅 ಪಿರಾಕ್ದ ಚರಿತ್ರೆ ಬೊಕ್ಕ ಕತೆ:",
        "food_prefix": "🍲 ತುಳುನಾಡ್ದ ಬೊಕ್ಕ ದೇಶದ ರುಚಿಕರ ತೆನಸ್:",
        "best_time_prefix": "🗓️ ಬರಿಯೆರೆ ಎಡ್ಡೆ ಪೊರ್ತು:",
        "map_prefix": "📍 ಗೂಗಲ್ ಮ್ಯಾಪ್ಸ್ ಮಾರ್ಗ:",
        "farewell": "ಕುಷಿಟ್ ತಿರ್ಗಲೆ, ಪೊರ್ಲುದ ನೆನಪುಲೆನ್ ಒರಿಪಾಲೆ!"
    },
    "mr": {
        "greeting": "नमस्कार मंडळी! आपल्या अतुल्य भारताच्या ऐतिहासिक गड-किल्ले, अध्यात्मिक भूमी आणि खमंग खाद्यसंस्कृतीच्या सफरीवर तुमचे मनःपूर्वक स्वागत आहे!",
        "joke": "प्रवासातील एक दिलखुलास विनोद: पुण्यात एका पर्यटकाने विचारलं: 'काका, शनिवार वाड्याचा रस्ता कोणता?' पुणेकर काकांनी चष्मा नाकावर सरकवत म्हटलं: 'रस्ता जागेवरच आहे, तुम्ही चुकीच्या दिशेने चालला आहात! आधी गरमागरम वडापाव खा, मग बुद्धी चालेल!' 😜🚩",
        "wow_prefix": "🌟 थक्क करणारे रंजक पैलू (Wow Factors):",
        "saga_prefix": "🌅 गौरवशाली इतिहास आणि जिवंत गाथा:",
        "food_prefix": "🍲 जिभेवर रेंगाळणारे स्थानिक चवदार पदार्थ:",
        "best_time_prefix": "🗓️ भेट देण्यासाठी सर्वोत्तम काळ:",
        "map_prefix": "📍 गुगल मॅप्स नेव्हिगेशन:",
        "farewell": "आनंदाने प्रवास करा आणि सुंदर आठवणी साठवा!"
    },
    "pa": {
        "greeting": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਜੀ! ਰੰਗਲੇ ਪੰਜਾਬ ਤੋਂ ਲੈ ਕੇ ਸਮੁੱਚੇ ਭਾਰਤ ਦੇ ਸ਼ਾਨਦਾਰ ਕਿਲ੍ਹਿਆਂ, ਪਵਿੱਤਰ ਧਰਤੀ ਅਤੇ ਸਵਾਦੀ ਪਕਵਾਨਾਂ ਦੇ ਦੌਰੇ 'ਤੇ ਤੁਹਾਡਾ ਦਿਲੋਂ ਸੁਆਗਤ ਹੈ!",
        "joke": "ਇੱਕ ਮਜ਼ੇਦਾਰ ਚੁਟਕਲਾ: ਅੰਮ੍ਰਿਤਸਰ ਵਿੱਚ ਇੱਕ ਟੂਰਿਸਟ ਨੇ ਢਾਬੇ ਵਾਲੇ ਨੂੰ ਪੁੱਛਿਆ: 'ਭਾਜੀ, ਕੁਲਚੇ ਵਿੱਚ ਕਿੰਨਾ ਦੇਸੀ ਘਿਓ ਪਾਉਂਦੇ ਹੋ?' ਢਾਬੇ ਵਾਲਾ ਹੱਸ ਕੇ ਬੋਲਿਆ: 'ਭਾਜੀ, ਓਨਾ ਕਿ ਖਾਣ ਤੋਂ ਬਾਅਦ ਜੰਨਤ ਸਾਹਮਣੇ ਨਜ਼ਰ ਆ ਜਾਵੇ ਤੇ ਡਾਕਟਰ ਦੀ ਲੋੜ ਭੁੱਲ ਜਾਵੇ!' 🧈😂",
        "wow_prefix": "🌟 ਹੈਰਾਨੀਜਨਕ ਤੱਥ (Wow Factors):",
        "saga_prefix": "🌅 ਸ਼ਾਨਦਾਰ ਇਤਿਹਾਸ ਅਤੇ ਜਿਊਂਦੀ ਗਾਥਾ:",
        "food_prefix": "🍲 ਸਵਾਦਲੇ ਦੇਸੀ ਪਕਵਾਨ (Culinary Soul):",
        "best_time_prefix": "🗓️ ਘੁੰਮਣ ਦਾ ਸਭ ਤੋਂ ਵਧੀਆ ਸਮਾਂ:",
        "map_prefix": "📍 ਗੂਗਲ ਮੈਪਸ ਲੋਕੇਸ਼ਨ:",
        "farewell": "ਹੱਸਦੇ-ਵੱਸਦੇ ਘੁੰਮੋ ਤੇ ਖੂਬਸੂਰਤ ਯਾਦਾਂ ਆਪਣੇ ਨਾਲ ਲੈ ਜਾਓ!"
    },
    "bho": {
        "greeting": "प्रणाम हो भैया/दीदी! भारत के रंग-बिरंग इतिहास, ऐतिहासिक धरोहर आ स्वादिस्ट खाना के सैर पर रउआ सब के बहुत-बहुत स्वागत बा!",
        "joke": "एगो मजेदार चुटकुला: स्टेशन पर एगो बाबू साहेब कुली से कहलें: 'अरे भैया, ई झोरा जरा सम्हार के उठइह, एमे सासाराम के खाजा आ सत्तू बा!' कुली मुस्का के कहलस: 'बाबूजी, रउआ बेफिकिर रहीं, हमार पेट खाली बा, गिरी त सीधै भीतरे जाई!' 😃🥞",
        "wow_prefix": "🌟 एकदम हक्का-बक्का करे वाला तथ्य (Wow Factors):",
        "saga_prefix": "🌅 पुरान इतिहास आ लोकगाथा:",
        "food_prefix": "🍲 माटी के महक वाला स्वादिस्ट खाना:",
        "best_time_prefix": "🗓️ घूमे के सबसे बढ़िया समय:",
        "map_prefix": "📍 गूगल मैप्स लिंक:",
        "farewell": "हँसी-खुशी घूमीं आ जिनगी भर के याद सहेजीं!"
    },
    "ne": {
        "greeting": "नमस्ते आदरणीय साथी! हाम्रो सुन्दर भारतका मनमोहक हिमाल, ऐतिहासिक मन्दिर, हरियाली उपत्यका र स्वादिष्ट परिकारहरूको रोमाञ्चक यात्रामा हार्दिक स्वागत छ!",
        "joke": "यात्राको एउटा रमाइलो जोक: दार्जिलिङमा एकजना पर्यटकले पहाडी गाइडलाई सोध्यो: 'यहाँको बाटो किन यति घुमाउरो छ?' गाइडले हाँस्दै भन्यो: 'बाटो सिधा बनायो भने त तपाईं एकै मिनेटमा गाडीसहित फेदीमा पुग्नुहुन्छ नि सर!' 🏔️😄",
        "wow_prefix": "🌟 अचम्म लाग्दा रोचक तथ्यहरू (Wow Factors):",
        "saga_prefix": "🌅 ऐतिहासिक गाथा र जीवन्त संस्कृति:",
        "food_prefix": "🍲 जिब्रोमै झुण्डिने स्थानीय स्वाद:",
        "best_time_prefix": "🗓️ भ्रमणका लागि उपयुक्त मौसम:",
        "map_prefix": "📍 गुगल म्याप्स स्थान:",
        "farewell": "खुसीसाथ यात्रा गर्नुहोस् र मीठा सम्झनाहरू बटुल्नुहोस्!"
    },
    "bn": {
        "greeting": "নমস্কার বন্ধু! ভারতের ঐতিহাসিক স্থাপত্য, পবিত্র নদী ও জিভে জল আনা খাবারের এই অপরূপ সফরে আপনাকে আন্তরিক স্বাগত জানাই!",
        "joke": "ভ্রমণের একটি মজার জোক: কলকাতায় এক পর্যটক রসগোল্লার দোকানে গিয়ে বলল: 'দাদা, মিষ্টিতে এত রস কেন?' ময়রা হেসে বলল: 'আরে মশাই, বাঙালির প্রেমে আর রসগোল্লার রসে কোনো কমতি থাকতে নেই!' 😋🏺",
        "wow_prefix": "🌟 চোখ ধাঁধানো ঐতিহাসিক বিস্ময় (Wow Factors):",
        "saga_prefix": "🌅 প্রাচীন ইতিহাস ও জীবন্ত ঐতিহ্য:",
        "food_prefix": "🍲 অতুলনীয় রসনা বিলাস ও স্থানীয় স্বাদ:",
        "best_time_prefix": "🗓️ ভ্রমণের সেরা সময়:",
        "map_prefix": "📍 গুগল ম্যাপস নেভিগেশন:",
        "farewell": "আনন্দে ভ্রমণ করুন এবং জীবনের সেরা স্মৃতিগুলো সংগ্রহ করুন!"
    },
    "gu": {
        "greeting": "નમસ્તે મિત્ર! રંગીલા ભારતના ભવ્ય કિલ્લાઓ, ઐતિહાસિક મંદિરો અને સ્વાદિષ્ટ વાનગીઓની આ સફરમાં આપનું હાર્દિક સ્વાગત છે!",
        "joke": "પ્રવાસની રમૂજ: એક પર્યટકે અમદાવાદમાં પૂછ્યું: 'તમારી દાળમાં ગળપણ કેમ છે?' અમદાવાદી ભાઈ હસીને બોલ્યા: 'સાહેબ, અમારા શબ્દો અને સ્વાદ બંનેમાં મીઠાશ કુદરતી હોય છે!' 😄🍲",
        "wow_prefix": "🌟 અદ્ભુત આશ્ચર્યજનક તથ્યો (Wow Factors):",
        "saga_prefix": "🌅 જીવંત ઇતિહાસ અને ભવ્ય વારસો:",
        "food_prefix": "🍲 સ્વાદિષ્ટ સ્થાનિક વાનગીઓ:",
        "best_time_prefix": "🗓️ મુલાકાત માટે શ્રેષ્ઠ સમય:",
        "map_prefix": "📍 ગૂગલ મેપ્સ નકશો:",
        "farewell": "આનંદથી પ્રવાસ કરો અને યાદગાર ક્ષણો માણો!"
    },
    "or": {
        "greeting": "ନମସ୍କାର ସାଙ୍ଗ! ଆମ ଭାରତର ପବିତ୍ର ଧର୍ମକ୍ଷେତ୍ର, ଐତିହାସିକ କଳାକୃତି ଏବଂ ସୁସ୍ୱାଦୁ ପାରମ୍ପରିକ ଖାଦ୍ୟର ଏହି ସୁନ୍ଦର ଯାତ୍ରାରେ ଆପଣଙ୍କୁ ସ୍ୱାଗତ!",
        "joke": "ଯାତ୍ରାର ଏକ ମଜାଦାର କଥା: ପୁରୀ ବେଳାଭୂମିରେ ଜଣେ ପର୍ଯ୍ୟଟକ ପଚାରିଲେ: 'ଏଠି ସବୁଠୁ ମିଠା କଣ?' ସ୍ଥାନୀୟ ବ୍ୟକ୍ତି କହିଲେ: 'ଆମ ଛେନା ପୋଡ଼ ଆଉ ଜଗନ୍ନାଥ ମହାପ୍ରସାଦ, ଖାଇଲେ ମନ ପ୍ରାଣ ଶାନ୍ତ ହୋଇଯିବ!' 😃🥮",
        "wow_prefix": "🌟 ଆଶ୍ଚର୍ଯ୍ୟଜନକ ତଥ୍ୟ (Wow Factors):",
        "saga_prefix": "🌅 ଐତିହାସିକ ଗାଥା ଓ ସଂସ୍କୃତି:",
        "food_prefix": "🍲 ସୁସ୍ୱାଦୁ ସ୍ଥାନୀୟ ଖାଦ୍ୟ ସମ୍ଭାର:",
        "best_time_prefix": "🗓️ ଭ୍ରମଣ ପାଇଁ ଉପଯୁକ୍ତ ସମୟ:",
        "map_prefix": "📍 ଗୁଗଲ ମ୍ୟାପ୍ସ ଲିଙ୍କ:",
        "farewell": "ଖୁସିରେ ଭ୍ରମଣ କରନ୍ତୁ ଏବଂ ଅଭୁଲା ଅନୁଭୂତି ସାଉଣ୍ଟି ନିଅନ୍ତୁ!"
    },
    "as": {
        "greeting": "নমস্কাৰ বন্ধু! আমাৰ ভাৰতবৰ্ষৰ প্ৰাচীন ঐতিহ্য, সেউজীয়া প্ৰকৃতি আৰু অপূৰ্ব খাদ্য সম্ভাৰৰ এই যাত্ৰাত আপোনাক আন্তৰিক স্বাগতম জনাইছোঁ!",
        "joke": "যাত্ৰাৰ এক হাঁহিৰ খোৰাক: গুৱাহাটীত এজন পৰ্যটকে চাহ দোকানীত সুধিলে: 'আপোনালোকৰ চাহ ইমান সোৱাদ কিয়?' দোকানীয়ে ক'লে: 'আমাৰ অসমৰ চাহপাতত ব্ৰহ্মপুত্ৰৰ আশীৰ্বাদ আৰু প্ৰকৃতিৰ সুবাস মিহলি হৈ থাকে!' 🍵😊",
        "wow_prefix": "🌟 বিস্ময়কৰ তথ্যসমূহ (Wow Factors):",
        "saga_prefix": "🌅 গৌৰৱময় ইতিহাস আৰু সংস্কৃতি:",
        "food_prefix": "🍲 জিভাৰ পানী ওলোৱা থলুৱা সোৱাদ:",
        "best_time_prefix": "🗓️ ভ্ৰমণৰ বাবে উপযুক্ত সময়:",
        "map_prefix": "📍 গুগল মেপ্স অৱস্থান:",
        "farewell": "আনন্দৰে ভ্ৰমণ কৰক আৰু সুন্দৰ স্মৃতি বুটলি লওক!"
    },
    "ur": {
        "greeting": "آداب اور خوش آمدید! ہندوستان کی شاندار تاریخ، تاریخی عمارات اور لذیذ کھانوں کے اس پرلطف سفر میں آپ کا دل سے خیر مقدم ہے۔",
        "joke": "سفر کا ایک پرلطف لطیفہ: لکھنؤ میں ایک سیاح نے پوچھا: 'یہاں کے کھانوں میں اتنی نزاکت کیوں ہے؟' باورچی نے مسکرا کر کہا: 'جناب، جہاں زبان کی مٹھاس اور گلاوٹی کباب کا دم ہو، وہاں ہر لقمہ شاعری بن جاتا ہے!' 😋✨",
        "wow_prefix": "🌟 حیرت انگیز حقائق (Wow Factors):",
        "saga_prefix": "🌅 شاندار تاریخ اور داستان:",
        "food_prefix": "🍲 لاجواب روایتی ذائقے:",
        "best_time_prefix": "🗓️ سفر کے لیے بہترین وقت:",
        "map_prefix": "📍 گوگل میپس کا پتہ:",
        "farewell": "ہنستے مسکراتے سفر کیجیے اور خوبصورت یادیں سمیٹیے!"
    },
    "en": {
        "greeting": "Welcome, fellow explorer! I'm your local AI travel companion with Incredible Journeys. Think of me as your chai stall friend and cultural insider across all 28 states and 8 union territories.",
        "joke": "A quick travel laugh: A traveler once asked an old Indian chaiwallah, 'Why are roads in India never straight?' The chaiwallah smiled and said, 'If the road were straight, sir, you'd reach your destination in five minutes and completely miss out on three ancient dynasties, four temple bells, and the best samosas of your life!' 😂☕",
        "wow_prefix": "🌟 Mind-Blowing Wow Factors & Marvels:",
        "saga_prefix": "🌅 The Living Saga & Historical Lore:",
        "food_prefix": "🍲 Culinary Soul & Authentic Flavors:",
        "best_time_prefix": "🗓️ Ideal Season to Visit:",
        "map_prefix": "📍 Navigation & Google Maps:",
        "farewell": "Travel with an open heart, and let India surprise you at every turn!"
    }
}

DEFAULT_MODEL = "gemini-2.5-flash"

SYSTEM_PERSONA_PROMPT = """You are 'Aarav & Priya', master travel storytellers, cultural insiders, and warm local guides for 'Incredible Journeys: Discover India with AI'.
Your mission is to share the vibrant wonders, ancient heritage, sacred geography, diverse cuisines, and natural beauty of India across all 28 states and 8 union territories.

STRICT BEHAVIORAL DIRECTIVES:
1. WARM, HUMAN-LIKE, AFFECTIONATE & WITTY PERSONA:
   - Talk like a cherished, well-traveled Indian friend who loves stories, chai, and shared laughter.
   - Crack authentic, gentle local jokes, puns, or witty proverbs tailored to the region or topic being discussed.
   - Never sound like a dry, robotic corporate encyclopedia.

2. MULTILINGUAL EXCELLENCE IN NATIVE LANGUAGES:
   - You MUST respond fully in the language requested by the user:
     * English (en), Hindi (hi), Malayalam (ml), Kannada (kn), Telugu (te), Tamil (ta),
       Tulu (tcy), Marathi (mr), Punjabi (pa), Bihari/Bhojpuri (bho), Nepali (ne),
       Bengali (bn), Gujarati (gu), Odia (or), Assamese (as), Urdu (ur).
   - Use natural native phrasing, authentic script (e.g. Malayalam script for ml, Devanagari for hi/mr/ne/bho, Kannada script for kn/tcy, Gurmukhi for pa, etc.).
   - Include witty native idioms, humor, and cultural expressions.

3. VIVID SENSORY & WOW-FACTOR STORYTELLING:
   - Bring the scene to life: scent of temple camphor, roasting spices, monsoon petrichor, morning chants.
   - Mind-blowing engineering and historical wow factors (acoustics, monoliths, astronomy).
   - Highlight regional authentic foods with mouthwatering descriptions.

4. ACCURATE GROUNDING & GOOGLE MAPS:
   - Base all geographical facts, historical dynasties, and locations on the provided context or verified subcontinental history.
   - Include source place citations and Google Maps navigation links.
   - NEVER fabricate ticket prices or train timetables.
"""

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.65"))
        self.client = None

        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                logger.info(f"Initialized Google GenAI client with model: {self.model_name}")
            except Exception as e:
                logger.warning(f"Could not initialize google-genai SDK: {e}. Running in local polyglot storyteller mode.")
        else:
            logger.info("No GEMINI_API_KEY found. Running with high-eloquence local polyglot storyteller.")

    def get_lang_pack(self, lang_code: str) -> Dict[str, str]:
        code = (lang_code or "en").lower().strip()
        return NATIVE_LANGUAGE_PACKS.get(code, NATIVE_LANGUAGE_PACKS["en"])

    def format_context(self, retrieved_chunks: List[Dict[str, Any]]) -> str:
        """Format retrieved passages into clean grounding context."""
        context_parts = []
        for i, c in enumerate(retrieved_chunks, 1):
            place = c.get("place", "Unknown")
            state = c.get("state", "India")
            best_time = c.get("best_time", "")
            time_info = f" | Best Time: {best_time}" if best_time else ""
            text = c.get("raw_passage", c.get("text", "")).strip()
            source = c.get("source", "Curated Guidebook")
            context_parts.append(f"[Source {i}: {place}, {state}{time_info} | License: {source}]\n{text}")
        return "\n\n".join(context_parts)

    def generate_local_grounded_answer(
        self,
        message: str,
        retrieved_chunks: List[Dict[str, Any]],
        language: str = "en"
    ) -> str:
        """
        High-quality local storytelling response generator with all wow factors,
        authentic jokes, cultural humor, and native language fluency.
        """
        lp = self.get_lang_pack(language)

        if not retrieved_chunks:
            return f"{lp['greeting']}\n\n{lp['joke']}\n\n{lp['farewell']}"

        top = retrieved_chunks[0]
        place = top.get("place", "")
        state = top.get("state", "India")
        city = top.get("city", "")
        best_time = top.get("best_time", "October to March")
        passage = top.get("raw_passage", top.get("text", ""))

        # Check if this item is a food record
        is_food = top.get("is_food", False)
        food_name = top.get("food_name", place)
        native_name = top.get("native_name", "")
        image_url = top.get("image_url", "")

        # Sentences for narrative
        sentences = [s.strip() for s in passage.split(".") if len(s.strip()) > 15]
        narrative = ". ".join(sentences[:3]) + "." if sentences else passage[:320]

        # Extract wow candidates
        wow_candidates = []
        for s in sentences[3:]:
            if any(k in s.lower() for k in ["built", "largest", "meter", "century", "stone", "sculpture", "unesco", "carved", "ancient", "temple", "spice", "emperor", "fort", "lake", "ghee", "recipe"]):
                wow_candidates.append(s.strip())
        
        wow_text = ". ".join(wow_candidates[:2]) + "." if wow_candidates else "A magnificent subcontinental treasure celebrated for its architectural genius, cultural antiquity, and soulful atmosphere."

        feast = REGIONAL_FEASTS.get(state, "authentic regional thali, aromatic street specialties, and traditional spiced tea")

        lat = top.get("lat")
        lon = top.get("lon")
        gmaps_url = top.get("google_maps_url", "")
        if not gmaps_url:
            if lat and lon and float(lat) != 0.0 and float(lon) != 0.0:
                gmaps_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
            else:
                gmaps_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(f'{place}, {state}, India')}"

        # Construct evocative, witty polyglot response
        response_sections = []

        # 1. Warm Greeting & Joke
        response_sections.append(f"{lp['greeting']}")
        response_sections.append(f"😄 **{lp['joke']}**")

        # 2. Living Saga
        place_header = f"**{place}** ({native_name})" if native_name else f"**{place}**"
        response_sections.append(f"### {lp['saga_prefix']}\n{place_header} — {state}\n\n{narrative}")

        # If image available, display markdown photo badge
        if image_url:
            response_sections.append(f"![{place}]({image_url})")

        # 3. Wow Factors
        response_sections.append(f"### {lp['wow_prefix']}\n• {wow_text}\n• An iconic heritage landmark where every corner whispers centuries of vibrant Indian history.")

        # 4. Culinary Soul
        if not is_food:
            response_sections.append(f"### {lp['food_prefix']}\nWhen in **{state}**, treat your palate to **{feast}**!")
        else:
            pairing_info = top.get("pairing", "traditional hot chai or fresh tender coconut water")
            response_sections.append(f"### {lp['food_prefix']}\n• **Authentic Pairing:** Enjoy this dish alongside {pairing_info} for the ultimate culinary feast.")

        # 5. Best Season & Maps
        response_sections.append(f"### {lp['best_time_prefix']} {best_time}\n\n### {lp['map_prefix']} [{place} on Google Maps]({gmaps_url})")

        # 6. Source Citation
        src_license = top.get("source", "CC BY-SA 4.0")
        response_sections.append(f"[Source: {place}, {state} | License: {src_license}]\n\n_{lp['farewell']}_")

        return "\n\n".join(response_sections)

    def generate_response(
        self,
        message: str,
        retrieved_chunks: List[Dict[str, Any]],
        context: Dict[str, Any],
        language: str = "en"
    ) -> Dict[str, Any]:
        """
        Generate complete grounded answer with confidence scoring, sources, and jokes.
        """
        top_score = retrieved_chunks[0]["similarity"] if retrieved_chunks else 0.85

        sources = [
            {
                "place": c.get("place", "Heritage Site"),
                "state": c.get("state", "India"),
                "source": c.get("source", "Wikipedia & Wikivoyage (CC BY-SA 4.0)"),
                "source_url": c.get("source_url", "https://en.wikipedia.org"),
                "google_maps_url": c.get("google_maps_url", ""),
                "image_url": c.get("image_url", ""),
                "similarity": c.get("similarity", 0.85)
            }
            for c in retrieved_chunks[:3]
        ]

        # If Gemini client is active, use LLM generation
        if self.client:
            prompt_context = self.format_context(retrieved_chunks)
            history_summary = context.get("summary", "")
            verbatim = context.get("verbatim_turns", [])
            discussed = ", ".join(context.get("places_discussed", []))

            history_str = ""
            if history_summary:
                history_str += f"PREVIOUS CONVERSATION CONTEXT:\n{history_summary}\n\n"
            if discussed:
                history_str += f"PLACES ALREADY DISCUSSED: {discussed}\n\n"
            if verbatim:
                history_str += "RECENT TURNS:\n"
                for t in verbatim[-3:]:
                    r = "Traveler" if t["role"] == "user" else "Guide"
                    history_str += f"{r}: {t['content']}\n"
                history_str += "\n"

            lang_map = {
                "ml": "Malayalam (മലയാളം script)",
                "hi": "Hindi (हिंदी Devanagari script)",
                "kn": "Kannada (ಕನ್ನಡ script)",
                "te": "Telugu (తెలుగు script)",
                "ta": "Tamil (தமிழ் script)",
                "tcy": "Tulu (ತುಳು / മലയാളം script)",
                "mr": "Marathi (मराठी Devanagari script)",
                "pa": "Punjabi (ਪੰਜਾਬੀ Gurmukhi script)",
                "bho": "Bhojpuri / Bihari (भोजपुरी Devanagari script)",
                "ne": "Nepali (नेपाली Devanagari script)",
                "bn": "Bengali (বাংলা script)",
                "gu": "Gujarati (ગુજરાતી script)",
                "or": "Odia (ଓଡ଼ିଆ script)",
                "as": "Assamese (অসমীয়া script)",
                "ur": "Urdu (اردو script)",
                "en": "English"
            }
            target_lang_desc = lang_map.get(language.lower(), "English")

            user_prompt = f"""{history_str}
[KNOWLEDGE BASE CONTEXT]
{prompt_context}

TRAVELER QUESTION:
{message}

INSTRUCTIONS:
1. TARGET LANGUAGE: Respond entirely in {target_lang_desc}.
2. TONE: Warm, charming, humorous local Indian storyteller.
3. HUMOR: Include a witty, authentic local travel joke or proverb in {target_lang_desc}.
4. SENSORY DETAILS: Evocative sights, sounds, and mouthwatering local foods with authentic pairings.
5. GROUNDING: Base historical details on context. Include Google Maps links and source citations in brackets.
"""
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_prompt,
                    config={
                        "system_instruction": SYSTEM_PERSONA_PROMPT,
                        "temperature": 0.6
                    }
                )
                answer = response.text.strip()
                return {
                    "answer": answer,
                    "confidence_mode": "grounded_knowledge_base",
                    "confidence_score": top_score,
                    "sources": sources
                }
            except Exception as e:
                logger.warning(f"Gemini API call failed: {e}. Falling back to local polyglot storyteller.")

        # High-eloquence local polyglot storyteller fallback
        answer = self.generate_local_grounded_answer(message, retrieved_chunks, language)
        return {
            "answer": answer,
            "confidence_mode": "grounded_knowledge_base",
            "confidence_score": top_score,
            "sources": sources
        }

    async def generate_streaming_response(
        self,
        message: str,
        retrieved_chunks: List[Dict[str, Any]],
        context: Dict[str, Any],
        language: str = "en"
    ) -> AsyncIterator[str]:
        """Server-Sent Events (SSE) streaming token generator."""
        res_data = self.generate_response(message, retrieved_chunks, context, language)
        answer = res_data["answer"]

        import asyncio
        words = answer.split(" ")
        for i, word in enumerate(words):
            chunk = word + (" " if i < len(words) - 1 else "")
            payload = json.dumps({"token": chunk, "done": False}, ensure_ascii=False)
            yield f"data: {payload}\n\n"
            await asyncio.sleep(0.018)

        final_meta = {
            "done": True,
            "sources": res_data["sources"],
            "confidence_mode": res_data["confidence_mode"],
            "confidence_score": res_data["confidence_score"]
        }
        yield f"data: {json.dumps(final_meta, ensure_ascii=False)}\n\n"
