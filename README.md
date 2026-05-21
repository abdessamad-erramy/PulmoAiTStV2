# 🫁 PulmoAI - Intelligent Pulmonary X-Ray Analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange.svg)](https://www.tensorflow.org/)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-yellowgreen.svg)](https://github.com/yourname/PulmoAI)

**Medical AI platform for intelligent detection and classification of pulmonary conditions from chest X-rays**

---

## 📋 What is PulmoAI?

PulmoAI analyzes chest X-ray images using artificial intelligence to detect:
-  **COVID-19** - Coronavirus infection detection
- **Pneumonia** - Bacterial/viral pneumonia classification
-  **Normal** - Healthy lung diagnosis

The system uses **InceptionV3** deep learning model trained on thousands of clinical X-rays and provides **Grad-CAM visualizations** to show exactly where the AI focuses.

---

##  Key Features

###  AI Analysis
- InceptionV3-based deep learning model
- Real-time X-ray analysis in seconds
- Per-class confidence scores (0-100%)
- Grad-CAM heatmap visualization (see where AI looks)

###  Security
- User authentication (login system)
- JWT token-based API authentication
- RGPD compliant data protection
- Secure password hashing

###  User Features
- Upload X-ray images (JPG, PNG, GIF, BMP)
- View analysis results with confidence scores
- See AI decision explanation (Grad-CAM heatmaps)
- Download analysis reports (PDF)
- View analysis history
- User dashboard

###  Data Management
- SQLite database for analysis history
- Secure image storage
- User management system
- Complete audit trail

---

##  Quick Start

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/abdessamad-erramy/PulmoAI.git
cd PulmoAI
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Application
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your settings (optional for development)
```

#### 5. Initialize Database
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized!')"
```

#### 6. Run Application
```bash
python app.py
```

Visit: **http://localhost:5000**

## DAROOORI Download AI Model

The trained InceptionV3 model is versioned with the code releases.

