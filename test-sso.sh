#!/bin/bash
# test-sso.sh - Script to test SAML SSO integration
# Place this in your project root for testing

echo "Testing SAML SSO Integration with TU Delft"
echo "=========================================="

BASE_URL="https://he.citg.tudelft.nl"

echo "1. Testing backend hello endpoint..."
curl -s "${BASE_URL}/api/hello" | jq .
echo ""

echo "2. Testing metadata endpoint..."
echo "First few lines of metadata:"
curl -s "${BASE_URL}/api/saml/metadata" | head -5
echo ""

echo "3. Testing authentication status (should be unauthenticated)..."
curl -s "${BASE_URL}/api/auth/status" | jq .
echo ""

echo "4. Testing login redirect..."
echo "Should return a 302 redirect to TU Delft:"
curl -s -I "${BASE_URL}/api/saml/login" | grep -E "(HTTP|Location)"
echo ""

echo "5. Manual testing steps:"
echo "   a) Visit: ${BASE_URL}/api/saml/login"
echo "   b) Login with your NetID at TU Delft"
echo "   c) Check status: ${BASE_URL}/api/auth/status"
echo ""

echo "6. Getting TU Delft metadata..."
if command -v curl &> /dev/null; then
    curl -s "https://login-test.tudelft.nl/sso/saml2/idp/metadata.php" > tudelft_metadata.xml
    echo "   Metadata saved to tudelft_metadata.xml"
    
    # Extract certificate
    if grep -q "X509Certificate" tudelft_metadata.xml; then
        grep -o '<ds:X509Certificate>[^<]*' tudelft_metadata.xml | sed 's/<ds:X509Certificate>//' > tudelft_cert.txt
        echo "   Certificate extracted to tudelft_cert.txt"
        echo "   Add this certificate to your SAML settings in backend/app.py"
    fi
fi
