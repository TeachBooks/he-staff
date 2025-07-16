from flask import Flask, request, redirect, session, jsonify
from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'secret-key-change-this-in-production')

# Health check endpoint
@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

# Root endpoint
@app.route('/')
def root():
    return jsonify({"message": "HE Staff Backend API is running"})

@app.route('/consume')
def consume_metadata():
    """Entity ID endpoint - return metadata"""
    return saml_metadata()

# SAML Configuration with explicit security settings (no signing)
def get_saml_settings():
    return {
        "sp": {
            "entityId": "https://he.citg.tudelft.nl/consume",
            "assertionConsumerService": {
                "url": "https://he.citg.tudelft.nl/api/auth/saml/consume",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST"
            },
            "singleLogoutService": {
                "url": "https://he.citg.tudelft.nl/api/auth/saml/logout",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "NameIDFormat": "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent",
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
        },
        "security": {
            # Explicitly disable all signing requirements
            "authnRequestsSigned": False,
            "logoutRequestSigned": False,
            "logoutResponseSigned": False,
            "signMetadata": False,
            
            # Response validation settings
            "wantAssertionsSigned": False,  # Don't require signed assertions
            "wantNameId": True,
            "wantAssertionsEncrypted": False,
            "wantNameIdEncrypted": False,
            
            # Authentication context
            "requestedAuthnContext": True,
            "requestedAuthnContextComparison": "exact",
            
            # XML validation
            "wantXMLValidation": True,
            
            # Destination validation
            "relaxDestinationValidation": True,  # More lenient validation
            "destinationStrictlyMatches": False,
            
            # Other settings
            "allowRepeatAttributeName": False,
            "rejectUnsolicitedResponsesWithInResponseTo": True,
            "signatureAlgorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"
        }
    }

def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, get_saml_settings())
    return auth


def prepare_flask_request(request):
    return {
        'https': 'on',
        'http_host': 'he.citg.tudelft.nl',
        'server_port': '443',
        'script_name': request.path,
        'get_data': request.args.copy(),
        'post_data': request.form.copy()
    }

# SAML endpoints matching TU Delft configuration
@app.route('/api/auth/saml/login')
def saml_login():
    """Initiate SAML login with improved debugging"""
    try:
        req = prepare_flask_request(request)
        print(f"SAML Login Request prepared: {req}")
        
        auth = init_saml_auth(req)
        sso_url = auth.login()
        
        print(f"SAML Login initiated, redirecting to: {sso_url}")
        
        # Check for errors in SAML request generation
        errors = auth.get_errors()
        if errors:
            print(f"SAML Login Errors: {errors}")
            return jsonify({'error': 'SAML login failed', 'details': errors}), 500
            
        return redirect(sso_url)
    except Exception as e:
        print(f"SAML Login Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'SAML login failed', 'details': str(e)}), 500

@app.route('/api/auth/saml/consume', methods=['POST'])
def saml_consume():
    """Process SAML response (matches TU Delft configuration)"""
    try:
        req = prepare_flask_request(request)
        auth = init_saml_auth(req)
        auth.process_response()

        errors = auth.get_errors()
        if not errors:
            # Store session data
            session['samlUserdata'] = auth.get_attributes()
            session['samlNameId'] = auth.get_nameid()
            session['samlSessionIndex'] = auth.get_session_index()

            # Extract NetID (TU Delft uses 'uid' attribute)
            uid = auth.get_attributes().get('uid', [None])[0]
            if uid:
                session['netid'] = uid
                session['authenticated'] = True
                print(f"SAML Authentication successful for user: {uid}")
                print(f"User attributes: {auth.get_attributes()}")
                
                # Redirect to frontend on success
                redirect_to = session.get('saml_redirect_to', '/admin/')
                return redirect(redirect_to)
            else:
                print("No NetID found in SAML response")
                return jsonify({'error': 'No NetID found in SAML response'}), 400
        else:
            print(f"SAML Authentication failed: {errors}")
            return jsonify({'error': 'SAML authentication failed', 'details': errors}), 400
    except Exception as e:
        print(f"SAML Consume Error: {str(e)}")
        return jsonify({'error': 'SAML consume failed', 'details': str(e)}), 500

@app.route('/api/auth/saml/logout')
def saml_logout():
    """Initiate SAML logout"""
    try:
        req = prepare_flask_request(request)
        auth = init_saml_auth(req)
        slo_url = auth.logout()
        print(f"SAML Logout initiated, redirecting to: {slo_url}")
        return redirect(slo_url)
    except Exception as e:
        print(f"SAML Logout Error: {str(e)}")
        return jsonify({'error': 'SAML logout failed', 'details': str(e)}), 500

@app.route('/api/auth/saml/sls')
def saml_sls():
    """Process SAML logout completion"""
    try:
        req = prepare_flask_request(request)
        auth = init_saml_auth(req)
        url = auth.process_slo(delete_session_cb=lambda: session.clear())
        errors = auth.get_errors()
        if not errors:
            return redirect(url or '/')
        else:
            return jsonify({'error': 'Logout failed', 'details': errors}), 400
    except Exception as e:
        print(f"SAML SLS Error: {str(e)}")
        return jsonify({'error': 'SAML SLS failed', 'details': str(e)}), 500

@app.route('/api/auth/saml/metadata')
def saml_metadata():
    """Provide SAML metadata"""
    try:
        settings = OneLogin_Saml2_Settings(get_saml_settings())
        metadata = settings.get_sp_metadata()
        resp = app.response_class(
            response=metadata,
            status=200,
            mimetype='text/xml'
        )
        return resp
    except Exception as e:
        print(f"SAML Metadata Error: {str(e)}")
        return jsonify({'error': 'Failed to generate metadata', 'details': str(e)}), 500

@app.route('/api/auth/status')
def auth_status():
    """Check authentication status"""
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
    """Redirect to login if authentication is required"""
    if not session.get('authenticated'):
        session['saml_redirect_to'] = request.args.get('redirect_to', '/admin/')
        return redirect('/api/auth/saml/login')
    else:
        return jsonify({'status': 'authenticated'})

# Legacy SAML endpoints (for backward compatibility)
@app.route('/api/saml/login')
def saml_login_legacy():
    """Legacy SAML login (redirect to new endpoint)"""
    return redirect('/api/auth/saml/login')

@app.route('/api/saml/acs', methods=['POST'])
def saml_acs_legacy():
    """Legacy SAML ACS (redirect to new endpoint)"""
    return redirect('/api/auth/saml/consume')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)