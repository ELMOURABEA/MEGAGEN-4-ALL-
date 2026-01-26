# MEGA-Bot Publishing Guide

Guide for publishing MEGA-Bot to PyPI and other distribution channels.

## Prerequisites

- Python 3.8+
- PyPI account (https://pypi.org/account/register/)
- TestPyPI account for testing (https://test.pypi.org/account/register/)
- Git repository with proper tagging

## Quick Publish

```bash
# Install build tools
pip install --upgrade build twine

# Build package
python -m build

# Upload to PyPI
twine upload dist/*
```

## Detailed Publishing Steps

### 1. Pre-Publishing Checklist

- [ ] All tests pass (`pytest`)
- [ ] Version number updated in `pyproject.toml` and `megabot/__init__.py`
- [ ] README.md is up to date
- [ ] CHANGELOG.md updated with release notes
- [ ] Documentation is current
- [ ] License file is present
- [ ] .gitignore excludes build artifacts

### 2. Configure PyPI Credentials

#### Option A: Using `.pypirc` (Recommended)
Create `~/.pypirc`:
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
```

#### Option B: Using Environment Variables
```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR-API-TOKEN
```

### 3. Build the Package

```bash
# Install build tools
pip install --upgrade build twine

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build source distribution and wheel
python -m build

# Verify build
ls -lh dist/
```

You should see:
- `megaagent-1.0.0.tar.gz` (source distribution)
- `megaagent-1.0.0-py3-none-any.whl` (wheel)

### 4. Test the Package Locally

```bash
# Create test environment
python -m venv test-env
source test-env/bin/activate

# Install from wheel
pip install dist/megaagent-1.0.0-py3-none-any.whl

# Test installation
megabot --version
python -c "from megabot import MegaBot; print('Success!')"

# Deactivate
deactivate
rm -rf test-env
```

### 5. Upload to TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps megaagent

# Test it works
megabot --version
```

### 6. Upload to PyPI

```bash
# Final upload to PyPI
twine upload dist/*

# Verify upload
pip install megaagent
```

### 7. Create Git Tag and Release

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Create GitHub release
# Go to https://github.com/ELMOURABEA/MEGAGENT/releases/new
# - Tag: v1.0.0
# - Title: MEGA-Bot v1.0.0
# - Description: Release notes from CHANGELOG.md
# - Attach: dist/megaagent-1.0.0.tar.gz and .whl files
```

## Version Management

### Semantic Versioning

Follow semver (MAJOR.MINOR.PATCH):
- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

### Update Version

1. Update `pyproject.toml`:
```toml
[project]
version = "1.0.1"
```

2. Update `megabot/__init__.py`:
```python
__version__ = "1.0.1"
```

3. Update CHANGELOG.md:
```markdown
## [1.0.1] - 2024-01-15
### Fixed
- Bug fix description
```

## Automated Publishing with GitHub Actions

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    
    - name: Build package
      run: python -m build
    
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

Add PyPI token to GitHub Secrets:
1. Go to repository Settings → Secrets → Actions
2. Add `PYPI_API_TOKEN` with your PyPI token

## Docker Publishing

### Build and Tag Docker Image

```bash
# Build image
docker build -t elmourabea/megabot:latest .
docker build -t elmourabea/megabot:1.0.0 .

# Test locally
docker run -p 5000:5000 elmourabea/megabot:latest
```

### Push to Docker Hub

```bash
# Login
docker login

# Push
docker push elmourabea/megabot:latest
docker push elmourabea/megabot:1.0.0
```

### Automated Docker Publishing

Create `.github/workflows/docker-publish.yml`:

```yaml
name: Publish Docker Image

on:
  release:
    types: [published]

jobs:
  docker:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to DockerHub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Extract version
      id: version
      run: echo "VERSION=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        push: true
        tags: |
          elmourabea/megabot:latest
          elmourabea/megabot:${{ steps.version.outputs.VERSION }}
```

## Distribution Channels

### 1. PyPI (Primary)
- Main Python package index
- `pip install megaagent`

### 2. Conda (Optional)
Create conda recipe and publish to conda-forge

### 3. GitHub Releases
- Binary distributions
- Source code archives
- Release notes

### 4. Docker Hub
- Container images
- `docker pull elmourabea/megabot`

## Post-Publishing

### 1. Verify Installation
```bash
# Create fresh environment
python -m venv verify-env
source verify-env/bin/activate

# Install from PyPI
pip install megaagent

# Test
megabot --version
megabot

# Cleanup
deactivate
rm -rf verify-env
```

### 2. Update Documentation
- Update README badges
- Update installation instructions
- Update version references

### 3. Announce Release
- GitHub Discussions
- Twitter/Social media
- Dev.to or Medium blog post
- Reddit (r/Python)

### 4. Monitor
- PyPI download statistics
- GitHub issues
- User feedback

## Troubleshooting

### Build Fails

**Problem:** Import errors during build
```bash
# Solution: Ensure all dependencies are listed
pip install -e .
python -m pytest
```

**Problem:** Package data missing
```bash
# Solution: Check MANIFEST.in includes all necessary files
python -m build --sdist
tar -tzf dist/megaagent-*.tar.gz | grep your-file
```

### Upload Fails

**Problem:** Version already exists
```bash
# Solution: Increment version number
# Edit pyproject.toml and megabot/__init__.py
```

**Problem:** Authentication failed
```bash
# Solution: Check PyPI token
# Regenerate token on PyPI
# Update ~/.pypirc or environment variables
```

**Problem:** File size too large
```bash
# Solution: Check .gitignore and MANIFEST.in
# Exclude large files, logs, databases
```

### Installation Fails

**Problem:** Dependencies not found
```bash
# Solution: Check dependencies in pyproject.toml
# Test in clean environment
```

**Problem:** Import errors after install
```bash
# Solution: Check package structure
# Ensure __init__.py files exist
```

## Best Practices

1. **Testing:** Always test on TestPyPI first
2. **Versioning:** Follow semantic versioning
3. **Changelog:** Maintain detailed CHANGELOG.md
4. **Documentation:** Keep docs updated
5. **Automation:** Use CI/CD for releases
6. **Security:** Never commit API tokens
7. **Backup:** Keep backups of release artifacts

## Release Checklist

```markdown
## Pre-Release
- [ ] All tests passing
- [ ] Version updated everywhere
- [ ] CHANGELOG.md updated
- [ ] Documentation current
- [ ] Clean build directory

## Build
- [ ] Source distribution created
- [ ] Wheel created
- [ ] Local testing passed

## Test Release
- [ ] Uploaded to TestPyPI
- [ ] Installed from TestPyPI
- [ ] Functionality verified

## Production Release
- [ ] Uploaded to PyPI
- [ ] Git tagged
- [ ] GitHub release created
- [ ] Docker image built and pushed

## Post-Release
- [ ] Installation verified
- [ ] Documentation updated
- [ ] Release announced
- [ ] Monitoring setup
```

## Resources

- PyPI: https://pypi.org/
- TestPyPI: https://test.pypi.org/
- Packaging Guide: https://packaging.python.org/
- Twine: https://twine.readthedocs.io/
- Build: https://build.pypa.io/

## Support

For publishing issues:
- PyPI Support: https://pypi.org/help/
- Python Packaging Guide: https://packaging.python.org/
- GitHub Issues: https://github.com/ELMOURABEA/MEGAGENT/issues
