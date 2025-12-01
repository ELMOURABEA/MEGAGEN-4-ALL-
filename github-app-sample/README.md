# MeGaOcToOoN GitHub App Sample

This is a minimal Node.js example that demonstrates how to authenticate as the **MeGaOcToOoN** GitHub App using [Octokit](https://github.com/octokit/octokit.js) and [@octokit/auth-app](https://github.com/octokit/auth-app.js).

## 🔐 Security First

> **⚠️ IMPORTANT**: This sample does NOT include any private keys or secrets. You must configure your own credentials securely.

- **NEVER** commit your private key to version control
- **NEVER** share your private key with anyone
- Use GitHub Secrets for CI/CD environments
- Rotate your private key regularly

## ✨ Features

- ✅ Authenticate as a GitHub App using JWT
- ✅ Call `GET /app` to retrieve App metadata
- ✅ List all installations of the App
- ✅ Create installation access tokens
- ✅ List repositories visible to installations
- ✅ Auto-select first installation (or specify one)

## 📋 Prerequisites

- [Node.js](https://nodejs.org/) 18+ (or Node.js 16+ with experimental ESM)
- A GitHub App ([create one](https://github.com/settings/apps/new) or use existing [MeGaOcToOoN](https://github.com/settings/apps/megaoctooon))
- The App's private key (downloaded from App settings)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd github-app-sample
npm install
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your credentials
nano .env  # or use your favorite editor
```

### 3. Get Your Credentials

1. **APP_ID**: Go to [GitHub App Settings](https://github.com/settings/apps/megaoctooon) → Look for "App ID"
2. **PRIVATE_KEY**: 
   - Go to your App settings
   - Scroll to "Private keys"
   - Click "Generate a private key"
   - Download the `.pem` file
   - Copy its contents to your `.env` file

### 4. Run the Script

```bash
npm start
# or
node index.js
```

## 📁 Project Structure

```
github-app-sample/
├── package.json      # Node.js dependencies and scripts
├── index.js          # Main script - GitHub App authentication
├── .env.example      # Template for environment variables
├── README.md         # This file
└── INSTALL.md        # Public installation guide
```

## 📝 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `APP_ID` | ✅ Yes | Your GitHub App's numeric ID |
| `PRIVATE_KEY` | ✅ Yes | Your App's RSA private key (PEM format) |
| `INSTALLATION_ID` | ❌ No | Specific installation ID (auto-selects first if not set) |

### Private Key Format

You can store the private key in two ways:

**Option A: Multi-line (recommended for local development)**
```env
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
MIIEoAIBAAKCAQEA...
...more lines...
-----END RSA PRIVATE KEY-----"
```

**Option B: Single line with \n**
```env
PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----\nMIIEo...\n-----END RSA PRIVATE KEY-----"
```

## 🔧 How It Works

1. **JWT Authentication**: The script uses your private key to sign a JWT, which authenticates as the GitHub App itself.

2. **App API Calls**: With the JWT, you can call App-level endpoints like `GET /app` and `GET /app/installations`.

3. **Installation Token**: To access repository data, the script exchanges the JWT for an installation access token.

4. **Repository Access**: With the installation token, you can access repositories where the App is installed.

```
┌─────────────┐      JWT       ┌─────────────┐
│  Your App   │ ──────────────>│   GitHub    │
│  (Script)   │                │   App API   │
└─────────────┘                └─────────────┘
       │                              │
       │  Installation Token          │
       │<─────────────────────────────│
       │                              │
       │  Access Repos                │
       └─────────────────────────────>│
                                      └───────> Repositories
```

## 🛡️ Security Best Practices

1. **Store secrets securely**:
   - Use environment variables (never hardcode)
   - Use GitHub Secrets for Actions
   - Use a secrets manager for production

2. **Limit permissions**:
   - Only request permissions your App needs
   - Use installation tokens with minimum required scope

3. **Rotate keys**:
   - Generate new private keys periodically
   - Revoke old keys after rotation

4. **Monitor usage**:
   - Check your App's usage in GitHub settings
   - Set up alerts for unusual activity

## 🔗 Related Documentation

- [GitHub Apps Documentation](https://docs.github.com/en/apps)
- [Creating a GitHub App](https://docs.github.com/en/apps/creating-github-apps)
- [Authenticating as a GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/about-authentication-with-a-github-app)
- [Octokit.js](https://github.com/octokit/octokit.js)
- [@octokit/auth-app](https://github.com/octokit/auth-app.js)

## 📜 License

MIT License - see the [LICENSE](../LICENSE) file for details.

## 🤝 Support

- 📧 Email: support@megagent.app
- 💬 Issues: [GitHub Issues](https://github.com/ELMOURABEA/MeGaOcto/issues)
- 📚 Documentation: [Main README](../README.md)

---

**Part of [MeGaOcToOoN](https://github.com/ELMOURABEA/MeGaOcto)** - The Ultimate AI SuperAgent 🐙
