#!/bin/sh

# This script runs at container startup and injects the correct API URL
# into the HTML file based on the current server hostname

# Find the main JavaScript file (it has a content hash)
JS_FILE=$(find /usr/share/nginx/html/assets -name "index-*.js" | head -n 1)

if [ -z "$JS_FILE" ]; then
  echo "Cannot find main JavaScript file"
  exit 1
fi

# Create a runtime-config.js file with the dynamic API URL
cat > /usr/share/nginx/html/runtime-config.js << EOF
window.RUNTIME_CONFIG = {
  API_URL: window.location.protocol + "//" + window.location.hostname + ":5001"
};
EOF

echo "Runtime configuration injected: API URL will be determined by client connection"

# Start nginx
exec "$@"
