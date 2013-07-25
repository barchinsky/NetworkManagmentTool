#!/usr/bin/env python

import logging
import logging.handlers


LOG_FILENAME = "network.mylog"

class Log:
    def __init__(self,_msg,_log_type=0):
        FORMAT = "%(levelname)s: %(asctime)-15s %(message)s"
        logging.basicConfig(filename='data/network.mylog',level=logging.DEBUG, format = FORMAT)

        if _log_type == 0: #info debug
            logging.info(_msg)
        elif _log_type == 1:
            logging.warning(_msg)

    def mylog(self,msg,log_type):
        if log_type:
            print "Log"
            #self.logger.info(self.msg)

