from collections import Counter

import bs4
import requests

from project.tasks import celery_app


@celery_app.task(acks_late=True)
async def parse_task(
    parse_task_id: int,
    parse_task_interface: ParseTaskInterface = get_parse_task_interface(),
):
    db_task = parse_task_interface.get(parse_task_id)

    # fetch webpage
    req = requests.get(db_task.url)
    soup = bs4.BeautifulSoup(req.text)

    # list with all tags, including repeative
    tags_raw = []
    # src= of each <script>
    script_srcs = []
    for tag in soup.find_all():
        if tag.name == "script":
            script_srcs.append(tag.attrs.get("src"))
        tags_raw.append(tag.name)

    # effectively count all occurences of each tag
    tags = Counter(tags_raw)

    # save results
    parse_task_interface.update(parse_task_id, tags=tags, scripts=script_srcs)
