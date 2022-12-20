"""
This script performs the following steps when run inside an artifact container:
  1. Modify a Maven project's POM to include the SpotBugs plugin.
  2. Generate SpotBugs reports by invoking the Maven build for the project.
  3. Copy the reports to the container-side sandbox to make them available from the host.

Requirements:
  1. This script is run with Python 2.x.
  2. This script is run inside an artifact container.
  3. This script is run from inside either the failed or passed repositories in the artifact container.
  4. The Python script that modifies the POM is in the same directory as this script.

"""

import os
import shutil
import subprocess
import sys


def main(argv=None):
    argv = argv or sys.argv

    image_tag, container_sandbox, modify_pom_script, f_or_p, l_or_h = _validate_input(argv)

    # Install dependencies for modifying the POM.
    _pip_install('beautifulsoup4')
    _pip_install('lxml')

    # Modify the POM.
    modify_command = 'python {} pom.xml {}'.format(modify_pom_script,l_or_h)
    _, stdout, stderr, ok = _run_command(modify_command)
    if not ok:
        _print_error('Failed to modify the POM. Exiting.', stdout, stderr)
        sys.exit(1)
    else:
        print('Modified the POM.')

    # Determine if project is Maven or Gradle


    # Compile project
    mvn_bin_pth = _get_maven_binary_path()
    compile_command = '{} test-compile compile'.format(mvn_bin_pth)
    _, stdout, stderr, _ = _run_command(compile_command)
    _print_error('Attempted to compile project.', stdout, stderr)
    # Install project dependencies
    _, stdout, stderr, _ = _run_command('{} clean install -U -DskipTests'.format(mvn_bin_pth))
    _print_error('Attempted to install project dependencies.', stdout, stderr)
    # Copy test .class files into classes folder
    _copy_test_classes_to_classes()
    # Generate SpotBugs reports.
    mvn_command = '{} com.github.spotbugs:spotbugs-maven-plugin:3.1.6:spotbugs'.format(mvn_bin_pth)
    _, stdout, stderr, _ = _run_command(mvn_command)
    # We cannot use the return code to determine success since the Maven command should always fail for failed jobs and
    # always pass for passed jobs. SpotBugs, we check stderr as a proxy.
    _print_error('Attempted to generate SpotBugs reports.', stdout, stderr)

    reports_destination = os.path.join(container_sandbox, image_tag, f_or_p)
    _copy_reports_to_sandbox(reports_destination)


def _run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8').strip()
    stderr = stderr.decode('utf-8').strip()
    ok = process.returncode == 0
    return process, stdout, stderr, ok


def _print_error(msg, stdout=None, stderr=None):
    print('Error: ' + msg)
    if stdout is not None:
        print('stdout:\n{}'.format(stdout.encode('utf-8')))
    if stderr is not None:
        print('stderr:\n{}'.format(stderr.encode('utf-8')))

def _find_pom():
    """
    Determine if the project is using the Maven build system by looking if there is a pom.xml file in the failed repo.
    :return: True if there is a pom.xml file in the failed repo, False otherwise.
    """
    cmd = 'find /home/travis/build/failed -name "pom.xml"'
    _, stdout, stderr, ok = _run_command(cmd)
    if ok:
        if len(stdout) != 0:
            return True
    return False

def _find_build_gradle():
    """
    Determine if the project is using the Gradle build system by looking if there is a build.gradle file in the failed repo.
    :return: True if there is a build.gradle file in the failed repo, False otherwise.
    """
    cmd = 'find /home/travis/build/failed -name "build.gradle"'
    _, stdout, stderr, ok = _run_command(cmd)
    if ok:
        if len(stdout) != 0:
            return True
    return False

def _copy_test_classes(directory):
    """
    """
    copy_command = 'cp -R {}/test-classes {}/classes'.format(directory, directory)
    _, stdout, stderr, ok = _run_command(copy_command)
    return stdout, stderr, ok


def _copy_test_classes_to_classes():
    """
    """
    _, stdout, stderr, ok = _run_command('find . -name "target"')
    if ok:
        target_list = stdout.split('\n')
        for target in target_list:
            has_classes = False
            has_test_classes = False
            for filename in  os.listdir(target):
                if filename == 'classes':
                    has_classes = True
                elif filename == 'test-classes':
                    has_test_classes = True
                if has_classes and has_test_classes:
                    stdout, stderr, ok = _copy_test_classes(target)
                    if not ok:
                        _print_error('Error copying test-classes', stdout, stderr)
    else:
        _print_error('Error finding target directories', stdout, stderr)
    # topdir = '.'
    # for currentdir, subdirs, files in os.walk(topdir):
    #     for f in files:
    #         if f == 'spotbugsXml.xml':
    #             src = os.path.join(currentdir, f)
    #             relative_path_to_file = os.path.relpath(os.path.join(currentdir, f), topdir)
    #             rel_path_split = relative_path_to_file.split('/')
    #             # target_index = rel_path_split.index('target')
    #             target_index = len(rel_path_split) - 2
    #             unique_fp_prefix = ''.join(rel_path_split[:target_index])
    #             dst = os.path.join(partial_destination, unique_fp_prefix, relative_path_to_file)
    #             # Make any needed directories.
    #             _py2_makedirs(dst)
    #             print('Copying {} to {}.'.format(src, dst))
    #             shutil.copy(src, dst)

