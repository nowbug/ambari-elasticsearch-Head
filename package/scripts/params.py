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

from resource_management import *
import os

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()

head_user = config['configurations']['head-env']['head_user']
head_group = config['configurations']['head-env']['head_group']

head_install_dir = config['configurations']['head-env']['head_install_dir']
es_port = config['configurations']['head-config']['es_port']
