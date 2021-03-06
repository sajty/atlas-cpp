#!/usr/bin/env python
#setup script used by distutils

#Copyright 2002 by Michael Koch <konqueror@gmx.de>
#Copyright 2002 by AIR-IX SUUNNITTELU/Ahiplan Oy

#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.

#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from distutils.core import setup

setup(name="Atlas-Python",
	version="0.2.9",
	description="Python Atlas library",
	author="Aloril",
	author_email="aloril@iki.fi",
	url="http://www.worldforge.org/dev/eng/protocols/",
	packages=['atlas', 'atlas.transport', 'atlas.transport.TCP', 'atlas.codecs', 'atlas.util'],
	package_dir={'atlas':'atlas'}
)
