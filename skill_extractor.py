from transformers import pipeline
from rapidfuzz import fuzz

ner_pipeline = pipeline(
    "ner",
    model="yashpwr/resume-ner-bert-v2",
    tokenizer="yashpwr/resume-ner-bert-v2",
    device='cpu',
    aggregation_strategy="simple"
)

skills_dict = {
    # Programming Languages
    "python": {"python"},
    "java": {"java"},
    "c": {"c"},
    "c++": {"c++", "cpp"},
    "c#": {"c#", "c sharp"},
    "r": {"r language", "r"},
    "javascript": {"javascript", "js"},
    "typescript": {"typescript", "ts"},
    "php": {"php"},
    "ruby": {"ruby"},
    "go": {"go", "golang"},
    "kotlin": {"kotlin"},
    "swift": {"swift"},
    "rust": {"rust"},
    "vb": {"vb", "visual basic"},
    "asp.net": {"asp.net", "asp net"},
    "pascal": {"pascal"},
    "assembler": {"assembler", "motorola 68000", "assembly"},

    # Frameworks / Libraries
    "machine learning": {"ml", "machine learning"},
    "deep learning": {"dl", "deep learning"},
    "natural language processing": {"nlp", "natural language processing"},
    "tensorflow": {"tensorflow", "tensor flow"},
    "pytorch": {"pytorch", "torch"},
    "keras": {"keras"},
    "scikit-learn": {"scikit-learn", "sklearn"},
    "pandas": {"pandas"},
    "numpy": {"numpy"},
    "matplotlib": {"matplotlib"},
    "react": {"react", "reactjs"},
    "angular": {"angular", "angularjs"},
    "node.js": {"node", "nodejs", "node.js"},
    "django": {"django"},
    "flask": {"flask"},
    "spring boot": {"spring boot", "springboot"},
    
    # Databases
    "sql": {"sql", "structured query language"},
    "mysql": {"mysql"},
    "postgresql": {"postgresql", "postgres"},
    "mongodb": {"mongodb", "mongo"},
    "oracle": {"oracle"},
    "firebase": {"firebase"},
    "redis": {"redis"},
    "access database": {"access", "microsoft access"},

    # Cloud & DevOps
    "aws": {"aws", "amazon web services"},
    "azure": {"azure", "microsoft azure"},
    "gcp": {"gcp", "google cloud"},
    "docker": {"docker"},
    "kubernetes": {"kubernetes", "k8s"},
    "jenkins": {"jenkins"},
    "git": {"git", "github", "gitlab"},
    "ci/cd": {"ci/cd", "continuous integration", "continuous delivery"},

    # Tools / Software
    "matlab": {"matlab"},
    "tableau": {"tableau"},
    "powerbi": {"powerbi", "power bi"},
    "excel": {"excel", "ms excel", "microsoft excel"},
    "microsoft office": {"microsoft office", "office suite"},
    "jira": {"jira"},
    "trello": {"trello"},
    "figma": {"figma"},
    "adobe acrobat": {"adobe acrobat", "acrobat"},
    "adobe photoshop": {"photoshop", "adobe photoshop"},
    "corel office": {"corel office"},
    "dreamweaver": {"dreamweaver"},
    "pro engineer": {"pro engineer", "proe"},
    "powerbuilder": {"powerbuilder"},
    "simply accounting": {"simply accounting"},

    # Methodologies & Soft Skills
    "agile": {"agile"},
    "scrum": {"scrum"},
    "kanban": {"kanban"},
    "tdd": {"tdd", "test driven development"},
    "oop": {"oop", "object oriented programming"},
    "pair programming": {"pair programming"},
    "stories": {"stories", "user stories"},
    "cad programming": {"cad programming"},
    "circuit debugging": {"circuit debugging"},
    "code debugging": {"code debugging"},
    "system optimization": {"system optimization"},
    "analog/digital controller design": {"controller design", "analog controller", "digital controller"},
    "analog/digital circuit design": {"circuit design", "analog circuit", "digital circuit"},
    "forward/inverse kinematics": {"kinematics", "forward kinematics", "inverse kinematics"},
    "surface patch design": {"surface patch design"},
}

all_aliases = {
    alias: skill for skill, aliases in skills_dict.items() for alias in aliases
}

def extract_skills(text, fuzzy_threshold=85):
    """
    Extract skills from resume/job description using:
    - Hugging Face NER model
    - Alias mapping
    - Fuzzy matching
    """

    text = text.lower()
    found = set()

    # NER model extraction
    entities = ner_pipeline(text)
    for ent in entities:
        if ent['entity_group'].lower() in ["skills", "technologies"]:  
            found.add(ent['word'].lower())

    # Direct alias match
    for skill, aliases in skills_dict.items():
        for alias in aliases:
            if alias in text:
                found.add(skill)

    # Fuzzy match for typos/variants
    for alias, skill in all_aliases.items():
        ratio = fuzz.partial_ratio(alias, text)
        if ratio >= fuzzy_threshold:
            found.add(skill)

    return sorted(found)
