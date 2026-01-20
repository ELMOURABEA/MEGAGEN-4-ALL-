/**
 * MeGaOcToOoN GitHub App - Auto Installation Script
 * 
 * This script helps users install the MeGaOcToOoN GitHub App to their
 * repositories by opening the installation URL and handling the callback.
 * 
 * @author ELMOURABEA
 * @license MIT
 * @see https://github.com/ELMOURABEA/MeGaOcto
 */

import 'dotenv/config';
import { exec } from 'child_process';

/**
 * Configuration for the GitHub App
 */
const APP_CONFIG = {
  // GitHub App slug (from the app URL)
  slug: 'megaoctooon',
  
  // Installation URL where users will be redirected
  installUrl: 'https://github.com/apps/megaoctooon/installations/new',
  
  // Callback URL after installation (configured in GitHub App settings)
  callbackUrl: process.env.CALLBACK_URL || 'http://localhost:8080/oauth/callback',
  
  // App permissions (for display purposes)
  permissions: {
    actions: 'write',
    checks: 'write',
    contents: 'write',
    deployments: 'write',
    issues: 'write',
    metadata: 'read',
    packages: 'write',
    pull_requests: 'write',
    repository_hooks: 'write',
    statuses: 'write',
    workflows: 'write'
  },
  
  // Events the app subscribes to
  events: [
    'push',
    'pull_request',
    'issues',
    'issue_comment',
    'check_run',
    'check_suite',
    'workflow_run',
    'workflow_job'
  ]
};

/**
 * Display installation instructions
 */
function displayInstructions() {
  console.log('\n' + '═'.repeat(60));
  console.log('🐙 MeGaOcToOoN GitHub App - Installation Guide');
  console.log('═'.repeat(60));
  
  console.log('\n📋 About This App:');
  console.log('   MeGaOcToOoN is the Ultimate 10-in-1 AI SuperAgent that');
  console.log('   integrates GitHub Copilot, Gemini, ChatGPT, and Grok');
  console.log('   for comprehensive research and automation.');
  
  console.log('\n🔐 Permissions Requested:');
  Object.entries(APP_CONFIG.permissions).forEach(([perm, access]) => {
    console.log(`   • ${perm}: ${access}`);
  });
  
  console.log('\n📬 Events Subscribed:');
  APP_CONFIG.events.forEach(event => {
    console.log(`   • ${event}`);
  });
  
  console.log('\n🚀 Installation Steps:');
  console.log('');
  console.log('   Step 1: Open the installation URL in your browser:');
  console.log(`   ${APP_CONFIG.installUrl}`);
  console.log('');
  console.log('   Step 2: Select the account/organization to install to');
  console.log('');
  console.log('   Step 3: Choose repositories:');
  console.log('   • "All repositories" - Access all repos in the account');
  console.log('   • "Only select repositories" - Choose specific repos');
  console.log('');
  console.log('   Step 4: Review permissions and click "Install"');
  console.log('');
  console.log('   Step 5: After installation, you will be redirected to:');
  console.log(`   ${APP_CONFIG.callbackUrl}`);
  
  console.log('\n💡 After Installation:');
  console.log('   1. Run `npm start` to verify the installation');
  console.log('   2. The script will show your installation ID');
  console.log('   3. Use the installation token to make API calls');
  
  console.log('\n📚 Additional Resources:');
  console.log(`   • App Page: https://github.com/apps/${APP_CONFIG.slug}`);
  console.log('   • Documentation: https://github.com/ELMOURABEA/MeGaOcto');
  console.log('   • Support: https://github.com/ELMOURABEA/MeGaOcto/issues');
  
  console.log('\n' + '═'.repeat(60));
  console.log('🔗 Quick Install Link:');
  console.log(`   ${APP_CONFIG.installUrl}`);
  console.log('═'.repeat(60) + '\n');
}

/**
 * Check if running in a browser-capable environment and open URL
 */
function openInstallUrl() {
  const installUrl = APP_CONFIG.installUrl;
  
  console.log('\n🌐 Opening installation page in your browser...\n');
  
  const platform = process.platform;
  
  let command;
  if (platform === 'darwin') {
    command = `open "${installUrl}"`;
  } else if (platform === 'win32') {
    command = `start "" "${installUrl}"`;
  } else {
    command = `xdg-open "${installUrl}"`;
  }
  
  exec(command, (error) => {
    if (error) {
      console.log('⚠️  Could not open browser automatically.');
      console.log('   Please open this URL manually:\n');
      console.log(`   ${installUrl}\n`);
    } else {
      console.log('✅ Browser opened! Complete the installation in your browser.\n');
    }
  });
}

/**
 * Main function
 */
function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    displayInstructions();
    return;
  }
  
  if (args.includes('--open') || args.includes('-o')) {
    openInstallUrl();
    return;
  }
  
  // Default: show instructions
  displayInstructions();
  
  // Ask if user wants to open the installation page
  console.log('Would you like to open the installation page now?');
  console.log('Run: npm run install-app -- --open\n');
}

// Execute
main();
