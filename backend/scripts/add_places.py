"""
Adds expanded destinations including Palakkad, Nilambur, Malappuram, Wayanad,
and architectural wonders of India to the knowledge base.
"""

import os
import json
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
SEED_CSV = BASE_DIR / "data" / "places_seed.csv"

NEW_PLACES = [
    {
        "id": "palakkad_fort_tipus_fort",
        "place": "Palakkad Fort (Tipu Sultan's Fort)",
        "state": "Kerala",
        "city": "Palakkad",
        "category": ["forts", "heritage", "architecture"],
        "wikipedia_title": "Palakkad_Fort",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Palakkad_Fort",
        "wikidata_id": "Q3525203",
        "lat": 10.7667,
        "lon": 76.6558,
        "text": "Palakkad Fort, popularly known as Tipu Sultan's Fort, is an exceptionally preserved granite fort situated in the heart of Palakkad town in Kerala, India. Rebuilt in 1766 AD by Hyder Ali of Mysore and later fortified by his son Tipu Sultan, the stronghold features massive square granite bastions, a deep protective moat that once teemed with crocodiles, and an ancient Hanuman temple revered by generations. Guarding the strategic 30-kilometer Palakkad Gap through the Western Ghats—the ancient commercial and military gateway connecting Kerala to Tamil Nadu and the Deccan—the fort grounds today encompass lush manicured lawns, the Rappadi open-air auditorium, and an Archaeological Survey of India museum.",
        "best_time": "October to March (pleasant tropical winter; ideal for heritage walks)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Palakkad_Fort",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "malampuzha_dam_and_gardens",
        "place": "Malampuzha Dam and Ornamental Gardens",
        "state": "Kerala",
        "city": "Palakkad",
        "category": ["nature", "gardens", "dam"],
        "wikipedia_title": "Malampuzha_Dam",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Malampuzha_Dam",
        "wikidata_id": "Q3595460",
        "lat": 10.8306,
        "lon": 76.6833,
        "text": "Malampuzha Dam is the largest reservoir dam in Kerala, set dramatically against the towering peaks of the Western Ghats near Palakkad. Commissioned in 1955 across the Malampuzha River (a tributary of the Bharathappuzha), the destination combines engineering prowess with sprawling Mughal-inspired landscaped gardens, dancing illuminated musical fountains, South India's first passenger ropeway soaring across the emerald lake, a freshwater aquarium shaped like a giant fish, and the legendary monumental Yakshi sculpture carved from concrete by master sculptor Kanayi Kunhiraman.",
        "best_time": "September to February (post-monsoon lush greenery and cool evenings)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Malampuzha_Dam",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "nilambur_teak_museum_and_conolly_plot",
        "place": "Nilambur Teak Museum and Conolly's Plot",
        "state": "Kerala",
        "city": "Nilambur, Malappuram",
        "category": ["nature", "museums", "forests"],
        "wikipedia_title": "Teak_Museum",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Teak_Museum",
        "wikidata_id": "Q7691232",
        "lat": 11.2789,
        "lon": 76.2269,
        "text": "The Nilambur Teak Museum, located 4 km from Nilambur town in Malappuram district, is the world's very first specialized museum dedicated to the teak tree (Tectona grandis). Managed by the Kerala Forest Research Institute, it chronicles the botanical structure, historical British timber logging, and shipbuilding traditions of Malabar. Just across the Chaliyar River via a scenic suspension bridge lies Conolly's Plot—the oldest teak plantation in the world, established in 1842 by Malabar District Collector H.V. Conolly. The towering giant Kannimara teak trees here soar more than 50 meters into the sky with girths exceeding 3.5 meters.",
        "best_time": "October to March (pleasant riverside breeze and forest canopy walks)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Teak_Museum",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "kottakkal_arya_vaidya_sala",
        "place": "Kottakkal Arya Vaidya Sala",
        "state": "Kerala",
        "city": "Kottakkal, Malappuram",
        "category": ["culture", "heritage", "ayurveda"],
        "wikipedia_title": "Arya_Vaidya_Sala",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Arya_Vaidya_Sala",
        "wikidata_id": "Q3595448",
        "lat": 10.9983,
        "lon": 75.9981,
        "text": "Kottakkal Arya Vaidya Sala is a world-renowned century-old charitable Ayurvedic healthcare institution established in 1902 by Vaidyaratnam P. S. Varier in Kottakkal, Malappuram district, Kerala. Globally celebrated as the cradle of authentic classical Ayurveda, Panchakarma rejuvenation treatments, and scientific herbal medicine preparation, Kottakkal attracts travelers, scholars, and dignitaries worldwide. Beyond medical sanatoriums, it sustains extensive medicinal plant botanical gardens and the P.S.V. Natyasangham, a legendary performing arts troupe that preserves classical Kathakali dance.",
        "best_time": "June to September for classical Monsoon Karkidaka rejuvenation; October to March for cultural visits",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Arya_Vaidya_Sala",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "thirunavaya_navamukunda_temple",
        "place": "Thirunavaya Navamukunda Temple and Mamankam Heritage",
        "state": "Kerala",
        "city": "Thirunavaya, Malappuram",
        "category": ["temple", "pilgrimage", "heritage"],
        "wikipedia_title": "Thirunavaya_Navamukunda_Temple",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Thirunavaya_Navamukunda_Temple",
        "wikidata_id": "Q7785315",
        "lat": 10.8667,
        "lon": 75.9833,
        "text": "Thirunavaya Navamukunda Temple is a sacred riverside shrine on the banks of the historic Bharathappuzha (River Nila) in Malappuram district, Kerala. One of the 108 revered Divya Desams of Lord Vishnu praised by Tamil Alvar saints, the temple's sandbanks were the battleground of Mamankam—a grand medieval festival held every 12 years. At Mamankam, sworn suicide warriors (Chaver) from the Valluvanad kingdom fought through thousands of the Kozhikode Zamorin's royal guards to attempt to slay the monarch standing on the Nilapaduthara stone platform. The preserved Nilapaduthara platform, Manikkinar well, and Changampalli martial kalari evoke the epic martial traditions of Malabar.",
        "best_time": "November to February (mild winter, sacred river rites)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Thirunavaya_Navamukunda_Temple",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "chembra_peak_and_heart_lake",
        "place": "Chembra Peak and Heart-Shaped Lake",
        "state": "Kerala",
        "city": "Meppadi, Wayanad",
        "category": ["mountain", "nature", "trekking"],
        "wikipedia_title": "Chembra_Peak",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Chembra_Peak",
        "wikidata_id": "Q3532729",
        "lat": 11.5128,
        "lon": 76.0886,
        "text": "Chembra Peak is the towering crown of Wayanad, rising 2,100 meters above sea level amidst tea plantations, spice estates, and misty shola forest cloud ridges. Managed under community eco-tourism by the forest department, the trek ascends through lush emerald meadows to 'Hridaya Saras'—a natural perennial alpine lake shaped perfectly like a heart. Believed by local tribes never to dry up even in harsh summer droughts, the mist that floats over the heart lake offers breathtaking panoramic vistas across the Nilgiri hills, Kozhikode coastline, and cloud-draped valleys of the Western Ghats.",
        "best_time": "September to March (clear blue skies, misty breeze, optimal trekking trails)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Chembra_Peak",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "banasura_sagar_dam_wayanad",
        "place": "Banasura Sagar Dam and Island Lake",
        "state": "Kerala",
        "city": "Padinjarathara, Wayanad",
        "category": ["nature", "dam", "lakes"],
        "wikipedia_title": "Banasura_Sagar_Dam",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Banasura_Sagar_Dam",
        "wikidata_id": "Q4854086",
        "lat": 11.6694,
        "lon": 75.9572,
        "text": "Banasura Sagar Dam in Wayanad is the largest earthen dam in India and the second largest in all of Asia, constructed using massive boulders and packed earth across the Karamanathodu tributary of the Kabini River. Named after the mythical demon king Banasura who performed penance in the surrounding mountain crags, the dam's reservoir submerged the valleys, transforming surrounding knolls into an archipelago of picturesque emerald islands against the rugged Banasura mountain backdrop. Visitors enjoy thrilling speedboat safaris, horse riding, ziplines, and nature trails through spice gardens.",
        "best_time": "October to May (crisp mountain breezes, calm blue reservoir waters)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Banasura_Sagar_Dam",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "chand_baori_stepwell_abhaneri",
        "place": "Chand Baori Stepwell, Abhaneri",
        "state": "Rajasthan",
        "city": "Abhaneri, Dausa",
        "category": ["heritage", "architecture", "monuments"],
        "wikipedia_title": "Chand_Baori",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Chand_Baori",
        "wikidata_id": "Q1061807",
        "lat": 27.0071,
        "lon": 76.6063,
        "text": "Chand Baori in Abhaneri, Rajasthan is one of the oldest, deepest, and most visually mesmerizing stepwells on Earth. Constructed in the 9th century by King Chanda of the Nikumbha dynasty, this geometric architectural wonder plunges 13 storeys (over 30 metres deep) into the desert bedrock through exactly 3,500 impeccably symmetrical, razor-sharp chevron stone stairs. Engineered as a sacred subterranean water sanctuary and social cooling palace during scorching desert heatwaves, the temperature at the bottom remains 5 to 6 degrees Celsius cooler than the surface. Adjacent to the ornate Harshat Mata Temple, its maze of shadow and stone is celebrated as an apex of medieval Indian hydraulic engineering.",
        "best_time": "October to March (cool desert mornings, dramatic sun angles casting geometric shadows)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Chand_Baori",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "kumbhalgarh_fort_great_wall",
        "place": "Kumbhalgarh Fort & The Great Wall of India",
        "state": "Rajasthan",
        "city": "Rajsamand",
        "category": ["fort", "unesco heritage", "heritage"],
        "wikipedia_title": "Kumbhalgarh",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Kumbhalgarh",
        "wikidata_id": "Q921160",
        "lat": 25.1528,
        "lon": 73.5872,
        "text": "Kumbhalgarh Fort, a UNESCO World Heritage Hill Fort of Rajasthan, was commissioned in the 15th century by Rana Kumbha atop a 1,100-meter peak in the Aravalli hills. Enclosing the colossal citadel is a continuous 36-kilometer stone rampart—officially recognized as the second longest continuous wall on Earth after the Great Wall of China. Up to 15 feet wide and fortified by watchtowers, eight war horses could gallop abreast along its top. The fort sheltered the rulers of Mewar in times of invasion, houses over 360 ancient temples, the high-altitude Badal Mahal (Palace of Clouds), and was the birthplace of Maharana Pratap.",
        "best_time": "October to March (crisp winters, panoramic vistas across the Thar desert edge)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Kumbhalgarh",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "kailasa_temple_ellora_cave_16",
        "place": "Kailasa Temple, Ellora (Cave 16)",
        "state": "Maharashtra",
        "city": "Chhatrapati Sambhaji Nagar",
        "category": ["unesco heritage", "temple", "heritage"],
        "wikipedia_title": "Kailasa_Temple,_Ellora",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Kailasa_Temple,_Ellora",
        "wikidata_id": "Q2081604",
        "lat": 20.0238,
        "lon": 75.1793,
        "text": "Kailasa Temple (Cave 16 of the Ellora Caves) in Maharashtra is the largest monolithic rock-cut structure on Earth. Commissioned in the 8th century by Rashtrakuta King Krishna I, ancient artisans carved the entire multi-storey temple complex top-to-bottom out of a single vertical volcanic basalt mountain slope. More than 200,000 to 400,000 tonnes of solid rock were chiselled away by hand without using a single crane, scaffolding, or mortar. Replicating Mount Kailash, it showcases monumental carved stone elephants, towering victory pillars, elaborate narrative friezes of the Ramayana, and soaring gopurams carved with astronomical precision.",
        "best_time": "November to March (cool pleasant winter; ideal for exploring rock-cut caves)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Kailasa_Temple,_Ellora",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "dhanushkodi_ghost_town_ram_setu",
        "place": "Dhanushkodi Ghost Town & Ram Setu",
        "state": "Tamil Nadu",
        "city": "Rameswaram",
        "category": ["beach", "nature", "heritage"],
        "wikipedia_title": "Dhanushkodi",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Dhanushkodi",
        "wikidata_id": "Q655169",
        "lat": 9.1764,
        "lon": 79.4144,
        "text": "Dhanushkodi is an atmospheric ghost town at the southeastern tip of Pamban Island in Tamil Nadu, merely 18 miles across the Palk Strait from Sri Lanka. Submerged and decimated by the powerful 1964 cyclone, the haunting skeleton ruins of its railway terminal, colonial church, and customs station stand half-submerged in glittering white coral sand dunes where the tranquil waters of the Bay of Bengal meet the roaring surf of the Indian Ocean. Dhanushkodi marks the sacred terminus where Lord Rama is believed to have marked the starting point of Ram Setu (Adam's Bridge) with the tip of his bow.",
        "best_time": "October to March (gentle coastal winds, stark ocean vistas, migratory flamingo flocks)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Dhanushkodi",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "double_decker_living_root_bridge_nongriat",
        "place": "Double Decker Living Root Bridge, Nongriat",
        "state": "Meghalaya",
        "city": "Cherrapunji, Sohra",
        "category": ["nature", "heritage", "adventure"],
        "wikipedia_title": "Living_root_bridge",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Living_root_bridge",
        "wikidata_id": "Q6659728",
        "lat": 25.2505,
        "lon": 91.6738,
        "text": "The Double Decker Living Root Bridge (Jingkieng Nongriat) deep in the subtropical valleys of Cherrapunji, Meghalaya, is a marvel of indigenous Khasi bio-engineering. Crafted by guiding the pliable aerial roots of Indian rubber trees (Ficus elastica) across roaring mountain torrents through hollowed areca-nut palms, these living bridges take 15 to 30 years of patient nurturing to span the chasm. Unlike steel or timber that quickly rots under the heaviest monsoon rains on Earth, the living root bridge grows thicker, stronger, and more resilient with age, standing for over two centuries and supporting dozens of travelers over turquoise natural swimming pools.",
        "best_time": "October to April (dry season, crystal emerald water pools beneath the bridges)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Living_root_bridge",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    }
]

def add_places():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    added = 0
    for place in NEW_PLACES:
        out_file = RAW_DIR / f"{place['id']}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(place, f, indent=2, ensure_ascii=False)
        added += 1

    print(f"Added {added} destination profiles to {RAW_DIR}")

if __name__ == "__main__":
    add_places()
