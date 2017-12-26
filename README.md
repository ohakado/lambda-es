# lambda-elasticsearch minimum sample

# local test
export AWS_DEFAULT_REGION=ap-northeast-1
export ES_ENDPOINT_URL=https://****.ap-northeast-1.es.amazonaws.com/alias/_search
python-lambda-local -f handler search-sample/index.py search-sample/event.json

