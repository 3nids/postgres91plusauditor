# About

Postgres 91 plus Auditor is [QGIS](http://www.qgis.org) plugin providing an interface to rollback on postgis layers using the [Audit Trigger 91 plus](http://wiki.postgresql.org/wiki/Audit_trigger_91plus)


# The Audit Trigger 91 plus

The [Audit Trigger 91 plus](http://wiki.postgresql.org/wiki/Audit_trigger_91plus) is a generic trigger function used for recording changes to tables into an audit log table. It records quite a bit more detail than the [older](http://wiki.postgresql.org/wiki/Audit_trigger) Audit trigger and does so in a more structured manner.

The trigger should be up-to-date on Postgres website but the trgger code lives on [github](https://github.com/2ndQuadrant/audit-trigger).

Follow the setps described on Postgres wiki to install and use the trigger.

# Rolling-back

The plugin allows you to
