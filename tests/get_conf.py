import yaml


def get_config():
    with open('conf.yml', 'r') as conffile:
        try:
            config = yaml.safe_load(conffile)
        except yaml.YAMLError as e:
            print(e)

        if not config.get('IP'):
            config['IP'] = '127.0.0.1'
        if not config.get('PORT'):
            config['PORT'] = 10001
        if not config.get('FILE_NAME'):
            config['FILE_NAME'] = 'programmers and other.jpg'
        if not config.get('ID'):
            config['ID'] = 123123
        if not config.get('TAG'):
            config['TAG'] = 'tag_'
        if not config.get('MIMETYPE'):
            config['MIMETYPE'] = 'application/octet-stream'
        if not config.get('REASON'):
            config['REASON'] = 'Created'
        if not config.get('STATUS'):
            config['STATUS'] = 201
        main_uri = 'http://' + str(config['IP']) + \
                   ':' + str(config['PORT'])
    return config, main_uri
