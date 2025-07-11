RESEARCH_AREAS = [
    "Medicine and Health Sciences",
    "Nursing and Midwifery", 
    "Public Health",
    "Pharmacy and Pharmaceutical Sciences",
    "Biomedical Sciences",
    "Clinical Psychology",
    "Epidemiology",
    "Health Policy and Management",
    "Nutrition and Dietetics",
    "Environmental Health",
    "Occupational Health and Safety",
    "Traditional and Alternative Medicine",
    "Medical Laboratory Sciences",
    "Physiotherapy and Rehabilitation",
    "Dentistry and Oral Health",
    "Health Information Management",
    "Physician Assistantship",
    "Optometry and Vision Science",
    "Sports and Exercise Medicine",
    "Others"
]

DEGREE_TYPES = [
    "PhD",
    "MPhil", 
    "MSc",
    "MA",
    "MPH",
    "MBA",
    "MD",
    "MBChB",
    "BPharm",
    "BSc",
    "BA",
    "Diploma",
    "Certificate",
    "Others"
]

# Generate academic years (last 10 years)
import datetime
current_year = datetime.datetime.now().year
ACADEMIC_YEARS = [f"{year}/{year+1}" for year in range(current_year, current_year-10, -1)]

# UHAS specific institutions/campuses with IDs
INSTITUTIONS = [
    {"id": 8, "name": "School of Medicine"},
    {"id": 9, "name": "School of Basic and Biomedical Sciences"},
    {"id": 10, "name": "School of Nursing and Midwifery"},
    {"id": 11, "name": "School of Public Health"},
    {"id": 12, "name": "School of Pharmacy"},
    {"id": 13, "name": "School of Allied Health Sciences"},
    {"id": 14, "name": "Institute of Traditional and Alternative Medicine"},
    {"id": 15, "name": "Nursing and Midwifery Training College"},
    {"id": 16, "name": "Others"}
]

# Helper function to get institution name by ID
def get_institution_by_id(institution_id):
    for inst in INSTITUTIONS:
        if inst["id"] == institution_id:
            return inst["name"]
    return "Unknown Institution"

# Image/Figure constants
MAX_FIGURES_PER_PROJECT = 20
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB per image
MAX_PROFILE_PICTURE_SIZE = 2 * 1024 * 1024  # 2MB for profile pictures

