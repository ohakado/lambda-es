import logging
import os
import json
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
from botocore.endpoint import BotocoreHTTPSession
from botocore.credentials import Credentials

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def request(option):
    logger.debug('option:{}'.format(option))

    request = AWSRequest(
        method="GET",
        url=os.environ["ES_ENDPOINT_URL"],
        data=json.dumps(option)
    )

    if ("AWS_ACCESS_KEY_ID" in os.environ):
        credentials = Credentials(os.environ["AWS_ACCESS_KEY_ID"], os.environ["AWS_SECRET_ACCESS_KEY"], os.environ["AWS_SESSION_TOKEN"])
        SigV4Auth(credentials, "es", os.environ["AWS_REGION"]).add_auth(request)
    
    response = BotocoreHTTPSession().send(request.prepare())
    result = response.json()
    logger.debug('result:{}'.format(result))

    if (("hits" in result) and ("hits" in result["hits"])):
        return list(map(lambda n:n["_source"], result["hits"]["hits"]))
    else:
        return []

def handler(event, context):
    key = event["key"] if ("key" in event) else None
    option = {"size" : 100, "query" : {"bool" : {"must" : [{"match": {"key" : key}}]}}}

    return {"results" : request(option)}
