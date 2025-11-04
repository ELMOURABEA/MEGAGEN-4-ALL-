"""
Workflow automation example for MEGA-Bot
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from megabot import MegaBot


async def workflow_example():
    """Demonstrate workflow automation capabilities"""
    print("MEGA-Bot Workflow Automation Example")
    print("=" * 80)
    
    bot = MegaBot()
    await bot.start()
    
    # Workflow 1: Comprehensive Analysis
    print("\nWorkflow 1: Comprehensive Analysis")
    print("-" * 80)
    result1 = await bot.execute_workflow(
        "comprehensive_analysis",
        topic="natural language processing"
    )
    print(f"Analysis: {result1['final_analysis']['summary']}")
    print(f"Research findings: {result1['final_analysis']['research_findings']}")
    
    # Workflow 2: Multi-Platform Query
    print("\nWorkflow 2: Multi-Platform Query")
    print("-" * 80)
    result2 = await bot.execute_workflow(
        "multi_platform_query",
        query="What are the benefits of cloud computing?"
    )
    print(f"Platforms responded: {len(result2['responses'])}")
    print(f"Average confidence: {result2['synthesis'].get('average_confidence', 'N/A')}")
    
    # Workflow 3: Deep Dive Research
    print("\nWorkflow 3: Deep Dive Research on Multiple Topics")
    print("-" * 80)
    result3 = await bot.execute_workflow(
        "deep_dive_research",
        topics=["computer vision", "reinforcement learning"]
    )
    print(f"Topics researched: {result3['topics_researched']}")
    for topic in result3['results']:
        print(f"  - {topic}: {len(result3['results'][topic]['platforms_used'])} platforms")
    
    # Document sync
    print("\nDocument Synchronization")
    print("-" * 80)
    await bot.sync_documents()
    updates = bot.get_updates(limit=10)
    print(f"Total updates available: {len(updates)}")
    for update in updates[:3]:
        print(f"  [{update['platform']}] {update['title']}")
    
    await bot.stop()
    print("\n" + "=" * 80)
    print("Workflow automation example completed!")


if __name__ == "__main__":
    asyncio.run(workflow_example())
