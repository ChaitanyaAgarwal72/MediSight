# MediSight 🩺
**AI-Powered Medical Assistant with Multi-Modal Intelligence**

## Overview
MediSight is an advanced AI medical assistant that provides intelligent health information, medical report analysis, and research-backed insights. Built with Flask and modern web technologies, it offers a comprehensive platform for medical inquiries and document analysis.

## ✨ Features

### 🤖 AI Medical Assistant
- Interactive chat interface with AI-powered medical guidance
- Professional medical disclaimer and safety protocols
- Session-based conversation memory for continuous context

### 📄 Medical Report Analysis
- PDF medical report upload and analysis
- Intelligent text extraction and interpretation
- Persistent report context throughout conversation sessions

### 📚 Medical Research Integration
- Real-time medical article search via Europe PMC API
- Sliding articles panel with responsive design
- Access to peer-reviewed research and publications

### 🎨 Modern User Interface
- Clean, professional medical-themed design
- Responsive layout for desktop and mobile devices
- Font Awesome icons and smooth animations
- Custom SVG favicon with medical branding

### 🔒 Safety & Compliance
- Comprehensive medical disclaimer modal
- Clear warnings about AI limitations
- Emphasis on professional medical consultation

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **PyMuPDF**: PDF text extraction
- **Session Management**: In-memory storage for scalability
- **Europe PMC API**: Medical research integration

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript ES6+**: Interactive functionality
- **Font Awesome**: Professional icon library
- **Marked.js**: Markdown rendering for AI responses

### Deployment Ready
- Session-based file storage (cloud-compatible)
- No local file dependencies
- Scalable architecture

## 📱 Screenshots

### Main Interface
*[Screenshot placeholder - Main chat interface with medical assistant]*

### Medical Report Analysis
*[Screenshot placeholder - PDF upload and analysis feature]*

### Articles Search Panel
*[Screenshot placeholder - Sliding research articles panel]*

### Medical Disclaimer
*[Screenshot placeholder - Professional disclaimer modal]*

### Cardio Risk Assessment (Coming Soon)
*[Screenshots will be added when feature is implemented]*

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Flask
- Google Gemini API key
- Required packages (see requirements.txt)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ChaitanyaAgarwal72/MediSight.git
cd MediSight
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```bash
touch .env
```

4. Add your API keys to the `.env` file:
```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_flask_secret_key_here
```

5. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to `http://localhost:5000`

## 📝 Usage

1. **Accept Disclaimer**: Read and accept the medical disclaimer to proceed
2. **Ask Questions**: Type medical questions in the chat interface
3. **Upload Reports**: Upload PDF medical reports for AI analysis
4. **Search Articles**: Use the articles panel to find relevant medical research
5. **Clear Session**: Use the clear button to remove uploaded reports

## ⚠️ Important Disclaimer

MediSight is an AI assistant designed for informational purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns.

## 📚 Data Sources

The AI model is trained and enhanced using comprehensive medical literature including:

- **The GALE ENCYCLOPEDIA of Alternative MEDICINE (Second Edition)** - Comprehensive reference for alternative and complementary medical practices
- **The British Medical Association A-Z FAMILY MEDICAL ENCYCLOPEDIA** - Authoritative guide to family health and medical conditions  
- **2022 CURRENT Medical Diagnosis & Treatment (Sixty-First Edition)** - Up-to-date clinical guidelines and treatment protocols

These authoritative medical references ensure that MediSight provides accurate, evidence-based health information while maintaining the highest standards of medical knowledge.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Chaitanya Agarwal**
- GitHub: [@ChaitanyaAgarwal72](https://github.com/ChaitanyaAgarwal72)
- LinkedIn: [chaitanya-agarwal7](https://www.linkedin.com/in/chaitanya-agarwal7/)

## 🙏 Acknowledgments

- Europe PMC for medical research API
- Font Awesome for icons
- Flask community for the excellent framework
