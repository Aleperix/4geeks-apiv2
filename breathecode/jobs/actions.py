import requests, os, logging
from .models import Job

logger = logging.getLogger(__name__)

ZYTE_API_DEPLOY = os.environ.get('ZYTE_API_DEPLOY')
ZYTE_API_KEY = os.environ.get('ZYTE_API_KEY')


def fetch_spider_data(spider):
    _continue = True
    incoming_jobs = []
    job_number = spider.zyte_job_number
    spider.status = 'PENDING'
    spider.save()

    while _continue:
        job_number = job_number + 1
        response = requests.get(
            f'https://storage.scrapinghub.com/requests/{ZYTE_API_DEPLOY}/{spider.zyte_spider_number}/{job_number}?apikey={ZYTE_API_KEY}&format=json'
        )

        if response.status_code == 404:
            _continue = False

        elif response.status_code != 200:
            raise Exception(
                f'There was a {response.status_code} error fetching spider {spider.zyte_spider_number} job {job_number}'
            )
        jobs = response.json()
        # print('jobs', jobs)
        print(
            'url',
            f'https://storage.scrapinghub.com/requests/{ZYTE_API_DEPLOY}/{spider.zyte_spider_number}/{job_number}?apikey={ZYTE_API_KEY}&format=json'
        )

        if len(jobs) == 0:
            logger.debug(f'No more jobs found for spider {spider.zyte_spider_number} job {job_number}')
            _continue = False

        elif 'fp' not in jobs[0]:
            logger.debug(f'{len(jobs)} jobs found for spider {spider.zyte_spider_number} job {job_number}')
            incoming_jobs.append(jobs)

    for jobs in incoming_jobs:
        for j in jobs:
            _job = Jobs(name=j['name'], )
            _job.save()

    spider.status = 'SYNCHED'
    spider.save()

    return spider
