import json
import logging

from requests import HTTPError
from gitlab import GitlabCreateRepository, GroupNotFound

logger = logging.getLogger()
myFormatter = logging.Formatter('[GITLAB CREATE REPO ACTION] >> %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(myFormatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def export_repository_url(repository_url: str):
    logger.info("Writing repository url into stk cli context file to be used by pipeline ...")
    with open("stk-local-context.json", "w") as file:
        json.dump(dict(outputs=dict(created_repository=repository_url)), file, indent=4)


def run(metadata):
    try:
        create_repo = GitlabCreateRepository(**metadata.inputs)
        repository_url = create_repo(**metadata.inputs)
        export_repository_url(repository_url=repository_url)
    except GroupNotFound as e:
        logger.error(e)
