#!/usr/bin/env python3
"""
GitHub Action runner script for MEGAGENT
Handles action inputs and orchestrates the MEGAGENT execution
"""
import argparse
import asyncio
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from megabot import MegaBot, Config


async def run_action(mode, prompt, depth='medium', workflow_name=None):
    """
    Run MEGAGENT based on action inputs
    
    Args:
        mode: Operation mode (query, research, workflow)
        prompt: Query or research topic
        depth: Research depth (shallow, medium, deep)
        workflow_name: Workflow name to execute
    
    Returns:
        dict: Result of the operation
    """
    # Initialize MegaBot with config
    config = Config()
    
    # Load config from megabot_config.json if it exists
    if os.path.exists('megabot_config.json'):
        with open('megabot_config.json', 'r') as f:
            config_data = json.load(f)
            for key, value in config_data.get('monetization', {}).items():
                config.set(f'monetization.{key}', value)
    
    bot = MegaBot(config)
    
    try:
        await bot.start()
        
        result = {}
        
        if mode == 'query':
            result = await bot.query(prompt)
        elif mode == 'research':
            result = await bot.research(prompt, depth=depth)
        elif mode == 'workflow':
            if not workflow_name:
                raise ValueError("workflow-name is required for workflow mode")
            result = await bot.execute_workflow(workflow_name, topic=prompt)
        else:
            raise ValueError(f"Invalid mode: {mode}. Must be 'query', 'research', or 'workflow'")
        
        await bot.stop()
        
        return result
        
    except Exception as e:
        await bot.stop()
        raise


def set_output(name, value):
    """Set GitHub Actions output"""
    # GitHub Actions output using environment file
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            # Escape newlines for multi-line values
            value_str = str(value).replace('%', '%25').replace('\n', '%0A').replace('\r', '%0D')
            f.write(f"{name}={value_str}\n")
    else:
        # Fallback for local testing
        print(f"::set-output name={name}::{value}")


def main():
    """Main entry point for the action runner"""
    parser = argparse.ArgumentParser(description='MEGAGENT GitHub Action Runner')
    parser.add_argument('--mode', required=True, choices=['query', 'research', 'workflow'],
                       help='Operation mode')
    parser.add_argument('--prompt', required=True,
                       help='Query prompt or research topic')
    parser.add_argument('--depth', default='medium', choices=['shallow', 'medium', 'deep'],
                       help='Research depth')
    parser.add_argument('--workflow-name', dest='workflow_name',
                       help='Workflow name to execute')
    
    args = parser.parse_args()
    
    try:
        # Run the action
        result = asyncio.run(run_action(
            mode=args.mode,
            prompt=args.prompt,
            depth=args.depth,
            workflow_name=args.workflow_name
        ))
        
        # Set outputs
        set_output('result', json.dumps(result))
        set_output('platforms-used', result.get('platforms_used', 0))
        
        # Get synthesis if available
        synthesis = result.get('synthesis', '')
        if not synthesis and 'responses' in result:
            # For query mode, create a simple synthesis
            synthesis = f"Received {len(result['responses'])} responses"
        set_output('synthesis', synthesis)
        
        # Print summary
        print(f"\n✅ MEGAGENT Action completed successfully!")
        print(f"Mode: {args.mode}")
        print(f"Platforms used: {result.get('platforms_used', 0)}")
        print(f"Result: {json.dumps(result, indent=2)[:500]}...")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error running MEGAGENT: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