def _copy_reports_to_sandbox(partial_destination):
    """
    Copy SpotBugs reports to the container-side sandbox. If needed, the destination directory is created in the
    container in the following format:
    <host-side sandbox>/<image_tag>/<'failed' or 'passed'>/<path to the original report, relative to repo_dir>

    Starts the recursive search for reports from the current directory.
    :param partial_destination: The destination without the path to the original report,
                                relative to the repository directory.
    """

    topdir = '.'
    for currentdir, subdirs, files in os.walk(topdir):
        for f in files:
            if f == 'spotbugsXml.xml':
                print('found spotbugsXml')
                src = os.path.join(currentdir, f)
                relative_path_to_file = os.path.relpath(os.path.join(currentdir, f), topdir)
                rel_path_split = relative_path_to_file.split('/')
                # target_index = rel_path_split.index('target')
                target_index = len(rel_path_split) - 2
                unique_fp_prefix = ''.join(rel_path_split[:target_index])
                dst = os.path.join(partial_destination, unique_fp_prefix, relative_path_to_file)
                dst = dst.encode('utf-8')
                # Make any needed directories.
                _py2_makedirs(dst)
                print('Copying {} to {}.'.format(src, dst))
                # shutil.copy(src, dst)
                try:
                    shutil.copy(src, dst)
                    print('Copied')
                except IOError, e:
                    print("Unable to copy file. {}".format(e))
                else:
                    print('Successfully copied file')

def _py2_makedirs(path):
    """
    Python 2 os.makedirs workaround that behaves similar to Python 3's os.makedirs with exist_ok=True.
    Removes the leaf part of the path before creating directories.
    """
    path, _ = os.path.split(path)
    command = 'mkdir -p {}'.format(path)
    _, stdout, stderr, ok  = _run_command(command)
    print('Creating directories',  stdout, stderr)
    if not ok:
        _print_error('Error creating directories', stdout, stderr)


def _get_maven_binary_path():
    """
    :return: The path to the Maven binary in the container.
    """
    command = 'find / -name mvn 2> /dev/null | sed -n 1p'
    _, stdout, stderr, ok = _run_command(command)
    first_line = stdout.splitlines()[0]
    if not ok:
        _print_error('Failed to get path to Maven binary. Exiting.', stdout, stderr)
        sys.exit(1)
    else:
        print('Got path to Maven binary: {}'.format(first_line))
    return first_line

def _get_gradle_binary_path():
    """
    :return: The path to the Gradle binary in the container.
    """
    command = 'find / -name gradle 2> /dev/null | sed -n 1p'
    _, stdout, stderr, ok = _run_command(command)
    first_line = stdout.splitlines()[0]
    if not ok:
        _print_error('Failed to get path to Gradle binary. Exiting.', stdout, stderr)
        sys.exit(1)
    else:
        print('Got path to Gradle binary: {}'.format(first_line))
    return first_line

def _pip_install(package):
    command = 'sudo pip install {}'.format(package)
    _, stdout, stderr, ok = _run_command(command)
    if not ok:
        _print_error('Failed to install {} with pip. Exiting.'.format(package), stdout, stderr)
        sys.exit(1)
    else:
        print('Installed {}.'.format(package))
    return ok


def _print_usage():
    print('Usage: python process.py <image_tag> <container_sandbox> <repo_dir> <modify_pom_script> <low-or-high>')
    print('repo_dir: The directory containing the actual failed or passed repository.')


def _validate_input(argv):
    if len(argv) != 6:
        _print_usage()
        sys.exit(1)
    image_tag = argv[1]
    container_sandbox = argv[2]
    modify_pom_script = argv[3]
    f_or_p = argv[4]
    l_or_h = argv[5]
    # Test the container sandbox, but not the host sandbox, argument since this script is run inside a container and
    # therefore cannot verify the host sandbox argument.
    if not os.path.isdir(container_sandbox):
        print('The container_sandbox argument ({}) is not a directory or does not exist. Exiting.'
              .format(container_sandbox))
        _print_usage()
        sys.exit(1)
    if f_or_p not in ['failed', 'passed']:
        print('The f_or_p argument must be either "failed" or "passed". Exiting.')
        _print_usage()
        sys.exit(1)
    return image_tag, container_sandbox, modify_pom_script, f_or_p, l_or_h


if __name__ == '__main__':
    sys.exit(main())
