# (c) 2012-2013 Continuum Analytics, Inc. / http://continuum.io
# All Rights Reserved
#
# conda is distributed under the terms of the BSD 3-clause license.
# Consult LICENSE.txt or http://opensource.org/licenses/BSD-3-Clause.

import os
import sys
from platform import machine
from os.path import abspath, expanduser, isfile, join



default_python = '2.7'
default_numpy = '1.7'

# ----- constant paths -----

root_dir = sys.prefix
pkgs_dir = join(root_dir, 'pkgs')
envs_dir = join(root_dir, 'envs')

# ----- default environment prefix -----

_default_env = os.getenv('CONDA_DEFAULT_ENV')
if not _default_env:
    default_prefix = root_dir
elif os.sep in _default_env:
    default_prefix = abspath(_default_env)
else:
    default_prefix = join(envs_dir, _default_env)

# ----- operating system and architecture -----

_sys_map = {'linux2': 'linux', 'linux': 'linux',
            'darwin': 'osx', 'win32': 'win'}
platform = _sys_map.get(sys.platform, 'unknown')
bits = 8 * tuple.__itemsize__

if platform == 'linux' and machine() == 'armv6l':
    subdir = 'linux-armv6l'
    arch_name = 'armv6l'
else:
    subdir = '%s-%d' % (platform, bits)
    arch_name = {64: 'x86_64', 32: 'x86'}[bits]

# ----- rc file -----

def get_rc_path():
    for path in [abspath(expanduser('~/.condarc')),
                 join(sys.prefix, '.condarc')]:
        if isfile(path):
            return path
    return None

rc_path = get_rc_path()

def load_condarc(path):
    import yaml

    return yaml.load(open(path))

# ----- channels -----

def get_channel_urls():
    if os.getenv('CIO_TEST'):
        base_urls = ['http://filer/pkgs/pro',
                     'http://filer/pkgs/free']
        if os.getenv('CIO_TEST') == '2':
            base_urls.insert(0, 'http://filer/test-pkgs')

    elif rc_path is None:
        base_urls = ['http://repo.continuum.io/pkgs/free',
                     'http://repo.continuum.io/pkgs/pro']

    else:
        rc = load_condarc(rc_path)
        if 'channels' not in rc:
            sys.exit("Error: config file '%s' is missing channels" % rc_path)
        base_urls = [url.rstrip('/') for url in rc['channels']]

    return ['%s/%s/' % (url, subdir) for url in base_urls]
