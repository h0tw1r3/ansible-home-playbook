#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) 2021, Jeffrey Clark <h0tw1r3@btolab.com>
#

import argparse
import getpass
import subprocess
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get a vault password from user keyring')

    parser.add_argument('--vault-id', action='store', default=None,
                        dest='vault_id',
                        help='name of the vault secret to get from keyring')
    parser.add_argument('--set', action='store_true', default=False,
                        dest='set_password',
                        help='set the password instead of getting it')
    args = parser.parse_args()

    keyname = 'ansible-%s' % (args.vault_id or 'default');

    if args.set_password:
        password = getpass.getpass().rstrip()
        confirm = getpass.getpass('Confirm password: ')
        if password == confirm:
            subprocess.Popen("keyctl add user {} '{}' @s".format(keyname, password), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            print('Passwords do not match', file=sys.stderr)
            raise SystemExit(1)
    else:
        try:
            keyid = int(subprocess.Popen("keyctl request user {} @s".format(keyname), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read())
        except ValueError:
            print('Key not found: %s' % (keyname), file=sys.stderr)
            raise SystemExit(2)

        secret = subprocess.Popen("keyctl print {}".format(keyid), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read().rstrip()

        print(secret.decode('utf-8'))
