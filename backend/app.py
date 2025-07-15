from flask import Flask, request, redirect, session, jsonify
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')

# Your existing hello endpoint
@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from HE backend!"})

# SAML Configuration
def get_saml_settings():
    return {
        "sp": {
            "entityId": "https://he.citg.tudelft.nl/consume",
            "assertionConsumerService": {
                "url": "https://he.citg.tudelft.nl/api/saml/acs",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            },
            "singleLogoutService": {
                "url": "https://he.citg.tudelft.nl/api/saml/sls",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "NameIDFormat": "urn:oasis:names:tc:SAML:1.1:nameid-format:unspecified",
            "x509cert": "",
            "privateKey": ""
        },
        "idp": {
            "entityId": "https://login-test.tudelft.nl/sso/saml2/idp/metadata.php",
            "singleSignOnService": {
                "url": "https://login-test.tudelft.nl/sso/module.php/saml/idp/singleSignOnService",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "singleLogoutService": {
                "url": "https://login-test.tudelft.nl/sso/module.php/saml/idp/singleLogout",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "x509cert": "MIIEGzCCAwOgAwIBAgIJAOZpaPLm92tzMA0GCSqGSIb3DQEBCwUAMIGjMQswCQYDVQQGEwJOTDEVMBMGA1UECAwMWnVpZC1Ib2xsYW5kMQ4wDAYDVQQHDAVEZWxmdDEmMCQGA1UECgwdVGVjaG5pc2NoZSBVbml2ZXJzaXRlaXQgRGVsZnQxFTATBgNVBAsMDElDVCBEaXJlY3RpZTEuMCwGA1UEAwwlbG9naW4tdGVzdC50dWRlbGZ0Lm5sIG1ldGFkYXRhIHNpZ25lcjAeFw0xOTA1MDkxNTIwMzRaFw0yOTA1MDgxNTIwMzRaMIGjMQswCQYDVQQGEwJOTDEVMBMGA1UECAwMWnVpZC1Ib2xsYW5kMQ4wDAYDVQQHDAVEZWxmdDEmMCQGA1UECgwdVGVjaG5pc2NoZSBVbml2ZXJzaXRlaXQgRGVsZnQxFTATBgNVBAsMDElDVCBEaXJlY3RpZTEuMCwGA1UEAwwlbG9naW4tdGVzdC50dWRlbGZ0Lm5sIG1ldGFkYXRhIHNpZ25lcjCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMV7uciTXKvoMwvFsYL79t6fMPn44/fOZRPHEz1cKQPjhecAsNKW72EqUUCoMLPk18AACagfd4Eil07l9FTwYhVoXSuvbmM3i51DSwfDEjI7VxoBtR8OdM2XFntcvuVxPiLOAJHA9hTDngA1gG1GYHbweDsgWhaCJ1VH6UB95klrq6++91vauXjqGx463QkLvVpFnPk2TZiTL253wfw6h2QHomiIPyyBdPtP5Lg5R7COTJrz4neGZk3adXJEnlSIZfA587kXm4TU3wPDoCMAM9xpozGtvWWGz1o9U79nxz7vJt1xIGA/TS7C0zvZ5BK0Te/3nLEcFnMnTqQxeKoqQK0CAwEAAaNQME4wHQYDVR0OBBYEFKo0sh4IIRzpRqD1+OIFjJCYres6MB8GA1UdIwQYMBaAFKo0sh4IIRzpRqD1+OIFjJCYres6MAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBADwqQgupwUjLHDUjvKc7zGEx01DA4QAYD1FWBd9EkVw2YBJvh8EMlPfmUshbqk6ruDA/TtSm8jhcUCGD2fDO5a4eC6lml8jVmDAVssjnc9dOmcxDUIss3YrWJV2nqwOUL2g4zS75duaPpYONVxvcZTkc/Idb5OLm8kc9VxZpZ4ynMiJOMir/5K3j5VL+oglmNx0zr9SU73OepKUCCKz/84tRduKWbWKpiO3bry8jY3w8XzVnOd+rrYz44FzxDH/+NcIF5Ur1Gw/402kQpjDLz303Z81L4jR9Lc5C1edtilEFkrrZ0ckqVmqFy2EDDfWfO+X3M3Vb00CHEZV0EejfcRw="
        }
    }

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, get_saml_settings())
    return auth

def prepare_flask_request(request):
    url_data = request.url.split('?')
    return {
        'https': 'on' if request.scheme == 'https' else 'off',
        'http_host': request.host,
        'server_port': request.environ.get('SERVER_PORT'),
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }

@app.route('/api/saml/login')
def saml_login():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.login())

@app.route('/api/saml/acs', methods=['POST'])
def saml_acs():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    auth.process_response()
    
    errors = auth.get_errors()
    if not errors:
        session['samlUserdata'] = auth.get_attributes()
        session['samlNameId'] = auth.get_nameid()
        session['samlSessionIndex'] = auth.get_session_index()
        
        uid = auth.get_attributes().get('uid', [None])[0]
        if uid:
            session['netid'] = uid
            session['authenticated'] = True
            return redirect(session.get('saml_redirect_to', '/admin/'))
        else:
            return jsonify({'error': 'No NetID found in SAML response'}), 400
    else:
        return jsonify({'error': 'SAML authentication failed', 'details': errors}), 400

@app.route('/api/saml/sls')
def saml_sls():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    url = auth.process_slo(delete_session_cb=lambda: session.clear())
    errors = auth.get_errors()
    if not errors:
        return redirect(url or '/')
    else:
        return jsonify({'error': 'Logout failed', 'details': errors}), 400

@app.route('/api/saml/logout')
def saml_logout():
    req = prepare_flask_request(request)
    auth = init_saml_auth(req)
    return redirect(auth.logout())

@app.route('/api/saml/metadata')
def saml_metadata():
    settings = OneLogin_Saml2_Settings(get_saml_settings())
    metadata = settings.get_sp_metadata()
    resp = app.response_class(
        response=metadata,
        status=200,
        mimetype='text/xml'
    )
    return resp

@app.route('/api/auth/status')
def auth_status():
    if session.get('authenticated'):
        return jsonify({
            'authenticated': True,
            'netid': session.get('netid'),
            'attributes': session.get('samlUserdata', {})
        })
    else:
        return jsonify({'authenticated': False})

@app.route('/api/auth/require')
def require_auth():
    if not session.get('authenticated'):
        session['saml_redirect_to'] = request.args.get('redirect_to', '/admin/')
        return redirect('/api/saml/login')
    else:
        return jsonify({'status': 'authenticated'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)