# SUPERVISORS - These are the same as faculty members but organized for dropdown selection
SUPERVISORS = [
    {
        "id": "samuel.akakpo",
        "name": "Mr. Samuel Bewiadzi Akakpo",
        "email": "samuel.akakpo@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Mr."
    },
    {
        "id": "mercy.klugar",
        "name": "Dr. Mercy Klugar",
        "email": "mercy.klugar@uhas.edu.gh",
        "institution": "School of Allied Health Sciences",
        "title": "Dr."
    },
    {
        "id": "richard.awubomu",
        "name": "Dr. Richard Awubomu",
        "email": "richard.awubomu@uhas.edu.gh",
        "institution": "School of Medicine",
        "title": "Dr."
    },
    {
        "id": "innocent.akorli",
        "name": "Mr. Innocent Akorli",
        "email": "innocent.akorli@uhas.edu.gh",
        "institution": "School of Medicine",
        "title": "Mr."
    },
    {
        "id": "benjamin.amoakohene",
        "name": "Dr. Benjamin Amoakohene",
        "email": "benjamin.amoakohene@uhas.edu.gh",
        "institution": "School of Medicine",
        "title": "Dr."
    },
    {
        "id": "peter.agbezorlie",
        "name": "Mr. Peter Agbezorlie",
        "email": "peter.agbezorlie@uhas.edu.gh",
        "institution": "School of Allied Health Sciences",
        "title": "Mr."
    },
    {
        "id": "prince.kubi",
        "name": "Dr. Prince Appiah Kubi",
        "email": "prince.kubi@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Dr."
    },
    {
        "id": "joyce.komesuor",
        "name": "Dr. Joyce Komesuor",
        "email": "joyce.komesuor@uhas.edu.gh",
        "institution": "School of Pharmacy",
        "title": "Dr."
    },
    {
        "id": "mark.ananga",
        "name": "Dr. Mark Kwame Ananga",
        "email": "mark.ananga@uhas.edu.gh",
        "institution": "School of Medicine",
        "title": "Dr."
    },
    {
        "id": "kweku.appiagyei",
        "name": "Dr. Kweku Appiagyei",
        "email": "kweku.appiagyei@uhas.edu.gh",
        "institution": "School of Public Health",
        "title": "Dr."
    },
    {
        "id": "francis.agyei",
        "name": "Dr. Francis Agyei",
        "email": "francis.agyei@uhas.edu.gh",
        "institution": "School of Pharmacy",
        "title": "Dr."
    },
    {
        "id": "awolu.adam",
        "name": "Dr. Awolu Adam",
        "email": "awolu.adam@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Dr."
    },
    {
        "id": "geoffrey.asalu",
        "name": "Dr. Geoffrey Adebayo Asalu",
        "email": "geoffrey.asalu@uhas.edu.gh",
        "institution": "School of Public Health",
        "title": "Dr."
    },
    {
        "id": "norbert.amuna",
        "name": "Mr. Norbert Amuna",
        "email": "norbert.amuna@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Mr."
    },
    {
        "id": "millicent.yirenkyi",
        "name": "Ms. Millicent Boadiwaa Yirenkyi",
        "email": "millicent.yirenkyi@uhas.edu.gh",
        "institution": "School of Public Health",
        "title": "Ms."
    },
    {
        "id": "isiah.agorinya",
        "name": "Dr. Isiah Agorinya",
        "email": "isiah.agorinya@uhas.edu.gh",
        "institution": "School of Public Health",
        "title": "Dr."
    },
    {
        "id": "gideon.kye-duodu",
        "name": "Dr. Gideon Kye-Duodu",
        "email": "gideon.kye-duodu@uhas.edu.gh",
        "institution": "School of Public Health",
        "title": "Dr."
    },
    {
        "id": "forgive.norvivor",
        "name": "Ms. Forgive Norvivor",
        "email": "forgive.norvivor@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Ms."
    },
    {
        "id": "nathaniel.annang",
        "name": "Dr. Nathaniel Armah Annang",
        "email": "nathaniel.annang@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Dr."
    },
    {
        "id": "mavis.kwabla",
        "name": "Dr. Mavis Pearl Kwabla",
        "email": "mavis.kwabla@uhas.edu.gh",
        "institution": "School of Public Health",
        "title": "Dr."
    },
    {
        "id": "gregory.amenuvegbe",
        "name": "Mr. Gregory Amenuvegbe",
        "email": "gregory.amenuvegbe@uhas.edu.gh",
        "institution": "School of Pharmacy",
        "title": "Mr."
    },
    {
        "id": "george.wak",
        "name": "Dr. George Pokoanti Wak",
        "email": "george.wak@uhas.edu.gh",
        "institution": "School of Basic and Biomedical Sciences",
        "title": "Dr."
    },
    {
        "id": "hubert.amu",
        "name": "Dr. Hubert Amu",
        "email": "hubert.amu@uhas.edu.gh",
        "institution": "School of Public Health",
        "title": "Dr."
    },
    {
        "id": "mawuli.kushitor",
        "name": "Dr. Mawuli Kushitor",
        "email": "mawuli.kushitor@uhas.edu.gh",
        "institution": "School of Pharmacy",
        "title": "Dr."
    },
    {
        "id": "pius.agbeviadey",
        "name": "Mr. Pius Agbeviadey",
        "email": "pius.agbeviadey@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Mr."
    },
    {
        "id": "martin.adjiuk",
        "name": "Mr. Martin Adjiuk",
        "email": "martin.adjiuk@uhas.edu.gh",
        "institution": "School of Basic and Biomedical Sciences",
        "title": "Mr."
    },
    {
        "id": "joyce.der",
        "name": "Dr. Joyce Der",
        "email": "joyce.der@uhas.edu.gh",
        "institution": "School of Pharmacy",
        "title": "Dr."
    },
    {
        "id": "wisdom.takramah",
        "name": "Dr. Wisdom Takramah",
        "email": "wisdom.takramah@uhas.edu.gh",
        "institution": "School of Allied Health Sciences",
        "title": "Dr."
    },
    {
        "id": "sitsofe.gbogbo",
        "name": "Dr. Sitsofe Gbogbo",
        "email": "sitsofe.gbogbo@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Dr."
    },
    {
        "id": "veronica.charles-unadike",
        "name": "Dr. Veronica Okwuchi Charles-Unadike",
        "email": "veronica.charles-unadike@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Dr."
    },
    {
        "id": "emmanuel.manu",
        "name": "Dr. Emmanuel Manu",
        "email": "emmanuel.manu@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Dr."
    },
    {
        "id": "mary.ampomah",
        "name": "Dr. Mary Ampomah",
        "email": "mary.ampomah@uhas.edu.gh",
        "institution": "School of Pharmacy",
        "title": "Dr."
    },
    {
        "id": "anthony.dongdem",
        "name": "Dr. Anthony Dongdem",
        "email": "anthony.dongdem@uhas.edu.gh",
        "institution": "School of Basic and Biomedical Sciences",
        "title": "Dr."
    },
    {
        "id": "eric.osei",
        "name": "Dr. Eric Osei",
        "email": "eric.osei@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Dr."
    },
    {
        "id": "cosmos.todoko",
        "name": "Dr. Cosmos Todoko",
        "email": "cosmos.todoko@uhas.edu.gh",
        "institution": "School of Public Health",
        "title": "Dr."
    },
    {
        "id": "clement.narh",
        "name": "Dr. Clement Narh",
        "email": "clement.narh@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Dr."
    },
    {
        "id": "phyllis.addo",
        "name": "Dr. Phyllis Addo",
        "email": "phyllis.addo@uhas.edu.gh",
        "institution": "School of Basic and Biomedical Sciences",
        "title": "Dr."
    },
    {
        "id": "elvis.tarkang",
        "name": "Prof. Elvis Tarkang",
        "email": "elvis.tarkang@uhas.edu.gh",
        "institution": "School of Allied Health Sciences",
        "title": "Prof."
    },
    {
        "id": "livingstone.asem",
        "name": "Dr. Asem Livingstone",
        "email": "livingstone.asem@uhas.edu.gh",
        "institution": "School of Nursing and Midwifery",
        "title": "Dr."
    },
    {
        "id": "others",
        "name": "Others (Please specify in supervisor field)",
        "email": "",
        "institution": "External/Other Institution",
        "title": ""
    }
]

