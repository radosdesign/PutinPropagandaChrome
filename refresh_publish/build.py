#!/usr/bin/env python

'''
PREREQUISITIES
--------------
 - Git
 - Npm
 - Python
'''

import subprocess, os
import webstore_upload


def log(message):
    '''
    Print message to the standard output
    '''

    print
    print(message)
    print


def build_dist_package():
    '''
    Refresh sites.js, build distribution package and upload it to webstore
    '''

    log('--> Update GIT repo')
    subprocess.call(["git", "pull"], cwd='../')

    log('--> Install node modules')
    subprocess.call(["npm", "install"], cwd='../')

    log('--> Update sites')
    subprocess.call(["node", "generate-sites.js"], cwd='../')

    log('--> Create distribution binary file')
    subprocess.call(["grunt"], cwd='../')

    log('--> Update extension in Webstore')
    os.environ["WEBSTORE_SECRETS_FILE"] = "webstore.json"
    os.environ["WEBSTORE_OAUTH2_FILE"] = "oauth2.dat"
    webstore_upload.do_upload()

    log('--> Push changes to GIT repo')
    subprocess.call(["git", "add", "version"], cwd='../')
    subprocess.call(["git", "add", "extension/sites.js"], cwd='../')
    subprocess.call(["git", "commit", "-m", "Version updated"], cwd='../')
    subprocess.call(["git", "push"], cwd='../')


if __name__ == '__main__':
    build_dist_package()
