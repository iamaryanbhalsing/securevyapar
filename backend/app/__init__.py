import os
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_url_path='/securevyapar/static', static_folder='static')
    CORS(app)
    
    # Load configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        VIRUSTOTAL_API_KEY=os.getenv('VIRUSTOTAL_API_KEY', ''),
    )
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # A simple page that says hello
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/securevyapar/')
    def securevyapar_index():
        return render_template('index.html')
    
    # API: Scan URL
    @app.route('/api/scan/url', methods=['POST'])
    def scan_url():
        data = request.get_json()
        url = data.get('url', '') if data else ''
        
        # Rule-based detection (same patterns as client-side)
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
        
        for pattern, category, title, risk in scam_patterns:
            import re
            if re.search(pattern, url, re.IGNORECASE):
                result = {
                    'risk': risk,
                    'category': category,
                    'title': title,
                    'explanation': f'This looks like a {title.lower().replace(" ", " ")}. {("Do not click." if risk == "high" else "")}',
                    'action': 'Ignore and delete the message.' if risk == 'high' else 'Be cautious and verify the source.',
                }
                break
        
        # If VirusTotal key is available, check it
        vt_key = app.config.get('VIRUSTOTAL_API_KEY', '')
        if vt_key:
            try:
                import requests
                VT_URL = f'https://www.virustotal.com/api/v3/urls'
                # Check if URL is already in VT
                headers = {'x-apikey': vt_key}
                # Submit for analysis
                resp = requests.post(VT_URL, headers=headers, json={'url': url})
                if resp.status_code == 200:
                    vt_data = resp.json()
                    data_id = vt_data.get('data', {}).get('id', '')
                    # Get analysis results
                    if data_id:
                        get_url = f'https://www.virustotal.com/api/v3/urls/{data_id}'
                        get_resp = requests.get(get_url, headers=headers)
                        if get_resp.status_code == 200:
                            analysis = get_resp.json()
                            attributes = analysis.get('data', {}).get('attributes', {})
                            stats = attributes.get('last_analysis_stats', {})
                            malicious = stats.get('malicious', 0)
                            suspicious = stats.get('suspicious', 0)
                            
                            if malicious > 0 or suspicious > 0:
                                result = {
                                    'risk': 'dangerous',
                                    'category': 'malware',
                                    'title': 'Malware/Dangerous URL',
                                    'explanation': f'This URL has been flagged by {malicious} antivirus engines as malicious and {suspicious} as suspicious.',
                                    'action': 'Do not under any circumstances click this link. Report it immediately.',
                                }
                            elif suspicious > 0:
                                result = {
                                    'risk': 'suspicious',
                                    'category': 'potential-malware',
                                    'title': 'Suspicious URL',
                                    'explanation': f'This URL has been flagged by {suspicious} antivirus engine(s) as suspicious.',
                                    'action': 'Exercise extreme caution. Do not enter any credentials or download files.',
                                }
            except Exception as e:
                # If API fails, fall back to rule-based
                pass
        
        return jsonify(result)
    
    # API: Scan file (hash)
    @app.route('/api/scan/file', methods=['POST'])
    def scan_file():
        data = request.get_json()
        file_hash = data.get('hash', '') if data else ''
        
        vt_key = app.config.get('VIRUSTOTAL_API_KEY', '')
        result = {
            'risk': 'low',
            'category': 'safe',
            'title': 'File appears safe',
            'explanation': 'No threats detected in hash lookup.',
            'action': 'Continue to use the file as normal.',
        }
        
        if vt_key:
            try:
                import requests
                VT_URL = f'https://www.virustotal.com/api/v3/files/{file_hash}'
                headers = {'x-apikey': vt_key}
                resp = requests.get(VT_URL, headers=headers)
                if resp.status_code == 200:
                    vt_data = resp.json()
                    data = vt_data.get('data', {})
                    attributes = data.get('attributes', {})
                    stats = attributes.get('last_analysis_stats', {})
                    malicious = stats.get('malicious', 0)
                    suspicious = stats.get('suspicious', 0)
                    total = stats.get 'harmless', 0) + stats.get('malicious', 0) + stats.get('suspicious', 0)
                    
                    if malicious > 0:
                        result = {
                            'risk': 'dangerous',
                            'category': 'malware',
                            'title': 'Malware Detected',
                            'explanation': f'This file is malicious. {malicious} out of {total} engines detected it as malware.',
                            'action': 'Delete the file immediately and run a full antivirus scan.',
                        }
                    elif suspicious > 0:
                        result = {
                            'risk': 'suspicious',
                            'category': 'potential-malware',
                            'title': 'Suspicious File',
                            'explanation': f'This file is suspicious. {suspicious} out of {total} engines flagged it.',
                            'action': 'Do not execute this file. Scan it with your antivirus.',
                        }
            except Exception:
                pass
        
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
    
    # Serve static files
    @app.route('/securevyapar/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)
    
    return app