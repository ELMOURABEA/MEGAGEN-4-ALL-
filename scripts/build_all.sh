#!/bin/bash
# Build script for all platforms - MEGAGENT V2.0
# Builds desktop (Windows, macOS, Linux), mobile (iOS, Android), and web

set -e

echo "🐙 MEGAGENT OCTOGEN V2.0 - Cross-Platform Build Script"
echo "======================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check required tools
check_requirements() {
    echo "Checking requirements..."
    
    # Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
    
    # Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"
    
    echo ""
}

# Build Python package
build_python() {
    echo "Building Python package..."
    python3 setup.py sdist bdist_wheel
    echo -e "${GREEN}✓ Python package built${NC}"
    echo ""
}

# Build desktop apps
build_desktop() {
    echo "Building desktop applications..."
    
    # Check if electron-builder is available
    if command -v electron-builder &> /dev/null; then
        echo "Building Windows app..."
        npm run build:win || echo -e "${YELLOW}⚠ Windows build skipped (not on Windows)${NC}"
        
        echo "Building macOS app..."
        npm run build:mac || echo -e "${YELLOW}⚠ macOS build skipped (not on macOS)${NC}"
        
        echo "Building Linux app..."
        npm run build:linux || echo -e "${YELLOW}⚠ Linux build requires electron-builder${NC}"
    else
        echo -e "${YELLOW}⚠ electron-builder not found. Install with: npm install -g electron-builder${NC}"
    fi
    
    echo ""
}

# Build mobile apps
build_mobile() {
    echo "Building mobile applications..."
    
    # Check if React Native is available
    if command -v react-native &> /dev/null; then
        echo "Building iOS app..."
        npm run build:ios || echo -e "${YELLOW}⚠ iOS build skipped (requires macOS and Xcode)${NC}"
        
        echo "Building Android app..."
        npm run build:android || echo -e "${YELLOW}⚠ Android build requires Android SDK${NC}"
    else
        echo -e "${YELLOW}⚠ React Native not found. Mobile builds skipped.${NC}"
    fi
    
    echo ""
}

# Build web app
build_web() {
    echo "Building web application..."
    
    if [ -f "package.json" ]; then
        npm run build:web || echo -e "${YELLOW}⚠ Web build requires Next.js setup${NC}"
    else
        echo -e "${YELLOW}⚠ package.json not found. Web build skipped.${NC}"
    fi
    
    echo ""
}

# Create distribution packages
package_distributions() {
    echo "Creating distribution packages..."
    
    mkdir -p dist/releases
    
    # Copy Python packages
    if [ -d "dist" ]; then
        cp dist/*.whl dist/releases/ 2>/dev/null || true
        cp dist/*.tar.gz dist/releases/ 2>/dev/null || true
    fi
    
    echo -e "${GREEN}✓ Distribution packages created in dist/releases${NC}"
    echo ""
}

# Main build process
main() {
    echo "Starting build process..."
    echo ""
    
    check_requirements
    
    # Parse command line arguments
    BUILD_ALL=true
    BUILD_PYTHON=false
    BUILD_DESKTOP=false
    BUILD_MOBILE=false
    BUILD_WEB=false
    
    if [ $# -gt 0 ]; then
        BUILD_ALL=false
        for arg in "$@"; do
            case $arg in
                python)
                    BUILD_PYTHON=true
                    ;;
                desktop)
                    BUILD_DESKTOP=true
                    ;;
                mobile)
                    BUILD_MOBILE=true
                    ;;
                web)
                    BUILD_WEB=true
                    ;;
                all)
                    BUILD_ALL=true
                    ;;
                *)
                    echo -e "${RED}Unknown argument: $arg${NC}"
                    echo "Usage: $0 [python|desktop|mobile|web|all]"
                    exit 1
                    ;;
            esac
        done
    fi
    
    # Execute builds
    if [ "$BUILD_ALL" = true ] || [ "$BUILD_PYTHON" = true ]; then
        build_python
    fi
    
    if [ "$BUILD_ALL" = true ] || [ "$BUILD_DESKTOP" = true ]; then
        build_desktop
    fi
    
    if [ "$BUILD_ALL" = true ] || [ "$BUILD_MOBILE" = true ]; then
        build_mobile
    fi
    
    if [ "$BUILD_ALL" = true ] || [ "$BUILD_WEB" = true ]; then
        build_web
    fi
    
    package_distributions
    
    echo "======================================================"
    echo -e "${GREEN}🎉 Build process completed!${NC}"
    echo ""
    echo "Built packages:"
    ls -lh dist/releases/ 2>/dev/null || echo "No packages found in dist/releases/"
    echo ""
    echo "Next steps:"
    echo "1. Test the packages on target platforms"
    echo "2. Create GitHub release with: gh release create v2.0.0"
    echo "3. Upload packages as release assets"
    echo ""
}

# Run main function
main "$@"
