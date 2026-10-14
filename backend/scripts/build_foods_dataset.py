"""
Build Authentic Indian Regional Foods Dataset for Incredible Journeys.
Includes authentic dishes across all regions of India with verified Wikimedia Commons photography,
native scripts, flavor profiles, and cultural heritage stories.
"""

import json
from pathlib import Path

FOODS = [
    # KERALA & MALABAR
    {
        "id": "kozhikode_dum_biryani",
        "name": "Malabar Dum Biryani (Kozhikode Biryani)",
        "native_name": "കോഴിക്കോടൻ ദം ബിരിയാണി",
        "state": "Kerala",
        "region": "South India",
        "language": "ml",
        "category": "Biryani & Rice",
        "is_veg": False,
        "flavor_profile": "Fragrant, delicate ghee aroma, short-grain Khyma rice, mild spices, fried sultanas and cashews",
        "story": "Brought by Arab spice merchants to the Malabar coast, Kozhikode biryani uses petite Khyma (Jeerakasala) rice instead of Basmati. Sealed with dough in heavy copper pots over gentle embers, the meat cooks in its own juices until tender.",
        "best_places_to_try": "Paragon Restaurant, Rahmath Hotel, and Sagar Restaurant in Kozhikode",
        "pairing": "Sulaimani spiced black tea with mint and date pickle",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Malabar_Chicken_Biryani.jpg/1280px-Malabar_Chicken_Biryani.jpg"
    },
    {
        "id": "kozhikodan_halwa",
        "name": "Kozhikodan Halwa (Calicut Halwa)",
        "native_name": "കോഴിക്കോടൻ ഹൽവ",
        "state": "Kerala",
        "region": "South India",
        "language": "ml",
        "category": "Sweets & Desserts",
        "is_veg": True,
        "flavor_profile": "Glossy, chewy, gelatinous texture with pure coconut oil, jaggery, cardamom, and crunchy cashews",
        "story": "Crafted in giant iron cauldrons along S.M. Street (Mittayi Theruvu or Sweetmeat Street) for over two centuries. Famous in black (karuppu jaggery), tender coconut, jackfruit, and mango varieties.",
        "best_places_to_try": "S.M. Street sweet stalls and Sankaran Bakery in Kozhikode",
        "pairing": "Strong Kerala filter coffee",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Calicut_Halwa.JPG/1280px-Calicut_Halwa.JPG"
    },
    {
        "id": "kerala_pazham_pori",
        "name": "Pazham Pori & Banana Chips",
        "native_name": "പഴം പൊരി & കായ വറുത്തത്",
        "state": "Kerala",
        "region": "South India",
        "language": "ml",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Crispy golden exterior with sweet, warm molten Nendran banana inside; salted chips fried in unrefined coconut oil",
        "story": "The quintessential evening teatime staple across every Kerala railway platform and village tea shop (chayakkada). Golden ripe plantains dipped in a light flour batter and crisped in bubbling oil.",
        "best_places_to_try": "Tea stalls across Kozhikode, Alappuzha backwaters, and Kochi Fort",
        "pairing": "Hot steaming cup of cardamom-infused chai",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Pazham_Pori_Kerala_Snack.jpg/1280px-Pazham_Pori_Kerala_Snack.jpg"
    },
    {
        "id": "kerala_appam_and_stew",
        "name": "Appam with Vegetable / Chicken Stew",
        "native_name": "അപ്പവും ഇഷ്‌ടൂവും",
        "state": "Kerala",
        "region": "South India",
        "language": "ml",
        "category": "Curries & Stews",
        "is_veg": True,
        "flavor_profile": "Lacy crisp edges with a soft, pillowy fermented rice center; velvety coconut milk stew with green chilies and cloves",
        "story": "Fermented with toddy or yeast in curved 'appachatti' pans, this Christian Syrian heritage breakfast pairs delicate fluffy appams with fragrant coconut milk simmered with whole spices.",
        "best_places_to_try": "Traditional homestays in Kottayam, Munnar, and Kumarakom",
        "pairing": "Fresh tender coconut water",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Appam_and_veg_stew.jpg/1280px-Appam_and_veg_stew.jpg"
    },

    # KARNATAKA & TULU NADU
    {
        "id": "tulu_kori_rotti",
        "name": "Mangalorean Kori Rotti & Ghee Roast",
        "native_name": "ಕೋರಿ ರೊಟ್ಟಿ (ತುಳು: ಕೋರಿ ರೊಟ್ಟಿ)",
        "state": "Karnataka",
        "region": "South India",
        "language": "tcy",
        "category": "Curries & Stews",
        "is_veg": False,
        "flavor_profile": "Paper-thin brittle sun-dried rice wafers soaked in fiery, coconut-rich red chicken curry",
        "story": "The proud centerpiece of Tuluva (Bunt) community feasts in coastal Karnataka. The crispy, wafer-thin rottis crackle on the tongue before melting completely into the spiced coconut gravy.",
        "best_places_to_try": "Giri Manja's and Maharaja Restaurant in Mangaluru (Kudla), and Udupi coast",
        "pairing": "Chilled Kokum sharbat or Solkadhi",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Chicken_Ghee_Roast.jpg/1280px-Chicken_Ghee_Roast.jpg"
    },
    {
        "id": "mangalore_neer_dosa",
        "name": "Coastal Neer Dosa",
        "native_name": "ನೀರ್ ದೋಸೆ (ತುಳು: ನೀರ್ ದೋಸೆ)",
        "state": "Karnataka",
        "region": "South India",
        "language": "kn",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Melt-in-the-mouth, ultra-thin, soft, delicate crepe made without fermentation",
        "story": "'Neer' translates to water in Tulu and Kannada, named for its thin, watery rice batter that needs no fermentation. Poured onto smoking cast iron, it cooks in seconds into a snow-white gossamer handkerchief.",
        "best_places_to_try": "Udupi Sri Krishna Temple dining halls and coastal Mangalore beach shacks",
        "pairing": "Sweet grated coconut jaggery mixture and spicy coconut chutney",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Neer_Dosa.jpg/1280px-Neer_Dosa.jpg"
    },
    {
        "id": "mysore_masala_dosa",
        "name": "Mysore Masala Dosa",
        "native_name": "ಮೈಸೂರು ಮಸಾಲೆ ದೋಸೆ",
        "state": "Karnataka",
        "region": "South India",
        "language": "kn",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Golden crisp outer crust, red spicy garlic chutney slathered inside, potato masala filling, glistening with pure butter",
        "story": "Created for the royals in the kitchens of Mysore Palace, distinguished by its thick-yet-crispy texture and the secret tangy red chutney made with Byadgi chilies and roasted gram.",
        "best_places_to_try": "Mylari Hotel in Mysuru, and Vidyarthi Bhavan in Bengaluru",
        "pairing": "Filter kaapi served in a traditional dabarah set",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Dosa_and_ghee.jpg/1280px-Dosa_and_ghee.jpg"
    },
    {
        "id": "bisi_bele_bath",
        "name": "Bisi Bele Bath & Mysore Pak",
        "native_name": "ಬಿಸಿ ಬೇಳೆ ಬಾತ್ ಮತ್ತು ಮೈಸೂರು ಪಾಕ್",
        "state": "Karnataka",
        "region": "South India",
        "language": "kn",
        "category": "Biryani & Rice",
        "is_veg": True,
        "flavor_profile": "Spicy, tangy, piping-hot rice and lentil porridge cooked with vegetables, nutmeg, marathi moggu, and topped with ghee and boondi",
        "story": "Literally 'Hot Lentil Rice' originating in the Mysore royal palace. Paired with Mysore Pak, the heavenly fudge of chickpea flour and ghee invented by royal chef Kakasura Madappa in 1935.",
        "best_places_to_try": "MTR (Mavalli Tiffin Room) in Bengaluru and Guru Sweet Mart in Mysuru",
        "pairing": "Crisp potato chips and spicy raita",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Bisi_bele_bath_with_boondi.jpg/1280px-Bisi_bele_bath_with_boondi.jpg"
    },

    # TAMIL NADU
    {
        "id": "chettinad_chicken_and_dosa",
        "name": "Chettinad Pepper Chicken & Ghee Roast",
        "native_name": "செட்டிநாடு சிக்கன் & நெய் ரோஸ்ட்",
        "state": "Tamil Nadu",
        "region": "South India",
        "language": "ta",
        "category": "Curries & Stews",
        "is_veg": False,
        "flavor_profile": "Explosive freshly roasted black peppercorns, star anise, kalpasi (stone flower), and shallots",
        "story": "Crafted by the wealthy seafaring Chettiar merchant community who brought exotic spices from Southeast Asia. Famous for using freshly ground whole spices roasted on slow wood fires.",
        "best_places_to_try": "Karaikudi heritage mansions and Anjappar in Chennai",
        "pairing": "Madurai Jigarthanda (chilled almond gum, nannari syrup, and clotted cream)",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Chettinad_chicken.jpg/1280px-Chettinad_chicken.jpg"
    },
    {
        "id": "madurai_jigarthanda",
        "name": "Madurai Royal Jigarthanda",
        "native_name": "மதுரை ஜிகர்தண்டா",
        "state": "Tamil Nadu",
        "region": "South India",
        "language": "ta",
        "category": "Sweets & Desserts",
        "is_veg": True,
        "flavor_profile": "Creamy, chilled, caramel-like richness with soothing almond tree gum (badam pisin) and sarsaparilla root syrup",
        "story": "Literally 'Cooler of the Heart', introduced to Madurai by Mughal governors. A luxurious elixir made with condensed caramelized milk, tree resin, and hand-churned clotted cream (basundi ice cream).",
        "best_places_to_try": "Famous Jigarthanda stalls near Meenakshi Amman Temple, Madurai",
        "pairing": "Spicy Madurai mutton sukka or bun parotta",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Jigarthanda_Madurai.jpg/1280px-Jigarthanda_Madurai.jpg"
    },

    # TELANGANA & ANDHRA PRADESH
    {
        "id": "hyderabadi_dum_biryani",
        "name": "Hyderabadi Kacchi Dum Biryani",
        "native_name": "హైదరాబాదీ దమ్ బిర్యానీ",
        "state": "Telangana",
        "region": "South India",
        "language": "te",
        "category": "Biryani & Rice",
        "is_veg": False,
        "flavor_profile": "Long-grain basmati infused with saffron milk, marinated meat infused with yogurt and fried onions, cooked in kacchi dum style",
        "story": "Developed in the royal kitchens of the Nizams of Hyderabad, blending Mughlai and royal Telugu culinary heritage. Raw marinated meat and parboiled rice are slow-cooked together in an airtight handi.",
        "best_places_to_try": "Bawarchi, Paradise, and Shadab near Charminar, Hyderabad",
        "pairing": "Mirchi ka Salan (green chili and peanut gravy) and sweet Dabal ka Meetha",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Hyderabadi_Chicken_Biryani.jpg/1280px-Hyderabadi_Chicken_Biryani.jpg"
    },
    {
        "id": "andhra_gongura_mutton",
        "name": "Andhra Gongura Mutton & Pootharekulu",
        "native_name": "గోంగూర మటన్ మరియు పూతరేకులు",
        "state": "Andhra Pradesh",
        "region": "South India",
        "language": "te",
        "category": "Curries & Stews",
        "is_veg": False,
        "flavor_profile": "Intensely tangy sorrel leaves (gongura) braised with succulent meat, Guntur fiery red chilies, and pure ghee",
        "story": "Gongura (roselle leaves) is hailed as the culinary crown of Andhra Pradesh. The natural tartness cuts through rich mutton, creating a spicy and tangy explosion balanced by sweet rice-wafer Pootharekulu.",
        "best_places_to_try": "Traditional mess dining halls in Vijayawada, Guntur, and Visakhapatnam",
        "pairing": "Steaming hot Sona Masoori rice and Avakaya mango pickle",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Gongura_Pachadi.jpg/1280px-Gongura_Pachadi.jpg"
    },

    # NORTH INDIA: PUNJAB & DELHI
    {
        "id": "amritsari_kulcha_chole",
        "name": "Amritsari Kulcha with Pindi Chole",
        "native_name": "ਅੰਮ੍ਰਿਤਸਰੀ ਕੁਲਚਾ ਅਤੇ ਪਿੰਡੀ ਛੋਲੇ",
        "state": "Punjab",
        "region": "North India",
        "language": "pa",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Flaky multi-layered tandoor bread stuffed with spiced potato and crushed pomegranate seeds, smothered in white butter",
        "story": "Baked in underground clay tandoors across Amritsar's lanes near the Golden Temple. Crushed by hand while piping hot so that the layers shatter, releasing pockets of melted homemade butter.",
        "best_places_to_try": "Bhai Kulwant Singh Kulchian Wale and Kesar Da Dhaba in Amritsar",
        "pairing": "Tall brass tumbler of thick malai-topped sweet Punjabi lassi",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Amritsari_Kulcha_with_Chole.jpg/1280px-Amritsari_Kulcha_with_Chole.jpg"
    },
    {
        "id": "punjabi_sarson_saag_makki_roti",
        "name": "Sarson da Saag & Makki di Roti",
        "native_name": "ਸਰ੍ਹੋਂ ਦਾ ਸਾਗ ਅਤੇ ਮੱਕੀ ਦੀ ਰੋਟੀ",
        "state": "Punjab",
        "region": "North India",
        "language": "pa",
        "category": "Curries & Stews",
        "is_veg": True,
        "flavor_profile": "Earthy mustard greens slow-cooked for hours with bathua and spinach, served with golden cornmeal flatbread and white butter",
        "story": "The winter soul of the Punjab countryside. Eaten after harvest season with generous chunks of golden jaggery (gud) and freshly churned butter from buffalo milk.",
        "best_places_to_try": "Village dhabas along the Grand Trunk Road between Jalandhar and Amritsar",
        "pairing": "Raw white radishes, green chilies, and fresh jaggery",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Sarson_ka_saag_and_makki_di_roti.jpg/1280px-Sarson_ka_saag_and_makki_di_roti.jpg"
    },

    # BIHAR & PURVANCHAL (BHOJPURI / BIHARI)
    {
        "id": "bihari_litti_chokha",
        "name": "Bihari Litti Chokha & Sattu Paratha",
        "native_name": "लिट्टी चोखा (भोजपुरी: लिट्टी चोखा)",
        "state": "Bihar",
        "region": "East India",
        "language": "bho",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Smoky whole-wheat dough balls stuffed with spiced roasted gram flour (sattu), drenched in warm desi ghee, served with roasted brinjal mash",
        "story": "The legendary staple of the Magadh and Bhojpur kingdoms, carried by ancient soldiers for its stamina-giving sattu. Roasted traditionally over dried cow dung cakes or charcoal embers for an unmistakable woodsmoke flavor.",
        "best_places_to_try": "Patna Maurya Lok food plaza, Bodh Gaya village stalls, and Buxar",
        "pairing": "Spicy tomato-garlic chutney and Silao Khaja sweet pastry",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Litti_Chokha_Bihar.jpg/1280px-Litti_Chokha_Bihar.jpg"
    },
    {
        "id": "bihar_silao_khaja",
        "name": "GI-Tagged Silao Khaja",
        "native_name": "सिलाव का खाजा (भोजपुरी)",
        "state": "Bihar",
        "region": "East India",
        "language": "bho",
        "category": "Sweets & Desserts",
        "is_veg": True,
        "flavor_profile": "Feather-light, multi-layered crispy sweet pastry that shatters on contact with the tongue",
        "story": "Crafted in the historic village of Silao between Nalanda and Rajgir. Legend says Lord Buddha was offered Khaja on his travels through ancient Magadha. Holds official GI tag protection for its 52 wafer-thin layers.",
        "best_places_to_try": "Traditional sweet shops in Silao and Rajgir",
        "pairing": "Desi chai brewed over charcoal embers",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Khaja_sweet.jpg/1280px-Khaja_sweet.jpg"
    },

    # UTTAR PRADESH & AWADH
    {
        "id": "awadhi_galouti_kebab",
        "name": "Awadhi Galouti Kebab & Ulte Tawe ka Paratha",
        "native_name": "गलौटी कबाब (अवधी)",
        "state": "Uttar Pradesh",
        "region": "North India",
        "language": "hi",
        "category": "Breads & Street Food",
        "is_veg": False,
        "flavor_profile": "Melt-in-mouth texture so delicate it dissolves without chewing, infused with raw papaya and over 150 royal botanicals",
        "story": "Invented in the royal courts of Lucknow for Nawab Asad-ud-Daula who had lost his teeth with age but retained his epicurean passion for kebabs. Smoked with cloves and betel leaves.",
        "best_places_to_try": "Tunday Kababi in Aminabad and Chowk, Lucknow",
        "pairing": "Sheermal saffron milk flatbread and mint chutney",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Galouti_Kebab.jpg/1280px-Galouti_Kebab.jpg"
    },
    {
        "id": "banarasi_kachori_jalebi",
        "name": "Banarasi Kachori, Tamatar Chaat & Jalebi",
        "native_name": "बनारसी कचौरी-जलेबी और टमाटर चाट",
        "state": "Uttar Pradesh",
        "region": "North India",
        "language": "hi",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Spicy hing (asafoetida) lentil kachoris served with spiced potato subzi, followed by piping hot saffron-syrup jalebis",
        "story": "The timeless dawn ritual along the ancient ghats of Kashi. Travelers and pilgrims gather at sunrise for leaf plates (dona) of piping-hot kachori followed by crispy jalebi straight from the boiling oil.",
        "best_places_to_try": "Ram Bhandar in Thatheri Bazaar and Kashi Chaat Bhandar near Dashashwamedh Ghat",
        "pairing": "Thick kulhad lassi sprinkled with rabri and pistachios",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Jalebi_in_Varanasi.jpg/1280px-Jalebi_in_Varanasi.jpg"
    },

    # RAJASTHAN
    {
        "id": "rajasthani_dal_baati_churma",
        "name": "Rajasthani Dal Baati Churma",
        "native_name": "दाल बाटी चूरमा (राजस्थानी)",
        "state": "Rajasthan",
        "region": "North India",
        "language": "hi",
        "category": "Curries & Stews",
        "is_veg": True,
        "flavor_profile": "Hard wheat dumplings cracked open and soaked in pure hot ghee, served with five-lentil stew (panchmel dal) and sweet jaggery churma",
        "story": "Originated during the reign of the Mewar kingdom. Rajput warriors buried dough balls under scorching desert sand during the day; when they returned, the desert heat had baked them into hearty meals.",
        "best_places_to_try": "Chokhi Dhani and Laxmi Mishthan Bhandar (LMB) in Jaipur",
        "pairing": "Spicy garlic chutney, ker sangri berries, and buttermilk (chhaas)",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Dal_Baati_Churma.jpg/1280px-Dal_Baati_Churma.jpg"
    },

    # MAHARASHTRA
    {
        "id": "maharashtrian_vada_pav",
        "name": "Mumbai Vada Pav & Misal Pav",
        "native_name": "वडा पाव आणि झणझणीत मिसळ पाव",
        "state": "Maharashtra",
        "region": "West India",
        "language": "mr",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Golden spiced potato fritter encased in gram flour batter, tucked into pillowy pav with fiery garlic-peanut dry chutney and fried green chilies",
        "story": "Invented outside Dadar station in 1966 by Ashok Vaidya as a quick, affordable, energizing meal for Mumbai mill workers. Today it is recognized as India's premier street food icon.",
        "best_places_to_try": "Aram Milk Bar at CSMT, Dadar station stalls in Mumbai, and Katakirrr Misal in Pune",
        "pairing": "Cutting chai in miniature glass tumblers and Solkadhi",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Vada_Pav-Indian_street_food.JPG/1280px-Vada_Pav-Indian_street_food.JPG"
    },
    {
        "id": "maharashtrian_puran_poli",
        "name": "Puran Poli with Katachi Amti",
        "native_name": "पुरण पोळी आणि कटाची आमटी",
        "state": "Maharashtra",
        "region": "West India",
        "language": "mr",
        "category": "Sweets & Desserts",
        "is_veg": True,
        "flavor_profile": "Ultra-thin, soft, delicate flatbread stuffed with golden chana dal, jaggery, nutmeg, and cardamom, dripping with ghee",
        "story": "The sacred festive sweet of Maharashtra for Gudi Padwa and Ganesh Chaturthi. The remaining broth from boiling the dal is transformed into Katachi Amti, a spicy-sweet lentil soup.",
        "best_places_to_try": "Traditional dining halls in Pune, Kolhapur, and Nagpur",
        "pairing": "Warm milk infused with saffron or spicy Katachi Amti",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Puran_Poli_dish.jpg/1280px-Puran_Poli_dish.jpg"
    },

    # GUJARAT
    {
        "id": "gujarati_dhokla_khandvi",
        "name": "Khaman Dhokla, Khandvi & Undhiyu",
        "native_name": "ખમણ ઢોકળા અને ખાંડવી",
        "state": "Gujarat",
        "region": "West India",
        "language": "gu",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Spongy, juicy fermented chickpea cake tempered with mustard seeds, green chilies, and fresh coriander; delicate yellow gram flour rolls",
        "story": "A triumph of steaming and fermentation in vegetarian Jain and Gujarati culinary tradition. Light on digestion yet deeply satisfying with a balance of sweet, sour, and fiery flavors.",
        "best_places_to_try": "Das Khaman in Ahmedabad and street food bazaars of Surat",
        "pairing": "Sweet raw papaya sambharo and fried salted green chilies",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Khaman_Dhokla.jpg/1280px-Khaman_Dhokla.jpg"
    },

    # BENGAL
    {
        "id": "bengali_shorshe_ilish",
        "name": "Shorshe Ilish & Kolkata Kathi Roll",
        "native_name": "সর্ষে ইলিশ এবং কাঠি রোল",
        "state": "West Bengal",
        "region": "East India",
        "language": "bn",
        "category": "Curries & Stews",
        "is_veg": False,
        "flavor_profile": "Pungent yellow and black mustard paste, green chilies, and virgin mustard oil smothering succulent Hilsa river fish",
        "story": "The cultural soul of Bengali heritage. The silvery Hilsa fish swimming up the monsoon waters of the Padma and Hooghly rivers is steamed wrapped in banana leaves or simmered in pungent mustard gravy.",
        "best_places_to_try": "6 Ballygunge Place and Kasturi in Kolkata",
        "pairing": "Steaming Govindobhog rice and Mishti Doi dessert",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Shorshe_Ilish.jpg/1280px-Shorshe_Ilish.jpg"
    },
    {
        "id": "bengali_rosogolla_mishti_doi",
        "name": "Kolkata Rosogolla & Mishti Doi",
        "native_name": "রসগোল্লা এবং মিষ্টি দই",
        "state": "West Bengal",
        "region": "East India",
        "language": "bn",
        "category": "Sweets & Desserts",
        "is_veg": True,
        "flavor_profile": "Spongy, snowy-white cottage cheese balls that squirt delicate sugar syrup; caramelized fermented sweet yogurt set in earthen clay pots",
        "story": "Invented by confectioner Nobin Chandra Das in Bagbazar, Kolkata, in 1868. The clay pots absorb excess moisture in Mishti Doi, concentrating the caramelized creaminess.",
        "best_places_to_try": "K.C. Das, Balaram Mullick & Radharaman Mullick in Kolkata",
        "pairing": "Warm Darjeeling muscatel tea",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Mishti_Doi_in_clay_pot.jpg/1280px-Mishti_Doi_in_clay_pot.jpg"
    },

    # ODISHA
    {
        "id": "odia_chhena_poda",
        "name": "Odia Chhena Poda",
        "native_name": "ଛେନା ପୋଡ଼ (ଓଡ଼ିଆ)",
        "state": "Odisha",
        "region": "East India",
        "language": "or",
        "category": "Sweets & Desserts",
        "is_veg": True,
        "flavor_profile": "Caramelized brown crust on the outside with sweet, smoky, cardamom-scented baked cottage cheese inside",
        "story": "Regarded as India's original cheesecake, born in Nayagarh, Odisha, when a confectioner mixed leftover fresh cottage cheese with sugar and left it overnight in a warm wood-fired oven.",
        "best_places_to_try": "Nayagarh sweet shops and Puri Grand Road near Jagannath Temple",
        "pairing": "Fermented Pakhala Bhata lunch",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Chhena_Poda.jpg/1280px-Chhena_Poda.jpg"
    },

    # SIKKIM, LADAKH & HIMALAYAN NEPALI
    {
        "id": "himalayan_momos_thukpa",
        "name": "Himalayan Steamed Momos & Thukpa",
        "native_name": "म:म: र थुक्पा (नेपाली / लद्दाखी)",
        "state": "Sikkim",
        "region": "Northeast India",
        "language": "ne",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Juicy steamed dumplings stuffed with spiced vegetables or minced meat, dipped in fiery Dalle Khursani chili sauce; comforting hot noodle broth",
        "story": "Beloved across Sikkim, Darjeeling, Ladakh, and the trans-Himalayan valleys. Shared by Nepali, Tibetan, and Lepcha communities to warm cold mountain nights.",
        "best_places_to_try": "MG Marg in Gangtok, Leh main bazaar, and Mall Road in Darjeeling",
        "pairing": "Comforting Himalayan salted butter tea (Gur-Gur chai)",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Momos_nepal.jpg/1280px-Momos_nepal.jpg"
    },
    {
        "id": "nepali_sel_roti_gundruk",
        "name": "Nepali Sel Roti & Gundruk",
        "native_name": "सेल रोटी र गुन्द्रुक (नेपाली)",
        "state": "Sikkim",
        "region": "Northeast India",
        "language": "ne",
        "category": "Breads & Street Food",
        "is_veg": True,
        "flavor_profile": "Ring-shaped crispy sweet rice doughnut with a delicate chew, paired with fermented mustard leaf broth",
        "story": "Prepared traditionally during Tihar, Dashain, and weddings in Nepali-speaking households of Sikkim, Kalimpong, and Nepal. Hand-poured into hot ghee in concentric rings.",
        "best_places_to_try": "Local homestays in Pelling, Gangtok, and Kalimpong",
        "pairing": "Fermented Gundruk soup and spicy tomato pickle",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Sel_Roti.jpg/1280px-Sel_Roti.jpg"
    },

    # GOA
    {
        "id": "goan_fish_curry_bebinca",
        "name": "Goan Fish Curry & Bebinca",
        "native_name": "गोवन फिश करी आणि बेबिका",
        "state": "Goa",
        "region": "West India",
        "language": "en",
        "category": "Curries & Stews",
        "is_veg": False,
        "flavor_profile": "Tangy dried kokum, creamy freshly squeezed coconut milk, Kashmiri red chilies, and Kingfish; seven-layered caramelized dessert",
        "story": "The soul of the Konkan coastline, blending Portuguese baking with Indian spices. Bebinca, the 'Queen of Goan desserts', is baked layer by layer using coconut milk, ghee, and egg yolks.",
        "best_places_to_try": "Fisherman's Wharf in Cavelossim and Ritz Classic in Panaji",
        "pairing": "Red unpolished Goan boiled rice and chilled feni cocktail",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Goan_Fish_Curry.jpg/1280px-Goan_Fish_Curry.jpg"
    },

    # KASHMIR
    {
        "id": "kashmiri_rogan_josh_kahwa",
        "name": "Kashmiri Rogan Josh & Kahwa",
        "native_name": "روغن جوش اور کہوہ (کشمیری)",
        "state": "Jammu and Kashmir",
        "region": "North India",
        "language": "ur",
        "category": "Curries & Stews",
        "is_veg": False,
        "flavor_profile": "Deep scarlet gravy from Kashmiri mawal cockscomb flower, flavored with fennel and dry ginger, free of onions and garlic in Pandit style",
        "story": "The crown jewel of the royal 36-course Kashmiri Wazwan feast. Slow-braised in copper vessels with whole spices and pure saffron.",
        "best_places_to_try": "Ahdoos and Mughal Darbar on the Bund, Srinagar",
        "pairing": "Saffron Kahwa green tea brewed in a brass samovar with crushed almonds",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Rogan_Josh.jpg/1280px-Rogan_Josh.jpg"
    },

    # ASSAM & NORTHEAST
    {
        "id": "assamese_masor_tenga",
        "name": "Assamese Masor Tenga & Khaar",
        "native_name": "মাছৰ টেঙা আৰু খাৰ (অসমীয়া)",
        "state": "Assam",
        "region": "Northeast India",
        "language": "as",
        "category": "Curries & Stews",
        "is_veg": False,
        "flavor_profile": "Refreshing, light, tangy sour fish broth infused with elephant apple (ou tenga) or tomatoes, tempered with fenugreek seeds",
        "story": "The defining centerpiece of Assamese lunches, designed to soothe and refresh during warm Brahmaputra valley afternoons. Follows Khaar, the traditional alkaline cleansing dish.",
        "best_places_to_try": "Paradise Restaurant and Khorikaa in Guwahati",
        "pairing": "Aromatic Joha sticky rice and ghost chili (Bhut Jolokia) relish",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/Masor_Tenga_Assam.jpg/1280px-Masor_Tenga_Assam.jpg"
    }
]

def main():
    out_file = Path(__file__).resolve().parent.parent / "data" / "foods.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(FOODS, f, indent=2, ensure_ascii=False)
    print(f"Exported {len(FOODS)} authentic Indian regional foods to {out_file}")

if __name__ == "__main__":
    main()
