import json
import sys
import subprocess, os

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
        sys.stderr.write("unable to run the shell command with the execute() function.")
        raise e