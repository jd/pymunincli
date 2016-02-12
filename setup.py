#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright © 2012  Julien Danjou <julien@danjou.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import setuptools

setuptools.setup(
    name="pymunincli",
    version="0.2",
    author="Julien Danjou",
    author_email="julien@danjou.info",
    description="munin client library",
    license="GPL",
    url="http://julien.danjou.info/software/pymunincli/",
    packages=['munin'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python"
    ],
    test_suite="test",
)
