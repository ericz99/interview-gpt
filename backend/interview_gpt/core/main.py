from recorder import Recorder
import asyncio
from dotenv import load_dotenv
import pinecone
import os
from loguru import logger
from interview_gpt.cli.test import test

load_dotenv()

pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENVIRONMENT")
)

# https://github.com/orgs/python-poetry/discussions/1135
# https://stackoverflow.com/questions/66474844/import-local-package-during-poetry-run

async def main():
    print(test())
    logger.debug("Running Main!")
    rec = Recorder("/output")
    # await rec.on_record_system()
    stream = rec.on_record_system()

    try:
        async for data in stream:
            logger.success(data)
    except asyncio.CancelledError:
        logger.error('Data stream cancelled')


if __name__ == "__main__":
    asyncio.run(main())
