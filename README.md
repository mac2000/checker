checker
=======

checker

Soft
====

supervisor
python-pycurl
python-pyquery
python-lxml
python-mysqldb

rabbitmq-server (requires additional repositories)

RabbitMQ
========

requeue example
http://gavinroy.com/deeper-down-the-rabbit-hole-of-message-redeli

Supervisor
==========

	[inet_http_server]
	port = *:9001
	username = checker
	password = *******

	[supervisorctl]
	;serverurl=unix:///tmp/supervisor.sock 
	serverurl=http://127.0.0.1:9001

	[include]
	files = /etc/supervisor/conf.d/*.conf /home/mac/supervisor/*.conf
