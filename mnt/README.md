This should be your app root, insyall apps here.
Contents of this dir, other than this README, are not checked into source control.

The config file for your tools should be here.
If you had two tools, called "hello" and "time", the config file might look like:

{
    "hello": {
        "dir": "/mnt/hello/",
        "cmd": "python",
        "args": [ "hello.py" ]
    },
    "time": {
        "dir": "/mnt/time",
        "cmd": "python",
        "args": [ "time.py" ]
    }
}