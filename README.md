grazyna
=======

Grazyna the polish irc bot
Example config is in default_config.ini

install
=======

% python setup.py install
% python -m grazyna path_to_config.ini

Docker workflow
===============

You can use simple Docker workflow for fast hacking/testing Grazyna without installed Python on local machine.

- make your modifications to project
- docker build -f Dockerfile -t grazyna:dev .
- docker run -it --rm grazyna:dev
- test your Grazyna modifications on IRC #chan1, #chan2, #chan3
- stop Grazyna container (Ctrl-C)
- repeat

cleanup:
- docker system prune -a