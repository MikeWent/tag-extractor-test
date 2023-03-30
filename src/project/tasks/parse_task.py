import asyncio
import logging
from collections import Counter
from typing import Union

import httpx
from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession

from project import models, schemas, services


async def parse_task(db_task: models.ParseTask, db: AsyncSession):
    db_task = await services.ParseTaskService(db=db).update(
        db_obj=db_task,
        obj_in=schemas.parse_task.ParseTaskUpdate(
            status=models.ParseTask.TaskStatus.PROCESSING
        ),
    )
    try:

        async def fetch_page(url: str) -> BeautifulSoup:
            # fetch webpage
            async with httpx.AsyncClient() as client:
                html = await client.get(url=db_task.url)
                logging.info("finished fetching")
                return BeautifulSoup(html, "html.parser")

        # number of occurences of each html tags

        async def count_tags(soup: BeautifulSoup) -> dict[str, int]:
            # effectively count all occurences of each html tag
            tags = Counter([tag.name for tag in soup.find_all()])
            logging.info("finished counting")
            return tags

        async def extract_scrpts(soup: BeautifulSoup) -> list[str]:
            # src of each script on page
            scripts: list[str] = [
                tag.get("src") for tag in soup.find_all(name="script") if tag.get("src")
            ]
            logging.info("finished extracting")
            return scripts

        # run
        soup = await fetch_page(url=db_task.url)
        tags, scripts = await asyncio.gather(count_tags(soup), extract_scrpts(soup))

        # save results
        await services.ParseTaskService(db=db).update(
            db_obj=db_task,
            obj_in=schemas.parse_task.ParseTaskUpdate(
                scripts=scripts,
                tags=tags,
                status=models.ParseTask.TaskStatus.FINISHED,
            ),
        )
    except Exception as e:
        logging.error(e)
        # task failed
        db_task = await services.ParseTaskService(db=db).update(
            db_obj=db_task,
            obj_in=schemas.parse_task.ParseTaskUpdate(
                status=models.ParseTask.TaskStatus.FAILED
            ),
        )
