# MEGAGENT SDK Integration Guide

Complete guide for integrating MEGAGENT into mobile apps, web apps, and third-party applications.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Platform-Specific Integration](#platform-specific-integration)
- [API Reference](#api-reference)
- [Authentication](#authentication)
- [Monetization Integration](#monetization-integration)
- [Examples](#examples)

## Overview

The MEGAGENT SDK provides a unified interface to integrate AI capabilities into your applications. It supports:
- Python applications (native)
- React Native (mobile apps)
- JavaScript/TypeScript (web apps)
- REST API (any platform)

## Installation

### Python SDK

```bash
# Install from PyPI (when published)
pip install megabot

# Or install from source
git clone https://github.com/ELMOURABEA/MEGAGEN-4-ALL-.git
cd MEGAGEN-4-ALL-
pip install -e .
```

### React Native SDK

```bash
npm install @megagent/react-native-sdk
# or
yarn add @megagent/react-native-sdk
```

### JavaScript/Web SDK

```bash
npm install @megagent/web-sdk
# or
yarn add @megagent/web-sdk
```

## Platform-Specific Integration

### Android Integration

#### 1. Add Dependencies

**build.gradle (app level)**:
```gradle
dependencies {
    implementation 'com.megagent:sdk:2.0.0'
    implementation 'com.google.android.gms:play-services-ads:22.0.0' // For AdMob
}
```

#### 2. AndroidManifest.xml

```xml
<manifest>
    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET"/>
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    
    <application>
        <!-- AdMob App ID -->
        <meta-data
            android:name="com.google.android.gms.ads.APPLICATION_ID"
            android:value="${ADMOB_APP_ID}"/>
        
        <!-- Deep linking for OAuth -->
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.VIEW"/>
                <category android:name="android.intent.category.DEFAULT"/>
                <category android:name="android.intent.category.BROWSABLE"/>
                <data
                    android:scheme="megagent"
                    android:host="oauth"/>
            </intent-filter>
        </activity>
    </application>
</manifest>
```

#### 3. Initialize SDK

```kotlin
// MainActivity.kt
import com.megagent.sdk.MegaBot
import com.megagent.sdk.Config

class MainActivity : AppCompatActivity() {
    private lateinit var megaBot: MegaBot
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Initialize MEGAGENT
        val config = Config.Builder()
            .setApiKey("your-api-key")
            .setSubscriptionTier("pro")
            .setDebugMode(BuildConfig.DEBUG)
            .build()
        
        megaBot = MegaBot(config)
        megaBot.start()
    }
    
    override fun onDestroy() {
        super.onDestroy()
        megaBot.stop()
    }
}
```

### iOS Integration

#### 1. Add Dependencies

**Podfile**:
```ruby
platform :ios, '14.0'

target 'MEGAGENT' do
  use_frameworks!
  
  # MEGAGENT SDK
  pod 'MEGAGENT', '~> 2.0.0'
  
  # Google AdMob
  pod 'Google-Mobile-Ads-SDK'
end
```

Then run:
```bash
pod install
```

#### 2. Info.plist Configuration

```xml
<dict>
    <!-- AdMob App ID -->
    <key>GADApplicationIdentifier</key>
    <string>${ADMOB_APP_ID}</string>
    
    <!-- URL Schemes for OAuth -->
    <key>CFBundleURLTypes</key>
    <array>
        <dict>
            <key>CFBundleURLSchemes</key>
            <array>
                <string>megagent</string>
            </array>
        </dict>
    </array>
    
    <!-- App Transport Security -->
    <key>NSAppTransportSecurity</key>
    <dict>
        <key>NSAllowsArbitraryLoads</key>
        <false/>
    </dict>
</dict>
```

#### 3. Initialize SDK

```swift
// AppDelegate.swift
import UIKit
import MEGAGENT

@main
class AppDelegate: UIResponder, UIApplicationDelegate {
    var megaBot: MegaBot?
    
    func application(_ application: UIApplication,
                    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        
        // Initialize MEGAGENT
        let config = MEGAGENTConfig(
            apiKey: "your-api-key",
            subscriptionTier: .pro,
            debugMode: true
        )
        
        megaBot = MegaBot(config: config)
        megaBot?.start()
        
        return true
    }
    
    func applicationWillTerminate(_ application: UIApplication) {
        megaBot?.stop()
    }
}
```

### React Native Integration

```javascript
// App.js
import React, { useEffect } from 'react';
import { MegaBot, SubscriptionTier } from '@megagent/react-native-sdk';

const App = () => {
  useEffect(() => {
    // Initialize MEGAGENT
    MegaBot.initialize({
      apiKey: 'your-api-key',
      subscriptionTier: SubscriptionTier.PRO,
      debugMode: __DEV__,
    });
    
    return () => {
      MegaBot.shutdown();
    };
  }, []);
  
  const handleQuery = async () => {
    const result = await MegaBot.query('What is AI?');
    console.log(result);
  };
  
  return (
    <View>
      <Button title="Query AI" onPress={handleQuery} />
    </View>
  );
};

export default App;
```

### Web Integration

```javascript
// index.js
import { MegaBot } from '@megagent/web-sdk';

// Initialize
const megaBot = new MegaBot({
  apiKey: 'your-api-key',
  subscriptionTier: 'pro',
  debugMode: process.env.NODE_ENV === 'development'
});

// Start the bot
await megaBot.start();

// Make a query
const result = await megaBot.query('Explain machine learning');
console.log(result);

// Research
const research = await megaBot.research('quantum computing', 'deep');
console.log(research);

// Cleanup
await megaBot.stop();
```

## API Reference

### Core Methods

#### `MegaBot.initialize(config)`
Initialize the MEGAGENT SDK.

**Parameters:**
- `config` (Object): Configuration object
  - `apiKey` (string): Your MEGAGENT API key
  - `subscriptionTier` (string): 'free', 'pro', or 'enterprise'
  - `debugMode` (boolean): Enable debug logging

#### `MegaBot.query(prompt, context?)`
Query all AI platforms.

**Parameters:**
- `prompt` (string): Query text
- `context` (Object, optional): Additional context

**Returns:** Promise<QueryResult>

#### `MegaBot.research(topic, depth)`
Perform deep research.

**Parameters:**
- `topic` (string): Research topic
- `depth` (string): 'shallow', 'medium', or 'deep'

**Returns:** Promise<ResearchResult>

#### `MegaBot.getStatus()`
Get current status.

**Returns:** Object with status information

### Monetization API

#### `MonetizationManager.checkTier()`
Check current subscription tier.

**Returns:** Object with tier information

#### `MonetizationManager.canQuery()`
Check if user can make a query.

**Returns:** `{allowed: boolean, reason?: string}`

#### `MonetizationManager.upgradePrompt()`
Show upgrade prompt UI.

### Advertising API

#### `AdvertisingCore.showBanner(position)`
Show banner ad.

**Parameters:**
- `position` (string): 'top' or 'bottom'

#### `AdvertisingCore.showInterstitial()`
Show interstitial ad.

#### `AdvertisingCore.showRewarded(rewardType)`
Show rewarded ad.

**Parameters:**
- `rewardType` (string): Type of reward

## Authentication

### OAuth Flow

```javascript
// Initialize OAuth
const oauth = new GitHubOAuth({
  clientId: 'your-client-id',
  redirectUri: 'megagent://oauth/callback'
});

// Start OAuth flow
const authUrl = oauth.getAuthorizationUrl();
// Open authUrl in browser

// Handle callback
oauth.handleCallback(callbackUrl)
  .then(tokens => {
    console.log('Access token:', tokens.accessToken);
  });
```

## Monetization Integration

### Subscription Management

```javascript
// Check subscription status
const tierInfo = megaBot.monetization.getTierInfo();
console.log('Current tier:', tierInfo.tier);
console.log('Queries today:', tierInfo.usage.queries_today);

// Check if action is allowed
const [canQuery, reason] = megaBot.monetization.canQuery();
if (!canQuery) {
  console.log('Cannot query:', reason);
  // Show upgrade prompt
}
```

### Payment Processing

```javascript
import { PaymentProcessor, PaymentMethod } from '@megagent/sdk';

const processor = new PaymentProcessor({
  stripeApiKey: 'your-stripe-key'
});

// Create payment intent
const payment = await processor.createPaymentIntent(
  9.99,
  'usd',
  PaymentMethod.STRIPE,
  { user_id: 'user123', subscription_tier: 'pro' }
);

console.log('Payment URL:', payment.payment_url);
```

### AdMob Integration

```javascript
// Initialize advertising
megaBot.advertising.initialize();

// Show banner ad
megaBot.advertising.showBanner('bottom');

// Show rewarded ad for bonus queries
const result = await megaBot.advertising.showRewarded('bonus_queries');
if (result.status === 'success') {
  console.log('User earned:', result.reward.description);
}
```

## Examples

### Example 1: Simple Query App

```javascript
import { MegaBot } from '@megagent/sdk';

async function main() {
  const bot = new MegaBot({ apiKey: 'your-key' });
  await bot.start();
  
  const result = await bot.query('What is the future of AI?');
  console.log('AI Response:', result);
  
  await bot.stop();
}

main();
```

### Example 2: Research Dashboard

```javascript
import { MegaBot } from '@megagent/sdk';

class ResearchDashboard {
  constructor() {
    this.bot = new MegaBot({
      apiKey: 'your-key',
      subscriptionTier: 'pro'
    });
  }
  
  async initialize() {
    await this.bot.start();
  }
  
  async performResearch(topic) {
    // Check if user can research
    const [canResearch, reason] = this.bot.monetization.canResearch('deep');
    if (!canResearch) {
      throw new Error(reason);
    }
    
    // Perform research
    const result = await this.bot.research(topic, 'deep');
    
    // Record usage
    this.bot.monetization.recordResearch();
    
    return result;
  }
}
```

### Example 3: Mobile App with Ads

```javascript
import React, { useState, useEffect } from 'react';
import { MegaBot } from '@megagent/react-native-sdk';

function AIQueryScreen() {
  const [result, setResult] = useState(null);
  
  useEffect(() => {
    // Show banner ad
    MegaBot.advertising.showBanner('bottom');
  }, []);
  
  const handleQuery = async (prompt) => {
    // Check tier limits
    const [canQuery, reason] = MegaBot.monetization.canQuery();
    
    if (!canQuery) {
      // Offer to watch rewarded ad for bonus queries
      const adResult = await MegaBot.advertising.showRewarded('bonus_queries');
      if (adResult.status === 'success') {
        // User earned bonus queries, try again
        return handleQuery(prompt);
      } else {
        alert(reason);
        return;
      }
    }
    
    // Perform query
    const result = await MegaBot.query(prompt);
    setResult(result);
    
    // Record usage
    MegaBot.monetization.recordQuery();
  };
  
  return (
    <View>
      <TextInput placeholder="Enter your query" />
      <Button title="Query" onPress={() => handleQuery(inputValue)} />
      {result && <Text>{JSON.stringify(result)}</Text>}
    </View>
  );
}
```

## Environment Configuration

Create a `.env` file for your application:

```bash
# MEGAGENT Configuration
MEGAGENT_API_KEY=your-api-key-here
MEGAGENT_DEBUG=true

# Subscription
MEGAGENT_TIER=pro

# AdMob (optional)
ADMOB_APP_ID=ca-app-pub-xxxxxxxxxxxxxxxx~xxxxxxxxxx
ADMOB_BANNER_ID=ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx
ADMOB_INTERSTITIAL_ID=ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx
ADMOB_REWARDED_ID=ca-app-pub-xxxxxxxxxxxxxxxx/xxxxxxxxxx

# Payment (optional)
STRIPE_API_KEY=your-stripe-test-key-here
BITCOIN_ADDRESS=your-bitcoin-address-here
DOGECOIN_ADDRESS=your-dogecoin-address-here
```

## Best Practices

1. **API Key Security**: Never commit API keys to version control
2. **Error Handling**: Always handle errors and provide user feedback
3. **Tier Limits**: Check tier limits before making API calls
4. **Caching**: Use built-in caching for better performance
5. **Debug Mode**: Enable debug mode during development
6. **Testing**: Test with different subscription tiers
7. **Monetization**: Implement proper paywall UI for upgrades

## Troubleshooting

### Common Issues

**Issue: "API key not valid"**
- Ensure your API key is correctly configured
- Check if the key is activated in your account

**Issue: "Tier limit exceeded"**
- User has reached their tier limit
- Prompt user to upgrade or wait for reset

**Issue: "AdMob ads not showing"**
- Verify AdMob IDs are correct
- Check if ads are enabled in your region
- Test with test ad units first

## Support

- Documentation: https://github.com/ELMOURABEA/MEGAGEN-4-ALL-
- Issues: https://github.com/ELMOURABEA/MEGAGEN-4-ALL-/issues
- Email: support@megagent.app

## License

MIT License - See LICENSE file for details
