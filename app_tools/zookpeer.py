#!/usr/bin/python

import sys
sys.path.append("..")
import discovery
import discovery

zk_config = "/opt/zookeeper/conf/zoo.cfg"


def append_mem_to_config():
    file_object = open(zk_config, 'a')
    members = discovery.discovery()

    for i in range(len(members)):
        #print("%s : %s" % (i, members[i]))
        data = "server." + str(i) + "=" + str(members[i]) + ":2888:3888\n"
        file_object.write(data)

    file_object.close()


if __name__ == '__main__':
    append_mem_to_config()

