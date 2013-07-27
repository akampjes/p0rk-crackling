p0rk-crackling
==============

Distributed password cracker for operating over high latency networks of loosely coupled hosts.

Complete docs, coming soon to a repo near you.

Setting up p0rk
---------------
### Requirements:
#### System packages
- rabbitmq-server
- your database of choice (postgresql, mysql or sqllite)

#### Python packages.
You can use pip install to download them
- django
- django-celery
- django-dajax
- database package, eg. psycopg2 (for postgresql)

### Setup
Create new a new user and database for p0rk eg.
```
$ psql template1
> create user p0rk with password 'p0rkpassword';
> create database p0rkcrackling;
> grant all privileges on database p0rkcrackling to p0rk;
```
Remember to set database setings in the p0rk/settings.py file.

Tell p0rk to setup the database

`$ python manage.py syncdb`

Keep in mind that amqp running on rabbitmq should probably have a password set.


### Security note
Currently there is no security authentication or authorization built into p0rk-crackling.
I recommend that you run it only on trusted networks or within a VPN.



Setting up crackling
--------------------