### Download
1. Go to **[Releases](https://github.com/abdessamad-erramy/PulmoAI/releases)**
2. Download `pulmo_model.h5` from the latest release
3. Place in `ai_model/` folder

Or download directly:
```bash
# Create ai_model folder if it doesn't exist
mkdir ai_model

# Download model (replace URL with latest release)
# Windows (PowerShell):
Invoke-WebRequest -Uri "https://github.com/abdessamad-erramy/PulmoAI/releases/download/v0.8.0/pulmo_model.h5" -OutFile "ai_model/pulmo_model.h5"

# macOS/Linux:
wget https://github.com/abdessamad-erramy/PulmoAI/releases/download/v0.8.0/pulmo_model.h5 -O ai_model/pulmo_model.h5
```

**Verify:**
```bash
ls ai_model/  # Should show pulmo_model.h5
```

## ⚠️ Important
The model file must be in `ai_model/pulmo_model.h5` before running the application.

---

## 📁 Project Structure

```
PulmoAI/
├── app.py                    Main Flask application
├── config.py                 Configuration settings
├── requirements.txt          Python dependencies
│
├── ai_model/
│   └── pulmo_model.h5       Trained InceptionV3 model (download separately)
│
├── database/
│   ├── pulmoai.db           SQLite database (auto-created)
│   └── init_db.py           Database initialization
│
├── models/
│   ├── user.py              User model (authentication)
│   ├── analysis.py          Analysis history model
│   └── __init__.py
│
├── routes/
│   ├── auth.py              Login/Register endpoints
│   ├── predict.py           AI prediction endpoints
│   ├── history.py           Analysis history endpoints
│   ├── report.py            PDF report generation
│   └── __init__.py
│
├── services/
│   ├── model_service.py     AI model inference
│   ├── image_service.py     Image upload handling
│   ├── image_preprocessing.py X-ray preprocessing
│   ├── gradcam_service.py   Grad-CAM visualization
│   ├── pdf_service.py       PDF report generation
│   └── __init__.py
│
├── static/
│   ├── css/
│   │   └── style.css        Application styles
│   ├── uploads/             User uploaded X-ray images
│   └── js/                  Frontend scripts
│
├── templates/
│   ├── base.html            Base template
│   ├── login.html           Login page
│   ├── upload.html          Upload page
│   ├── dashboard.html       User dashboard
│   └── result.html          Analysis results page
│
└── venv/                    Virtual environment (created locally)
```

---

## 🔧 Configuration

### Environment Variables (.env)

Create a `.env` file based on `.env.example`:

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE=database/pulmoai.db

# AI Model
MODEL_PATH=ai_model/pulmo_model.h5
IMG_SIZE=224
LAST_CONV_LAYER=mixed10
CLASS_NAMES=Covid,Normal,Pneumonia

# Security
JWT_SECRET_KEY=your-jwt-secret-key
MAX_CONTENT_LENGTH=16777216
```

**Important**: 
- Change `SECRET_KEY` and `JWT_SECRET_KEY` in production
- Never commit `.env` to Git (use `.env.example` instead)

---

##  How to Use

### 1. Create Account
- Go to **http://localhost:5000**
- Register with username and password
- Login with your credentials

### 2. Upload X-Ray
- Click "Upload" menu
- Select X-ray image (JPG, PNG, GIF, BMP)
- Wait for analysis (usually 2-5 seconds)

### 3. View Results
- See AI prediction (COVID-19, Pneumonia, or Normal)
- View confidence score
- See Grad-CAM heatmap (where AI focused)
- Download PDF report

### 4. Check History
- Go to "History" to see all analyses
- View previous results anytime
- Track diagnosis patterns

---

##  Tech Stack

### Backend
- **Flask 2.3.0** - Web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database

### AI/ML
- **TensorFlow 2.13** - Deep learning framework
- **Keras** - Neural network API
- **OpenCV** - Image processing
- **NumPy** - Scientific computing
- **Matplotlib** - Visualization (Grad-CAM)

### Authentication
- **Flask-JWT-Extended** - API token authentication
- **Flask-Login** - Session-based authentication
- **Werkzeug** - Password hashing

### Utilities
- **Pillow** - Image handling
- **ReportLab** (optional) - PDF generation
- **python-dotenv** - Environment configuration

---

##  Testing

Test the application:

```bash
# Run Flask development server
python app.py

# In another terminal, test endpoints
curl http://localhost:5000/

# Test API with sample image
curl -X POST http://localhost:5000/api/predict \
  -F "image=@sample.jpg"
```

---

##  API Endpoints

### Authentication
```
POST /api/login
POST /api/logout
POST /api/register
```

### Prediction
```
POST /api/predict
GET /api/predict/<analysis_id>
GET /api/predict/history
```

### Reports
```
GET /api/report/<analysis_id>/pdf
```

---

##  Troubleshooting

### "ModuleNotFoundError: No module named 'tensorflow'"
```bash
pip install -r requirements.txt
```

### "No such table: user"
Database not initialized. Run:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### "Model file not found"
Download `pulmo_model.h5` and place in `ai_model/` folder.

### "Port 5000 already in use"
Use different port:
```bash
flask run --port 5001
```

### Database locked error
Delete old database:
```bash
rm database/pulmoai.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

##  Security Notes

 **For Development Only**
- Default SECRET_KEY is insecure
- Debug mode is ON
- CORS is open (demo mode)

 **For Production**
- Set `FLASK_ENV=production`
- Generate strong SECRET_KEY:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
- Set `FLASK_DEBUG=False`
- Use HTTPS/SSL
- Configure proper CORS
- Use environment variables for secrets

---

##  Team Setup

### For New Team Members

1. **Clone repository**
   ```bash
   git clone https://github.com/yourname/PulmoAI.git
   cd PulmoAI
   ```

2. **Setup environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

3. **Initialize database**
   ```bash
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

4. **Run application**
   ```bash
   python app.py
   ```

5. **Start developing**
   - Make changes to files
   - Test locally
   - Create pull request

### Code Guidelines

- Follow PEP 8 (Python style)
- Write docstrings for functions
- Add comments for complex logic
- Test changes before committing
- Create pull requests for review

---

##  Model Information

### Model Type
**InceptionV3** - Google's pre-trained convolutional neural network

### Input
- Image size: 224 × 224 pixels
- Format: RGB (3 channels)
- Preprocessing: Normalization to [0, 1]

### Output
- 3-class classification:
  - COVID-19
  - Pneumonia
  - Normal
- Per-class probability scores

### Training Data
- Thousands of clinical chest X-rays
- Balanced across all three classes
- Data augmentation applied

---

##  Workflow

### Development
```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Make changes
# ... edit files ...

# 3. Test
python app.py

# 4. Commit
git add .
git commit -m "feat: description of change"

# 5. Push
git push origin feature/your-feature

# 6. Create Pull Request on GitHub
```

### Code Review
- Other team members review code
- Suggestions and improvements
- Tests must pass
- Merge when approved

---

##  Documentation

- **[requirements.txt](./requirements.txt)** - All dependencies
- **[.env.example](./.env.example)** - Configuration template
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Development guidelines

---

##  License

This project is licensed under the **MIT License** - see [LICENSE](./LICENSE) file for details.

---

##  Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Bug reporting guidelines
- Feature request process
- Development setup
- Code style guidelines
- Pull request process

---

##  Support

### Questions or Issues?
- Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
- Open an issue on GitHub
- Ask the team in your chat/email

### Need Help?
- Read this README carefully
- Check the troubleshooting section
- Ask team members
- Create a GitHub issue

---

##  Project Status

| Component | Status |
|-----------|--------|
| Backend API | ✅ Complete |
| Frontend UI | ✅ Complete |
| AI Model | Trained tbarklah 3la khoya simo |
| Grad-CAM | Working ms khasha chwiya  |
| Authentication |  Complete khasha chwiya |
| Database |  Ready |
| Documentation |  In Progress |
| Testing |  In Progress |

---

##  Next Steps

1.  Clone the repository
2.  Install dependencies
3.  Setup .env file
4.  Initialize database
5.  Run `python app.py`
6.  Open http://localhost:5000
7.  Create account and test
8.  Start contributing!

---

##  Contact



---

##  Version History

- **v0.8.0** (Current) - Beta release with premium UI
- **v0.7.0** - Grad-CAM implementation
- **v0.6.0** - API & TensorFlow integration
- **v0.5.0** - Core Flask application
- **v0.1.0** - Project initialization

---

**Made with love hhhh by the PulmoAI Team abdessamad & simo & walid**

[⬆ Back to Top](#pulmoai---intelligent-pulmonary-x-ray-analysis)