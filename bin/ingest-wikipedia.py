#!/usr/bin/python3

SERVER = 'localhost'
INDEX = 'wiki'

MAPPING = {
            "index_patterns": ["PUT SOMETHING HERE"],
            "settings": {
                "number_of_shards": 1,
                "index": {"mapping.ignore_malformed": True},
            },
            "mappings": {
                "_source": { "enabled": True },
                #"dynamic": "runtime",
                "properties": {
                    "@timestamp": {
                        "format": "strict_date_optional_time||epoch_millis",
                        "type": "date"
                    },
                    "Pool": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "Queue": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "Platform": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "Project": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "Project Name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "Group": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                    "Name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},

                    "QueueAllocationSum": {"type": "long"},
                    "L3Allocation": {"type": "long"},
                    "L3AllocationSum": {"type": "long"},
                    "L5Allocation": {"type": "long"},
		}
}

def parseArgs():
    global DRY_RUN
    global VERBOSE

    description = f'''Tool to suck in wikipedia archives and index them in elastic.'''
    epilog = f'''tbd'''
    parser = argparse.ArgumentParser(
                    # prog=args[0],
                    description=description,
                    epilog=epilog)
    arg_p = parser.add_argument(
                    '-p', '--pool', action='store',
                    help="Specify the pool to work on.")
    arg_d = parser.add_argument('-d', '--dry_run', action='store_true',
                help="Don't cache or upload any data.",
                default=False)
    arg_v = parser.add_argument('-v', '--verbose', action='store_true',
                help="Print lots of extra data for review.",
                default=False)
    arg_m = parser.add_argument('-m', '--push_mapping', action='store_true',
                help="(Re)Submit the mapping for the index.",
                default=False)
    arg_z = parser.add_argument('-z', '--drop_all', action='store_true',
                help="Drop the wiki index so we can start over.",
                default=False)
    args = parser.parse_args()

    DRY_RUN=args.dry_run
    VERBOSE=args.verbose

    error_obj = None
    if not args.push_mapping and not args.pool:
        error_obj = arg_p
        error_msg = arg_p.help

    if not error_obj is None:
        raise argparse.ArgumentError(error_obj, error_msg)

    return args


def curl(url='', json_body='', verb='get', return_string=False):
    # pass header option for content type if request has a
    # body to avoid Content-Type error in Elasticsearch v6.0
    if not url.startswith('http'):
        global SERVER
        url = f'{SERVER}/{url}'

    headers = { 'Content-Type': 'application/json', }

    verb_map = {'delete': requests.delete, 'get': requests.get, 'post': requests.post, 'put': requests.put}
    vprint('curl:', verb, url)
    try:
        if verb == 'delete':
            resp = verb_map[verb](url, headers=headers)
        else:
            resp = verb_map[verb](url, headers=headers, data=json_body)
        if return_string:
            try:
                resp_text = json.loads(resp.text)
            except:
                resp_text = resp.text
        else:
            resp_text = resp.text

    except Exception as error:
        print ('\nelasticsearch_curl() error:', error)
        resp_text = error

    #print ("resp_text:", resp_text)
    return resp_text


def pushMapping():
    global DRY_RUN
    global MAPPING
    global SERVER
    global INDEX

    index = f'{INDEX}-*'

    MAPPING['index_patterns'] = [index,]
    mapping = json.dumps(MAPPING)
    url = f'{SERVER}/_template/{INDEX}'
    vprint(f'Putting template: {url}')
    if DRY_RUN:
        print('Dry Run.  Curl args:')
        print(url, mapping, 'put')
    else:
        result = curl(url, mapping, 'put')
        vprint(f'Result: {result}')


def dropIndex():
    global SERVER
    global INDEX
    for index in getWWIndexes(INDEX):
        url = f'{SERVER}/{index}'
        if DRY_RUN:
            print('Dry Run. Curl args:')
            print(url, 'delete')
        else:
            for count in range(3):
                time.sleep(1)
                print('.')
            result = curl(url, verb='delete')
            print(f'Result: {result}')


if __name__ == '__main__':
    args = parseArgs()
    if args.drop_all:
        dropIndex()
    elif args.push_mapping:
        pushMapping()
    else:
        pass
