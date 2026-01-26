"""
API Client for MEGA-Bot
Provides easy integration with MEGA-Bot API server from Python applications
"""
from typing import Dict, Any, Optional, List
try:
    import requests
except ImportError:
    requests = None


class APIClient:
    """
    Client for interacting with MEGA-Bot REST API
    
    Example:
        client = APIClient("http://localhost:5000")
        client.start()
        result = client.query("What is AI?")
        print(result)
        client.stop()
    """
    
    def __init__(self, base_url: str = "http://localhost:5000", timeout: int = 30):
        """
        Initialize API client
        
        Args:
            base_url: Base URL of the MEGA-Bot API server
            timeout: Request timeout in seconds
        """
        if requests is None:
            raise ImportError(
                "requests library is required for API client. "
                "Install it with: pip install requests"
            )
        
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def _request(self, method: str, endpoint: str, 
                 data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make HTTP request to API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            data: Request data for POST requests
            
        Returns:
            Response data as dictionary
            
        Raises:
            Exception: If request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = self.session.get(url, timeout=self.timeout)
            elif method == 'POST':
                response = self.session.post(
                    url, 
                    json=data,
                    headers={'Content-Type': 'application/json'},
                    timeout=self.timeout
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {e}")
    
    def health(self) -> Dict[str, Any]:
        """
        Check API health
        
        Returns:
            Health status information
        """
        return self._request('GET', '/health')
    
    def start(self) -> Dict[str, Any]:
        """
        Start the MEGA-Bot service
        
        Returns:
            Status response
        """
        return self._request('POST', '/api/v1/start')
    
    def stop(self) -> Dict[str, Any]:
        """
        Stop the MEGA-Bot service
        
        Returns:
            Status response
        """
        return self._request('POST', '/api/v1/stop')
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get bot status
        
        Returns:
            Status information including running state and active integrations
        """
        return self._request('GET', '/api/v1/status')
    
    def get_capabilities(self) -> List[str]:
        """
        Get bot capabilities
        
        Returns:
            List of capabilities
        """
        result = self._request('GET', '/api/v1/capabilities')
        return result.get('capabilities', [])
    
    def query(self, prompt: str) -> Dict[str, Any]:
        """
        Query all AI platforms
        
        Args:
            prompt: Query prompt
            
        Returns:
            Query results from all platforms
        """
        return self._request('POST', '/api/v1/query', {'prompt': prompt})
    
    def research(self, topic: str, depth: str = 'medium') -> Dict[str, Any]:
        """
        Perform deep research
        
        Args:
            topic: Research topic
            depth: Research depth (shallow, medium, deep)
            
        Returns:
            Research results
        """
        return self._request('POST', '/api/v1/research', {
            'topic': topic,
            'depth': depth
        })
    
    def execute_workflow(self, workflow_name: str, **params) -> Dict[str, Any]:
        """
        Execute a workflow
        
        Args:
            workflow_name: Name of the workflow to execute
            **params: Workflow parameters
            
        Returns:
            Workflow execution results
        """
        return self._request('POST', '/api/v1/workflow', {
            'workflow_name': workflow_name,
            'params': params
        })
    
    def get_updates(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get latest platform updates
        
        Args:
            limit: Maximum number of updates to retrieve
            
        Returns:
            List of updates
        """
        result = self._request('GET', f'/api/v1/updates?limit={limit}')
        return result.get('updates', [])
    
    def sync_documents(self) -> Dict[str, Any]:
        """
        Sync documents from all platforms
        
        Returns:
            Sync status response
        """
        return self._request('POST', '/api/v1/sync')
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


# Example usage
if __name__ == '__main__':
    # Example 1: Basic usage
    client = APIClient()
    
    try:
        # Check health
        health = client.health()
        print(f"API Status: {health['status']}")
        
        # Start bot
        client.start()
        
        # Get status
        status = client.get_status()
        print(f"Bot running: {status['running']}")
        
        # Query
        result = client.query("What is artificial intelligence?")
        print(f"Query responses: {len(result['responses'])}")
        
        # Research
        research = client.research("machine learning", depth="medium")
        print(f"Research platforms: {len(research['platforms_used'])}")
        
        # Stop bot
        client.stop()
    
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Using context manager
    print("\nUsing context manager:")
    try:
        with APIClient() as client:
            result = client.query("What are neural networks?")
            print(f"Query completed: {result.get('synthesis', {}).get('platforms_responded', 0)} platforms")
    except Exception as e:
        print(f"Error: {e}")
