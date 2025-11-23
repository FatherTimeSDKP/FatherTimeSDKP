# File: .devcontainer/post-create.sh

echo "Running SDKP Container Post-Create Setup..."

# Recommended: Use Hadolint to check the Dockerfile for best practices (Source 3.2)
# If you install Hadolint in your build stage:
# hadolint /home/vscode/SDKP_Project/Dockerfile

# Recommended: Run a quick security check on dependencies (Source 3.2)
# Ensure you install these tools in the 'build' stage of your Dockerfile
# grype /home/vscode/SDKP_Project/src
# trivy fs --scanners vuln,config /home/vscode/SDKP_Project

echo "Setting permissions on key directories..."
# Ensure core SDKP code directory has correct permissions
chmod -R 755 /home/vscode/SDKP_Project/src
echo "Setup complete. Welcome, FatherTimeSDKP."
