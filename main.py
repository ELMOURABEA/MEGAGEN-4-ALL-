"""
Main entry point for MEGA-Bot
"""
import asyncio
import sys
from megabot import MegaBot, Config, __version__


async def demo():
    """Demo of MEGA-Bot capabilities"""
    print("=" * 80)
    print("XXXL MEGA BOT - Deep Research & Multi-Platform AI Integration")
    print(f"Version {__version__}")
    print("=" * 80)
    print()
    
    # Initialize MEGA-Bot
    config = Config()
    bot = MegaBot(config)
    
    # Start the bot
    await bot.start()
    print()
    
    # Display status
    print("=" * 80)
    print("MEGA-Bot Status")
    print("=" * 80)
    status = bot.get_status()
    print(f"Running: {status['running']}")
    print(f"Active Integrations: {status['integrations']['active']}/{status['integrations']['total']}")
    print(f"Platforms: {', '.join([p['name'] for p in status['integrations']['platforms'] if p['available']])}")
    print()
    
    # Display capabilities
    print("=" * 80)
    print("Combined Capabilities")
    print("=" * 80)
    capabilities = bot.get_capabilities()
    for i, cap in enumerate(capabilities, 1):
        print(f"{i}. {cap}")
    print()
    
    # Demo 1: Multi-platform query
    print("=" * 80)
    print("Demo 1: Multi-Platform Query")
    print("=" * 80)
    query_result = await bot.query("What are the latest advances in AI technology?")
    synthesis = query_result.get('synthesis', {})
    print(f"Platforms responded: {synthesis.get('platforms_responded', 0)}")
    print(f"Average confidence: {synthesis.get('average_confidence', 'N/A')}")
    print()
    if query_result.get('responses'):
        for platform, response in query_result['responses'].items():
            print(f"[{platform}]")
            print(f"  Response: {response.get('response', 'N/A')}")
            print()
    else:
        print("Note: No API keys configured. Using simulated mode.")
        print("To enable real integrations, add API keys to .env or config.json")
        print()
    
    # Demo 2: Deep research
    print("=" * 80)
    print("Demo 2: Deep Research")
    print("=" * 80)
    research_result = await bot.research("machine learning algorithms", depth="medium")
    print(f"Topic: {research_result.get('topic', 'N/A')}")
    print(f"Depth: {research_result.get('depth', 'N/A')}")
    print(f"Platforms used: {len(research_result.get('platforms_used', []))}")
    synthesis = research_result.get('synthesis', {})
    print(f"Total findings: {synthesis.get('total_findings', 0)}")
    if not research_result.get('platforms_used'):
        print("Note: Configure API keys to enable platform integrations")
    print()
    
    # Demo 3: Comprehensive analysis workflow
    print("=" * 80)
    print("Demo 3: Comprehensive Analysis Workflow")
    print("=" * 80)
    workflow_result = await bot.execute_workflow(
        "comprehensive_analysis",
        topic="artificial intelligence ethics"
    )
    final_analysis = workflow_result.get('final_analysis', {})
    print(f"Analysis summary: {final_analysis.get('summary', 'N/A')}")
    print()
    
    # Display latest updates
    print("=" * 80)
    print("Latest Platform Updates")
    print("=" * 80)
    updates = bot.get_updates(limit=10)
    for update in updates[:5]:  # Show first 5
        print(f"[{update['platform']}] {update['title']}")
        print(f"  {update['description']}")
        print()
    
    # Stop the bot
    await bot.stop()
    print()
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)


async def interactive_mode():
    """Interactive mode for MEGA-Bot"""
    config = Config()
    bot = MegaBot(config)
    
    await bot.start()
    print(f"\nMEGA-Bot v{__version__} - Interactive Mode")
    print("Type 'help' for commands, 'exit' to quit.\n")
    
    try:
        while True:
            try:
                command = input("MEGA-Bot> ").strip()
                
                if not command:
                    continue
                
                if command.lower() == 'exit':
                    break
                elif command.lower() == 'help':
                    print("\nAvailable commands:")
                    print("  query <prompt>     - Query all AI platforms")
                    print("  research <topic>   - Perform deep research")
                    print("  status             - Show bot status")
                    print("  capabilities       - List all capabilities")
                    print("  updates            - Show latest updates")
                    print("  sync               - Sync documents from platforms")
                    print("  version            - Show version information")
                    print("  exit               - Exit interactive mode")
                    print()
                elif command.lower() == 'version':
                    print(f"\nMEGA-Bot version {__version__}")
                    print("For more information, visit: https://github.com/ELMOURABEA/MEGAGENT")
                    print()
                elif command.lower() == 'status':
                    status = bot.get_status()
                    print(f"\nStatus: {'Running' if status['running'] else 'Stopped'}")
                    print(f"Active platforms: {status['integrations']['active']}")
                    print()
                elif command.lower() == 'capabilities':
                    caps = bot.get_capabilities()
                    print(f"\nTotal capabilities: {len(caps)}")
                    for cap in caps:
                        print(f"  - {cap}")
                    print()
                elif command.lower() == 'updates':
                    updates = bot.get_updates(limit=5)
                    print(f"\nLatest {len(updates)} updates:")
                    for update in updates:
                        print(f"  [{update['platform']}] {update['title']}")
                    print()
                elif command.lower() == 'sync':
                    await bot.sync_documents()
                    print("✓ Documents synchronized\n")
                elif command.lower().startswith('query '):
                    prompt = command[6:].strip()
                    result = await bot.query(prompt)
                    print(f"\nQuery results from {len(result['responses'])} platforms:")
                    for platform, resp in result['responses'].items():
                        print(f"\n[{platform}]")
                        print(f"  {resp.get('response', 'N/A')}")
                    print()
                elif command.lower().startswith('research '):
                    topic = command[9:].strip()
                    result = await bot.research(topic, "medium")
                    print(f"\nResearch results for: {topic}")
                    print(f"Platforms: {len(result['platforms_used'])}")
                    print(f"Findings: {result['synthesis'].get('total_findings', 0)}")
                    print()
                else:
                    print("Unknown command. Type 'help' for available commands.\n")
            
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.\n")
                continue
            except Exception as e:
                print(f"Error: {e}\n")
    
    finally:
        await bot.stop()


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(demo())


if __name__ == "__main__":
    main()
