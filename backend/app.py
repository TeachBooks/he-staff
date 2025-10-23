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

# SAML Configuration with explicit security settings
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
            "entityId": "https://login.tudelft.nl/sso/saml2/idp/metadata.php",
            "singleSignOnService": {
                "url": "https://login.tudelft.nl/sso/module.php/saml/idp/singleSignOnService",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "singleLogoutService": {
                "url": "https://login.tudelft.nl/sso/module.php/saml/idp/singleLogout",
                "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
            },
            "x509cert": "MIIEETCCAvmgAwIBAgIJAPlfQEGrHWVOMA0GCSqGSIb3DQEBCwUAMIGeMQswCQYDVQQGEwJOTDEVMBMGA1UECAwMWnVpZC1Ib2xsYW5kMQ4wDAYDVQQHDAVEZWxmdDEmMCQGA1UECgwdVGVjaG5pc2NoZSBVbml2ZXJzaXRlaXQgRGVsZnQxFTATBgNVBAsMDElDVCBEaXJlY3RpZTEpMCcGA1UEAwwgbG9naW4udHVkZWxmdC5ubCBtZXRhZGF0YSBzaWduZXIwHhcNMjAwMTE2MTIyNDA4WhcNMzAwMTE1MTIyNDA4WjCBnjELMAkGA1UEBhMCTkwxFTATBgNVBAgMDFp1aWQtSG9sbGFuZDEOMAwGA1UEBwwFRGVsZnQxJjAkBgNVBAoMHVRlY2huaXNjaGUgVW5pdmVyc2l0ZWl0IERlbGZ0MRUwEwYDVQQLDAxJQ1QgRGlyZWN0aWUxKTAnBgNVBAMMIGxvZ2luLnR1ZGVsZnQubmwgbWV0YWRhdGEgc2lnbmVyMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwZfwGzcC4i0/t/nVWwvPqJ5OV+h+hG+D4cocsylwlg7DPcxNH3fVp+skGqg29j3KtmgUR8qiSrgin4Wec/+jMLs9X/D3ulhxQ4Tax1plKeVH5VohGGCtHwkEAcm9im5zhKCcm/y9wqfNLGaLbwTHs4yPNouqf87Zz9qM7X9ONUYx6CqwfWFwDGP48plZY+8PJlSdWId6shHdHmqn7Zf61hAeii8oiGCW/lBq0VXoB1CoCl/FmDoE+aIse4wTgrt9KTnF0/3E5qwwIJq4ugkM9yXrU9qg3/HHl89bH9/mlOdaEWsK4NgPUc2gES5qHopl5jWS+YqP4Nji3dQ+fgjoZQIDAQABo1AwTjAdBgNVHQ4EFgQU8nGBmwWwq4zx+uKB2Ro9BR72vHswHwYDVR0jBBgwFoAU8nGBmwWwq4zx+uKB2Ro9BR72vHswDAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAG/l8hS5V0xVaLCTKnKbf9vbKZP5dwevzfOVQO0tYX88oA2v5/6BXH1zOcHcUilZ0+ENCYeveyUDiZC7zA/w/P06WvWL/6IGUVoxwWtJYo0DCUffVzuh50QGDUrk/pdsHBtyFQdE9ZcDRGrHSyvd0NDApwLGVLeoDHkB2VDAoyfI5UXrBmaCL5+rkPbd1JPo8vHtpgD4ccL2bHefdx4feSPGOOJXyMzHFUigRbtzUUXh7hNKCHrsqvUGoY2MsD9o3lSLysDrUALxMl1GyydFzTLx03m8PCESRQ1BekMCfHA5rDqQs0QhZgeKFzaT3+zkymWhERdB/YeprbvDZz+peQg=="
        },
        "security": {
            "authnRequestsSigned": False,
            "logoutRequestSigned": False,
            "logoutResponseSigned": False,
            "signMetadata": False,
            "wantAssertionsSigned": True,
            "wantNameId": True,
            "wantAssertionsEncrypted": False,
            "wantNameIdEncrypted": False,
            "requestedAuthnContext": True,
            "requestedAuthnContextComparison": "exact",
            "wantXMLValidation": True,
            "relaxDestinationValidation": True,
            "destinationStrictlyMatches": False,
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
            attrs = auth.get_attributes()
            name_id = auth.get_nameid()

            session['samlUserdata'] = attrs
            session['samlNameId'] = name_id
            session['samlSessionIndex'] = auth.get_session_index()

            def first_val(a, key):
                v = a.get(key)
                if isinstance(v, list) and len(v) > 0:
                    return v[0]
                return None

            candidates = [
                'uid',
                'urn:oid:0.9.2342.19200300.100.1.1',
                'eduPersonPrincipalName',
                'urn:oid:1.3.6.1.4.1.5923.1.1.1.6',
                'mail',
                'email'
            ]

            uid = None
            for k in candidates:
                uid = first_val(attrs, k)
                if uid:
                    break

            if not uid and name_id:
                uid = name_id

            if uid:
                session['netid'] = uid
                session['authenticated'] = True
                print(f"SAML Authentication successful for user: {uid}")
                print(f"User attributes: {attrs}")

                redirect_to = session.get('saml_redirect_to', '/intro.html')
                return redirect(redirect_to)
            else:
                print(f"No accepted user identifier found in SAML response. Attributes keys: {list(attrs.keys())}, NameID: {name_id}")
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

@app.route('/api/auth/check')
def auth_check():
    """Return 204 when authenticated, 401 otherwise (for Nginx auth_request)"""
    if session.get('authenticated'):
        return ('', 204)
    else:
        return ('', 401)

@app.route('/api/auth/require')
def require_auth():
    """Redirect to login if authentication is required"""
    if not session.get('authenticated'):
        session['saml_redirect_to'] = request.args.get('redirect_to', '/intro.html')
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