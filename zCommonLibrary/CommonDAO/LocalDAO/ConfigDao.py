import configparser

relative_path = 'resources/'


def getDbConfig():
    config = configparser.ConfigParser()
    filename = 'db_settings.properties'
    config.read(relative_path + filename)
    config = {
        'host': config['EnglishTopics']['host'],
        'port': config['EnglishTopics']['port'],
        'database': config['EnglishTopics']['dbname'],
        'user': config['EnglishTopics']['user'],
        'password': config['EnglishTopics']['password'],
    }
    return config


def getTopicEnvironmentFromConfig():
    config = configparser.ConfigParser()
    filename = 'TopicEnvironment.properties'
    config.read(relative_path + filename)

    themeNumber = config['Info']['themeNumber']
    themeName = config['Info']['themeName']
    topicNumber = config['Info']['topicNumber']
    return [themeNumber, themeName, topicNumber]
