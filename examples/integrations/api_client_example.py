"""
Example: Using MEGA-Bot API Client
Demonstrates how to integrate MEGA-Bot in any Python application using the API client
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from megabot.api.client import APIClient


def example_basic_usage():
    """Example 1: Basic API client usage"""
    print("=" * 80)
    print("Example 1: Basic API Client Usage")
    print("=" * 80)
    
    # Note: Make sure MEGA-Bot API server is running first
    # Run: megabot-server --port 5000
    
    client = APIClient("http://localhost:5000")
    
    try:
        # Check health
        health = client.health()
        print(f"✓ API Status: {health['status']}")
        print(f"  Version: {health['version']}")
        print()
        
        # Start bot
        print("Starting MEGA-Bot...")
        client.start()
        print("✓ Bot started")
        print()
        
        # Get status
        status = client.get_status()
        print(f"Bot Status:")
        print(f"  Running: {status['running']}")
        print(f"  Active Integrations: {status['integrations']['active']}")
        print()
        
        # Get capabilities
        capabilities = client.get_capabilities()
        print(f"Capabilities: {len(capabilities)} total")
        for cap in capabilities[:5]:  # Show first 5
            print(f"  - {cap}")
        print()
        
        # Query
        print("Querying: 'What is artificial intelligence?'")
        result = client.query("What is artificial intelligence?")
        print(f"✓ Received responses from {len(result['responses'])} platforms")
        print()
        
        # Research
        print("Researching: 'machine learning'")
        research = client.research("machine learning", depth="medium")
        print(f"✓ Research completed")
        print(f"  Platforms used: {len(research['platforms_used'])}")
        print(f"  Total findings: {research['synthesis'].get('total_findings', 0)}")
        print()
        
        # Stop bot
        print("Stopping MEGA-Bot...")
        client.stop()
        print("✓ Bot stopped")
        
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure the API server is running:")
        print("  megabot-server --port 5000")


def example_context_manager():
    """Example 2: Using context manager"""
    print("\n" + "=" * 80)
    print("Example 2: Using Context Manager")
    print("=" * 80)
    
    try:
        with APIClient("http://localhost:5000") as client:
            # Bot is automatically started
            print("✓ Bot started automatically")
            
            # Perform operations
            result = client.query("What are neural networks?")
            print(f"✓ Query completed")
            print(f"  Platforms responded: {result['synthesis'].get('platforms_responded', 0)}")
            
            # Bot is automatically stopped when exiting context
        
        print("✓ Bot stopped automatically")
        
    except Exception as e:
        print(f"Error: {e}")


def example_integration_in_app():
    """Example 3: Integration in a custom application"""
    print("\n" + "=" * 80)
    print("Example 3: Integration in Custom Application")
    print("=" * 80)
    
    class MyApplication:
        """Example custom application using MEGA-Bot"""
        
        def __init__(self):
            self.megabot = APIClient("http://localhost:5000")
            self.megabot.start()
            print("✓ MyApplication initialized with MEGA-Bot")
        
        def process_user_query(self, query: str):
            """Process user query using MEGA-Bot"""
            print(f"\nProcessing query: '{query}'")
            result = self.megabot.query(query)
            
            # Extract and format responses
            responses = []
            for platform, data in result['responses'].items():
                responses.append({
                    'platform': platform,
                    'response': data.get('response', ''),
                    'confidence': data.get('confidence', 0)
                })
            
            return responses
        
        def perform_research(self, topic: str):
            """Perform research using MEGA-Bot"""
            print(f"\nPerforming research on: '{topic}'")
            result = self.megabot.research(topic, depth="deep")
            
            return {
                'topic': result['topic'],
                'platforms': result['platforms_used'],
                'findings': result['synthesis'].get('total_findings', 0)
            }
        
        def shutdown(self):
            """Shutdown application"""
            self.megabot.stop()
            print("✓ MyApplication shut down")
    
    try:
        # Create application
        app = MyApplication()
        
        # Use MEGA-Bot features
        responses = app.process_user_query("What is deep learning?")
        print(f"✓ Received {len(responses)} responses")
        
        research = app.perform_research("quantum computing")
        print(f"✓ Research completed: {research['findings']} findings")
        
        # Shutdown
        app.shutdown()
        
    except Exception as e:
        print(f"Error: {e}")


def example_error_handling():
    """Example 4: Proper error handling"""
    print("\n" + "=" * 80)
    print("Example 4: Error Handling")
    print("=" * 80)
    
    client = APIClient("http://localhost:5000", timeout=10)
    
    try:
        # Try to connect
        client.start()
        
        # Perform operation with error handling
        try:
            result = client.query("Test query")
            print(f"✓ Query successful")
            print(f"  Platforms responded: {result['synthesis'].get('platforms_responded', 0)}")
        except Exception as e:
            print(f"Query failed: {e}")
        
        # Always cleanup
        client.stop()
        
    except Exception as e:
        print(f"Connection error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure API server is running: megabot-server")
        print("2. Check the server URL and port")
        print("3. Verify network connectivity")


if __name__ == '__main__':
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "MEGA-Bot API Client Examples" + " " * 30 + "║")
    print("╚" + "═" * 78 + "╝")
    print()
    print("IMPORTANT: Start the API server first:")
    print("  megabot-server --port 5000")
    print()
    input("Press Enter when server is ready...")
    
    # Run examples
    example_basic_usage()
    example_context_manager()
    example_integration_in_app()
    example_error_handling()
    
    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)
