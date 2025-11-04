"""
Basic usage example for MEGA-Bot
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from megabot import MegaBot


async def basic_example():
    """Basic usage of MEGA-Bot"""
    print("Starting MEGA-Bot basic example...")
    print("-" * 80)
    
    # Initialize bot
    bot = MegaBot()
    
    # Start bot
    await bot.start()
    
    # Example 1: Simple query
    print("\n1. Simple Query Example")
    print("-" * 80)
    result = await bot.query("What is machine learning?")
    print(f"Platforms responded: {len(result['responses'])}")
    for platform, response in result['responses'].items():
        print(f"\n{platform}:")
        print(f"  {response['response'][:100]}...")
    
    # Example 2: Research
    print("\n2. Research Example")
    print("-" * 80)
    research = await bot.research("neural networks", depth="medium")
    print(f"Research topic: {research['topic']}")
    print(f"Platforms used: {len(research['platforms_used'])}")
    print(f"Total findings: {research['synthesis'].get('total_findings', 0)}")
    
    # Example 3: Get status
    print("\n3. Bot Status")
    print("-" * 80)
    status = bot.get_status()
    print(f"Running: {status['running']}")
    print(f"Active platforms: {status['integrations']['active']}")
    
    # Example 4: Get capabilities
    print("\n4. Capabilities")
    print("-" * 80)
    capabilities = bot.get_capabilities()
    print(f"Total capabilities: {len(capabilities)}")
    print("Sample capabilities:", capabilities[:5])
    
    # Stop bot
    await bot.stop()
    print("\n" + "-" * 80)
    print("Example completed!")


if __name__ == "__main__":
    asyncio.run(basic_example())