# Helper functions for supervisors
def get_supervisor_by_id(supervisor_id):
    """Get supervisor information by ID"""
    for supervisor in SUPERVISORS:
        if supervisor["id"] == supervisor_id:
            return supervisor
    return None

def get_supervisors_by_institution(institution_name):
    """Get all supervisors from a specific institution"""
    return [s for s in SUPERVISORS if s["institution"] == institution_name and s["id"] != "others"]

def get_all_supervisors_for_dropdown():
    """Get all supervisors formatted for dropdown selection"""
    return [
        {
            "value": supervisor["id"],
            "label": f"{supervisor['name']} ({supervisor['institution']})",
            "name": supervisor["name"],
            "institution": supervisor["institution"],
            "title": supervisor["title"]
        }
        for supervisor in SUPERVISORS
    ]

def search_supervisors(query):
    """Search supervisors by name or institution"""
    query = query.lower()
    return [
        supervisor for supervisor in SUPERVISORS
        if query in supervisor["name"].lower() or 
           query in supervisor["institution"].lower() or
           query in supervisor["email"].lower()
    ]

# Faculty members data for creation (same as supervisors but with additional fields)
FACULTY_MEMBERS = [
    {
        "name": "Mr. Samuel Bewiadzi Akakpo",
        "email": "samuel.akakpo@uhas.edu.gh",
                "institution_id": 10,
        "username": "samuel.akakpo"
    },
    {
        "name": "Dr. Mercy Klugar",
        "email": "mercy.klugar@uhas.edu.gh",
        "institution_id": 13,
        "username": "mercy.klugar"
    },
    {
        "name": "Dr. Richard Awubomu",
        "email": "richard.awubomu@uhas.edu.gh",
        "institution_id": 8,
        "username": "richard.awubomu"
    },
    {
        "name": "Mr. Innocent Akorli",
        "email": "innocent.akorli@uhas.edu.gh",
        "institution_id": 8,
        "username": "innocent.akorli"
    },
    {
        "name": "Dr. Benjamin Amoakohene",
        "email": "benjamin.amoakohene@uhas.edu.gh",
        "institution_id": 8,
        "username": "benjamin.amoakohene"
    },
    {
        "name": "Mr. Peter Agbezorlie",
        "email": "peter.agbezorlie@uhas.edu.gh",
        "institution_id": 13,
        "username": "peter.agbezorlie"
    },
    {
        "name": "Dr. Prince Appiah Kubi",
        "email": "prince.kubi@uhas.edu.gh",
        "institution_id": 10,
        "username": "prince.kubi"
    },
    {
        "name": "Dr. Joyce Komesuor",
        "email": "joyce.komesuor@uhas.edu.gh",
        "institution_id": 12,
        "username": "joyce.komesuor"
    },
    {
        "name": "Dr. Mark Kwame Ananga",
        "email": "mark.ananga@uhas.edu.gh",
        "institution_id": 8,
        "username": "mark.ananga"
    },
    {
        "name": "Dr. Kweku Appiagyei",
        "email": "kweku.appiagyei@uhas.edu.gh",
        "institution_id": 11,
        "username": "kweku.appiagyei"
    },
    {
        "name": "Dr. Francis Agyei",
        "email": "francis.agyei@uhas.edu.gh",
        "institution_id": 12,
        "username": "francis.agyei"
    },
    {
        "name": "Dr. Awolu Adam",
        "email": "awolu.adam@uhas.edu.gh",
        "institution_id": 10,
        "username": "awolu.adam"
    },
    {
        "name": "Dr. Geoffrey Adebayo Asalu",
        "email": "geoffrey.asalu@uhas.edu.gh",
        "institution_id": 11,
        "username": "geoffrey.asalu"
    },
    {
        "name": "Mr. Norbert Amuna",
        "email": "norbert.amuna@uhas.edu.gh",
        "institution_id": 10,
        "username": "norbert.amuna"
    },
    {
        "name": "Ms. Millicent Boadiwaa Yirenkyi",
        "email": "millicent.yirenkyi@uhas.edu.gh",
        "institution_id": 11,
        "username": "millicent.yirenkyi"
    },
    {
        "name": "Dr. Isiah Agorinya",
        "email": "isiah.agorinya@uhas.edu.gh",
        "institution_id": 11,
        "username": "isiah.agorinya"
    },
    {
        "name": "Dr. Gideon Kye-Duodu",
        "email": "gideon.kye-duodu@uhas.edu.gh",
        "institution_id": 11,
        "username": "gideon.kye-duodu"
    },
    {
        "name": "Ms. Forgive Norvivor",
        "email": "forgive.norvivor@uhas.edu.gh",
        "institution_id": 10,
        "username": "forgive.norvivor"
    },
    {
        "name": "Dr. Nathaniel Armah Annang",
        "email": "nathaniel.annang@uhas.edu.gh",
        "institution_id": 10,
        "username": "nathaniel.annang"
    },
    {
        "name": "Dr. Mavis Pearl Kwabla",
        "email": "mavis.kwabla@uhas.edu.gh",
        "institution_id": 11,
        "username": "mavis.kwabla"
    },
    {
        "name": "Mr. Gregory Amenuvegbe",
        "email": "gregory.amenuvegbe@uhas.edu.gh",
        "institution_id": 12,
        "username": "gregory.amenuvegbe"
    },
    {
        "name": "Dr. George Pokoanti Wak",
        "email": "george.wak@uhas.edu.gh",
        "institution_id": 9,
        "username": "george.wak"
    },
    {
        "name": "Dr. Hubert Amu",
        "email": "hubert.amu@uhas.edu.gh",
        "institution_id": 11,
        "username": "hubert.amu"
    },
    {
        "name": "Dr. Mawuli Kushitor",
        "email": "mawuli.kushitor@uhas.edu.gh",
        "institution_id": 12,
        "username": "mawuli.kushitor"
    },
    {
        "name": "Mr. Pius Agbeviadey",
        "email": "pius.agbeviadey@uhas.edu.gh",
        "institution_id": 10,
        "username": "pius.agbeviadey"
    },
    {
        "name": "Mr. Martin Adjiuk",
        "email": "martin.adjiuk@uhas.edu.gh",
        "institution_id": 9,
        "username": "martin.adjiuk"
    },
    {
        "name": "Dr. Joyce Der",
        "email": "joyce.der@uhas.edu.gh",
        "institution_id": 12,
        "username": "joyce.der"
    },
    {
        "name": "Dr. Wisdom Takramah",
        "email": "wisdom.takramah@uhas.edu.gh",
        "institution_id": 13,
        "username": "wisdom.takramah"
    },
    {
        "name": "Dr. Sitsofe Gbogbo",
        "email": "sitsofe.gbogbo@uhas.edu.gh",
        "institution_id": 10,
        "username": "sitsofe.gbogbo"
    },
    {
        "name": "Dr. Veronica Okwuchi Charles-Unadike",
        "email": "veronica.charles-unadike@uhas.edu.gh",
        "institution_id": 10,
        "username": "veronica.charles-unadike"
    },
    {
        "name": "Dr. Emmanuel Manu",
        "email": "emmanuel.manu@uhas.edu.gh",
        "institution_id": 10,
        "username": "emmanuel.manu"
    },
    {
        "name": "Dr. Mary Ampomah",
        "email": "mary.ampomah@uhas.edu.gh",
        "institution_id": 12,
        "username": "mary.ampomah"
    },
    {
        "name": "Dr. Anthony Dongdem",
        "email": "anthony.dongdem@uhas.edu.gh",
        "institution_id": 9,
        "username": "anthony.dongdem"
    },
    {
        "name": "Dr. Eric Osei",
        "email": "eric.osei@uhas.edu.gh",
        "institution_id": 10,
        "username": "eric.osei"
    },
    {
        "name": "Dr. Cosmos Todoko",
        "email": "cosmos.todoko@uhas.edu.gh",
        "institution_id": 11,
        "username": "cosmos.todoko"
    },
    {
        "name": "Dr. Clement Narh",
        "email": "clement.narh@uhas.edu.gh",
        "institution_id": 10,
        "username": "clement.narh"
    },
    {
        "name": "Dr. Phyllis Addo",
        "email": "phyllis.addo@uhas.edu.gh",
        "institution_id": 9,
        "username": "phyllis.addo"
    },
    {
        "name": "Prof. Elvis Tarkang",
        "email": "elvis.tarkang@uhas.edu.gh",
        "institution_id": 13,
        "username": "elvis.tarkang"
    },
    {
        "name": "Dr. Asem Livingstone",
        "email": "livingstone.asem@uhas.edu.gh",
        "institution_id": 10,
        "username": "livingstone.asem"
    }
]

