# MEGAGENT Mobile App Setup Guide

This guide explains how to build and run the MEGAGENT application on iOS and Android devices.

## Overview

MEGAGENT is built using:
- **React** for the UI
- **Vite** for fast development and building
- **Capacitor** for native mobile capabilities
- **Supabase** for database and authentication

## Prerequisites

### For Both Platforms
- Node.js 18+ installed
- Git installed

### For Android
- Android Studio installed
- Java Development Kit (JDK) 17+
- Android SDK installed via Android Studio

### For iOS (macOS only)
- Xcode 14+ installed
- CocoaPods installed (`sudo gem install cocoapods`)
- Valid Apple Developer account for device deployment

## Initial Setup

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Build the Web App**
   ```bash
   npm run build
   ```

3. **Add Mobile Platforms** (First time only)
   ```bash
   # Add Android
   npx cap add android

   # Add iOS (macOS only)
   npx cap add ios
   ```

## Building for Android

1. **Build and Open Android Studio**
   ```bash
   npm run android
   ```

2. **In Android Studio:**
   - Wait for Gradle sync to complete
   - Connect an Android device or start an emulator
   - Click the "Run" button (green play icon)

3. **Alternative: Build APK**
   - In Android Studio: Build > Build Bundle(s) / APK(s) > Build APK(s)
   - APK will be in: `android/app/build/outputs/apk/debug/`

## Building for iOS

1. **Build and Open Xcode** (macOS only)
   ```bash
   npm run ios
   ```

2. **In Xcode:**
   - Select your development team in Signing & Capabilities
   - Select a target device (simulator or physical device)
   - Click the "Run" button (play icon)

3. **For Physical Device:**
   - Connect your iOS device via USB
   - Trust the computer on your device
   - Select the device in Xcode
   - Build and run

## Development Workflow

### Making Changes

1. **Update Web Code**
   - Modify React components in `src/`
   - Test in web browser: `npm run dev`

2. **Sync to Mobile**
   ```bash
   npm run build
   npx cap sync
   ```

3. **Rebuild Mobile App**
   - Reopen in Android Studio or Xcode
   - Run the app again

### Quick Sync Commands

```bash
# Sync all platforms
npx cap sync

# Sync specific platform
npx cap sync android
npx cap sync ios

# Update native dependencies
npx cap update
```

## Configuration

### App Info
Edit `capacitor.config.json`:
```json
{
  "appId": "com.megagent.app",
  "appName": "MEGAGENT",
  "webDir": "dist"
}
```

### Android Specific
- Minimum SDK: 22 (Android 5.1)
- Target SDK: 34 (Android 14)
- Edit: `android/app/build.gradle`

### iOS Specific
- Minimum iOS version: 13.0
- Edit: `ios/App/App/Info.plist`

## Environment Variables

Create `.env` file with:
```
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

These are automatically included in the build.

## Permissions

### Android Permissions
Edit `android/app/src/main/AndroidManifest.xml`:
```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

### iOS Permissions
Edit `ios/App/App/Info.plist`:
```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

## Troubleshooting

### Android Issues

**Gradle Sync Failed:**
- Open Android Studio: File > Sync Project with Gradle Files
- Clean build: Build > Clean Project

**App Won't Install:**
- Uninstall old version from device
- Check device has enough storage
- Enable "Install via USB" in developer options

### iOS Issues

**Code Signing Error:**
- Go to Signing & Capabilities in Xcode
- Select your development team
- Xcode will automatically create certificates

**Device Not Recognized:**
- Reconnect USB cable
- Trust computer on iOS device
- Restart Xcode

### General Issues

**White Screen on Launch:**
- Clear app data and cache
- Rebuild: `npm run build && npx cap sync`
- Check browser console in development

**Supabase Connection Failed:**
- Verify `.env` file has correct values
- Check internet connection
- Verify Supabase project is running

## Publishing

### Android (Google Play Store)

1. **Generate Release APK/Bundle:**
   - In Android Studio: Build > Generate Signed Bundle/APK
   - Create or use existing keystore
   - Generate release bundle (.aab)

2. **Upload to Play Console:**
   - Create app listing
   - Upload bundle
   - Complete store listing
   - Submit for review

### iOS (Apple App Store)

1. **Archive Build:**
   - In Xcode: Product > Archive
   - Wait for archive to complete

2. **Upload to App Store Connect:**
   - Open Organizer (Window > Organizer)
   - Select archive
   - Click "Distribute App"
   - Follow wizard to upload

3. **Submit for Review:**
   - Go to App Store Connect
   - Complete app information
   - Submit for review

## Testing

### Web Testing
```bash
npm run dev
# Open http://localhost:3000
```

### Android Testing
- Use Android Emulator in Android Studio
- Or connect physical Android device

### iOS Testing
- Use iOS Simulator in Xcode
- Or connect physical iOS device

## Additional Resources

- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Android Developer Guide](https://developer.android.com)
- [iOS Developer Guide](https://developer.apple.com)
- [Supabase Documentation](https://supabase.com/docs)

## Support

For issues or questions:
- Check the main README.md
- Open an issue on GitHub
- Contact: support@megagent.app
