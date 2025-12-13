from queue import Queue

class _GroupSubscriber:
    group:str
    q: Queue

    def __init__(self, group:str):
        self.group = group
        self.q = Queue()

    


"""
"topic-1": {
            "group-a": _Subscriber(),
            "group-b": _Subscriber(),
        }, 
        "topic-2": {
            "group-a": _Subscriber(),
        }
"""
class _BasePubSub:
    """
    _BasePubSub is a singleton class, that will manage all the information in memory making the simulation of a real PubSub without I/O.
    """
    _instance = None
    _subscribers: dict[str, dict[str, _GroupSubscriber]] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(_BasePubSub, cls).__new__(cls)
            cls._instance._subscribers = {}
        return cls._instance
    
    def _add_subscriber(self, group:str, topic:str) -> _GroupSubscriber:
        """
        Add subscriber. This will add only 1 group for topic.
        
        :param group: Group name
        :type group: str
        :param topic: Topic to subscribe
        :type topic: str
        :return: object that container the queue to use for the subscription
        :rtype: _GroupSubscriber
        """
        if topic not in self._subscribers:
            # Not exist topic.
            _group_sub = _GroupSubscriber(group)
            topic_dict = {
                group: _group_sub
            }
            self._subscribers[topic] = topic_dict
            return _group_sub
        
        topic_dict = self._subscribers[topic]
        if group not in topic_dict:
            # Not exist group
            _group_sub = _GroupSubscriber(group)
            topic_dict[group] = _group_sub
            return _group_sub
        
        # Return existing group
        return topic_dict[group]

        
    def _publish(self, topic:str, payload):
        """
        Publis
        
        :param self: Description
        :param topic: Description
        :type topic: str
        :param payload: Description
        """
        if topic not in self._instance._subscribers:
            return
        
        topic_dict = self._instance._subscribers[topic]
        for i,v in topic_dict.items():
            v.q.put(payload)