# Default password for faculty members
DEFAULT_FACULTY_PASSWORD = "faculty2024@UHAS"

# Supervisor selection options for frontend dropdowns
SUPERVISOR_OPTIONS = [
    {
        "value": "",
        "label": "Select a Supervisor",
        "disabled": True
    }
] + get_all_supervisors_for_dropdown()

# Grouped supervisors by institution for better organization in frontend
SUPERVISORS_BY_INSTITUTION = {
    "School of Medicine": [
        {"id": "richard.awubomu", "name": "Dr. Richard Awubomu"},
        {"id": "innocent.akorli", "name": "Mr. Innocent Akorli"},
        {"id": "benjamin.amoakohene", "name": "Dr. Benjamin Amoakohene"},
        {"id": "mark.ananga", "name": "Dr. Mark Kwame Ananga"}
    ],
    "School of Basic and Biomedical Sciences": [
        {"id": "george.wak", "name": "Dr. George Pokoanti Wak"},
        {"id": "martin.adjiuk", "name": "Mr. Martin Adjiuk"},
        {"id": "anthony.dongdem", "name": "Dr. Anthony Dongdem"},
        {"id": "phyllis.addo", "name": "Dr. Phyllis Addo"}
    ],
    "School of Nursing and Midwifery": [
        {"id": "samuel.akakpo", "name": "Mr. Samuel Bewiadzi Akakpo"},
        {"id": "prince.kubi", "name": "Dr. Prince Appiah Kubi"},
        {"id": "awolu.adam", "name": "Dr. Awolu Adam"},
        {"id": "norbert.amuna", "name": "Mr. Norbert Amuna"},
        {"id": "forgive.norvivor", "name": "Ms. Forgive Norvivor"},
        {"id": "nathaniel.annang", "name": "Dr. Nathaniel Armah Annang"},
        {"id": "sitsofe.gbogbo", "name": "Dr. Sitsofe Gbogbo"},
        {"id": "veronica.charles-unadike", "name": "Dr. Veronica Okwuchi Charles-Unadike"},
        {"id": "emmanuel.manu", "name": "Dr. Emmanuel Manu"},
        {"id": "eric.osei", "name": "Dr. Eric Osei"},
        {"id": "clement.narh", "name": "Dr. Clement Narh"},
        {"id": "pius.agbeviadey", "name": "Mr. Pius Agbeviadey"},
        {"id": "livingstone.asem", "name": "Dr. Asem Livingstone"}
    ],
    "School of Public Health": [
        {"id": "kweku.appiagyei", "name": "Dr. Kweku Appiagyei"},
        {"id": "geoffrey.asalu", "name": "Dr. Geoffrey Adebayo Asalu"},
        {"id": "millicent.yirenkyi", "name": "Ms. Millicent Boadiwaa Yirenkyi"},
        {"id": "isiah.agorinya", "name": "Dr. Isiah Agorinya"},
        {"id": "gideon.kye-duodu", "name": "Dr. Gideon Kye-Duodu"},
        {"id": "mavis.kwabla", "name": "Dr. Mavis Pearl Kwabla"},
        {"id": "hubert.amu", "name": "Dr. Hubert Amu"},
        {"id": "cosmos.todoko", "name": "Dr. Cosmos Todoko"}
    ],
    "School of Pharmacy": [
        {"id": "joyce.komesuor", "name": "Dr. Joyce Komesuor"},
        {"id": "francis.agyei", "name": "Dr. Francis Agyei"},
        {"id": "gregory.amenuvegbe", "name": "Mr. Gregory Amenuvegbe"},
        {"id": "mawuli.kushitor", "name": "Dr. Mawuli Kushitor"},
        {"id": "joyce.der", "name": "Dr. Joyce Der"},
        {"id": "mary.ampomah", "name": "Dr. Mary Ampomah"}
    ],
    "School of Allied Health Sciences": [
        {"id": "mercy.klugar", "name": "Dr. Mercy Klugar"},
        {"id": "peter.agbezorlie", "name": "Mr. Peter Agbezorlie"},
        {"id": "wisdom.takramah", "name": "Dr. Wisdom Takramah"},
        {"id": "elvis.tarkang", "name": "Prof. Elvis Tarkang"}
    ],
    "External/Other": [
        {"id": "others", "name": "Others (Please specify in supervisor field)"}
    ]
}

# Function to get supervisor options for a specific institution
def get_supervisor_options_by_institution(institution_name):
    """Get supervisor options filtered by institution"""
    return SUPERVISORS_BY_INSTITUTION.get(institution_name, [])

# Function to validate supervisor selection
def is_valid_supervisor(supervisor_id):
    """Check if supervisor ID is valid"""
    return any(supervisor["id"] == supervisor_id for supervisor in SUPERVISORS)

# Function to get supervisor display name
def get_supervisor_display_name(supervisor_id, custom_supervisor_name=None):
    """Get display name for supervisor, handling 'others' case"""
    if supervisor_id == "others":
        return custom_supervisor_name if custom_supervisor_name else "External Supervisor"
    
    supervisor = get_supervisor_by_id(supervisor_id)
    return supervisor["name"] if supervisor else "Unknown Supervisor"
