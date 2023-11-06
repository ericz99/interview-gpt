from recorder import Recorder
import asyncio

async def main():
    print('Running Main!')
    rec = Recorder('/output')
    await rec.on_record_system(10)


if __name__ == "__main__":
    asyncio.run(main())