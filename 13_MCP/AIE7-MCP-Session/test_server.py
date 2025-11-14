from fastmcp import Client

async def main():
    # Connect via stdio to a local script
    async with Client("server.py") as client:
        tools = await client.list_tools()
        print(f"Available tools: {tools}")
        
        # Test calculator tool
        calc_result = await client.call_tool("calculate", {"expression": "5 * 3 + 2"})
        print(f"Calculator result: {calc_result}")
        
        # Test dice roller tool
        dice_result = await client.call_tool("roll_dice", {"notation": "2d6", "num_rolls": 3})
        print(f"Dice roller result: {dice_result}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())