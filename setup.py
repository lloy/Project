#!/usr/bin/env python

from setuptools import setup, find_packages


__author__ = 'Hardy.zheng'
__version = '0.1'

setup(
    name='cdsagent',
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
    packages=find_packages('cdsagent'),
    entry_points={
        'fetch': [
            'mongodb = cdsagent.plugin.mongodb:Connection'],
        'push': [
            'mysqldb = cdsagent.plugin.mysqldb:Connection'],
        'float_ip': [
            'openstack_api = cdsagent.vnic.openstack_api:Client',
            'cds-mysql = cdsagent.vnic.cds_api:Client'],
        'nic': [
            'port = cdsagent.vnic.port:PortPoller'],
        'disk': [
            'openstack = cdsagent.vdisk.disk:DiskPoller']},
    package_dir={'': 'cdsagent'},
    include_package_data=True,
    namespace_packages=['cdsagent'])
