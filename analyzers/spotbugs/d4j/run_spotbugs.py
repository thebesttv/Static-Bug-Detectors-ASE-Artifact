import inspect
import os
import sys

from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
sys.path.insert(0, parent_dir)
import utils

MODIFY_BUILD_XML_SCRIPT='modify_build_xml.py'
MODIFY_POM_XML_SCRIPT='modify_pom.py'
BUGS_DIR='../../results/sb-proj-files'
REPORTS_DIR='../../results/sb-proj-reports'


def _run_command(command: str):
    return utils.run_command(command)


def run_spotbugs(bug_id: str, build_script: str, low_or_high: str):
    for b_or_f in ['b', 'f']:
        bug_id_dir = os.path.join(BUGS_DIR, bug_id + b_or_f)   # e.g. Chart-14b, Chart-14f
        report_dir = os.path.join(REPORTS_DIR, bug_id, b_or_f) # e.g. Chart-14/b, Chart-14/f
        report_dir_path = Path(report_dir).absolute()
        mkdir_cmd = 'mkdir -p {}'.format(report_dir)
        _, _, _, ok = _run_command(mkdir_cmd)
        if build_script == 'build.xml':
            cmd = 'python3 -u {} {} {}'.format(MODIFY_BUILD_XML_SCRIPT, os.path.join(bug_id_dir, build_script), low_or_high)
            _, stdout, stderr, ok = _run_command(cmd)
            compile_cmd = 'cd {} && ant compile && ant spotbugs'.format(bug_id_dir)
            _, sb_output, stderr, ok = _run_command(compile_cmd)
            cp_cmd = 'cp {}/spotbugsXml.xml {}'.format(bug_id_dir, report_dir_path)
            _, _, _, _ = _run_command(cp_cmd)
        else:                   # pom.xml
            cmd = 'python3 -u {} {} {}'.format(MODIFY_POM_XML_SCRIPT, os.path.join(bug_id_dir, build_script), low_or_high)
            _, stdout, stderr, ok = _run_command(cmd)
            compile_cmd = 'cd {} && mvn test-compile compile'.format(bug_id_dir)
            _, sb_output, stderr, ok = _run_command(compile_cmd)
            sb_cmd = 'cd {} && mvn com.github.spotbugs:spotbugs-maven-plugin:3.1.6:spotbugs'.format(bug_id_dir)
            _, sb_output, stderr, ok = _run_command(sb_cmd)
            cp_cmd = 'pwd && cd {} && pwd && cp target/spotbugsXml.xml {}'.format(bug_id_dir, report_dir_path)
            _, stdout, stderr, _ = _run_command(cp_cmd)
        print('Copied spotbugsXml.xml to {}'.format(report_dir_path))


def _print_usage():
    print('Usage: python3 run_spotbugs.py <bug_ids_file> <h_or_l>')
    print('bug_ids_file: Path to a file containing a csv-separated list of (bug ids, build script to process).')


def _validate_input(argv):
    if len(argv) != 3:
        _print_usage()
        sys.exit(1)
    fp = argv[1]
    low_or_high = argv[2]
    return fp, low_or_high

def main(argv=None):
    argv = argv or sys.argv

    bugs_fp, low_or_high = _validate_input(argv)
    global BUGS_DIR
    global REPORTS_DIR
    effort = 'lt' if low_or_high == 'low' else 'ht'
    BUGS_DIR='../../results/sb{}-proj-files'.format(effort)
    REPORTS_DIR='../../results/sb{}-proj-reports'.format(effort)

    bug_tuples = []
    with open(bugs_fp) as f:
        # Example:
        #   Chart-14,build.xml
        #   Lang-33,pom.xml
        bug_tuples = [bug.strip().split(',') for bug in f.readlines()]

    for bug in bug_tuples:
        print(bug[0], bug[1])
        run_spotbugs(bug[0], bug[1], low_or_high)

if __name__ == '__main__':
    sys.exit(main())

