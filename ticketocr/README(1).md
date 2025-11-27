# Application OCR de Tickets de Caisse

Une application Django avancée pour l'extraction et l'analyse automatique de tickets de caisse tunisiens utilisant plusieurs moteurs OCR et IA.

## 🚀 Fonctionnalités

### Moteurs OCR
- **DocTR** : OCR basé sur deep learning
- **Tesseract** : OCR traditionnel robuste
- **Docling** : OCR moderne et précis

### Analyses IA
- **Qwen3-30B** (via Hugging Face) : Modèle LLM puissant pour l'extraction structurée
- **Google Gemini 1.5 Flash** : IA de Google pour l'analyse de documents
- **Analyse Regex** : Extraction rapide par expressions régulières

### Fonctionnalités Avancées
- Validation croisée entre différents moteurs
- Correction automatique des erreurs OCR
- Détection de timbres fiscaux tunisiens
- Validation mathématique des totaux
- Génération de rapports comptables PDF
- Historique des analyses
- Interface web moderne et responsive

## 📋 Prérequis

- Python 3.8+
- Django 4.2+
- Tesseract OCR installé
- Clés API (optionnelles) :
  - Hugging Face Token
  - Google Generative AI API Key

## 🛠️ Installation

1. **Cloner le repository**
```bash
git clone <repository-url>
cd ticketocr
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configuration des variables d'environnement**
```bash
cp .env.example .env
# Éditer le fichier .env avec vos clés API
```

5. **Migrations de base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

## 🔧 Configuration

### Variables d'environnement (.env)

```env
# Hugging Face API Token pour Qwen3-30B
HF_TOKEN=your_huggingface_token_here

# Google Generative AI API Key pour Gemini
GOOGLE_API_KEY=your_google_api_key_here

# Django Secret Key
SECRET_KEY=your_django_secret_key_here

DEBUG=True
```

### Obtenir les clés API

#### Hugging Face Token
1. Créer un compte sur [Hugging Face](https://huggingface.co/)
2. Aller dans Settings → Access Tokens
3. Créer un nouveau token avec permissions de lecture

#### Google Generative AI API Key
1. Aller sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Créer un nouveau projet ou utiliser un existant
3. Générer une clé API

## 🎯 Utilisation

### Interface Web

1. **Upload d'image** : Glissez-déposez ou sélectionnez une image de ticket
2. **Choisir l'analyse** :
   - **Extraction OCR** : Extraction de texte uniquement
   - **Analyse Qwen3-30B** : Analyse IA complète avec Hugging Face
   - **Analyse Google Gemini** : Analyse IA avec Google Generative AI
   - **Analyse Regex** : Extraction rapide par patterns
   - **Analyse Complète** : OCR + IA combinés

### Types d'analyses

#### 🔵 Extraction OCR
- Extrait le texte brut avec les 3 moteurs
- Rapide et sans API requise
- Idéal pour vérifier la qualité OCR

#### 🟢 Analyse Qwen3-30B
- Analyse IA avancée via Hugging Face
- Extraction structurée des données
- Validation et correction automatique
- Nécessite HF_TOKEN

#### 🟣 Analyse Google Gemini
- IA de Google pour documents
- Format JSON structuré
- Détection avancée des éléments
- Nécessite GOOGLE_API_KEY

#### 🟡 Analyse Regex
- Extraction par expressions régulières
- Très rapide, fonctionne hors ligne
- Validation mathématique des totaux
- Pas d'API requise

## 📊 Fonctionnalités Comptables

- **Génération de bilans PDF**
- **Historique des tickets**
- **Filtrage par dates**
- **Validation des totaux**
- **Détection automatique des timbres fiscaux tunisiens**

## 🏗️ Architecture

```
ticketocr/
├── ocrapp/                 # Application principale
│   ├── models.py          # Modèles de données
│   ├── views.py           # Logique métier
│   ├── templates/         # Templates HTML
│   └── static/            # Fichiers statiques
├── media/                 # Images uploadées
├── requirements.txt       # Dépendances Python
├── .env.example          # Configuration exemple
└── README.md             # Documentation
```

## 🔍 Détails Techniques

### Modèles de Données
- **ExtractionHistory** : Historique des extractions
- **TicketHistory** : Tickets analysés
- **AccountingEntry** : Écritures comptables

### Validation et Correction
- Correction automatique des erreurs OCR (O→0, I→1)
- Validation mathématique des totaux
- Détection des timbres fiscaux tunisiens
- Validation croisée entre moteurs

### Formats Supportés
- Images : JPG, PNG, TIFF, BMP
- Tickets tunisiens avec timbres fiscaux
- Monnaie : Dinars tunisiens (DT)

## 🚨 Dépannage

### Erreurs courantes

1. **"Clé API manquante"**
   - Vérifier le fichier .env
   - S'assurer que les variables sont correctement définies

2. **"Tesseract not found"**
   - Installer Tesseract OCR
   - Ajouter au PATH système

3. **"Timeout API"**
   - Vérifier la connexion internet
   - Essayer avec un autre modèle

## 📈 Performance

| Méthode | Vitesse | Précision | API Requise |
|---------|---------|-----------|-------------|
| Regex   | ⚡⚡⚡    | ⭐⭐      | Non         |
| Qwen3-30B | ⚡⚡     | ⭐⭐⭐⭐⭐  | Oui         |
| Gemini  | ⚡⚡     | ⭐⭐⭐⭐    | Oui         |

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Ajouter de nouveaux moteurs OCR/IA

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🆘 Support

Pour toute question ou problème :
1. Vérifier cette documentation
2. Consulter les logs d'erreur
3. Ouvrir une issue sur GitHub
