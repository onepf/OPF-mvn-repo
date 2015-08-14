#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import getopt
from os.path import realpath
from os.path import join
from os.path import basename
import subprocess

help_message = \
    'mvn-push.py --group package --id package --version version --file file [--javadoc file|path] [--sources file]'
mvn_repo = os.getcwd()

cleanup = ''


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               shell=True)
    proc_stdout = process.communicate()[0].strip()
    if proc_stdout:
        print proc_stdout


def check_required(arg_value_name_pairs):
    for pair in arg_value_name_pairs:
        if not pair[0]:
            print pair[1], 'is empty or invalid'
            sys.exit(1)


def detect_packaging(file_path):
    file_extension = file_path[-4:]
    if file_extension == '.aar':
        return 'aar'
    elif file_extension == '.jar':
        return 'jar'
    else:
        print 'wrong file extension'
        sys.exit(1)


def pack_javadoc(file_path, javadoc):
    if not javadoc:
        return javadoc
    else:
        global cleanup
        temp_jar = basename('%s-javadoc.jar' % file_path[:-4])
        subprocess_cmd('cd {0}; jar cf {1} *'.format(javadoc, temp_jar))
        cleanup = cleanup + ' ' + join(javadoc, temp_jar)
        return join(javadoc, temp_jar)


def deploy(
    group_id,
    artifact_id,
    version,
    file_path,
    javadoc,
    sources,
    packaging,
    ):
    mvn_deploy = \
        'mvn deploy:deploy-file -Durl=file://{0} -DgroupId={1} -DartifactId={2} -Dversion={3} -Dpackaging={4} -Dfile={5}'.format(
        mvn_repo,
        group_id,
        artifact_id,
        version,
        packaging,
        file_path,
        )

    if sources:
        mvn_deploy += ' -Dsources=%s' % sources
    if javadoc:
        mvn_deploy += ' -Djavadoc=%s' % javadoc
    subprocess_cmd(mvn_deploy)


def main(argv):
    group_id = ''
    artifact_id = ''
    version = ''
    file_path = ''
    javadoc = ''
    sources = ''

    try:
        (opts, args) = getopt.getopt(argv, 'h:', [
            'group=',
            'id=',
            'version=',
            'file=',
            'javadoc=',
            'sources=',
            ])
    except getopt.GetoptError:
        print help_message
        sys.exit(1)

    if len(opts) == 0:
        print help_message
        sys.exit(1)

    for (opt, arg) in opts:
        if opt == '-h':
            print help_message
            sys.exit()
        elif opt == '--group':
            group_id = arg
        elif opt == '--id':
            artifact_id = arg
        elif opt == '--version':
            version = arg
        elif opt == '--file':
            file_path = realpath(arg)
        elif opt == '--javadoc':
            javadoc = realpath(arg)
        elif opt == '--sources':
            sources = realpath(arg)

    check_required(((group_id, 'group'), (artifact_id, 'id'), (version,
                   'version'), (file_path, 'file')))
    packaging = detect_packaging(file_path)
    javadoc = pack_javadoc(file_path, javadoc)
    deploy(
        group_id,
        artifact_id,
        version,
        file_path,
        javadoc,
        sources,
        packaging,
        )
    subprocess_cmd('rm %s' % cleanup)


if __name__ == '__main__':
    main(sys.argv[1:])
