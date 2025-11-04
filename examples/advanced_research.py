"""
Advanced research example for MEGA-Bot
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from megabot import MegaBot


async def advanced_research():
    """Advanced research capabilities"""
    print("MEGA-Bot Advanced Research Example")
    print("=" * 80)
    
    bot = MegaBot()
    await bot.start()
    
    # Deep research on multiple topics
    topics = [
        "quantum computing",
        "artificial intelligence",
        "blockchain technology"
    ]
    
    print("\nPerforming deep research on multiple topics...")
    print("-" * 80)
    
    for topic in topics:
        print(f"\nResearching: {topic}")
        result = await bot.research(topic, depth="deep")
        
        print(f"  Platforms: {', '.join(result['platforms_used'])}")
        print(f"  Findings: {result['synthesis'].get('total_findings', 0)}")
        print(f"  Sources: {len(result['aggregated_sources'])}")
        
        # Show key insights
        if 'key_insights' in result['synthesis']:
            print("  Key insights:")
            for insight in result['synthesis']['key_insights'][:2]:
                print(f"    - [{insight['platform']}] {insight['insight'][:60]}...")
    
    # Comprehensive workflow
    print("\n" + "=" * 80)
    print("Executing comprehensive analysis workflow...")
    print("-" * 80)
    
    workflow_result = await bot.execute_workflow(
        "comprehensive_analysis",
        topic="machine learning algorithms"
    )
    
    print(f"Workflow completed!")
    print(f"Summary: {workflow_result['final_analysis']['summary']}")
    print(f"Platforms used: {workflow_result['final_analysis']['platforms_used']}")
    
    await bot.stop()
    print("\n" + "=" * 80)
    print("Advanced research example completed!")


if __name__ == "__main__":
    asyncio.run(advanced_research())
