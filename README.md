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

### Running
To run the web interface, just for testing or a low usage/no secruity server, run
`python manage.py runserver` from within the django root folder.

To collect results you need to run a celery worker process, by default (can change in the settings.py file)
it will run every seven seconds.
`python manage.py celery worker -B -l info -Q beats`

Setting up crackling
--------------------
### Requirements
#### Python packages
- celery

#### Binary
- Hashcat (http://hashcat.net/hashcat/)
- oclHashcat-lite (http://hashcat.net/oclhashcat-lite/)

### Setup
#### config.py
- Configure `CRACKLING_BROKER`, `CRACKLING_BACKEND` to point to the
location of the rabbitmq amqp server.
- Configure `HASHCAT_PATH`, `OCLLITE_PATH` with the location of hashact and
oclhashcat-lite respectively.

#### hashcat
- Run hashcat and ocllite and accept the licence so that the `eula.accepted` file is
created in the same folder as the hashcat binary.

### Running
Back one directory from the crackling folder (in p0rk-crackling/ if you just grabbed off github)
run `celery worker --app=crackling -l info -Q crackling`
