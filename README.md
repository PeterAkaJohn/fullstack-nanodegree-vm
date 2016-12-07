rdb-fullstack
=============

Common code for the Relational Databases and Full Stack Fundamentals courses

#Usage:

 * have Vagrant and VirtualBox installed

 * then open the terminal in the directory and run `cd /vagrant` and then `vagrant up` followed by `vagrant ssh`

 * next run
 `cd /vagrant
  cd tournament
  psql
  create database tournament
  \c tournament
  \i tournament.sql`

 * press ctrl+z and then run `python tournament_test.py`
