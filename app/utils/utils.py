import json
import sys
import subprocess
import os


def get_system_load():
    avgs = os.getloadavg()
    return {'load1': avgs[0], 'load5': avgs[1], 'load15': avgs[2]}


def get_ram_load():
    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:])
    return {'total': total_memory, 'used': used_memory, 'free': free_memory}


# executes a shell command and captures output
# See shell.py of the naked toolshed (https://github.com/chrissimpkins/naked/blob/master/lib/Naked/toolshed/shell.py)


async def execute_command(cmd: str):
    try:
        proc = subprocess.Popen(cmd, shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                bufsize=1)
        out, err = proc.communicate()
        print("returning execution artifacts")
        return (proc, out, err)
    except subprocess.CalledProcessError as cpe:
        try:
            sys.stderr.write(cpe.output)
        except TypeError as te:
            sys.stderr.write(str(cpe.output))
    except Exception as e:
        sys.stderr.write(
            "unable to run the shell command with the execute() function.")
        raise e


def execute_python_command(pythonbin, rootdir, pyfile, args, kwargs):
    cwd = rootdir
    code = pyfile
    cmdargs = [arg for arg in args]
    for kwarg in kwargs.keys():
        cmdargs.append("-%s" % kwarg)
        cmdargs.append("%s" % kwargs[kwarg])
    proc_args = [pythonbin, code, *cmdargs]
    return execute(proc_args, cwd)
