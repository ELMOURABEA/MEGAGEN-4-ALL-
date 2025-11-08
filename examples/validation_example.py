"""
Example: Using Input Validation and Logging
Demonstrates validation and logging features introduced in v1.1.0 and available in v1.2.0
"""
import asyncio
from megabot import MegaBot, Config, setup_logging, validate_query, validate_topic


async def validation_example():
    """Demonstrate input validation and logging features"""
    
    # Set up logging
    print("Setting up logging...")
    setup_logging("INFO")
    print("✓ Logging configured\n")
    
    # Initialize bot
    config = Config()
    bot = MegaBot(config)
    await bot.start()
    
    print("=" * 80)
    print("Example 1: Query Validation")
    print("=" * 80)
    
    # Valid query
    query1 = "What is artificial intelligence?"
    is_valid, error = validate_query(query1)
    print(f"\nQuery: '{query1}'")
    print(f"Valid: {is_valid}")
    if error:
        print(f"Error: {error}")
    
    # Empty query
    query2 = ""
    is_valid, error = validate_query(query2)
    print(f"\nQuery: '{query2}'")
    print(f"Valid: {is_valid}")
    if error:
        print(f"Error: {error}")
    
    # Query with dangerous content
    query3 = "Hello <script>alert('xss')</script>"
    is_valid, error = validate_query(query3)
    print(f"\nQuery: '{query3}'")
    print(f"Valid: {is_valid}")
    if error:
        print(f"Error: {error}")
    
    print("\n" + "=" * 80)
    print("Example 2: Topic Validation")
    print("=" * 80)
    
    # Valid topic
    topic1 = "Machine Learning"
    is_valid, error = validate_topic(topic1)
    print(f"\nTopic: '{topic1}'")
    print(f"Valid: {is_valid}")
    if error:
        print(f"Error: {error}")
    
    # Topic too long
    topic2 = "a" * 501
    is_valid, error = validate_topic(topic2)
    print(f"\nTopic: '{topic2[:50]}...' (length: {len(topic2)})")
    print(f"Valid: {is_valid}")
    if error:
        print(f"Error: {error}")
    
    print("\n" + "=" * 80)
    print("Example 3: Automatic Validation in API")
    print("=" * 80)
    
    # Try querying with valid input - this works
    print("\nQuerying with valid input...")
    result = await bot.query("What are the benefits of AI?")
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"✓ Query successful, {len(result['responses'])} platforms responded")
    
    # Try querying with invalid input - this is rejected
    print("\nQuerying with invalid input (empty query)...")
    result = await bot.query("")
    if "error" in result:
        print(f"✓ Query rejected: {result['error']}")
    else:
        print(f"Unexpected: Query succeeded")
    
    # Try research with valid topic
    print("\nResearching valid topic...")
    result = await bot.research("quantum computing", "shallow")
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"✓ Research successful")
    
    # Try research with invalid topic
    print("\nResearching invalid topic (empty)...")
    result = await bot.research("", "shallow")
    if "error" in result:
        print(f"✓ Research rejected: {result['error']}")
    else:
        print(f"Unexpected: Research succeeded")
    
    print("\n" + "=" * 80)
    print("Example 4: Input Sanitization")
    print("=" * 80)
    
    # Demonstrate automatic sanitization
    dirty_query = "Hello <script>world</script> & friends"
    print(f"\nOriginal query: '{dirty_query}'")
    print("Submitting to bot (automatically sanitized)...")
    result = await bot.query(dirty_query)
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print("✓ Query processed safely (dangerous content removed)")
    
    await bot.stop()
    
    print("\n" + "=" * 80)
    print("Validation Example Complete")
    print("=" * 80)
    print("\nKey Features Demonstrated:")
    print("  • Query validation prevents malicious input")
    print("  • Topic validation ensures safe research")
    print("  • Automatic input sanitization")
    print("  • Comprehensive logging for debugging")
    print("  • Error messages guide proper usage")


if __name__ == "__main__":
    asyncio.run(validation_example())
