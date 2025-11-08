"""
Example: Using Monetization and Advertising Features
Demonstrates the v1.2.0 monetization and advertising system
"""
import asyncio
from megabot import MegaBot, Config, MonetizationManager


async def monetization_example():
    """Demonstrate monetization and advertising features"""
    
    print("=" * 80)
    print("MEGA-Bot Monetization System Demo")
    print("=" * 80)
    print()
    
    # ========================================================================
    # Example 1: View Available Subscription Tiers
    # ========================================================================
    print("=" * 80)
    print("Example 1: Available Subscription Tiers")
    print("=" * 80)
    
    tiers = MonetizationManager.get_all_tiers()
    for tier_name, tier_info in tiers.items():
        print(f"\n{tier_info['name']} - {tier_info['price']}")
        print("Features:")
        for feature in tier_info['features']:
            print(f"  • {feature}")
    
    # ========================================================================
    # Example 2: Free Tier with Limits
    # ========================================================================
    print("\n" + "=" * 80)
    print("Example 2: Free Tier Usage (with limits)")
    print("=" * 80)
    print()
    
    # Initialize bot with free tier (default)
    config_free = Config()
    config_free.set("monetization.tier", "free")
    bot_free = MegaBot(config_free)
    await bot_free.start()
    
    # Check tier info
    tier_info = bot_free.get_tier_info()
    print(f"Current Tier: {tier_info['tier']}")
    print(f"Queries today: {tier_info['usage']['queries_today']}/{tier_info['limits']['max_queries_per_day']}")
    print(f"Research today: {tier_info['usage']['research_today']}/{tier_info['limits']['max_research_per_day']}")
    
    # Try shallow research (allowed in free tier)
    print("\n✓ Attempting shallow research (allowed in free tier)...")
    result = await bot_free.research("AI basics", "shallow")
    if "error" not in result:
        print("  Success! Shallow research completed")
    else:
        print(f"  Error: {result['error']}")
    
    # Try deep research (not allowed in free tier)
    print("\n✗ Attempting deep research (not allowed in free tier)...")
    result = await bot_free.research("AI advanced", "deep")
    if "error" in result:
        print(f"  Expected limitation: {result['error']}")
    
    await bot_free.stop()
    
    # ========================================================================
    # Example 3: Pro Tier with Unlimited Access
    # ========================================================================
    print("\n" + "=" * 80)
    print("Example 3: Pro Tier Usage (unlimited)")
    print("=" * 80)
    print()
    
    # Initialize bot with Pro tier
    config_pro = Config()
    config_pro.set("monetization.tier", "pro")
    bot_pro = MegaBot(config_pro)
    await bot_pro.start()
    
    # Check tier info
    tier_info = bot_pro.get_tier_info()
    print(f"Current Tier: {tier_info['tier']}")
    print(f"Queries: Unlimited")
    print(f"Research: Unlimited, all depths")
    
    # Try deep research (allowed in pro tier)
    print("\n✓ Attempting deep research (allowed in pro tier)...")
    result = await bot_pro.research("quantum computing", "deep")
    if "error" not in result:
        print("  Success! Deep research completed")
    else:
        print(f"  Error: {result['error']}")
    
    await bot_pro.stop()
    
    # ========================================================================
    # Example 4: Advertising Integration
    # ========================================================================
    print("\n" + "=" * 80)
    print("Example 4: Advertising System")
    print("=" * 80)
    print()
    
    # Initialize bot with advertising enabled
    config_ads = Config()
    config_ads.set("monetization.advertising_enabled", True)
    bot_ads = MegaBot(config_ads)
    await bot_ads.start()
    
    # Show banner ad
    print("Showing banner advertisement...")
    result = bot_ads.show_banner_ad("bottom")
    print(f"  Status: {result['status']}")
    print(f"  Ad Unit: {result.get('ad_unit_id', 'N/A')}")
    
    # Show rewarded ad for bonus queries
    print("\nShowing rewarded advertisement for bonus queries...")
    result = bot_ads.show_rewarded_ad("bonus_queries")
    if result.get("status") == "success":
        reward = result.get("reward", {})
        print(f"  Reward earned: {reward.get('description', 'N/A')}")
    
    # Show rewarded ad for tier upgrade
    print("\nShowing rewarded advertisement for temporary tier upgrade...")
    result = bot_ads.show_rewarded_ad("tier_upgrade")
    if result.get("status") == "success":
        reward = result.get("reward", {})
        print(f"  Reward earned: {reward.get('description', 'N/A')}")
    
    await bot_ads.stop()
    
    # ========================================================================
    # Example 5: Monitoring Usage
    # ========================================================================
    print("\n" + "=" * 80)
    print("Example 5: Usage Monitoring")
    print("=" * 80)
    print()
    
    # Create a free tier bot and use it
    config_monitor = Config()
    config_monitor.set("monetization.tier", "free")
    bot_monitor = MegaBot(config_monitor)
    await bot_monitor.start()
    
    # Make some queries
    print("Making 3 queries...")
    for i in range(3):
        result = await bot_monitor.query(f"Test query {i+1}")
        print(f"  Query {i+1}: {'Success' if 'error' not in result else 'Error'}")
    
    # Check updated usage
    tier_info = bot_monitor.get_tier_info()
    print(f"\nUsage after 3 queries:")
    print(f"  Queries used: {tier_info['usage']['queries_today']}/10")
    print(f"  Queries remaining: {10 - tier_info['usage']['queries_today']}")
    
    await bot_monitor.stop()
    
    print("\n" + "=" * 80)
    print("Monetization Example Complete")
    print("=" * 80)
    print("\nKey Features Demonstrated:")
    print("  • Three subscription tiers (Free, Pro, Full Energy)")
    print("  • Usage limits and tracking")
    print("  • Feature restrictions by tier")
    print("  • Advertising integration with AdMob")
    print("  • Banner and rewarded ads")
    print("  • Real-time usage monitoring")
    print("\nTo upgrade your tier, set MEGABOT_TIER environment variable:")
    print("  export MEGABOT_TIER=pro")
    print("  export MEGABOT_TIER=full_energy")


if __name__ == "__main__":
    asyncio.run(monetization_example())
