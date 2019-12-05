#!/usr/bin/env python

from setuptools import setup

package_name = 'catmux'

setup( name=package_name,
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    scripts=['script/create_session'],
    package_dir={'': 'src'}
)
