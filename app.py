import streamlit as st
import PyPDF2
import re
import pandas as pd
from io import BytesIO

# =====================================================
# ATS Keywords Dataset (Flattened for matching)
# =====================================================
ats_keywords_full = {
# ---------------- Quantum Computing ----------------
    "Quantum Computing": {
        "qiskit": "Qiskit",
        "quantum circuits": "Quantum Circuits",
        "quantum algorithms": "Quantum Algorithms",
        "quantum entanglement": "Quantum Entanglement",
        "quantum machine learning": "Quantum Machine Learning",
        "quantum cryptography": "Quantum Cryptography"
    },

    # ---------------- Blockchain / Crypto ----------------
    "Blockchain / Crypto": {
        "blockchain development": "Blockchain Development",
        "ethereum": "Ethereum",
        "solidity": "Solidity",
        "smart contracts": "Smart Contracts",
        "hyperledger": "Hyperledger",
        "cryptocurrency": "Cryptocurrency",
        "defi": "Decentralized Finance (DeFi)",
        "nft development": "NFT Development",
        "web3": "Web3"
    },

    # ---------------- IoT / Edge Computing ----------------
    "IoT / Edge Computing": {
        "iot": "Internet of Things (IoT)",
        "edge computing": "Edge Computing",
        "sensor networks": "Sensor Networks",
        "mqtt": "MQTT Protocol",
        "coap": "CoAP Protocol",
        "iot security": "IoT Security",
        "iot analytics": "IoT Analytics",
        "connected devices": "Connected Devices"
    },

    # ---------------- Robotics / Automation ----------------
    "Robotics / Automation": {
        "robotics engineering": "Robotics Engineering",
        "robot programming": "Robot Programming",
        "ros": "Robot Operating System (ROS)",
        "industrial automation": "Industrial Automation",
        "autonomous robots": "Autonomous Robots",
        "path planning": "Path Planning",
        "robot kinematics": "Robot Kinematics",
        "robot perception": "Robot Perception"
    },

    # ---------------- Design / UX ----------------
    "Design / UX": {
        "user experience": "User Experience (UX)",
        "user interface": "User Interface (UI)",
        "wireframing": "Wireframing",
        "prototyping": "Prototyping",
        "adobe xd": "Adobe XD",
        "sketch": "Sketch",
        "usability testing": "Usability Testing",
        "design thinking": "Design Thinking"
    },

    # ---------------- AR / VR ----------------
    "AR / VR": {
        "augmented reality": "Augmented Reality (AR)",
        "virtual reality": "Virtual Reality (VR)",
        "unity 3d": "Unity 3D",
        "unreal engine": "Unreal Engine",
        "oculus development": "Oculus Development",
        "vr interaction design": "VR Interaction Design",
        "arkit": "ARKit",
        "arcore": "ARCore"
    },
    # ---------------- API / Web Services ----------------
    "API / Web Services": {
        "api development": "API Development",
        "rest api": "REST API",
        "restful services": "RESTful Services",
        "soap api": "SOAP API",
        "graphql": "GraphQL",
        "api integration": "API Integration",
        "api testing": "API Testing",
        "postman": "Postman",
        "swagger": "Swagger",
        "openapi": "OpenAPI",
        "oauth": "OAuth",
        "jwt": "JSON Web Token (JWT)",
        "api security": "API Security",
        "rate limiting": "Rate Limiting",
        "webhooks": "Webhooks",
        "api documentation": "API Documentation"
    },
    # ---------------- Programming Languages ----------------
    "Programming Languages": {
        "python": "Python",
        "r": "R Programming",
        "c": "C Programming",
        "c++": "C++ Programming",
        "c#": "C# Programming",
        "java": "Java",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "php": "PHP",
        "ruby": "Ruby",
        "go": "Go",
        "rust": "Rust",
        "kotlin": "Kotlin",
        "swift": "Swift",
        "dart": "Dart",
        "scala": "Scala",
        "perl": "Perl",
        "matlab": "MATLAB",
        "julia": "Julia",
        "vba": "Visual Basic for Applications",
        "shell": "Shell Scripting",
        "objective-c": "Objective-C",
        "haskell": "Haskell",
        "f#": "F#",
        "erlang": "Erlang",
        "groovy": "Groovy",
        "lisp": "Lisp",
        "prolog": "Prolog",
        "cobol": "COBOL",
        "fortran": "Fortran",
        "delphi": "Delphi",
        "scratch": "Scratch",
        "assembly": "Assembly Language",
        "sql": "Structured Query Language",
        "pl/sql": "Procedural Language/SQL"
    },

    # ---------------- Python Packages ----------------
    "Python Packages": {
        "numpy": "NumPy",
        "pandas": "Pandas",
        "matplotlib": "Matplotlib",
        "seaborn": "Seaborn",
        "scikit-learn": "Scikit-learn",
        "tensorflow": "TensorFlow",
        "keras": "Keras",
        "torch": "PyTorch",
        "torchvision": "Torchvision",
        "torchaudio": "Torchaudio",
        "pytorch-lightning": "PyTorch Lightning",
        "fastai": "FastAI",
        "xgboost": "XGBoost",
        "lightgbm": "LightGBM",
        "catboost": "CatBoost",
        "sympy": "SymPy",
        "scipy": "SciPy",
        "networkx": "NetworkX",
        "tqdm": "TQDM",
        "joblib": "Joblib",
        "python-dateutil": "Python Dateutil",
        "pillow": "Pillow",
        "opencv-python": "OpenCV-Python",
        "opencv-contrib-python": "OpenCV-Contrib-Python",
        "nltk": "Natural Language Toolkit",
        "spacy": "spaCy",
        "textblob": "TextBlob",
        "beautifulsoup4": "BeautifulSoup4",
        "requests": "Requests",
        "flask": "Flask",
        "django": "Django",
        "plotly": "Plotly",
        "dash": "Dash",
        "mlflow": "MLflow",
        "optuna": "Optuna",
        "accelerate": "Accelerate",
        "albumentations": "Albumentations",
        "pytorch-geometric": "PyTorch Geometric",
        "sentence-transformers": "Sentence Transformers",
        "diffusers": "Diffusers",
        "huggingface_hub": "HuggingFace Hub",
        "openai": "OpenAI",
        "fairseq": "Fairseq",
        "dgl": "Deep Graph Library",
        "gym": "OpenAI Gym",
        "stable-baselines3": "Stable Baselines3",
        "triton": "Triton",
        "gradio": "Gradio",
        "fairlearn": "Fairlearn",
        "yellowbrick": "Yellowbrick",
        "eli5": "ELI5",
        "shap": "SHAP",
        "lime": "LIME"
    },

    # ---------------- AI / ML / DL / CV / NLP ----------------
    "AI / ML / DL / CV / NLP Packages": {
        "ml": "Machine Learning",
        "machine learning": "Machine Learning",
        "dl": "Deep Learning",
        "deep learning": "Deep Learning",
        "ai": "Artificial Intelligence",
        "artificial intelligence": "Artificial Intelligence",
        "cv": "Computer Vision",
        "computer vision": "Computer Vision",
        "nlp": "Natural Language Processing",
        "natural language processing": "Natural Language Processing",
        "reinforcement learning": "Reinforcement Learning",
        "rl": "Reinforcement Learning",
        "predictive analytics": "Predictive Analytics",
        "prescriptive analytics": "Prescriptive Analytics",
        "data mining": "Data Mining",
        "time series analysis": "Time Series Analysis",
        "recommendation systems": "Recommendation Systems",
        "anomaly detection": "Anomaly Detection",
        "sentiment analysis": "Sentiment Analysis",
        "transformers": "Transformers",
        "fastai": "FastAI",
        "tensorflow": "TensorFlow",
        "keras": "Keras",
        "torch": "PyTorch",
        "pytorch": "PyTorch",
        "scikit-learn": "Scikit-learn",
        "xgboost": "XGBoost",
        "lightgbm": "LightGBM",
        "catboost": "CatBoost",
        "pytorch-lightning": "PyTorch Lightning",
        "huggingface": "HuggingFace",
        "openai": "OpenAI",
        "detectron2": "Detectron2",
        "albumentations": "Albumentations"
    },

    # ---------------- Development Tools & Platforms ----------------
    "Development Tools & Platforms": {
        "vs code": "Visual Studio Code",
        "pycharm": "PyCharm",
        "jupyter notebook": "Jupyter Notebook",
        "jupyterlab": "JupyterLab",
        "spyder": "Spyder",
        "anaconda": "Anaconda",
        "git": "Git",
        "github": "GitHub",
        "gitlab": "GitLab",
        "bitbucket": "Bitbucket",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "aws": "Amazon Web Services (AWS)",
        "amazon web services": "Amazon Web Services (AWS)",
        "azure": "Microsoft Azure",
        "google cloud": "Google Cloud Platform (GCP)",
        "heroku": "Heroku",
        "firebase": "Firebase",
        "power bi": "Power BI",
        "tableau": "Tableau",
        "apache spark": "Apache Spark",
        "hadoop": "Hadoop",
        "airflow": "Apache Airflow",
        "dvc": "Data Version Control (DVC)",
        "postman": "Postman",
        "figma": "Figma",
        "notion": "Notion",
        "slack": "Slack",
        "trello": "Trello",
        "jira": "Jira",
        "confluence": "Confluence",
        "replit": "Replit",
        "google colab": "Google Colab",
        "kaggle": "Kaggle",
        "codesandbox": "CodeSandbox",
        "jenkins": "Jenkins",
        "terraform": "Terraform",
        "ansible": "Ansible"
    },

    # ---------------- Domain / IT / DS / BI / AI Skills ----------------
    "Domain / IT / DS / BI / AI Skills": {
        "data analysis": "Data Analysis",
        "data visualization": "Data Visualization",
        "eda": "Exploratory Data Analysis (EDA)",
        "exploratory data analysis": "Exploratory Data Analysis (EDA)",
        "statistical analysis": "Statistical Analysis",
        "feature engineering": "Feature Engineering",
        "model deployment": "Model Deployment",
        "sql queries": "SQL Queries",
        "nosql databases": "NoSQL Databases",
        "big data analytics": "Big Data Analytics",
        "business intelligence": "Business Intelligence (BI)",
        "bi": "Business Intelligence (BI)",
        "etl": "ETL",
        "dashboarding": "Dashboarding",
        "reporting": "Reporting",
        "version control": "Version Control",
        "cloud computing": "Cloud Computing",
        "devops": "DevOps",
        "web development": "Web Development",
        "backend development": "Backend Development",
        "frontend development": "Frontend Development",
        "full stack development": "Full Stack Development",
        "api development": "API Development",
        "automation": "Automation",
        "robotic process automation": "Robotic Process Automation (RPA)",
        "rpa": "Robotic Process Automation (RPA)",
        "cybersecurity basics": "Cybersecurity Basics",
        "networking basics": "Networking Basics",
        "containerization": "Containerization",
        "microservices": "Microservices",
        "continuous integration": "Continuous Integration",
        "ci/cd": "Continuous Integration / Continuous Deployment (CI/CD)",
        "scrum": "Scrum",
        "kanban": "Kanban",
        "agile methodology": "Agile Methodology",
        "time series analysis": "Time Series Analysis",
        "sentiment analysis": "Sentiment Analysis",
        "recommendation systems": "Recommendation Systems",
        "anomaly detection": "Anomaly Detection",
        "data mining": "Data Mining",
        "statistical modeling": "Statistical Modeling",
        "ab testing": "A/B Testing",
        "data warehousing": "Data Warehousing"
    },

    # ---------------- Soft Skills ----------------
    "Soft Skills": {
        "communication": "Communication",
        "presentation": "Presentation",
        "leadership": "Leadership",
        "teamwork": "Teamwork",
        "time management": "Time Management",
        "problem solving": "Problem Solving",
        "critical thinking": "Critical Thinking",
        "decision making": "Decision Making",
        "creativity": "Creativity",
        "adaptability": "Adaptability",
        "negotiation": "Negotiation",
        "conflict resolution": "Conflict Resolution",
        "emotional intelligence": "Emotional Intelligence",
        "networking": "Networking",
        "organization": "Organization",
        "mentoring": "Mentoring",
        "collaboration": "Collaboration",
        "active listening": "Active Listening",
        "stress management": "Stress Management",
        "work ethic": "Work Ethic",
        "attention to detail": "Attention to Detail",
        "customer service": "Customer Service",
        "public speaking": "Public Speaking",
        "interpersonal skills": "Interpersonal Skills",
        "analytical thinking": "Analytical Thinking",
        "strategic planning": "Strategic Planning",
        "persuasion": "Persuasion",
        "influencing skills": "Influencing Skills",
        "positive attitude": "Positive Attitude",
        "empathy": "Empathy",
        "flexibility": "Flexibility"
    },

    # ---------------- Experience ----------------
    "Experience": {
        "internship experience": "Internship Experience",
        "1 year experience": "1 Year Experience",
        "2 years experience": "2 Years Experience",
        "3 years experience": "3 Years Experience",
        "4 years experience": "4 Years Experience",
        "5+ years experience": "5+ Years Experience",
        "entry level experience": "Entry Level Experience",
        "mid level experience": "Mid Level Experience",
        "senior level experience": "Senior Level Experience",
        "project experience": "Project Experience",
        "industry experience": "Industry Experience",
        "startup experience": "Startup Experience",
        "corporate experience": "Corporate Experience",
        "freelance experience": "Freelance Experience",
        "research experience": "Research Experience",
        "team lead experience": "Team Lead Experience",
        "management experience": "Management Experience",
        "client handling experience": "Client Handling Experience",
        "cross-functional experience": "Cross-Functional Experience",
        "hands-on project experience": "Hands-On Project Experience",
        "certification experience": "Certification Experience"
    },

    # ---------------- MS Office / Productivity Tools ----------------
    "MS Office / Productivity Tools": {
        "microsoft word": "Microsoft Word",
        "microsoft excel": "Microsoft Excel",
        "microsoft powerpoint": "Microsoft PowerPoint",
        "microsoft access": "Microsoft Access",
        "microsoft outlook": "Microsoft Outlook",
        "microsoft onenote": "Microsoft OneNote",
        "excel formulas": "Excel Formulas",
        "excel pivot tables": "Excel Pivot Tables",
        "excel charts": "Excel Charts",
        "powerpoint presentations": "PowerPoint Presentations",
        "word formatting": "Word Formatting",
        "outlook email management": "Outlook Email Management",
        "onenote organization": "OneNote Organization"
    },

    # ---------------- SAP ----------------
    "SAP": {
        "sap": "SAP",
        "sap erp": "SAP ERP",
        "sap fico": "SAP FICO",
        "sap mm": "SAP MM",
        "sap sd": "SAP SD",
        "sap hr": "SAP HR",
        "sap bw": "SAP BW",
        "sap hana": "SAP HANA",
        "sap abap": "SAP ABAP",
        "sap crm": "SAP CRM",
        "sap scm": "SAP SCM",
        "sap basis": "SAP BASIS",
        "sap s/4hana": "SAP S/4HANA",
        "sap ui5": "SAP UI5",
        "sap successfactors": "SAP SuccessFactors",
        "sap ariba": "SAP Ariba",
        "sap bpc": "SAP BPC",
        "sap gts": "SAP GTS",
        "sap ewm": "SAP EWM",
        "sap analytics cloud": "SAP Analytics Cloud",
        "sap fiori": "SAP Fiori",
        "sap business one": "SAP Business One",
        "sap business objects": "SAP Business Objects",
        "sap lumira": "SAP Lumira",
        "sap financials": "SAP Financials",
        "sap plant maintenance": "SAP Plant Maintenance",
        "sap quality management": "SAP Quality Management",
        "sap project systems": "SAP Project Systems"
    },

    # ---------------- Mechanical ----------------
    "Mechanical": {
        "solidworks": "SolidWorks",
        "autocad mechanical": "AutoCAD Mechanical",
        "catia": "CATIA",
        "proe": "Pro/ENGINEER",
        "nx unigraphics": "NX Unigraphics",
        "fusion 360": "Fusion 360",
        "ansys": "ANSYS",
        "matlab mechanical": "MATLAB Mechanical",
        "mechanical design": "Mechanical Design",
        "thermodynamics": "Thermodynamics",
        "fluid mechanics": "Fluid Mechanics",
        "mechanical simulation": "Mechanical Simulation",
        "finite element analysis": "Finite Element Analysis (FEA)",
        "hvac design": "HVAC Design",
        "manufacturing processes": "Manufacturing Processes",
        "product design": "Product Design",
        "sheet metal design": "Sheet Metal Design",
        "thermal analysis": "Thermal Analysis",
        "mechanical drawing": "Mechanical Drawing",
        "piping design": "Piping Design",
        "robotics": "Robotics",
        "automation design": "Automation Design",
        "cad modeling": "CAD Modeling",
        "cam": "CAM"
    },

    # ---------------- Civil ----------------
    "Civil": {
        "autocad civil": "AutoCAD Civil",
        "staad pro": "STAAD Pro",
        "etabs": "ETABS",
        "sap2000": "SAP2000",
        "revit": "Revit",
        "archicad": "ArchiCAD",
        "structural analysis": "Structural Analysis",
        "construction management": "Construction Management",
        "civil engineering": "Civil Engineering",
        "geotechnical engineering": "Geotechnical Engineering",
        "surveying": "Surveying",
        "building information modeling": "Building Information Modeling (BIM)",
        "transportation engineering": "Transportation Engineering",
        "urban planning": "Urban Planning",
        "road design": "Road Design",
        "bridge design": "Bridge Design",
        "hydraulic engineering": "Hydraulic Engineering",
        "environmental engineering": "Environmental Engineering",
        "construction estimation": "Construction Estimation",
        "project management": "Project Management"
    },

    # ---------------- Embedded ----------------
    "Embedded": {
        "embedded systems": "Embedded Systems",
        "microcontroller": "Microcontroller",
        "arduino": "Arduino",
        "raspberry pi": "Raspberry Pi",
        "stm32": "STM32",
        "pic": "PIC Microcontroller",
        "iot": "IoT (Internet of Things)",
        "firmware development": "Firmware Development",
        "freertos": "FreeRTOS",
        "rtos": "Real-Time Operating System",
        "sensor interfacing": "Sensor Interfacing",
        "actuator control": "Actuator Control",
        "communication protocols": "Communication Protocols",
        "c programming for embedded": "C Programming for Embedded",
        "arm cortex": "ARM Cortex",
        "hardware design": "Hardware Design",
        "pcb design": "PCB Design",
        "spi": "SPI Protocol",
        "i2c": "I2C Protocol",
        "uart": "UART Protocol",
        "can bus": "CAN Bus",
        "embedded linux": "Embedded Linux"
    },

    # ---------------- Fullstack ----------------
    "Fullstack": {
        "full stack development": "Full Stack Development",
        "angular": "Angular",
        "react": "React",
        "vue": "Vue.js",
        "node.js": "Node.js",
        "spring boot": "Spring Boot",
        "django": "Django",
        "flask": "Flask",
        "express": "Express.js",
        "html": "HTML",
        "css": "CSS",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "api development": "API Development",
        "rest api": "REST API",
        "graphql": "GraphQL",
        "bootstrap": "Bootstrap",
        "material ui": "Material UI",
        "react native": "React Native",
        "next.js": "Next.js",
        "nuxt.js": "Nuxt.js",
        "svelte": "Svelte",
        "laravel": "Laravel",
        "php": "PHP",
        "mongodb": "MongoDB",
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "firebase": "Firebase",
        "aws amplify": "AWS Amplify",
        "docker": "Docker",
        "kubernetes": "Kubernetes"
    },

    # ---------------- Cybersecurity ----------------
    "Cybersecurity": {
        "network security": "Network Security",
        "application security": "Application Security",
        "penetration testing": "Penetration Testing",
        "vulnerability assessment": "Vulnerability Assessment",
        "firewalls": "Firewalls",
        "intrusion detection": "Intrusion Detection",
        "siem": "SIEM",
        "risk assessment": "Risk Assessment",
        "ethical hacking": "Ethical Hacking",
        "encryption": "Encryption",
        "cyber threat intelligence": "Cyber Threat Intelligence",
        "malware analysis": "Malware Analysis",
        "incident response": "Incident Response",
        "forensics": "Forensics",
        "identity access management": "Identity Access Management",
        "penetration tools": "Penetration Tools",
        "wireshark": "Wireshark",
        "metasploit": "Metasploit",
        "burp suite": "Burp Suite",
        "nessus": "Nessus",
        "ossec": "OSSEC",
        "tcp/ip security": "TCP/IP Security",
        "security policies": "Security Policies",
        "threat modeling": "Threat Modeling"
    },

    # ---------------- Cloud / DevOps ----------------
    "Cloud / DevOps": {
        "aws": "Amazon Web Services (AWS)",
        "azure": "Microsoft Azure",
        "google cloud": "Google Cloud Platform (GCP)",
        "devops": "DevOps",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "ci/cd": "Continuous Integration / Continuous Deployment (CI/CD)",
        "jenkins": "Jenkins",
        "terraform": "Terraform",
        "ansible": "Ansible",
        "cloud computing": "Cloud Computing",
        "serverless architecture": "Serverless Architecture",
        "prometheus": "Prometheus",
        "grafana": "Grafana",
        "nagios": "Nagios",
        "packer": "Packer",
        "helm": "Helm",
        "artifact repository": "Artifact Repository",
        "ci pipelines": "CI Pipelines",
        "cloud security": "Cloud Security",
        "cloud monitoring": "Cloud Monitoring",
        "aws lambda": "AWS Lambda",
        "cloud formation": "CloudFormation",
        "eks": "Amazon EKS",
        "aks": "Azure AKS",
        "gke": "Google GKE"
    },

    # ---------------- Data Analyst / BI ----------------
    "Data Analyst / BI": {
        "data analysis": "Data Analysis",
        "data visualization": "Data Visualization",
        "power bi": "Power BI",
        "tableau": "Tableau",
        "excel": "Microsoft Excel",
        "sql": "SQL",
        "mysql": "MySQL",
        "reporting": "Reporting",
        "dashboards": "Dashboards",
        "kpi": "Key Performance Indicators (KPI)",
        "data modeling": "Data Modeling",
        "data cleaning": "Data Cleaning",
        "data preprocessing": "Data Preprocessing",
        "power query": "Power Query",
        "dax": "DAX",
        "excel pivot tables": "Excel Pivot Tables",
        "excel charts": "Excel Charts",
        "google data studio": "Google Data Studio",
        "qlikview": "QlikView",
        "kpi tracking": "KPI Tracking",
        "trend analysis": "Trend Analysis"
    },

    # ---------------- Database ----------------
    "Database": {
        "mysql": "MySQL",
        "sql server": "SQL Server",
        "oracle": "Oracle",
        "postgresql": "PostgreSQL",
        "mongodb": "MongoDB",
        "sqlite": "SQLite",
        "nosql": "NoSQL",
        "redis": "Redis",
        "cassandra": "Cassandra",
        "database design": "Database Design",
        "indexing": "Indexing",
        "normalization": "Normalization",
        "joins": "Joins",
        "triggers": "Triggers",
        "stored procedures": "Stored Procedures",
        "pl/sql": "PL/SQL",
        "t-sql": "T-SQL",
        "performance tuning": "Performance Tuning",
        "backup and recovery": "Backup and Recovery",
        "data warehousing": "Data Warehousing",
        "etl": "ETL"
    },

    # ---------------- Digital Marketing ----------------
    "Digital Marketing": {
        "seo": "Search Engine Optimization (SEO)",
        "sem": "Search Engine Marketing (SEM)",
        "google analytics": "Google Analytics",
        "content marketing": "Content Marketing",
        "social media marketing": "Social Media Marketing",
        "email marketing": "Email Marketing",
        "ppc": "Pay Per Click (PPC)",
        "affiliate marketing": "Affiliate Marketing",
        "marketing automation": "Marketing Automation",
        "facebook ads": "Facebook Ads",
        "instagram ads": "Instagram Ads",
        "linkedin marketing": "LinkedIn Marketing",
        "tiktok marketing": "TikTok Marketing",
        "adwords": "Google AdWords",
        "keyword research": "Keyword Research",
        "google tag manager": "Google Tag Manager",
        "landing page optimization": "Landing Page Optimization",
        "conversion rate optimization": "Conversion Rate Optimization"
    },

    # ---------------- Animations ----------------
    "Animations": {
        "2d animation": "2D Animation",
        "3d animation": "3D Animation",
        "after effects": "Adobe After Effects",
        "maya": "Autodesk Maya",
        "blender": "Blender",
        "cinema 4d": "Cinema 4D",
        "unity": "Unity 3D",
        "unreal engine": "Unreal Engine",
        "motion graphics": "Motion Graphics",
        "character animation": "Character Animation",
        "rigging": "Rigging",
        "animation scripting": "Animation Scripting",
        "autodesk motionbuilder": "Autodesk MotionBuilder",
        "toon boom": "Toon Boom",
        "storyboarding": "Storyboarding"
    },

    # ---------------- Business Intelligence ----------------
    "Business Intelligence": {
        "power bi": "Power BI",
        "tableau": "Tableau",
        "qlikview": "QlikView",
        "bi": "Business Intelligence (BI)",
        "data modeling": "Data Modeling",
        "dashboarding": "Dashboarding",
        "reporting": "Reporting",
        "dax": "DAX",
        "etl": "ETL",
        "kpi": "Key Performance Indicators (KPI)",
        "performance analysis": "Performance Analysis",
        "data visualization": "Data Visualization",
        "data warehousing": "Data Warehousing"
    },

    # ---------------- Business Analyst ----------------
    "Business Analyst": {
        "business analysis": "Business Analysis",
        "requirement gathering": "Requirement Gathering",
        "requirement analysis": "Requirement Analysis",
        "gap analysis": "Gap Analysis",
        "process mapping": "Process Mapping",
        "workflow analysis": "Workflow Analysis",
        "stakeholder management": "Stakeholder Management",
        "use cases": "Use Cases",
        "user stories": "User Stories",
        "functional specification": "Functional Specification",
        "non-functional requirements": "Non-Functional Requirements",
        "brd": "Business Requirement Document (BRD)",
        "frd": "Functional Requirement Document (FRD)",
        "data analysis": "Data Analysis",
        "reporting": "Reporting",
        "dashboards": "Dashboards",
        "business process improvement": "Business Process Improvement",
        "decision support": "Decision Support",
        "kpi tracking": "KPI Tracking",
        "workflow optimization": "Workflow Optimization",
        "jira": "Jira",
        "confluence": "Confluence",
        "trello": "Trello",
        "microsoft excel": "Microsoft Excel",
        "power bi": "Power BI",
        "tableau": "Tableau",
        "uml": "Unified Modeling Language (UML)",
        "process documentation": "Process Documentation",
        "agile methodology": "Agile Methodology"
    }
}

