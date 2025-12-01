# Installing MeGaOcToOoN GitHub App

This guide explains how to install the MeGaOcToOoN GitHub App on your repositories.

## 🌟 For Public Users (Easy One-Click Install)

### Step 1: Visit the App Page

Go to the MeGaOcToOoN GitHub App installation page:

```
https://github.com/apps/megaoctooon/installations/new
```

### Step 2: Select Account/Organization

Choose where to install the app:
- Your personal account
- An organization you own or have admin access to

### Step 3: Select Repositories

Choose which repositories the app can access:
- **All repositories**: The app can access all current and future repositories
- **Only select repositories**: Choose specific repositories

### Step 4: Review Permissions

The app will request these permissions:
- ✅ **Contents**: Read and write (for code analysis)
- ✅ **Pull Requests**: Read and write (for PR automation)
- ✅ **Issues**: Read and write (for issue management)
- ✅ **Actions**: Read and write (for workflow automation)
- ✅ **Metadata**: Read (required for all apps)

### Step 5: Authorize

Click **Install** to complete the installation!

---

## 🔧 For Developers (Advanced)

### Using the Manifest Flow

If you want to create your own instance of the app:

1. **Fork the Repository**
   ```bash
   git clone https://github.com/ELMOURABEA/MeGaOcto.git
   cd MeGaOcto
   ```

2. **Create a GitHub App from Manifest**
   - Visit: `https://github.com/settings/apps/new?manifest=true`
   - Or use the manifest file in this repo: `github_app_manifest.json`

3. **Configure Your App**
   - Set your webhook URL
   - Download your private key
   - Note your App ID

4. **Run the Sample Script**
   ```bash
   cd github-app-sample
   npm install
   cp .env.example .env
   # Add your APP_ID and PRIVATE_KEY to .env
   npm start
   ```

### Programmatic Installation

For automated installation flows:

```javascript
// Redirect user to install the app
const installUrl = `https://github.com/apps/megaoctooon/installations/new`;
window.location.href = installUrl;

// After installation, GitHub redirects to your callback URL with:
// - installation_id: The new installation ID
// - setup_action: "install" or "update"
```

---

## 📱 Platform-Specific Installation

### Web Application

The web app handles GitHub OAuth automatically:
1. Click "Sign in with GitHub"
2. Authorize the application
3. The app will be installed automatically

### Mobile Apps (iOS/Android)

1. Download from App Store / Google Play
2. Open the app and tap "Connect GitHub"
3. Sign in with your GitHub account
4. Select repositories to authorize

### Desktop Apps (Windows/macOS/Linux)

1. Download from [GitHub Releases](https://github.com/ELMOURABEA/MeGaOcto/releases)
2. Install and launch
3. Click "Connect to GitHub"
4. Complete the OAuth flow in your browser

---

## 🔒 Security Notes

### What the App CAN Do:
- Read and analyze your code
- Create issues and pull requests
- Run automated workflows
- Comment on PRs and issues

### What the App CANNOT Do:
- Access your email or personal data
- Access repositories not authorized
- Make changes without your permission
- Share your code with third parties

### Revoking Access

You can revoke the app's access at any time:
1. Go to [GitHub Settings > Applications](https://github.com/settings/installations)
2. Find MeGaOcToOoN
3. Click "Configure" then "Suspend" or "Uninstall"

---

## 🆘 Troubleshooting

### "Installation failed"

- Ensure you have admin access to the repository/organization
- Check if the app is already installed
- Try refreshing the page and installing again

### "Permission denied"

- The app may not have access to that repository
- Reconfigure the app to include the repository

### "Rate limit exceeded"

- Wait a few minutes and try again
- The app respects GitHub's rate limits

---

## 📞 Support

Need help? Reach out:

- 📧 Email: support@megagent.app
- 💬 GitHub Issues: [Create an issue](https://github.com/ELMOURABEA/MeGaOcto/issues/new)
- 📖 Documentation: [Full docs](https://github.com/ELMOURABEA/MeGaOcto#readme)

---

## 🎉 After Installation

Once installed, you can:

1. **Use in GitHub Actions**
   ```yaml
   - name: Run MeGaOcToOoN
     uses: ELMOURABEA/MeGaOcto@v1
     with:
       mode: 'query'
       prompt: 'Analyze this code'
   ```

2. **Use the API**
   ```javascript
   const response = await fetch('https://megagent.app/api/analyze', {
     method: 'POST',
     headers: {
       'Authorization': `Bearer ${installation_token}`,
       'Content-Type': 'application/json'
     },
     body: JSON.stringify({ repo: 'owner/repo' })
   });
   ```

3. **Use the Dashboard**
   - Visit [megagent.app](https://megagent.app)
   - Sign in with GitHub
   - Access all your connected repositories

---

**Welcome to MeGaOcToOoN!** 🐙✨
