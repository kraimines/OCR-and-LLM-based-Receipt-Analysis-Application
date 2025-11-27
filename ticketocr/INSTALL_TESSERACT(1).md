# Installation de Tesseract OCR sur Windows

## Méthode 1: Installation manuelle (Recommandée)

### 1. Télécharger Tesseract
- Allez sur: https://github.com/UB-Mannheim/tesseract/wiki
- Téléchargez: `tesseract-ocr-w64-setup-5.3.3.20231005.exe`
- Ou lien direct: https://digi.bib.uni-mannheim.de/tesseract/

### 2. Installer Tesseract
1. Exécutez le fichier .exe téléchargé
2. **IMPORTANT**: Installez dans `C:\Program Files\Tesseract-OCR\`
3. Cochez "Add to PATH" pendant l'installation
4. Sélectionnez les langues: English + French (pour les tickets tunisiens)

### 3. Vérifier l'installation
Ouvrez PowerShell et tapez:
```powershell
tesseract --version
```

### 4. Si PATH non configuré automatiquement
Ajoutez manuellement à votre PATH système:
```
C:\Program Files\Tesseract-OCR\
```

## Méthode 2: Via Chocolatey (Alternative)

```powershell
# Installer Chocolatey d'abord (si pas déjà installé)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Installer Tesseract
choco install tesseract
```

## Méthode 3: Via Scoop (Alternative)

```powershell
# Installer Scoop d'abord (si pas déjà installé)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex

# Installer Tesseract
scoop install tesseract
```

## Configuration pour l'application Django

Une fois Tesseract installé, l'application devrait fonctionner automatiquement.

Si vous avez encore des problèmes, vous pouvez spécifier le chemin explicitement dans le code Python:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Test de fonctionnement

Après installation, testez avec:
```powershell
tesseract --list-langs
```

Vous devriez voir au minimum:
- eng (English)
- fra (French) - optionnel mais recommandé
