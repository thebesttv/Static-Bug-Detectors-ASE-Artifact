import subprocess


def run_command(command):
    def capture_stdout_stderr_live(process):
        import sys
        import selectors

        sel = selectors.DefaultSelector()
        sel.register(process.stdout, selectors.EVENT_READ)
        sel.register(process.stderr, selectors.EVENT_READ)

        stdout = ''
        stderr = ''

        # live output both stdout & stderr while preserving order
        # https://stackoverflow.com/a/56918582
        while True:
            for key, _ in sel.select():
                data = key.fileobj.read1().decode()
                if not data:
                    return stdout.strip(), stderr.strip()
                if key.fileobj is process.stdout:
                    print(data, end="")
                    sys.stdout.flush()
                    stdout += data
                else:
                    print(data, end="", file=sys.stderr)
                    stderr += data

    process = subprocess.Popen(command, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)

    stdout, stderr = capture_stdout_stderr_live(process)
    ok = process.returncode == 0
    return process, stdout, stderr, ok


def print_error(msg, stdout=None, stderr=None):
    print('Error: ' + msg)
    if stdout is not None:
        print('stdout:\n{}'.format(stdout))
    if stderr is not None:
        print('stderr:\n{}'.format(stderr))


def container_running(container_name):
    cmd = 'docker ps -a | grep {}'.format(container_name)
    _, stdout, stderr, ok = run_command(cmd)
    if not ok:
        return False
    if container_name in stdout:
        return True
    return False

