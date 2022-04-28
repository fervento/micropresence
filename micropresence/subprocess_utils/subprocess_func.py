"""
Module with utility functions to start and monitor subprocesses
"""

import logging
from subprocess import *

log = logging.getLogger(__name__)


def port_forward(specs, ssh_name):
    """
    function to reroute remote port to localhost trough ssh
    :param specs: services' specs
    :param ssh_name: ssh server as in ssh config
    :return: ssh subprocess' reference
    """
    ssh_args = ["ssh"]
    for spec in specs:
        ssh_args.append("-R")
        ssh_args.append("{}:localhost:{}".format(spec.target_port, spec.target_port))

    ssh_args.append(ssh_name)

    return Popen(ssh_args, stdin=PIPE)


def monitor_subprocess(process, timeout):
    """
    Function to monitor a subprocess for a finite amount of time wrapping in a try-except schema to trigger smooth exit
    from micropresence
    :param process: subprocess to monitor
    :param timeout: timeout for process.wait()
    :return: void
    """
    try:
        status = process.wait(timeout)
        raise Exception("Process {} terminated in status {}!".format(process.pid, status))
    except TimeoutExpired:
        pass


def terminate_subprocess(process):
    """
    Function to force termination of process param.
    :param process: process to be terminated
    :return:
    """

    return process.kill()


def sshuttle(ssh_name):
    """
    Function to set a sshuttle vpn towards specified host
    :param ssh_name: host to connect, must have a match in .ssh/config
    :return: sshuttle subprocess' reference.
    """
    return Popen(["sshuttle", "-N", "--ssh-cmd", ssh_name, "--dns"], stdin=PIPE)
