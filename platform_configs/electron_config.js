/**
 * Electron Configuration for Desktop Apps
 * Windows, macOS, Linux (Ubuntu) support
 */
module.exports = {
  appId: 'com.megagent.octogen',
  productName: 'MEGAGENT OCTOGEN',
  copyright: 'Copyright © 2025 MEGAGENT Team',
  
  // Directories
  directories: {
    output: 'dist',
    buildResources: 'build'
  },
  
  // Files to include
  files: [
    'build/**/*',
    'node_modules/**/*',
    'package.json'
  ],
  
  // Windows configuration
  win: {
    target: [
      {
        target: 'nsis',
        arch: ['x64', 'arm64']
      },
      {
        target: 'portable',
        arch: ['x64']
      }
    ],
    icon: 'build/icon.ico',
    publisherName: 'MEGAGENT Team',
    verifyUpdateCodeSignature: false
  },
  
  nsis: {
    oneClick: false,
    perMachine: false,
    allowToChangeInstallationDirectory: true,
    deleteAppDataOnUninstall: true,
    createDesktopShortcut: true,
    createStartMenuShortcut: true,
    shortcutName: 'MEGAGENT OCTOGEN'
  },
  
  // macOS configuration
  mac: {
    target: [
      {
        target: 'dmg',
        arch: ['x64', 'arm64']
      },
      {
        target: 'zip',
        arch: ['x64', 'arm64']
      }
    ],
    icon: 'build/icon.icns',
    category: 'public.app-category.developer-tools',
    hardenedRuntime: true,
    gatekeeperAssess: false,
    entitlements: 'build/entitlements.mac.plist',
    entitlementsInherit: 'build/entitlements.mac.plist',
    notarize: false
  },
  
  dmg: {
    contents: [
      {
        x: 130,
        y: 220
      },
      {
        x: 410,
        y: 220,
        type: 'link',
        path: '/Applications'
      }
    ],
    window: {
      width: 540,
      height: 380
    }
  },
  
  // Linux configuration
  linux: {
    target: [
      {
        target: 'AppImage',
        arch: ['x64', 'arm64']
      },
      {
        target: 'deb',
        arch: ['x64', 'arm64']
      },
      {
        target: 'rpm',
        arch: ['x64', 'arm64']
      },
      {
        target: 'snap',
        arch: ['x64']
      }
    ],
    icon: 'build/icons',
    category: 'Development',
    vendor: 'MEGAGENT Team',
    maintainer: 'MEGAGENT Team <megagent@example.com>',
    synopsis: 'The Ultimate 10-in-1 AI SuperAgent',
    description: 'MEGAGENT OCTOGEN - Unified AI agent with OAuth integration'
  },
  
  // Snap specific config
  snap: {
    confinement: 'classic',
    grade: 'stable',
    summary: 'The Ultimate 10-in-1 AI SuperAgent'
  },
  
  // Auto-update configuration
  publish: {
    provider: 'github',
    owner: 'ELMOURABEA',
    repo: 'MEGAGENT',
    releaseType: 'release'
  }
};
