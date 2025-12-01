/**
 * MeGaOcToOoN GitHub App Sample
 * 
 * This script demonstrates how to authenticate as a GitHub App using Octokit.
 * It performs the following operations:
 * 1. Authenticate as the App (using JWT signed with private key)
 * 2. Call GET /app to retrieve App metadata
 * 3. List all installations of the App
 * 4. Create an installation access token
 * 5. List repositories visible to the installation
 * 
 * @author ELMOURABEA
 * @license MIT
 */

import 'dotenv/config';
import { Octokit } from "octokit";
import { createAppAuth } from "@octokit/auth-app";

/**
 * Normalize the private key by converting escaped newlines to actual newlines.
 * This handles the case where the PEM key is stored as a single line with \n literals.
 * @param {string} raw - The raw private key string
 * @returns {string} - The normalized private key with proper newlines
 */
function normalizePrivateKey(raw) {
  if (!raw) return raw;
  // If user pasted a single-line PEM with literal \n characters, convert them to real newlines.
  if (raw.includes('\\n')) {
    return raw.replace(/\\n/g, '\n');
  }
  return raw;
}

/**
 * Main function to demonstrate GitHub App authentication and API calls
 */
async function run() {
  const { APP_ID, PRIVATE_KEY, INSTALLATION_ID } = process.env;

  // Validate required environment variables
  if (!APP_ID || !PRIVATE_KEY) {
    console.error("❌ ERROR: APP_ID and PRIVATE_KEY must be set in your .env file");
    console.error("   See .env.example in this directory for setup instructions.");
    console.error("\n   Steps to configure (run from github-app-sample directory):");
    console.error("   1. Copy .env.example to .env");
    console.error("   2. Get your APP_ID from https://github.com/settings/apps/megaoctooon");
    console.error("   3. Download your private key from the GitHub App settings");
    console.error("   4. Add the private key to your .env file");
    process.exit(1);
  }

  const privateKey = normalizePrivateKey(PRIVATE_KEY);

  console.log("🐙 MeGaOcToOoN GitHub App Sample");
  console.log("================================\n");

  // Create Octokit instance authenticated as the App via JWT
  const octokit = new Octokit({
    authStrategy: createAppAuth,
    auth: {
      appId: APP_ID,
      privateKey,
    },
  });

  try {
    // =========================================================================
    // Step 1: Get App Metadata
    // =========================================================================
    console.log("📋 GET /app (App metadata)");
    console.log("----------------------------");
    const { data: app } = await octokit.request("GET /app", {
      headers: {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
      }
    });
    console.log(`   Name: ${app.name}`);
    console.log(`   ID: ${app.id}`);
    console.log(`   Slug: ${app.slug}`);
    console.log(`   Owner: ${app.owner?.login || 'N/A'}`);
    console.log(`   Description: ${app.description || 'No description'}`);
    console.log(`   External URL: ${app.external_url || 'N/A'}`);
    console.log(`   Installations: ${app.installations_count || 0}`);
    console.log("");

    // =========================================================================
    // Step 2: List Installations
    // =========================================================================
    console.log("📦 GET /app/installations (All installations)");
    console.log("----------------------------------------------");
    const { data: installations } = await octokit.request("GET /app/installations", {
      headers: {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
      }
    });

    if (!installations || installations.length === 0) {
      console.log("   ⚠️  No installations found for this app.");
      console.log("   Install the app to your account/organization at:");
      console.log(`   https://github.com/apps/${app.slug}/installations/new`);
      console.log("\n✅ Done (no installations to process)");
      return;
    }

    console.log(`   Found ${installations.length} installation(s):\n`);
    installations.forEach((inst, index) => {
      console.log(`   ${index + 1}. Installation ID: ${inst.id}`);
      console.log(`      Account: ${inst.account?.login || 'N/A'} (${inst.account?.type || 'unknown'})`);
      console.log(`      App Slug: ${inst.app_slug}`);
      console.log(`      Permissions: ${Object.keys(inst.permissions || {}).join(', ') || 'none'}`);
      console.log("");
    });

    // =========================================================================
    // Step 3: Create Installation Access Token
    // =========================================================================
    // Use provided INSTALLATION_ID or default to first installation
    const targetInstallationId = INSTALLATION_ID || installations[0].id;
    const targetInstallation = installations.find(i => String(i.id) === String(targetInstallationId)) || installations[0];

    console.log(`🔑 Creating installation access token for installation ${targetInstallationId}`);
    console.log(`   Account: ${targetInstallation.account?.login || 'N/A'}`);
    console.log("------------------------------------------------------");

    const { data: tokenData } = await octokit.request(
      "POST /app/installations/{installation_id}/access_tokens",
      {
        installation_id: parseInt(targetInstallationId, 10),
        headers: {
          "Accept": "application/vnd.github+json",
          "X-GitHub-Api-Version": "2022-11-28"
        }
      }
    );

    console.log(`   ✅ Token created successfully!`);
    console.log(`   Expires at: ${tokenData.expires_at}`);
    console.log(`   Permissions: ${Object.keys(tokenData.permissions || {}).join(', ')}`);
    // NOTE: We don't log the actual token for security reasons
    console.log("   (Token value hidden for security)\n");

    // =========================================================================
    // Step 4: Use Installation Token to List Repositories
    // =========================================================================
    console.log("📂 GET /installation/repositories (Visible repositories)");
    console.log("---------------------------------------------------------");

    // Create a new Octokit instance authenticated with the installation token
    const installationOctokit = new Octokit({ 
      auth: tokenData.token,
    });

    const { data: reposData } = await installationOctokit.request("GET /installation/repositories", {
      headers: {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
      },
      per_page: 10 // Limit to first 10 for demo
    });

    if (reposData.repositories.length === 0) {
      console.log("   No repositories accessible to this installation.");
    } else {
      console.log(`   Found ${reposData.total_count} total repositories (showing first ${reposData.repositories.length}):\n`);
      reposData.repositories.forEach((repo, index) => {
        console.log(`   ${index + 1}. ${repo.full_name}`);
        console.log(`      Private: ${repo.private}`);
        console.log(`      Default Branch: ${repo.default_branch}`);
        console.log("");
      });
    }

    console.log("✅ MeGaOcToOoN GitHub App authentication successful!");
    console.log("\n🎉 You can now use the installation token to make authenticated API calls.");
    console.log("   For more information, see: https://docs.github.com/en/apps");

  } catch (err) {
    console.error("\n❌ Error:", err.message || err);
    if (err.status) {
      console.error("   HTTP Status:", err.status);
    }
    // If API returned a body with details, print it (careful with tokens)
    if (err.response && err.response.data) {
      console.error("   Response:", JSON.stringify(err.response.data, null, 2));
    }
    console.error("\n   Common issues:");
    console.error("   - Invalid APP_ID: Check your GitHub App settings");
    console.error("   - Invalid private key: Ensure the PEM format is correct");
    console.error("   - App not installed: Install the app to your account first");
    process.exit(1);
  }
}

// Run the main function
run();
