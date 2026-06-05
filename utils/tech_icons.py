"""Mapeamento de ícones/emojis para tecnologias."""

TECH_ICONS = {
    # Linguagens
    "Python": "🐍",
    "R": "📊",
    "SQL": "🗄️",
    "JavaScript": "📜",
    "HTML": "🌐",
    "CSS": "🎨",
    "Java": "☕",
    "C++": "⚙️",
    "Go": "🐹",
    "Rust": "🦀",
    "Ruby": "💎",
    "PHP": "🐘",
    "VBA": "📋",
    "DAX": "📈",
    "M": "🔤",

    # Banco de Dados
    "PostgreSQL": "🐘",
    "MySQL": "🐬",
    "MongoDB": "🍃",
    "SQLite": "📦",
    "SQL Server": "🗄️",
    "Redis": "🔴",
    "Elasticsearch": "🔍",
    "Firebase": "🔥",
    "Neon": "💫",
    "Alembic": "📜",

    # Data Science & ML
    "pandas": "🐼",
    "numpy": "🔢",
    "scipy": "🧪",
    "scikit-learn": "🤖",
    "statsmodels": "📊",
    "TensorFlow": "🧠",
    "PyTorch": "🔥",
    "Keras": "⚡",
    "XGBoost": "🚀",
    "LightGBM": "💡",
    "CatBoost": "🐱",
    "SHAP": "📊",
    "MLflow": "🔄",
    "Weights & Biases": "🎯",

    # Deep Learning & CV
    "YOLOv8": "👁️",
    "OpenCV": "🎬",
    "Pillow": "🖼️",
    "Albumentations": "🎭",
    "Detectron2": "🔍",
    "Ultralytics": "🚀",

    # NLP
    "NLTK": "📚",
    "spaCy": "🌍",
    "Transformers": "🤗",
    "GPT": "🧠",
    "BERT": "📖",
    "LangChain": "⛓️",
    "RAG": "🔗",

    # Web Framework & API
    "FastAPI": "⚡",
    "Django": "🎸",
    "Flask": "🫖",
    "Uvicorn": "🚀",
    "Gunicorn": "🦅",
    "Streamlit": "🎈",
    "Dash": "📊",
    "Plotly": "📈",
    "Flask-RESTful": "🔌",

    # Frontend & Visualização
    "React": "⚛️",
    "Vue": "💚",
    "Angular": "🔴",
    "D3.js": "📊",
    "Matplotlib": "📉",
    "Seaborn": "🌊",
    "ECharts": "📊",
    "Tableau": "📊",
    "Power BI": "📊",
    "Grafana": "📈",

    # Cloud & DevOps
    "AWS": "☁️",
    "Google Cloud": "☁️",
    "Azure": "☁️",
    "Docker": "🐳",
    "Kubernetes": "☸️",
    "Jenkins": "🔨",
    "GitHub Actions": "⚙️",
    "GitLab CI": "🦊",
    "Render": "🎬",
    "Heroku": "🚀",
    "Streamlit Cloud": "☁️",

    # Data Engineering
    "Spark": "⚡",
    "Hadoop": "🐘",
    "Kafka": "🔄",
    "Airflow": "✈️",
    "Dbt": "🔧",
    "ETL": "🔀",
    "Web Scraping": "🕷️",
    "RPA": "🤖",

    # Tools & Utilities
    "Git": "🐙",
    "GitHub": "🐙",
    "GitLab": "🦊",
    "Jupyter": "📓",
    "VS Code": "💻",
    "PyCharm": "🧠",
    "Conda": "🐍",
    "pip": "📦",
    "pytest": "✅",
    "Sphinx": "📚",

    # Streaming & Real-time
    "Kafka": "🔄",
    "RabbitMQ": "🐰",
    "Apache Flink": "⚡",
    "Spark Streaming": "🔥",

    # Machine Learning Ops
    "MLOps": "🔄",
    "Model Registry": "📦",
    "Feature Store": "🏪",
    "Monitoring": "📡",

    # Outros
    "Selenium": "🕷️",
    "Beautiful Soup": "🥣",
    "Requests": "📡",
    "httpx": "📨",
    "PyInstaller": "📦",
    "Tkinter": "🖥️",
    "PyQT": "🖥️",
    "Pydantic": "✓",
    "SQLAlchemy": "🔗",
}


def get_icon(tech: str) -> str:
    """Retorna o ícone de uma tecnologia. Se não encontrar, retorna um padrão."""
    return TECH_ICONS.get(tech, "⚙️")


def render_tech_badge(tech: str) -> str:
    """Renderiza um badge HTML com ícone e nome da tecnologia."""
    icon = get_icon(tech)
    return f'<span class="tech-badge">{icon} {tech}</span>'