# =====================================================
# DOMAIN MAP
# =====================================================
DOMAIN_MAP = {
    "AI / ML / DL / CV / NLP": [
        "Python", "Machine Learning", "Deep Learning",
        "TensorFlow", "Keras", "Computer Vision",
        "Natural Language Processing"
    ],
    "Data Analyst / BI": [
        "Power BI", "Tableau", "SQL", "Excel",
        "DAX", "Dashboarding", "Data Analysis"
    ]
}
# =====================================================
# FUNCTIONS
# =====================================================
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + " "
    # Remove line breaks, extra spaces, non-alphanumeric chars except dots and commas
    text = re.sub(r"[^\w\s.,]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.lower()

def extract_skills(text):
    found = set()
    for category in ats_keywords_full.values():
        for key, label in category.items():
            # Only match full words/phrases, not single letters alone
            if len(key) <= 1:
                continue
            if re.search(rf"\b{re.escape(key.lower())}\b", text):
                found.add(label)
    return sorted(found)

def detect_domain(skills):
    scores = {}
    for domain, domain_skills in DOMAIN_MAP.items():
        scores[domain] = len(set(skills) & set(domain_skills))
    return max(scores, key=scores.get) if scores else "Unknown"

def extract_experience(text):
    text = text.replace("–", "-").replace("—", "-").lower()
    total_months = 0

    # Match Month Year - Month Year or Month Year - Present/Till Date
    month_year_ranges = re.findall(
        r'([A-Za-z]{3,9}\s\d{4})\s*-\s*(till date|present|current|[A-Za-z]{3,9}\s\d{4})',
        text, flags=re.IGNORECASE
    )

    # Match MM/YYYY - MM/YYYY
    numeric_ranges = re.findall(
        r'(\d{1,2}/\d{4})\s*-\s*(\d{1,2}/\d{4}|present|till date|current)',
        text, flags=re.IGNORECASE
    )

    # Match Year - Year
    year_ranges = re.findall(
        r'(\d{4})\s*-\s*(\d{4}|present|till date|current)',
        text, flags=re.IGNORECASE
    )

    # Match X+ years
    simple_years = re.findall(r'(\d+)\+?\s*years?', text)

    for start_str, end_str in month_year_ranges + numeric_ranges + year_ranges:
        try:
            # Parse start date
            if re.match(r'\d{1,2}/\d{4}', start_str):
                start_date = datetime.strptime(start_str, "%m/%Y")
            elif re.match(r'\d{4}$', start_str):
                start_date = datetime.strptime(start_str, "%Y")
            else:
                start_date = parser.parse(start_str)

            # Parse end date
            if end_str.lower() in ['till date', 'present', 'current']:
                end_date = datetime.today()
            elif re.match(r'\d{1,2}/\d{4}', end_str):
                end_date = datetime.strptime(end_str, "%m/%Y")
            elif re.match(r'\d{4}$', end_str):
                end_date = datetime.strptime(end_str, "%Y")
            else:
                end_date = parser.parse(end_str)

            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            total_months += months
        except:
            continue

    # Add simple X+ years mentions
    for y in simple_years:
        total_months += int(y) * 12

    if total_months == 0:
        return "Not specified"

    years = total_months // 12
    months = total_months % 12
    return f"{years} Years {months} Months" if months else f"{years}+ Years"

# =====================================================
# STREAMLIT UI
# =====================================================
st.set_page_config(page_title="ATS Resume Matcher", layout="wide")
st.title("ATS Score")

uploaded_files = st.file_uploader(
    "Upload Resumes (PDF)",
    type="pdf",
    accept_multiple_files=True
)

jd_text = st.text_area("Paste Job Description", height=180)

# =====================================================
# ANALYSIS
# =====================================================
if st.button("Check ATS Score"):
    if not uploaded_files:
        st.error("Please upload resumes")
    elif not jd_text.strip():
        st.error("Please paste Job Description")
    else:
        # Show uploaded resume list
        st.subheader("Uploaded Resume List")
        for f in uploaded_files:
            st.write("•", f.name)
        st.divider()

        jd_text = jd_text.lower()
        jd_skills = extract_skills(jd_text)
        jd_domain = detect_domain(jd_skills)
        jd_exp = extract_experience(jd_text)

        final_rows = []
        shortlisted_resumes = []

        for file in uploaded_files:
            resume_text = extract_text_from_pdf(file)
            resume_skills = extract_skills(resume_text)
            resume_domain = detect_domain(resume_skills)
            resume_exp = extract_experience(resume_text)

            matched = set(resume_skills) & set(jd_skills)
            missing = set(jd_skills) - set(resume_skills)

            ats_score = round(
                (len(matched) / max(len(jd_skills), 1)) * 100, 2
            )

            verdict = (
                "Strong Match" if ats_score >= 75 else
                "Partial Match" if ats_score >= 40 else
                "Poor Match"
            )

            final_rows.append({
                "Resume Name": file.name,
                "ATS Score (%)": ats_score,
                "Verdict": verdict,
                "Primary Resume Domain": resume_domain,
                "Primary JD Domain": jd_domain,
                "JD Required Skills": ", ".join(jd_skills),
                "Resume Skills": ", ".join(resume_skills),
                "Matched Skills": ", ".join(matched) if matched else "None",
                "Missing Skills": ", ".join(missing) if missing else "None",
                "Resume Experience": resume_exp,
                "JD Experience": jd_exp
            })

            if ats_score >= 40:  # Shortlist only
                shortlisted_resumes.append(file.name)

        df = pd.DataFrame(final_rows).sort_values(
            by="ATS Score (%)", ascending=False
        )

        st.subheader("ATS Screening Results")
        st.dataframe(df, use_container_width=True)

        # =====================================================
        # Display Only Shortlisted Resume Names
        # =====================================================
        st.subheader("Shortlisted Resumes")
        if shortlisted_resumes:
            for name in shortlisted_resumes:
                st.write("•", name)
        else:
            st.info("No resumes shortlisted based on the ATS score threshold.")

        # =====================================================
        # EXCEL EXPORT
        # =====================================================
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            # Main ATS report
            df.to_excel(writer, index=False, sheet_name="ATS_Report")

            # Shortlisted resumes sheet
            shortlist_df = pd.DataFrame({
                "Shortlisted Resumes": shortlisted_resumes
            })
            shortlist_df.to_excel(writer, index=False, sheet_name="Shortlisted_Resumes")

        st.download_button(
            label="⬇ Download Excel Report",
            data=buffer.getvalue(),
            file_name="ATS_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )