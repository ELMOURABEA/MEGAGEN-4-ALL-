# MeGaOcToOoN GitHub App

This module provides authentication and API access for the **MeGaOcToOoN** GitHub App. It allows you to:

- Authenticate as the GitHub App using a private key
- Get app metadata via `GET /app`
- List all app installations
- Create installation access tokens
- Access repositories as an installed app

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ installed
- A registered GitHub App (MeGaOcToOoN)
- Private key downloaded from GitHub App settings

### Installation

```bash
# Navigate to the github-app directory
cd github-app

# Install dependencies
npm install

# Copy and configure environment
cp .env.example .env
# Edit .env with your APP_ID and PRIVATE_KEY
```

### Configuration

1. **Get your App ID** from [GitHub App Settings](https://github.com/settings/apps/megaoctooon)

2. **Generate a Private Key**:
   - Go to your app's settings page
   - Scroll to "Private keys" section
   - Click "Generate a private key"
   - Download the `.pem` file

3. **Configure `.env`**:
```env
APP_ID=123456
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
YOUR_KEY_CONTENT_HERE
-----END RSA PRIVATE KEY-----"
```

### Running

```bash
# Authenticate and test the app
npm start

# Get installation help
npm run install-app
```

## 📖 How It Works

### Authentication Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Your Server   │     │  GitHub API     │     │   Target Repo   │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         │ 1. Sign JWT with      │                       │
         │    Private Key        │                       │
         │──────────────────────>│                       │
         │                       │                       │
         │ 2. GET /app           │                       │
         │   (Authenticated)     │                       │
         │<──────────────────────│                       │
         │                       │                       │
         │ 3. POST /app/         │                       │
         │    installations/     │                       │
         │    {id}/access_tokens │                       │
         │──────────────────────>│                       │
         │                       │                       │
         │ 4. Installation Token │                       │
         │<──────────────────────│                       │
         │                       │                       │
         │ 5. API calls with     │                       │
         │    installation token │                       │
         │───────────────────────────────────────────────>│
         │                       │                       │
```

### Scripts

| Script | Description |
|--------|-------------|
| `npm start` | Authenticate as the app and list installations |
| `npm run install-app` | Display installation instructions |
| `npm run install-app -- --open` | Open installation page in browser |

## 🔐 Security Best Practices

1. **Never commit `.env`** - It's in `.gitignore`
2. **Protect your private key** - Store it securely
3. **Rotate keys regularly** - Generate new keys periodically
4. **Use GitHub Secrets** - For CI/CD pipelines
5. **Minimal permissions** - Request only what you need

## 📱 Public Installation

Users can install MeGaOcToOoN from:

**https://github.com/apps/megaoctooon**

### For App Stores

When publishing to app stores (Google Play, App Store):

1. Users click "Install" in your mobile app
2. Open the GitHub installation URL in a browser
3. User authenticates and selects repositories
4. Callback redirects back to your app
5. Your app receives the installation ID

### Callback URLs

Configure these callback URLs in your GitHub App settings:

- **Web**: `https://megagent.app/oauth/callback`
- **Mobile**: `megagent://oauth/callback`
- **Development**: `http://localhost:8080/oauth/callback`

## 🧪 Testing

```bash
# Test authentication
npm start

# Expected output:
# ✅ App Name: MeGaOcToOoN
# ✅ Found X installation(s)
# ✅ Installation token created successfully!
```

## 📚 API Reference

### Get App Metadata

```javascript
import { Octokit } from "octokit";
import { createAppAuth } from "@octokit/auth-app";

const octokit = new Octokit({
  authStrategy: createAppAuth,
  auth: { appId: APP_ID, privateKey: PRIVATE_KEY }
});

const { data: app } = await octokit.request("GET /app");
console.log(app.name, app.id);
```

### List Installations

```javascript
const { data: installations } = await octokit.request("GET /app/installations");
installations.forEach(inst => {
  console.log(inst.id, inst.account.login);
});
```

### Create Installation Token

```javascript
const { data: tokenData } = await octokit.request(
  "POST /app/installations/{installation_id}/access_tokens",
  { installation_id: INSTALLATION_ID }
);
// Use tokenData.token for API calls
```

### Access Repositories

```javascript
const installationOctokit = new Octokit({ auth: tokenData.token });
const repos = await installationOctokit.request("GET /installation/repositories");
repos.data.repositories.forEach(repo => {
  console.log(repo.full_name);
});
```

## 🔗 Related Documentation

- [GitHub Apps Documentation](https://docs.github.com/en/apps)
- [Authenticating as a GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app)
- [Octokit.js Documentation](https://octokit.github.io/octokit.js/)
- [@octokit/auth-app](https://github.com/octokit/auth-app.js)

## 🆘 Troubleshooting

### "401 Unauthorized"
- Check that `APP_ID` is correct
- Verify private key is valid and not expired
- Ensure private key belongs to the correct app

### "404 Not Found"
- Verify the app exists on GitHub
- Check installation ID is valid

### "Private key not found"
- Ensure `.env` file exists with `PRIVATE_KEY`
- Check PEM format is correct (including headers)

## 📄 License

MIT License - See [LICENSE](../LICENSE) for details.

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

---

**Built with ❤️ by the MeGaOcToOoN Team**

For support: [GitHub Issues](https://github.com/ELMOURABEA/MeGaOcto/issues)
