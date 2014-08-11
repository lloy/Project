#
# Copyright 2013 Julien Danjou
# Copyright 2014 Red Hat, Inc
#
# Authors: Julien Danjou <julien@danjou.info>
#          Eoghan Glynn <eglynn@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


# from stevedore import extension

from cdsagent.log import LOG
from cdsagent import cfg
from cdsagent import service as os_service


tasks = {
    'nic': lambda: task_nic(),
    'disk': lambda: task_disk(),
    'load': lambda: task_load()}


def task_nic():
    LOG.info("i' am nic task")


def task_disk():
    LOG.info("i' am disk task")


def task_load():
    LOG.info("i' am load task")


class AgentManager(os_service.Service):

    def start(self):
        for task in tasks:
            s = getattr(cfg.CONF, task, 60)
            if isinstance(s, cfg.Section):
                interval = int(s.interval)
            else:
                interval = s
            self.tg.add_timer(interval,
                              self.interval_task,
                              task=tasks[task])

    @staticmethod
    def interval_task(task):
        task()
