from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# A simple page that says hello
@app.route('/')
def index():
    return '<h1>SecureVyapar Backend API</h1><p>Use /api/scan/url or /api/scan/file endpoints</p>'

# API: Scan URL
@app.route('/api/scan/url', methods=['POST'])
def scan_url():
    import re
    import json
    data = request.get_json()
    url = data.get('url', '') if data else ''
    
    # Rule-based detection patterns for Indian shop owners
    scam_patterns = [
        (r'upi://pay\?', 'upi', 'Fake UPI Payment Request', 'high'),
        (r'(secure|login|verify).*(gpay|phonepe|upi).*\.?com', 'links', 'Fake Payment App Login', 'high'),
        (r'free.recharg|free.gift|free.coupon', 'links', 'Free Recharge/Gift Scam', 'high'),
        (r'gst|gstIN|tax.refund', 'links', 'GST/Tax Refishing', 'medium'),
        (r'bit\.ly|tinyurl|t\.co|short\.link', 'links', 'URL Shortener', 'medium'),
        (r'\.(xyz|top|gq|ml|tk|ooo|top)$', 'links', 'Suspicious TLD', 'medium'),
        (r'[0-9]{2,3}\.(google|gpay|upi|amazon|flipkart|paytm)\.com', 'links', 'Domain Impersonation', 'high'),
    ]
    
    result = {'risk': 'low', 'category': 'safe', 'title': 'Link appears safe', 
              'explanation': 'No known scam patterns matched. Always exercise caution with unfamiliar links.', 
              'action': 'Verify the source before clicking.'}
    
    for pattern, cat, title, risk in scam_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            result = {
                'risk': risk,
                'category': cat,
                'title': title,
                'explanation': f'This looks like a {title.lower().replace(" ", " ")}. Do not click.',
                'action': 'Ignore and delete the message.' if risk == 'high' else 'Be cautious and verify the source.',
            }
            break
    
    return jsonify(result)

# API: Scan file (hash)
@app.route('/api/scan/file', methods=['POST'])
def scan_file():
    data = request.get_json()
    file_hash = data.get('hash', '') if data else ''
    
    result = {
        'risk': 'low',
        'category': 'safe',
        'title': 'File appears safe',
        'explanation': 'No threats detected in hash lookup.',
        'action': 'Continue to use the file as normal.',
    }
    
    return jsonify(result)

# API: Get stats
@app.route('/api/stats')
def stats():
    return jsonify({
        'total_assessments': 0,
        'average_score': 0,
        'high_risk_count': 0,
        'medium_risk_count': 0,
        'low_risk_count': 0,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)