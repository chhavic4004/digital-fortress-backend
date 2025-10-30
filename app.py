from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import re
from urllib.parse import urlparse
from datetime import datetime
from utils.logger import log_info, log_error, log_warning

app = Flask(__name__)
CORS(app)

SCAMS_FILE = 'scams.json'
stats = {
    'wifi_scans': 0,
    'fraud_detections': 0,
    'scam_reports': 0,
    'urls_checked': 0
}

def load_scams():
    if os.path.exists(SCAMS_FILE):
        try:
            with open(SCAMS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            log_error(f"Error reading {SCAMS_FILE}, returning empty list")
            return []
    return []

def save_scams(scams):
    try:
        with open(SCAMS_FILE, 'w') as f:
            json.dump(scams, f, indent=2)
        return True
    except Exception as e:
        log_error(f"Error saving scams: {e}")
        return False

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "name": "Digital Fortress Backend API",
        "version": "1.0.0",
        "description": "Cybersecurity platform providing Wi-Fi security, fraud detection, chatbot, scam reporting, and URL scanning.",
        "endpoints": {
            "health": "GET /health",
            "stats": "GET /stats",
            "wifi_scan": "POST /wifi_scan",
            "detect_fraud": "POST /detect_fraud",
            "chatbot": "POST /chatbot",
            "add_scam": "POST /add_scam",
            "get_scams": "GET /get_scams",
            "url_scan": "POST /url_scan"
        },
        "documentation": "See README.md for detailed API documentation"
    }), 200

@app.route('/health', methods=['GET'])
def health():
    log_info("Health check requested")
    return jsonify({"status": "OK"}), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    log_info("Stats requested")
    return jsonify(stats), 200

