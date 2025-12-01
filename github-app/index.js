/**
 * MeGaOcToOoN GitHub App Authentication Script
 * 
 * This script authenticates as the GitHub App, calls GET /app to retrieve
 * app metadata, lists installations, and creates installation access tokens.
 * 
 * @author ELMOURABEA
 * @license MIT
 * @see https://github.com/ELMOURABEA/MeGaOcto
 */

import 'dotenv/config';
import { Octokit } from "octokit";
import { createAppAuth } from "@octokit/auth-app";

/**
 * Normalizes and validates private key format
 * @param {string} raw - The raw private key string
 * @returns {string} - The normalized private key
 * @throws {Error} - If the key format is invalid
 */
function normalizePrivateKey(raw) {
  if (!raw) return raw;
  
  // Convert escaped newlines to actual newlines
  let key = raw;
  if (key.includes('\\n')) {
    key = key.replace(/\\n/g, '\n');
  }
  
  // Validate PEM format
  const pemHeaderRegex = /-----BEGIN (RSA |EC )?PRIVATE KEY-----/;
  const pemFooterRegex = /-----END (RSA |EC )?PRIVATE KEY-----/;
  
  if (!pemHeaderRegex.test(key)) {
    throw new Error('Invalid private key: Missing PEM header (-----BEGIN PRIVATE KEY-----)');
  }
  if (!pemFooterRegex.test(key)) {
    throw new Error('Invalid private key: Missing PEM footer (-----END PRIVATE KEY-----)');
  }
  
  return key;
}

/**
 * Main execution function
 * Authenticates as the GitHub App and performs operations
 */
