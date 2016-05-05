#!/usr/bin/python -u
###
# This file is part of Arduino Ciao
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Copyright 2016 Arduino Srl (http://www.arduino.org/)
#
# authors:
#	giuseppe@arduino.org
#	sergio@arduino.org
#
# notes: if you want to use gmail remember to turn on access for less
#	secure apps here: https://www.google.com/settings/u/2/security/lesssecureapps
###

#import smtplib, ciaotools, os
#from email.mime.text import MIMEText

import ciaotools, os, urllib, urllib2

# DEFINE CONNECTOR HANDLERS AND FUNCTIONS

# function to make request to Phant instance
def phant_request(url, pub_key, priv_key, data):
	#adding private key (phant) into the header of the request
	headers = { "Phant-Private-Key" : priv_key}

	#data is a key=value string separated by ";" char
	# it's simpler than a string separated by &, like in GET request
	data_hash = {}
	for element in data.split(";"):
		if element.strip():
			(key, value) = element.strip().split("=")
			data_hash[key] = value
		else:
			logger.debug("Empty element passed to connector: ignored!")

	#turn data_hash into URL encoded string for GET request
	data = urllib.urlencode(data_hash)
	req = urllib2.Request(url + pub_key, data, headers)
	try:
		response = urllib2.urlopen(req)
		result = response.read()
		logger.debug("Request answer: %s" % result)
	except Exception, e:
		logger.error("Request issue: %s" % e)


def handler(entry):
	if entry['type'] == "out":
		pub_key = str(entry['data'][0])
		if not pub_key:
			logger.warning("Missing public key, dropping message")
			return

		priv_key = str(entry['data'][1])
		if not priv_key:
			logger.warning("Missing private key, dropping message")
			return
		logger.debug("Private Key: %s" % priv_key)

		data = str(entry['data'][2])
		if not data:
			logger.warning("Missing data param, dropping message")
			return
		logger.debug("Phant Data: %s" % data)

		phant_request(phant_url, pub_key, priv_key, data)

# the absolute path of the connector
working_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep

# LOAD CONFIGURATION

# load configuration object with configuration file smtp.conf.json
config = ciaotools.load_config(working_dir)

# load parameters
phant_host = config["params"]["host"]
phant_port = config["params"]["port"]
phant_base_uri = config["params"]["base_uri"]

phant_url = phant_host + ":" + str(phant_port) + "/" + phant_base_uri

# name of the connector
name = config["name"]

# CREATE LOGGER

log_config = config["log"] if "log" in config else None
logger = ciaotools.get_logger(name, logconf=log_config, logdir=working_dir, async = True)

# CALL BASE CONNECTOR

#Call a base connector object to help connection to ciao core
ciao_connector = ciaotools.BaseConnector(name, logger, config["ciao"])

#register an handler to manage data from core/mcu
ciao_connector.receive(handler)

# start the connector thread
ciao_connector.start()
