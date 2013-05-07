# About

Postgres 91 plus Auditor is [QGIS](http://www.qgis.org) plugin providing an interface to rollback on postgis layers using the [Audit Trigger 91 plus](http://wiki.postgresql.org/wiki/Audit_trigger_91plus)


# The Audit Trigger 91 plus

The [Audit Trigger 91 plus](http://wiki.postgresql.org/wiki/Audit_trigger_91plus) is a generic trigger function used for recording changes to tables into an audit log table. It records quite a bit more detail than the [older](http://wiki.postgresql.org/wiki/Audit_trigger) Audit trigger and does so in a more structured manner.

The trigger should be up-to-date on Postgres website but the trigger code lives on [github](https://github.com/2ndQuadrant/audit-trigger).

Follow the setps described on Postgres wiki to install and use the trigger.

# Rolling-back

The plugin allows you to rollback individual features. It is more aimed at correcting editing errors than viewing a whole dataset at a previous state.
You can restore or recreate a feature from any logged action. The rollback will not erase the logged actions but rather create a new state. In other words, the rollbacks is considered as an update and a new row will therefore be added to the logged actions table.
Hence, even a rollback can be rollbacked.

# Plugin setup

Once ou have enabled the trigger, just add the *logged_actions* table as a no geometry layer. Then, _define the logged actions layer_ from the plugin menu.

The option **Redefine layer subset to increase performance** is recommended. While looking for actions, instead of looping over all rows it will redefine a SQL layer subset which is drastically faster.

# Use the plugin

You can start looking for any changes by clicking the plugin icon ![](https://raw.github.com/3nids/postgres91plusauditor/master/icons/qaudit-64.png). Choose a layer and eventually specify a feature ID.
Restrictions can be set to search insert/update/delete action, only geometry changes or by date.

You can also search for a specific feature changes, by right-clicking on the feature edit form and choosing _History audit_.

Once logged actions have been found, click on a row to see the differences with current feature if it exists.

If the corresponding layer is in editing mode, the feature can be reset.





