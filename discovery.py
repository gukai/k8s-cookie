#!/usr/bin/python

import os
import time
import k8s



def discovery():
    pod = k8s.Pod()
    podname =  pod.get_my_name()
    podnamespace = pod.get_my_namespace()
    podrc = pod.get_my_replicationcontroller()
    #print("pod info: podname = %s, podnamespace = %s, podrc = %s" % (podname,podnamespace, podrc))

    rc = k8s.RepelicationController(podrc, podnamespace)
    rc_replicas_status = rc.get_replicas_status()
    rc_replicas_def = rc.get_replicas_definition()
    #print("rc info: rc_replicas_status = %s, rc_replicas_def = %s" % (rc_replicas_status, rc_replicas_def))

    times = 0
    while rc_replicas_status != rc_replicas_def:
        if times >= 10:
            print("ERROR: timeout to wait for all pods started in cluster.")
            os.exit(1)
        print("We define %s replicas in Cluster, now only %s running,"
                " waiting for 10s and try again...." % (rc_replicas_def,rc_replicas_status ))
        time.sleep(10)
        times = times + 1


    ip_list = pod.pods_ip_list_in_rc(podrc)
    print("%s" % ip_list)
    return ip_list

    #import code
    #code.interact(banner="",local=locals())


if __name__ == '__main__':
    discovery()
