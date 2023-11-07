from recorder import Recorder
import asyncio
from dotenv import load_dotenv
import pinecone
import os
load_dotenv()

pinecone.init(
    api_key=os.getenv('PINECONE_API_KEY'),
    environment=os.getenv('PINECONE_ENVIRONMENT')
)

async def main():
    print('Running Main!')
    rec = Recorder('/output')
    await rec.on_record_system()

if __name__ == "__main__":
    asyncio.run(main())