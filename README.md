# Digital Fortress Backend

A comprehensive cybersecurity platform backend built with Flask, providing REST APIs for Wi-Fi security scanning, fraud detection, AI chatbot assistance, community scam reporting, and URL protection.

## Features

- **Wi-Defend**: Public Wi-Fi security analyzer with risk scoring
- **Fraud Detector**: Message and call phishing detection
- **AI Cyber Guardian**: Rule-based cybersecurity chatbot
- **Community Storyboard**: Scam reporting and database
- **URL Scanner**: Browser extension protection system
- **Statistics Dashboard**: Platform usage metrics

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will start on `http://0.0.0.0:8080`

## API Endpoints

### Health Check
**GET** `/health`

Returns server status.

**Response:**
```json
{
  "status": "OK"
}
```

### Statistics
**GET** `/stats`

Returns platform usage statistics.

**Response:**
```json
{
  "wifi_scans": 32,
  "fraud_detections": 58,
  "scam_reports": 24,
  "urls_checked": 19
}
```

### Wi-Defend - Wi-Fi Security Scan
**POST** `/wifi_scan`

Analyzes Wi-Fi network security and provides risk assessment.

**Request:**
```json
{
  "ssid": "Cafe_Free_WiFi",
  "encryption": "OPEN",
  "dns": "8.8.8.8",
  "activity": "bank_login"
}
```

**Response:**
```json
{
  "ssid": "Cafe_Free_WiFi",
  "risk_score": 85,
  "risk_level": "High",
  "message": "Sensitive data like banking details can be intercepted on public Wi-Fi. Use a VPN or mobile data instead.",
  "risk_factors": ["No encryption detected", "Sensitive activity detected"]
}
```

### Fraud Detection
**POST** `/detect_fraud`

Analyzes messages or calls for phishing and fraud patterns.

**Request:**
```json
{
  "text": "Your KYC is expiring. Click here to update."
}
```

**Response:**
```json
{
  "fraud_score": 92,
  "risk_level": "High",
  "risky_keywords": ["kyc", "click here"],
  "advice": "Likely phishing attempt. Do not click unknown links or share personal information."
}
```

### AI Chatbot
**POST** `/chatbot`

Provides cybersecurity guidance and answers.

**Request:**
```json
{
  "query": "How do I protect my WhatsApp from hacking?"
}
```

**Response:**
```json
{
  "response": "Enable two-step verification on WhatsApp and never share verification codes. Go to Settings > Account > Two-step verification to set it up."
}
```

### Add Scam Report
**POST** `/add_scam`

Submit a scam report to the community database.

**Request:**
```json
{
  "user": "Amit",
  "message": "I got a fake job offer on email.",
  "category": "Job Scam",
  "date": "2025-10-30"
}
```

**Response:**
```json
{
  "message": "Scam report added successfully",
  "id": 4
}
```

### Get Scam Reports
**GET** `/get_scams`

Retrieve scam reports from the database.

**Optional Query Parameters:**
- `category`: Filter by scam category (e.g., `?category=Banking%20Scam`)

**Response:**
```json
[
  {
    "id": 1,
    "user": "Amit",
    "category": "Job Scam",
    "message": "Fake job offer",
    "date": "2025-10-30"
  }
]
```

### URL Scanner
**POST** `/url_scan`

Analyze URLs for security threats (for browser extension).

**Request:**
```json
{
  "url": "https://bank-verification-kyc.net"
}
```

**Response:**
```json
{
  "url": "https://bank-verification-kyc.net",
  "safe": false,
  "reason": "Contains suspicious keyword: 'kyc'; Contains suspicious keyword: 'bank'",
  "risk_score": 88
}
```

## Project Structure

```
/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── scams.json            # Scam database (JSON storage)
├── utils/
│   ├── logger.py         # Logging utilities
│   └── ai_utils.py       # AI/ML model utilities
├── models/               # ML models directory (future use)
└── data/                 # Data storage directory
```

## Deployment

### Deploy to Render/Railway

1. Push code to GitHub repository
2. Connect repository to Render/Railway
3. Set environment variables if needed
4. Deploy (app runs on port 8080 by default)

### CORS Configuration

CORS is enabled for all origins to support frontend deployment on Vercel. For production, configure specific allowed origins in `app.py`.

## Security Features

- Input sanitization and validation
- Comprehensive error handling
- Request logging
- JSON-based secure storage
- Risk scoring algorithms

## Future Enhancements

- Machine learning model integration for advanced fraud detection
- OpenAI API integration for enhanced chatbot responses
- PostgreSQL database for scalability
- User authentication with JWT
- Real-time threat intelligence feeds

## License

MIT License

## Support

For issues or questions, please open an issue in the repository.