async function run() {
  const { APP_ID, PRIVATE_KEY, INSTALLATION_ID } = process.env;

  // Validate required environment variables
  if (!APP_ID || !PRIVATE_KEY) {
    console.error("❌ ERROR: APP_ID and PRIVATE_KEY must be set");
    console.error("   See .env.example for configuration details");
    console.error("   Download private key from: https://github.com/settings/apps/megaoctooon");
    process.exit(1);
  }

  const privateKey = normalizePrivateKey(PRIVATE_KEY);

  // Create Octokit instance authenticated as the App via JWT
  const octokit = new Octokit({
    authStrategy: createAppAuth,
    auth: {
      appId: APP_ID,
      privateKey,
    },
  });

  try {
    // ==========================================
    // Step 1: Get App Metadata
    // ==========================================
    console.log("🔍 === GET /app (App Metadata) ===\n");
    const { data: app } = await octokit.request("GET /app", {
      headers: {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
      }
    });
    
    console.log(`✅ App Name: ${app.name}`);
    console.log(`   App ID: ${app.id}`);
    console.log(`   Slug: ${app.slug}`);
    console.log(`   Owner: ${app.owner?.login || 'N/A'}`);
    console.log(`   Description: ${app.description || 'N/A'}`);
    console.log(`   External URL: ${app.external_url || 'N/A'}`);
    console.log(`   HTML URL: ${app.html_url}`);
    console.log(`   Created: ${app.created_at}`);
    console.log(`   Updated: ${app.updated_at}`);
    console.log(`   Installations: ${app.installations_count || 0}`);

    // ==========================================
    // Step 2: List Installations
    // ==========================================
    console.log("\n📋 === GET /app/installations (App Installations) ===\n");
    const { data: installations } = await octokit.request("GET /app/installations", {
      headers: {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
      }
    });
    
    if (!installations || installations.length === 0) {
      console.log("⚠️  No installations found for this app.");
      console.log("   Users can install from: https://github.com/apps/megaoctooon");
      return;
    }
    
    console.log(`✅ Found ${installations.length} installation(s):\n`);
    installations.forEach((inst, index) => {
      console.log(`   ${index + 1}. Installation ID: ${inst.id}`);
      console.log(`      Account: ${inst.account?.login || 'N/A'} (${inst.account?.type || 'N/A'})`);
      console.log(`      App Slug: ${inst.app_slug}`);
      console.log(`      Target Type: ${inst.target_type}`);
      console.log(`      Permissions: ${Object.keys(inst.permissions || {}).join(', ')}`);
      console.log(`      Events: ${(inst.events || []).slice(0, 5).join(', ')}${inst.events?.length > 5 ? '...' : ''}`);
      console.log('');
    });

    // ==========================================
    // Step 3: Create Installation Access Token
    // ==========================================
    const installationId = INSTALLATION_ID || installations[0]?.id;
    
    if (!installationId) {
      console.log("⚠️  No installation ID available.");
      console.log("   Set INSTALLATION_ID in .env or install the app first.");
      return;
    }

    console.log(`🔑 === Creating Installation Access Token (Installation: ${installationId}) ===\n`);

    const { data: tokenData } = await octokit.request(
      "POST /app/installations/{installation_id}/access_tokens",
      { 
        installation_id: Number(installationId),
        headers: {
          "Accept": "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28"
        }
      }
    );
    
    console.log(`✅ Installation token created successfully!`);
    console.log(`   Expires at: ${tokenData.expires_at}`);
    console.log(`   Permissions: ${Object.keys(tokenData.permissions || {}).join(', ')}`);
    console.log(`   Repository selection: ${tokenData.repository_selection}`);
    // NOTE: For security, we do NOT log the actual token

    // ==========================================
    // Step 4: Use Token to List Repositories
    // ==========================================
    console.log("\n📂 === Repositories Accessible to Installation ===\n");

    // Create new Octokit instance with installation token
    const installationOctokit = new Octokit({ auth: tokenData.token });
    
    const repos = await installationOctokit.request("GET /installation/repositories", {
      headers: {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
      }
    });
    
    // Clear sensitive token from memory after use
    const tokenExpiry = tokenData.expires_at;
    tokenData.token = null;
    
    if (repos.data.repositories.length === 0) {
      console.log("   No repositories accessible to this installation.");
    } else {
      console.log(`✅ Found ${repos.data.total_count} accessible repository(ies):\n`);
      repos.data.repositories.forEach((repo, index) => {
        console.log(`   ${index + 1}. ${repo.full_name}`);
        console.log(`      Private: ${repo.private}`);
        console.log(`      Default Branch: ${repo.default_branch}`);
        console.log('');
      });
    }

    // ==========================================
    // Success Summary
    // ==========================================
    console.log("═".repeat(50));
    console.log("🎉 GitHub App authentication successful!");
    console.log("═".repeat(50));
    console.log("\n📌 Quick Reference:");
    console.log(`   App Install URL: https://github.com/apps/${app.slug}`);
    console.log(`   Settings URL: https://github.com/settings/apps/${app.slug}`);
    console.log(`   Token expires at: ${tokenExpiry}`);
    console.log("\n💡 Next Steps:");
    console.log("   1. Use the installation token to make API calls");
    console.log("   2. Set up webhooks to receive events");
    console.log("   3. Implement your app logic");
    console.log("\n📚 Documentation: https://docs.github.com/en/apps");

  } catch (err) {
    console.error("\n❌ Error:", err.message || err);
    if (err.status) console.error("   HTTP Status:", err.status);
    
    // Provide helpful error messages
    if (err.status === 401) {
      console.error("\n💡 Authentication failed. Check:");
      console.error("   - APP_ID is correct");
      console.error("   - PRIVATE_KEY is valid and not expired");
      console.error("   - Private key belongs to the correct app");
    } else if (err.status === 404) {
      console.error("\n💡 Resource not found. Check:");
      console.error("   - App exists at GitHub");
      console.error("   - Installation ID is valid");
    }
    
    if (err.response?.data) {
      console.error("   Response data:", JSON.stringify(err.response.data, null, 2));
    }
    process.exit(1);
  }
}

// Execute the main function
run();
