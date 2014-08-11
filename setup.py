#!/usr/bin/env python
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT
from setuptools import setup, find_packages

# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215


__author__ = 'Hardy.zheng'
__version = '0.1'

setup(
    name='vnicagent',
    version=__version,
    description='cds-agent ',
    author='hardy.Zheng',
    author_email='wei.zheng@cds.com',
    install_requires=[
        'oslo.messaging>=1.3.0',
        'lxml>=2.3',
        'jsonschema>=2.0.0,<3.0.0',
        'jsonpath-rw>=1.2.0,<2.0',
        'anyjson>=0.3.3'],

    entry_points={
        'in_pulgin': [
            'mongodb = cdsagent.plugin.mongodb.Connection'],
        'outpulgin': [
            'mysqldb = cdsagent.plugin.mysqldb.Connection'],
        'float_ip': [
            'openstack_api = cdsagent.vnic.novaapi.Client',
            'cds-mysql = cdsagent.vnic.cdsapi.Client']},
    packages=find_packages('cdsagent'),
    package_dir={'': 'cdsagent'},
    namespace_packages=['cdsagent'],
    include_package_data=True)
