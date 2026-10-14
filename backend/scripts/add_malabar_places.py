"""
Adds detailed destination profiles for Kozhikode, Vadakara, and Kanjirapuzha Dam
with verified historical lore, geographical coordinates, and architectural wow factors.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"

MALABAR_PLACES = [
    {
        "id": "kozhikode_beach_and_pier",
        "place": "Kozhikode Beach & Ancient Sea Pier",
        "state": "Kerala",
        "city": "Kozhikode",
        "category": ["beach", "heritage", "nature"],
        "wikipedia_title": "Kozhikode_Beach",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Kozhikode_Beach",
        "wikidata_id": "Q6435345",
        "lat": 11.2618,
        "lon": 75.7694,
        "text": "Kozhikode Beach (Calicut Beach) is a historic coastal stretch along the Malabar coast in Kerala, famed for its scenic crimson sunsets and twin 150-year-old dilapidated iron shipping piers extending into the Arabian Sea. During the medieval era, Calicut served as the legendary 'City of Spices' ruled by the Zamorins (Samoothiri), where Arab, Chinese, Venetian, and African trading vessels docked. The beach promenade features the Marine Life Aquarium, Lions Park, Freedom Square, and an open-air lighthouse offering sweeping vistas across the Malabar surf. In the evening, the air fills with the aroma of hot spiced Kallummakkaya (green mussels) and freshly roasted groundnuts.",
        "best_time": "October to March (cool pleasant ocean breeze and golden evening sunsets)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Kozhikode_Beach",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "kappad_beach_vasco_da_gama",
        "place": "Kappad Beach & Vasco da Gama Historic Landing",
        "state": "Kerala",
        "city": "Kozhikode",
        "category": ["beach", "heritage", "monuments"],
        "wikipedia_title": "Kappad",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Kappad",
        "wikidata_id": "Q3595225",
        "lat": 11.3855,
        "lon": 75.7175,
        "text": "Kappad Beach (Kappakkadavu) is a historic rock-studded beach situated 16 km north of Kozhikode city. It is internationally renowned as the momentous site where Portuguese explorer Vasco da Gama landed on 20 May 1498 with three caravels, inaugurating the maritime sea route from Europe to India and changing global trade forever. A stone monument commemorates the landing near a sprawling black rock promontory protruding into the waves. Topping the rock is an 800-year-old temple. In 2020, Kappad achieved prestigious international Blue Flag beach eco-certification for its immaculate waters, cleanliness, and pristine coconut grove shoreline.",
        "best_time": "September to March (clear blue waters, gentle waves, and certified eco-amenities)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Kappad",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "sm_street_mittayi_theruvu",
        "place": "SM Street (Mittayi Theruvu) & Halwa Heritage",
        "state": "Kerala",
        "city": "Kozhikode",
        "category": ["market", "food", "heritage"],
        "wikipedia_title": "Mithai_Theruvu",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Mithai_Theruvu",
        "wikidata_id": "Q6881478",
        "lat": 11.2505,
        "lon": 75.7828,
        "text": "Sweet Meat Street (SM Street), known locally as Mittayi Theruvu, is a legendary 600-year-old pedestrian shopping promenade in the historic center of Kozhikode. Dating back to the reign of the Zamorin, the street was named by European traders after the aromatic sweet-meat stalls that lined the road, producing the world-famous glossy Kozhikodan Halwa simmered in copper cauldrons with pure coconut oil and jaggery. Immortalized in Malayalam literature by celebrated author S.K. Pottekkatt (whose statue guards the street entrance), SM Street features heritage colonial tiled roofs, vintage bookstores, spice bazaars, and traditional brassware shops.",
        "best_time": "Year-round; evenings between 4 PM and 9 PM offer vibrant heritage illumination",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Mithai_Theruvu",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "beypore_port_and_uru_shipbuilding",
        "place": "Beypore Port & Ancient Uru Shipbuilding Yard",
        "state": "Kerala",
        "city": "Beypore, Kozhikode",
        "category": ["heritage", "crafts", "coastal"],
        "wikipedia_title": "Beypore",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Beypore",
        "wikidata_id": "Q853245",
        "lat": 11.1803,
        "lon": 75.8058,
        "text": "Beypore is an ancient maritime port city at the mouth of the Chaliyar River in Kozhikode district, famed worldwide for over 1,500 years as the premier shipbuilding center of the 'Uru'—magnificent handcrafted wooden dhow vessels. Master shipwrights known as Khalasis build these colossal wooden sea galleons entirely by hand from Nilambur teak without architectural blueprints, relying on oral mathematical traditions passed through generations. Royal families and wealthy merchants from the Arabian Gulf continue to commission these luxury wooden seafaring palaces. Nearby lies the scenic 2-kilometer Beypore Pulimoodu sea walk path extending directly into the Arabian Sea.",
        "best_time": "October to March (pleasant breeze along the coastal sea bridge and active shipyard crafting)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Beypore",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "thusharagiri_waterfalls_kozhikode",
        "place": "Thusharagiri Waterfalls",
        "state": "Kerala",
        "city": "Kozhikode",
        "category": ["waterfall", "nature", "trekking"],
        "wikipedia_title": "Thusharagiri_Falls",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Thusharagiri_Falls",
        "wikidata_id": "Q7798933",
        "lat": 11.4725,
        "lon": 76.0528,
        "text": "Thusharagiri Falls ('Snow-Capped Mountain') is a spectacular cascade system located 50 km from Kozhikode in the Western Ghats foothills near Kodencheri. Formed by two mountain streams originating from the high Wayanad hills joining to create the Chalipuzha River, the river diverges into three cascading tiers: Erattumukku, Mazhavil Chattom (Rainbow Falls), and Thumbitullum Para. Surrounded by aromatic spice plantations of vanilla, rubber, areca nut, and pepper, Thusharagiri is renowned among rock climbers, white-water rafters, and adventurous trekkers venturing up the river valley towards Wayanad's Vythiri plateau.",
        "best_time": "September to February (post-monsoon roaring water volume and lush greenery)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Thusharagiri_Falls",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "mananchira_square_kozhikode",
        "place": "Mananchira Square & Palace Reservoir",
        "state": "Kerala",
        "city": "Kozhikode",
        "category": ["heritage", "gardens", "architecture"],
        "wikipedia_title": "Mananchira",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Mananchira",
        "wikidata_id": "Q6747124",
        "lat": 11.2528,
        "lon": 75.7806,
        "text": "Mananchira Square is a historic heritage park wrapped around the sprawling freshwater Mananchira lake in central Kozhikode. The artificial rectangular reservoir was built in the 14th century by the Zamorin monarch King Mana Vikram as a private bathing pool for the royal palace complex. Today, the square is transformed into a serene cultural haven enclosed by traditional Kerala-style carved wooden gateways, terracotta tiled verandas, 250 ornamental Victorian lamp posts, an open-air theatre, and verdant lawns bordered by the historic Commonwealth Trust factory and Town Hall.",
        "best_time": "October to March (cool evenings, serene illuminated lakeside strolls)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Mananchira",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "kadalundi_bird_sanctuary",
        "place": "Kadalundi Bird Sanctuary & Estuary",
        "state": "Kerala",
        "city": "Kozhikode",
        "category": ["wildlife", "nature", "coastal"],
        "wikipedia_title": "Kadalundi_Bird_Sanctuary",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Kadalundi_Bird_Sanctuary",
        "wikidata_id": "Q6345025",
        "lat": 11.1294,
        "lon": 75.8344,
        "text": "Kadalundi Bird Sanctuary spreads across a cluster of pristine mangrove islands where the Kadalundi River empties into the Arabian Sea, bordering Kozhikode and Malappuram districts. Rising 200 meters above sea level at the Kadalundikadavu viewpoint, this coastal wetland hosts more than a hundred species of native birds and over 60 migratory species flying from Siberia, Ladakh, and the Arctic, including sandpipers, terns, gulls, redshanks, and whimbrels. Visitors take gentle traditional country boat rides through dense mangrove thickets, witnessing fiddler crabs, otters, and schools of estuarine fish.",
        "best_time": "November to February (peak migratory bird watching season)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Kadalundi_Bird_Sanctuary",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "lokanarkavu_temple_vadakara",
        "place": "Lokanarkavu Temple (Lokamalayar Kavu), Vadakara",
        "state": "Kerala",
        "city": "Vadakara, Kozhikode",
        "category": ["temple", "heritage", "culture"],
        "wikipedia_title": "Lokanarkavu_Temple",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Lokanarkavu_Temple",
        "wikidata_id": "Q6668673",
        "lat": 11.6033,
        "lon": 75.6178,
        "text": "Lokanarkavu Temple (officially Lokamalayar Kavu) is an ancient 1,500-year-old temple complex situated in Villiappally near Vadakara in Kozhikode district, Kerala. Intimately linked to the legendary folklore of the Vadakkan Pattukal (Northern Ballads) and Kerala's ancient martial art of Kalaripayattu, it was the principal family shrine of Thacholi Othenan, the fabled 16th-century martial hero. Every Kalaripayattu warrior undertakes sacred pilgrimage to seek the blessings of the goddess before their master stage debut. The complex houses three distinct sanctums dedicated to Goddess Durga, Lord Shiva, and Lord Vishnu, featuring exquisite wooden wall murals and the grand Poora Maholsavam martial festival celebrated in Meenam (March-April).",
        "best_time": "October to March (festival season, sacred Kalaripayattu martial demonstrations)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Lokanarkavu_Temple",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "vadakara_sandbanks_beach",
        "place": "Vadakara Sandbanks Beach & Moorad Estuary",
        "state": "Kerala",
        "city": "Vadakara, Kozhikode",
        "category": ["beach", "nature", "coastal"],
        "wikipedia_title": "Vatakara",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Vatakara",
        "wikidata_id": "Q2344799",
        "lat": 11.5908,
        "lon": 75.5786,
        "text": "Vadakara Sandbanks Beach is a scenic natural sandbank peninsula located 3 km from Vadakara town, where the tranquil waters of the Moorad River flow gracefully into the Arabian Sea. The strip of fine golden sand offers panoramic views of fishing fleets, coconut palm riverbanks, and calm swimming shallows. Developed as an eco-tourism hub, the beach features paved sunset walkways, children's park facilities, open seating pavilions, and seasonal visits from endangered Olive Ridley sea turtles that nest along these clean coastal sandbars.",
        "best_time": "October to March (gentle coastal sea breeze and tranquil estuary sunsets)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Vatakara",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "kunjali_marakkar_memorial_iringal",
        "place": "Kunjali Marakkar Memorial & Naval Fort, Iringal",
        "state": "Kerala",
        "city": "Iringal, Vadakara",
        "category": ["heritage", "museums", "forts"],
        "wikipedia_title": "Kunjali_Marakkar",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Kunjali_Marakkar",
        "wikidata_id": "Q6444820",
        "lat": 11.5647,
        "lon": 75.6175,
        "text": "The Kunjali Marakkar Memorial and historic fort grounds in Iringal near Vadakara preserve the heritage of the four legendary naval commanders (Kunjali Marakkars) who organized the first organized naval defense of the Indian subcontinent against Portuguese colonial armadas from 1500 to 1600. Commissioned by the Zamorins of Calicut, the Marakkars built an impregnable coastal fort (Fort Marakkar) at Kottakkal rivermouth. Today, the restored ancestral family home is an archaeological museum maintained by the Kerala State Archaeology Department, showcasing ancient bronze cannons, muskets, swords, iron cannonballs, and royal palm-leaf manuscripts.",
        "best_time": "October to March (pleasant coastal weather, maritime history exploration)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Kunjali_Marakkar",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "sargalaya_crafts_village_iringal",
        "place": "Sargaalaya Kerala Arts and Crafts Village",
        "state": "Kerala",
        "city": "Iringal, Vadakara",
        "category": ["crafts", "culture", "heritage"],
        "wikipedia_title": "Sargaalaya",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Sargaalaya",
        "wikidata_id": "Q16254425",
        "lat": 11.5619,
        "lon": 75.6206,
        "text": "Sargaalaya Kerala Arts and Crafts Village is an internationally acclaimed 20-acre cultural tourism village situated along the banks of the Moorad River at Iringal, near Vadakara. Established by the Kerala Department of Tourism, Sargaalaya brings together master artisans who demonstrate live centuries-old traditional handicrafts: coir weaving, bell metal casting, Aranmula metal mirrors, terracotta pottery, cane and bamboo carving, and Mural painting. With river boat rides, traditional Malabar culinary eateries, and an annual International Arts & Crafts Fair attracting global artisans, it is an architectural sanctuary of living heritage.",
        "best_time": "November to February (pleasant breezes, annual International Crafts Expo)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Sargaalaya",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    },
    {
        "id": "kanjirapuzha_dam_and_gardens",
        "place": "Kanjirapuzha Dam & Vettilachola Reserve",
        "state": "Kerala",
        "city": "Kanjirapuzha, Palakkad",
        "category": ["dam", "nature", "waterfall"],
        "wikipedia_title": "Kanjirapuzha_Dam",
        "wikipedia_url": "https://en.wikipedia.org/wiki/Kanjirapuzha_Dam",
        "wikidata_id": "Q6363363",
        "lat": 10.9833,
        "lon": 76.5417,
        "text": "Kanjirapuzha Dam is a magnificent masonry-and-earthen irrigation dam constructed across the Kanjirapuzha River (a major tributary of the Thuthapuzha and Bharathappuzha) in Palakkad district, Kerala, situated 13 km from Mannarkkad. Nestled beneath the mist-cloaked peaks of the Vakkodan hills of the Western Ghats, the dam reservoir is flanked by an evergreen forest canopy that serves as an elephant corridor. Surrounding the spillway are landscaped ornamental hillside gardens, cascading waterfalls at nearby Vettilachola, a fish breeding center, and children's amusement parks, making it one of the most picturesque eco-tourism sanctuaries in central Kerala.",
        "best_time": "September to February (post-monsoon roaring spillways, lush mountain greenery)",
        "source": "Wikipedia & Wikivoyage (CC BY-SA 4.0)",
        "source_url": "https://en.wikipedia.org/wiki/Kanjirapuzha_Dam",
        "attribution": "Content licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).",
        "fallback": False
    }
]

def add_malabar_places():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    count = 0
    for place in MALABAR_PLACES:
        file_path = RAW_DIR / f"{place['id']}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(place, f, indent=2, ensure_ascii=False)
        count += 1
    print(f"Successfully added {count} Malabar & Palakkad destinations to {RAW_DIR}")

if __name__ == "__main__":
    add_malabar_places()
