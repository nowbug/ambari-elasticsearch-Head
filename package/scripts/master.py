#!/usr/bin/env python

"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import os
import glob
import pwd
import grp
import signal
import time
from resource_management import *
from resource_management.core import sudo


class Master(Script):
    # Install Elasticsearch
    def install(self, env):
        import params

        env.set_params(params)

        self.install_packages(env)

        # Create user and group for Elasticsearch if they don't exist
        try:
            grp.getgrnam(params.head_group)
        except KeyError:
            Group(group_name=params.head_group)

        try:
            pwd.getpwnam(params.head_user)
        except KeyError:
            User(username=params.head_user,
                 gid=params.head_group,
                 groups=[params.head_group],
                 ignore_failures=True
                 )

        # Create Elasticsearch Head install dir
        Directory([params.head_install_dir],
                  mode=0755,
                  owner=params.head_user,
                  group=params.head_group,
                  create_parents=True
                  )

        cmd = format("cd {head_install_dir}; git clone git://github.com/mobz/elasticsearch-head.git")
        Execute(cmd)

        # fast install phantomjs"
        cmd = format("cd {head_install_dir}/elasticsearch-head; npm install phantomjs-prebuilt@2.1.14 --ignore-script")
        Execute(cmd)

        # Install Elasticsearch head
        cmd = format("cd {head_install_dir}/elasticsearch-head;npm install")
        Execute(cmd)

        Execute('echo "Install complete"')

    def configure(self, env):
        import params

        env.set_params(params)
        config = Script.get_config()
        configurations = params.config['configurations']['elastic-config']

        File(format("{head_install_dir}/elasticsearch-head/_site/app.js"),
             content=Template("app.js.j2",
                              configurations=configurations
                              ),
             owner='root', group='root'
             )

        Execute('echo "Configuration complete"')

    def stop(self, env):
        import params

        env.set_params(params)

        # Stop Elasticsearch
        Execute('sudo ps -ef| grep grunt  |grep -v "grep"|cut -c 9-15 |xargs kill -9')

    def start(self, env):
        import params
        env.set_params(params)

        # Configure Elasticsearch
        self.configure(env)

        # Start Elasticsearch
        num = 'cd /usr/share/head/elasticsearch-head;nohup npm run start&'
        files = os.popen(num)
        pid = os.fork()
        if pid == 0:
            files.read()
        print pid
        time.sleep(1)

    def status(self, env):
        import status_params
        env.set_params(status_params)
        cmd = 'sudo ps -ef | grep grunt  | grep -v "grep" | wc -l'
        num = os.popen(cmd).read()
        if int(num) < 1:
            check_process_status(True)


if __name__ == "__main__":
    Master().execute()
