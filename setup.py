#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    setup.py - Distutil setup script for PyVISA
#
#    Copyright © 2005 Gregor Thalhammer <gth@users.sourceforge.net>,
#		      Torsten Bronger <bronger@physik.rwth-aachen.de>.
#
#    This file is part of PyVISA.
#
#    PyVISA is free software; you can redistribute it and/or modify it under
#    the terms of the GNU General Public License as published by the Free
#    Software Foundation; either version 2 of the License, or (at your option)
#    any later version.
#
#    pyvisa is distributed in the hope that it will be useful, but WITHOUT ANY
#    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#    FOR A PARTICULAR PURPOSE.	See the GNU General Public License for more
#    details.
#
#    You should have received a copy of the GNU General Public License along
#    with pyvisa; if not, write to the Free Software Foundation, Inc., 59
#    Temple Place, Suite 330, Boston, MA 02111-1307 USA
#

from distutils.core import setup
import shutil, os.path, atexit

def prune_tree(path):
    try:
	shutil.rmtree(path)
    except OSError:
	pass

prune_tree("build")

# The following code may be very specific to my own home configuration,
# although I hope that it's useful to other who try to create PyVISA packages,
# too.
#
# The goal is to override an existing local RPM configuration.  Distutils only
# works togather with a widely untouched configuration, so I have to disable
# any extisting one represented by the file ~/.rpmmacros.  I look for this file
# and move it to ~/.rpmmacros.original.  After setup.py is terminated, this
# renaming is reverted.
#
# Additionally, if a file ~/.rpmmacros.distutis exists, it is used for
# ~/.rpmmacros while setup.py is running.  So you can still make use of things
# like "%vendor" or "%packager".

home_dir = os.environ['HOME']
real_rpmmacros_name = os.path.join(home_dir, '.rpmmacros')
distutils_rpmmacros_name = os.path.join(home_dir, '.rpmmacros.distutils')
temp_rpmmacros_name = os.path.join(home_dir, '.rpmmacros.original')

def restore_rpmmacros():
    shutil.move(temp_rpmmacros_name, real_rpmmacros_name)

# I check wheter temp_rpmmacros_name exists for two reasons: First, I don't
# want to overwrite it, and secondly, I don't want this renaming to take place
# twice.  This would happen otherwise, because setup.py is called more than
# once per building session.
if os.name == 'posix' and os.path.isfile(real_rpmmacros_name) and \
	not os.path.isfile(temp_rpmmacros_name):
    shutil.move(real_rpmmacros_name, temp_rpmmacros_name)
    if os.path.isfile(distutils_rpmmacros_name):
	shutil.copy(distutils_rpmmacros_name, real_rpmmacros_name)
    atexit.register(restore_rpmmacros)


setup(name = 'pyvisa',
      description = 'Python support for the VISA I/O standard',
      version = '0.2',
      long_description = \
      """A Python package for support of the "Virtual Instrument Software
Architecture" (VISA), in order to control measurement devices and test
equipment via GPIB, RS232, or USB.""",
      author = 'Gregor Thalhammer, Torsten Bronger',
      author_email = 'Gregor.Thalhammer@uibk.ac.at',
      maintainer_email = 'pyvisa-devel@lists.sourceforge.net',
      url = 'http://pyvisa.sourceforge.net',
      download_url = 'http://sourceforge.net/projects/pyvisa/',
      keywords = 'VISA GPIB USB serial RS232 measurement acquisition',
      license = 'GNU General Public License',
      classifiers = [
	'Development Status :: 4 - Beta',
	'Intended Audience :: Developers',
	'Intended Audience :: Science/Research',
	'License :: OSI Approved :: GNU General Public License (GPL)',
	'Operating System :: Microsoft :: Windows',
	'Operating System :: POSIX :: Linux',
	'Programming Language :: Python',
	'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
	'Topic :: Software Development :: Libraries :: Python Modules',
	],
      package_dir = {'visa': 'src'},
      packages = ['visa'])
