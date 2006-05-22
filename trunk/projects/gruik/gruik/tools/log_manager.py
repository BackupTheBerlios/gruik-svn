#!/usr/bin/python

import logging
import logging.config

logging.config.fileConfig("/etc/gruik/logging.conf")
logger = logging.getLogger("main")


