import os
import newrelic.agent

def init_app(app):
    try:
        newrelic.agent.initialize('/home/superdesk/temp/newrelic/newrelic.ini')
        newrelic_module = newrelic.agent
        app.on_pre_GET += on_pre_request_get_callback
        app.on_post_GET += on_post_request_get_callback
    except ImportError:
        pass
    except Exception as e:
        print(e)


def _is_profile_resource(resource):
    return resource in {'search', 'archive', 'archived', 'published', 'publish_queue'}


def on_pre_request_get_callback(resource, request, lookup):
    if _is_profile_resource(resource):
        print('on_request_start {} --- {} --- {}'.format(resource, request, lookup))
        name = resource
        group = 'Python/EveFramework/EndPoint'
        try:
            newrelic.agent.set_transaction_name(name, group=group)
        except Exception as e:
            print('failed to set transaction name. {}'.format(e))


def on_post_request_get_callback(resource, request, lookup):
    try:
        if _is_profile_resource(resource):
            print('on_request_start {} --- {} --- {}'.format(resource, request, lookup))
            newrelic.agent.end_of_transaction()
    except Exception as e:
        print('failed to set transaction name. {}'.format(e))


