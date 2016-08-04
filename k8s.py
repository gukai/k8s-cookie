#!/usr/bin/python

import os
import json
import requests
import socket


KUBERNETES_RO_SERVICE_HOST = os.getenv('KUBERNETES_RO_SERVICE_HOST')
KUBERNETES_RO_SERVICE_PORT = os.getenv('KUBERNETES_RO_SERVICE_PORT')

def get_to_json(url):
    r = requests.get(url)
    return r.json()

def encode_utf8(value):
    return unicode(value).encode('utf-8')

class RepelicationController(object):
    def __init__(self, name=None , namespace=None):
        self.name = name
        self.namespace = namespace
        self.myrc = self._get_my_rc()

    def _get_my_rc(self):
        if self.namespace and self.name :
            #http://kubernetes.io/docs/api-reference/v1/operations/
            #GET /api/v1/namespaces/{namespace}/replicationcontrollers/{name}
            url = "http://" + KUBERNETES_RO_SERVICE_HOST + ":" + KUBERNETES_RO_SERVICE_PORT + \
                  "/api/v1/namespaces/" + self.namespace + "/replicationcontrollers/" + self.name
            return get_to_json(url)

        return None

    def get_replicas_status(self):
        #  http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_replicationcontrollerstatus
        #  Replicas is the most recently oberved number of replicas.
        if self.myrc != None:
            return self.myrc['status']['replicas']

    def get_replicas_definition(self):
        # http://kubernetes.io/docs/api-reference/v1/definitions/#_v1_replicationcontrollerspec
        # Replicas is the number of desired replicas.
        # This is a pointer to distinguish between explicit zero and unspecified. Defaults to 1
        if self.myrc != None:
            return self.myrc['spec']['replicas']


class Pod(object):
    def __init__(self):
        self.allpods = self._get_all_pods()
        self.mypod = self._get_my_pod()

    def _get_all_pods(self):
        url = "http://" + KUBERNETES_RO_SERVICE_HOST + ":" + KUBERNETES_RO_SERVICE_PORT + \
              "/api/v1/pods"
        return get_to_json(url)

    def _get_my_pod(self):
        hostname = socket.gethostname()
        url = None

        for item in self.allpods['items']:
            if encode_utf8(item['metadata']['name']) == hostname:
                link = encode_utf8(item['metadata']['selfLink'])
                url = "http://" + KUBERNETES_RO_SERVICE_HOST + ":" + KUBERNETES_RO_SERVICE_PORT + link

        if url != None:
            return get_to_json(url)

        return None

    def get_my_namespace(self):
        return self.mypod['metadata']['namespace']

    def get_my_name(self):
        return self.mypod['metadata']['name']

    def get_my_replicationcontroller(self):
        created_info = json.loads(self.mypod['metadata']['annotations']['kubernetes.io/created-by'])
        return created_info['reference']['name']

    def pods_ip_list_in_rc(self, rcname):
        ip_list = []
        for item in self.allpods['items']:
            created_info = json.loads(item['metadata']['annotations']['kubernetes.io/created-by'])
            if created_info['reference']['name'] == rcname:
                ip_list.append(item['status']['podIP'])

        return  ip_list




def test():
    pod = Pod()
    podname =  pod.get_my_name()
    podnamespace = pod.get_my_namespace()
    podrc = pod.get_my_replicationcontroller()
    print("pod info: podname = %s, podnamespace = %s, podrc = %s" % (podname,podnamespace, podrc))
    ip_list = pod.pods_ip_list_in_rc("redis-cluster")
    print("redis-cluster rc pod ip list is %s" % ip_list)

    rc = RepelicationController(podrc, podnamespace)
    rc_replicas_status = rc.get_replicas_status()
    rc_replicas_def = rc.get_replicas_definition()
    print("rc info: rc_replicas_status = %s, rc_replicas_def = %s" % (rc_replicas_status, rc_replicas_def))
    #import code
    #code.interact(banner="",local=locals())



if __name__ == '__main__':
    test()


