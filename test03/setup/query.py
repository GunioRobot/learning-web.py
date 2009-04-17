# -*- coding: utf-8 -*-
u'''
setup database
'''

__version__ = u'200904171930'

SETUP_QUERY = (
u'''

CREATE TABLE `res` (
  `id` INTEGER NOT NULL PRIMARY KEY,
  `thread_id` INTEGER NOT NULL,
  `name` TEXT NOT NULL,
  `message` TEXT NOT NULL,
  `create_time` TEXT NOT NULL
);

CREATE TABLE `thread` (
  `id` INTEGER NOT NULL PRIMARY KEY,
  `title` TEXT NOT NULL,
  `make_time` TEXT NOT NULL,
  `update_time` TEXT NOT NULL
);

CREATE TABLE `token` (
  `id` INTEGER NOT NULL PRIMARY KEY,
  `thread_id` INTEGER NOT NULL,
  `res_id` INTEGER NOT NULL,
  `token` TEXT NOT NULL,
  `create_time` TEXT NOT NULL
);

CREATE INDEX `t_k` ON `thread`(`title`);
CREATE INDEX `tid_k` ON `res`(`thread_id`);
CREATE INDEX `to_tid_k` ON `token`(`thread_id`);
CREATE INDEX `to_rid_k` ON `token`(`res_id`);

''')
