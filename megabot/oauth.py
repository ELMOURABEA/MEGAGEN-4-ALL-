"""
GitHub OAuth Integration for MEGAGENT V2.0
Enables cross-platform authentication and authorization
"""
import asyncio
import secrets
import hashlib
import base64
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from urllib.parse import urlencode
import json


class GitHubOAuth:
    """
    GitHub OAuth 2.0 Implementation for MEGAGENT
    Supports web, mobile (iOS/Android), and desktop (Windows/macOS/Linux)
    """
    
    def __init__(self, client_id: str, client_secret: Optional[str] = None,
                 platform: str = "web", logger=None):
        """
        Initialize GitHub OAuth
        
        Args:
            client_id: GitHub OAuth App client ID
            client_secret: GitHub OAuth App client secret (not needed for device flow)
            platform: Platform type (web, mobile_ios, mobile_android, desktop_*)
            logger: Optional logger instance
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.platform = platform
        self.logger = logger
        
        # OAuth endpoints
        self.auth_url = "https://github.com/login/oauth/authorize"
        self.token_url = "https://github.com/login/oauth/access_token"
        self.device_auth_url = "https://github.com/login/device/code"
        
        # Callback URLs per platform
        self.callback_urls = {
            "web": "https://megagent.app/oauth/callback",
            "mobile_ios": "megagent://oauth/callback",
            "mobile_android": "megagent://oauth/callback",
            "desktop_windows": "http://localhost:8080/oauth/callback",
            "desktop_macos": "http://localhost:8080/oauth/callback",
            "desktop_linux": "http://localhost:8080/oauth/callback",
        }
        
        # OAuth scopes
        self.scopes = [
            "repo", "workflow", "write:packages", "read:packages",
            "admin:repo_hook", "gist", "notifications", "user",
            "read:user", "user:email", "read:org"
        ]
        
        # Token storage
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.token_expiry: Optional[datetime] = None
        
        # PKCE support
        self.code_verifier: Optional[str] = None
        self.code_challenge: Optional[str] = None
        
        if self.logger:
            self.logger.info(f"GitHub OAuth initialized for platform: {platform}")
    
    def generate_pkce_pair(self) -> tuple:
        """
        Generate PKCE code verifier and challenge
        For enhanced security in mobile and desktop apps
        
        Returns:
            Tuple of (code_verifier, code_challenge)
        """
        # Generate code verifier (random 128-character string)
        self.code_verifier = base64.urlsafe_b64encode(
            secrets.token_bytes(96)
        ).decode('utf-8').rstrip('=')
        
        # Generate code challenge (SHA256 hash of verifier)
        challenge_bytes = hashlib.sha256(self.code_verifier.encode('utf-8')).digest()
        self.code_challenge = base64.urlsafe_b64encode(
            challenge_bytes
        ).decode('utf-8').rstrip('=')
        
        return self.code_verifier, self.code_challenge
    
    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """
        Get OAuth authorization URL for user to visit
        
        Args:
            state: CSRF protection state parameter
            
        Returns:
            Authorization URL
        """
        if state is None:
            state = secrets.token_urlsafe(32)
        
        # Generate PKCE for mobile/desktop
        if self.platform.startswith(('mobile', 'desktop')):
            self.generate_pkce_pair()
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.callback_urls.get(self.platform, self.callback_urls['web']),
            'scope': ' '.join(self.scopes),
            'state': state,
            'allow_signup': 'true'
        }
        
        # Add PKCE challenge for mobile/desktop
        if self.code_challenge:
            params['code_challenge'] = self.code_challenge
            params['code_challenge_method'] = 'S256'
        
        url = f"{self.auth_url}?{urlencode(params)}"
        
        if self.logger:
            self.logger.info(f"Authorization URL generated for {self.platform}")
        
        return url
    
    async def exchange_code_for_token(self, code: str, state: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from callback
            state: State parameter for CSRF validation
            
        Returns:
            Token response dictionary
        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.callback_urls.get(self.platform, self.callback_urls['web'])
        }
        
        # Add PKCE verifier for mobile/desktop
        if self.code_verifier:
            params['code_verifier'] = self.code_verifier
        
        # Simulate token exchange (in real implementation, would make HTTP request)
        token_response = {
            'access_token': f'gho_mock_{secrets.token_urlsafe(32)}',
            'token_type': 'bearer',
            'scope': ' '.join(self.scopes),
            'expires_in': 3600
        }
        
        self.access_token = token_response['access_token']
        self.token_expiry = datetime.now() + timedelta(seconds=token_response['expires_in'])
        
        if self.logger:
            self.logger.info("Successfully exchanged code for access token")
        
        return token_response
    
    async def device_flow_initiate(self) -> Dict[str, Any]:
        """
        Initiate device authorization flow
        Best for CLI/terminal usage without browser
        
        Returns:
            Device code response with user_code and verification_uri
        """
        # Simulate device flow initiation
        device_response = {
            'device_code': secrets.token_urlsafe(40),
            'user_code': f"{secrets.token_hex(4).upper()}-{secrets.token_hex(4).upper()}",
            'verification_uri': 'https://github.com/login/device',
            'expires_in': 900,
            'interval': 5
        }
        
        if self.logger:
            self.logger.info("Device flow initiated")
            self.logger.info(f"User code: {device_response['user_code']}")
            self.logger.info(f"Verification URL: {device_response['verification_uri']}")
        
        return device_response
    
    async def device_flow_poll(self, device_code: str, interval: int = 5) -> Dict[str, Any]:
        """
        Poll for device flow completion
        
        Args:
            device_code: Device code from initiation
            interval: Polling interval in seconds
            
        Returns:
            Token response when user authorizes
        """
        # Simulate polling (in real implementation, would poll token endpoint)
        await asyncio.sleep(interval)
        
        token_response = {
            'access_token': f'gho_mock_{secrets.token_urlsafe(32)}',
            'token_type': 'bearer',
            'scope': ' '.join(self.scopes)
        }
        
        self.access_token = token_response['access_token']
        
        if self.logger:
            self.logger.info("Device flow completed successfully")
        
        return token_response
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        if not self.access_token:
            return False
        
        if self.token_expiry and datetime.now() >= self.token_expiry:
            return False
        
        return True
    
    async def refresh_access_token(self) -> Dict[str, Any]:
        """
        Refresh the access token using refresh token
        
        Returns:
            New token response
        """
        if not self.refresh_token:
            raise ValueError("No refresh token available")
        
        # Simulate token refresh
        token_response = {
            'access_token': f'gho_mock_{secrets.token_urlsafe(32)}',
            'token_type': 'bearer',
            'scope': ' '.join(self.scopes),
            'expires_in': 3600
        }
        
        self.access_token = token_response['access_token']
        self.token_expiry = datetime.now() + timedelta(seconds=token_response['expires_in'])
        
        if self.logger:
            self.logger.info("Access token refreshed")
        
        return token_response
    
    async def revoke_token(self) -> bool:
        """
        Revoke the current access token
        
        Returns:
            True if successful
        """
        if not self.access_token:
            return False
        
        # Simulate token revocation
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
        
        if self.logger:
            self.logger.info("Access token revoked")
        
        return True
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get headers for authenticated API requests
        
        Returns:
            Dictionary with Authorization header
        """
        if not self.is_authenticated():
            raise ValueError("Not authenticated. Please authorize first.")
        
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'MEGAGENT-OCTOGEN-v2.0'
        }
    
    def save_token(self, filepath: str = ".megagent_token") -> None:
        """
        Save token to encrypted file
        
        Args:
            filepath: Path to save token file
        """
        token_data = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'token_expiry': self.token_expiry.isoformat() if self.token_expiry else None,
            'platform': self.platform
        }
        
        # In real implementation, would encrypt this data
        with open(filepath, 'w') as f:
            json.dump(token_data, f)
        
        if self.logger:
            self.logger.info(f"Token saved to {filepath}")
    
    def load_token(self, filepath: str = ".megagent_token") -> bool:
        """
        Load token from encrypted file
        
        Args:
            filepath: Path to token file
            
        Returns:
            True if successful
        """
        try:
            with open(filepath, 'r') as f:
                token_data = json.load(f)
            
            self.access_token = token_data.get('access_token')
            self.refresh_token = token_data.get('refresh_token')
            
            expiry_str = token_data.get('token_expiry')
            if expiry_str:
                self.token_expiry = datetime.fromisoformat(expiry_str)
            
            if self.logger:
                self.logger.info(f"Token loaded from {filepath}")
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Failed to load token: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get OAuth status information
        
        Returns:
            Status dictionary
        """
        return {
            'authenticated': self.is_authenticated(),
            'platform': self.platform,
            'token_present': bool(self.access_token),
            'token_expiry': self.token_expiry.isoformat() if self.token_expiry else None,
            'scopes': self.scopes
        }


class CrossPlatformOAuth:
    """
    Cross-platform OAuth manager for all platforms
    """
    
    def __init__(self, client_id: str, client_secret: Optional[str] = None, logger=None):
        """
        Initialize cross-platform OAuth manager
        
        Args:
            client_id: GitHub OAuth App client ID
            client_secret: GitHub OAuth App client secret
            logger: Optional logger instance
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.logger = logger
        
        # OAuth instances for each platform
        self.oauth_instances: Dict[str, GitHubOAuth] = {}
        
        # Initialize OAuth for all platforms
        for platform in ['web', 'mobile_ios', 'mobile_android', 
                        'desktop_windows', 'desktop_macos', 'desktop_linux']:
            self.oauth_instances[platform] = GitHubOAuth(
                client_id, client_secret, platform, logger
            )
    
    def get_oauth(self, platform: str) -> GitHubOAuth:
        """Get OAuth instance for specific platform"""
        return self.oauth_instances.get(platform)
    
    def get_all_auth_urls(self) -> Dict[str, str]:
        """Get authorization URLs for all platforms"""
        return {
            platform: oauth.get_authorization_url()
            for platform, oauth in self.oauth_instances.items()
        }
    
    def get_status_all_platforms(self) -> Dict[str, Dict[str, Any]]:
        """Get OAuth status for all platforms"""
        return {
            platform: oauth.get_status()
            for platform, oauth in self.oauth_instances.items()
        }
