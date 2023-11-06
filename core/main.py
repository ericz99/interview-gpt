from recorder import Recorder
import asyncio

async def main():
    print('Running Main!')
    rec = Recorder('/output')
    await rec.on_record_system()


if __name__ == "__main__":
    asyncio.run(main())