@app.route('/wifi_scan', methods=['POST'])
def wifi_scan():
    try:
        data = request.get_json()
        
        if not data or 'ssid' not in data:
            return jsonify({"error": "SSID is required"}), 400
        
        ssid = data.get('ssid', '')
        encryption = data.get('encryption', 'UNKNOWN').upper()
        dns = data.get('dns', '')
        activity = data.get('activity', 'browsing').lower()
        
        risk_score = 0
        risk_factors = []
        
        if encryption in ['OPEN', 'NONE', '']:
            risk_score += 40
            risk_factors.append("No encryption detected")
        elif encryption in ['WEP']:
            risk_score += 30
            risk_factors.append("Weak encryption (WEP)")
        elif encryption in ['WPA']:
            risk_score += 15
            risk_factors.append("Older encryption (WPA)")
        elif encryption in ['WPA2', 'WPA3']:
            risk_score += 5
        
        suspicious_dns = ['8.8.8.8', '1.1.1.1']
        if dns and dns not in suspicious_dns:
            risk_score += 10
            risk_factors.append("Unknown DNS server")
        
        sensitive_activities = ['bank_login', 'payment', 'login', 'banking', 'transaction']
        if any(act in activity for act in sensitive_activities):
            risk_score += 30
            risk_factors.append("Sensitive activity detected")
        
        if risk_score >= 70:
            risk_level = "High"
            if any(act in activity for act in sensitive_activities):
                message = f"Sensitive data like banking details can be intercepted on public Wi-Fi. Use a VPN or mobile data instead."
            else:
                message = "This network is not secure. Avoid accessing sensitive information."
        elif risk_score >= 40:
            risk_level = "Medium"
            message = "This network has moderate security risks. Use caution with sensitive data."
        else:
            risk_level = "Low"
            message = "This network appears relatively safe, but always use caution on public Wi-Fi."
        
        stats['wifi_scans'] += 1
        log_info(f"Wi-Fi scan completed for SSID: {ssid}, Risk Level: {risk_level}")
        
        return jsonify({
            "ssid": ssid,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "message": message,
            "risk_factors": risk_factors
        }), 200
        
    except Exception as e:
        log_error(f"Error in wifi_scan: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/detect_fraud', methods=['POST'])
def detect_fraud():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"error": "Text is required"}), 400
        
        text = data.get('text', '').lower()
        
        fraud_keywords = {
            'kyc': 15,
            'otp': 12,
            'urgent': 10,
            'verify': 10,
            'expire': 12,
            'suspend': 12,
            'click here': 15,
            'link': 8,
            'prize': 10,
            'won': 10,
            'lottery': 15,
            'bank': 8,
            'account': 7,
            'password': 10,
            'confirm': 8,
            'update': 7,
            'credit card': 12,
            'debit card': 12,
            'reward': 9,
            'congratulations': 10,
            'act now': 12,
            'limited time': 10,
            'refund': 9,
            'tax': 8,
            'aadhaar': 10,
            'pan': 8
        }
        
        fraud_score = 0
        risky_keywords = []
        
        for keyword, score in fraud_keywords.items():
            if keyword in text:
                fraud_score += score
                risky_keywords.append(keyword)
        
        if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text):
            fraud_score += 15
            if 'link' not in risky_keywords:
                risky_keywords.append('suspicious link')
        
        fraud_score = min(fraud_score, 100)
        
        if fraud_score >= 70:
            risk_level = "High"
            advice = "Likely phishing attempt. Do not click unknown links or share personal information."
        elif fraud_score >= 40:
            risk_level = "Medium"
            advice = "This message shows suspicious characteristics. Verify the source before taking action."
        else:
            risk_level = "Low"
            advice = "This message appears safe, but always verify sender authenticity."
        
        stats['fraud_detections'] += 1
        log_info(f"Fraud detection completed, Risk Level: {risk_level}")
        
        return jsonify({
            "fraud_score": fraud_score,
            "risk_level": risk_level,
            "risky_keywords": risky_keywords,
            "advice": advice
        }), 200
        
    except Exception as e:
        log_error(f"Error in detect_fraud: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/chatbot', methods=['POST'])
def chatbot():
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({"error": "Query is required"}), 400
        
        query = data.get('query', '').lower()
        
        responses = {
            'whatsapp': "Enable two-step verification on WhatsApp and never share verification codes. Go to Settings > Account > Two-step verification to set it up.",
            'wifi': "Avoid using public Wi-Fi for sensitive activities like banking. Use a VPN or mobile data for secure connections.",
            'phishing': "Never click suspicious links in emails or messages. Always verify the sender's identity and check URLs before clicking.",
            'password': "Use strong, unique passwords for each account. Enable two-factor authentication wherever possible. Consider using a password manager.",
            'scam': "Common scam signs: urgent requests, suspicious links, requests for OTP/passwords, prize notifications. Always verify before sharing information.",
            'kyc': "Banks never ask for KYC updates via SMS or email links. Always visit the official website or app directly.",
            'otp': "Never share OTP codes with anyone. Legitimate services never ask for OTPs via call or message.",
            'bank': "Banks never call asking for card details, PIN, or OTP. If in doubt, hang up and call the bank's official number.",
            'email': "Check sender email carefully for misspellings. Hover over links before clicking. Be wary of urgent requests or threats.",
            'social media': "Keep your profiles private, don't accept friend requests from strangers, and be careful what you share publicly.",
            'vpn': "A VPN encrypts your internet traffic and hides your IP address. Use reputable VPN services, especially on public Wi-Fi.",
            'antivirus': "Keep your antivirus software updated. Run regular scans and be cautious when downloading files from unknown sources.",
            'ransomware': "Backup your data regularly. Don't click suspicious links or download unknown attachments. Keep software updated.",
            'fraud': "Report fraud immediately to your bank and local authorities. Document all communication and don't engage with scammers."
        }
        
        response = None
        for key, value in responses.items():
            if key in query:
                response = value
                break
        
        if not response:
            response = "I can help with cybersecurity questions about Wi-Fi safety, phishing, passwords, scams, WhatsApp security, and more. What would you like to know?"
        
        log_info(f"Chatbot query processed: {query[:50]}...")
        
        return jsonify({"response": response}), 200
        
    except Exception as e:
        log_error(f"Error in chatbot: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/add_scam', methods=['POST'])
def add_scam():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        scams = load_scams()
        
        new_id = max([scam.get('id', 0) for scam in scams], default=0) + 1
        
        new_scam = {
            'id': new_id,
            'user': data.get('user', 'Anonymous'),
            'message': data.get('message', ''),
            'category': data.get('category', 'General'),
            'date': data.get('date', datetime.now().strftime('%Y-%m-%d')),
            'source': data.get('source', 'Web')
        }
        
        scams.append(new_scam)
        
        if save_scams(scams):
            stats['scam_reports'] += 1
            log_info(f"Scam report added: ID {new_id}")
            return jsonify({"message": "Scam report added successfully", "id": new_id}), 200
        else:
            return jsonify({"error": "Failed to save scam report"}), 500
        
    except Exception as e:
        log_error(f"Error in add_scam: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/get_scams', methods=['GET'])
def get_scams():
    try:
        scams = load_scams()
        
        category = request.args.get('category')
        if category:
            scams = [scam for scam in scams if scam.get('category', '').lower() == category.lower()]
        
        log_info(f"Scams retrieved: {len(scams)} records")
        return jsonify(scams), 200
        
    except Exception as e:
        log_error(f"Error in get_scams: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/url_scan', methods=['POST'])
def url_scan():
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({"error": "URL is required"}), 400
        
        url = data.get('url', '')
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
        except Exception:
            return jsonify({
                "url": url,
                "safe": False,
                "reason": "Invalid URL format",
                "risk_score": 95
            }), 200
        
        risk_score = 0
        reasons = []
        
        suspicious_keywords = [
            'verify', 'login', 'secure', 'account', 'update', 'confirm',
            'kyc', 'bank', 'payment', 'signin', 'authentication',
            'password', 'credential', 'urgent', 'suspended'
        ]
        
        for keyword in suspicious_keywords:
            if keyword in domain or keyword in path:
                risk_score += 15
                reasons.append(f"Contains suspicious keyword: '{keyword}'")
        
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
            risk_score += 30
            reasons.append("IP address instead of domain name")
        
        if domain.count('-') > 2:
            risk_score += 15
            reasons.append("Excessive hyphens in domain")
        
        if len(domain) > 50:
            risk_score += 20
            reasons.append("Unusually long domain name")
        
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top']
        if any(domain.endswith(tld) for tld in suspicious_tlds):
            risk_score += 25
            reasons.append("Suspicious top-level domain")
        
        if '@' in url:
            risk_score += 30
            reasons.append("URL contains @ symbol (phishing indicator)")
        
        risk_score = min(risk_score, 100)
        
        safe = risk_score < 50
        
        if not reasons:
            reason = "URL appears safe"
        else:
            reason = "; ".join(reasons)
        
        stats['urls_checked'] += 1
        log_info(f"URL scanned: {url[:50]}..., Risk Score: {risk_score}")
        
        return jsonify({
            "url": url,
            "safe": safe,
            "reason": reason,
            "risk_score": risk_score
        }), 200
        
    except Exception as e:
        log_error(f"Error in url_scan: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    if not os.path.exists(SCAMS_FILE):
        save_scams([])
        log_info(f"Created {SCAMS_FILE}")
    
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    log_info(f"Digital Fortress Backend Starting on port 8080 (Debug: {debug_mode})...")
    app.run(host='0.0.0.0', port=8080, debug=debug_mode)
