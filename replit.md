# Digital Fortress Backend - Project Documentation

## Overview
Digital Fortress is a comprehensive cybersecurity platform backend built with Python Flask. The system provides REST APIs for multiple security features including Wi-Fi security scanning, fraud detection, AI-powered chatbot assistance, community scam reporting, and URL security analysis.

**Status**: Production-ready
**Version**: 1.0.0
**Last Updated**: October 30, 2025

## Project Goals
Build a modular, secure, and production-ready backend that:
- Analyzes Wi-Fi network security with risk scoring
- Detects phishing and fraud patterns in messages/calls
- Provides cybersecurity guidance through an AI chatbot
- Enables community-driven scam reporting
- Scans URLs for security threats (browser extension support)
- Easily integrates with React + Vite + Tailwind frontend on Vercel

## Current Architecture

### Tech Stack
- **Framework**: Flask 3.0.0
- **Language**: Python 3.11
- **CORS**: Flask-CORS 4.0.0 (enabled for Vercel frontend)
- **Storage**: JSON file-based (scams.json)
- **Logging**: Python logging module with custom utilities
- **Port**: 8080 (configurable)

### Project Structure
```
/
├── app.py              # Main Flask application with all endpoints
├── requirements.txt    # Python dependencies
├── scams.json         # Scam database (JSON storage)
├── utils/
│   ├── logger.py      # Logging utilities
│   └── ai_utils.py    # AI/ML model utilities (placeholder)
├── models/            # ML models directory (future use)
├── data/              # Data storage directory
└── README.md          # API documentation
```

### API Endpoints
1. **GET /** - API information and endpoint list
2. **GET /health** - Health check endpoint
3. **GET /stats** - Platform usage statistics
4. **POST /wifi_scan** - Wi-Fi security analysis
5. **POST /detect_fraud** - Fraud/phishing detection
6. **POST /chatbot** - Cybersecurity chatbot
7. **POST /add_scam** - Add scam report
8. **GET /get_scams** - Retrieve scam reports (supports filtering)
9. **POST /url_scan** - URL security analysis

## Key Features Implemented

### 1. Wi-Defend (Wi-Fi Security Scanner)
- Evaluates encryption type (OPEN, WEP, WPA, WPA2, WPA3)
- Checks DNS server safety
- Context-aware risk scoring based on user activity (browsing, banking, etc.)
- Provides actionable security recommendations

### 2. Fraud Detector
- Keyword-based phishing detection
- Pattern matching for common scam indicators
- Risk level classification (Low, Medium, High)
- Identifies risky keywords and provides security advice

### 3. AI Cyber Guardian Chatbot
- Rule-based response system
- Covers topics: WhatsApp security, Wi-Fi safety, phishing, passwords, scams, etc.
- Expandable to NLP/ML models in future

### 4. Community Scam Database
- JSON-based storage with auto-ID generation
- Category filtering support
- Safe read/write operations
- Sample data included

### 5. URL Scanner
- Domain analysis for suspicious patterns
- Keyword detection (kyc, verify, login, bank, etc.)
- IP address detection
- TLD analysis (.tk, .ml, .xyz, etc.)
- Risk scoring for browser extension integration

## Security Features
- **Debug Mode**: Environment-controlled (FLASK_DEBUG), defaults to False
- **Input Validation**: All endpoints validate required fields
- **Error Handling**: Comprehensive try-catch blocks with proper status codes
- **CORS**: Configured for cross-origin requests
- **Logging**: All requests and errors are logged
- **Safe Storage**: JSON file operations with error handling

## Recent Changes
- **Oct 30, 2025**: Initial implementation complete
  - All 9 API endpoints implemented and tested
  - Security fix: Changed debug mode from hardcoded True to environment variable
  - Added root endpoint (/) for API information
  - Created comprehensive README with deployment instructions
  - Added environment variable documentation

## Environment Variables
- `FLASK_DEBUG`: Controls debug mode (default: false for security)

## Deployment Notes
- **Development**: Run with `python app.py` (Flask dev server)
- **Production**: Use Gunicorn or uWSGI for better performance and security
  - Example: `gunicorn --bind 0.0.0.0:8080 --workers 4 app:app`
- **Platform**: Compatible with Render, Railway, Replit Deploy
- **Port**: 8080 (standard configuration)

## Testing
All endpoints have been tested and verified:
- ✅ Root endpoint returns API information
- ✅ Health check works
- ✅ Statistics tracking functional
- ✅ Wi-Fi scanning with various encryption types
- ✅ Fraud detection with keyword matching
- ✅ Chatbot responses for security queries
- ✅ Scam reporting and retrieval
- ✅ URL scanning with risk assessment

## Future Enhancements (Next Phase)
1. **Machine Learning Integration**
   - Train fraud detection model
   - Implement model loading from /models directory
   - Enhanced prediction accuracy

2. **OpenAI Integration**
   - Natural language understanding for chatbot
   - Contextual responses
   - Multi-turn conversations

3. **Database Migration**
   - PostgreSQL for scalability
   - Better concurrent access
   - Data relationships

4. **Authentication**
   - JWT token-based auth
   - User profiles
   - Personalized scam history

5. **Threat Intelligence**
   - Real-time phishing URL databases
   - Malware domain feeds
   - Automatic updates

## User Preferences
- Production-ready code with security best practices
- Modular architecture for easy extensibility
- Comprehensive documentation
- Clean JSON responses
- Proper error handling and logging

## Maintenance Notes
- Scams database grows with user submissions (monitor file size)
- For production: Consider implementing database cleanup/archival
- Review CORS settings before production deployment
- Update fraud keywords based on emerging threats
- Monitor stats endpoint for usage patterns
