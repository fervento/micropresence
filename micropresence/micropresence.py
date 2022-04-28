#! /usr/bin/python3
import argparse
import micropresence

from micropresence.kubernetes_utils import *
from micropresence.subprocess_utils import *

log = logging.getLogger(__name__)


class ServiceSpec(object):
    """
    Data structure for service specification
    """
    def __init__(self, service_name, port_name, target_port):
        super().__init__()
        self.service_name = service_name
        self.port_name = port_name
        self.target_port = target_port


def main(*args, **kwargs):
    """
    app main
    :param args: unused
    :param kwargs: unused
    :return: app exit code
    """
    return_code = 0

    parser = _parse()
    parsed = parser.parse_args()
    if parsed.version:
        return _version()
    child_processes = []

    selector = parsed.selector.split(":")

    if len(selector) != 2:
        parser.print_help()
        return 1

    selector_key = selector[0]
    selector_value = selector[1]

    specs = []
    for arg in parsed.args:
        params = arg.split(":")
        if len(params) == 3:
            specs.append(ServiceSpec(params[0], params[1], params[2]))
        else:
            log.debug("Arg {} is not valid, arguments must comply with <service_name>:<port_name>:<target_port> format."
                      .format(arg))
    namespace = parsed.namespace

    child_processes.append(port_forward(specs=specs, ssh_name=parsed.ssh_connection_name))
    if parsed.vpn:
        sshuttle(ssh_name=parsed.ssh_connection_name)
    update_services_for_micropresence(namespace, specs, selector_key=selector_key, selector_value=selector_value)

    try:
        while True:
            for p in child_processes:
                monitor_subprocess(p, 1)
    except Exception as e:
        return_code = e
    finally:
        [terminate_subprocess(p) for p in child_processes]
        restore_services_at_before_micropresence(namespace, specs)
        return return_code


def _version():
    """
    print version and exit
    :return: void
    """
    print(micropresence.__version__)
    return


def _parse(*args, **kwargs):
    """
    function to parse command line arguments
    :param args: unused
    :param kwargs: unused
    :return: defined ArgumentParser
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-V", "--version", help="print version and exit",
                        action="store_true")
    parser.add_argument("-n", "--namespace",
                        help="namespace for k8s' services, defaults to \'default\'",
                        default="default")
    parser.add_argument("-s", "--selector",
                        help="namespace for k8s' ssh service,"
                             " defaults to <\'app.kubernetes.io/name\'>:<\'ssh-service\'>",
                        default="app.kubernetes.io/name:ssh-server")
    parser.add_argument("-c", "--ssh-connection-name",
                        help="name for ssh connection to use for reverse port forwarding",
                        required=True)
    parser.add_argument("--vpn", help="flag to set up a VPN via sshuttle",
                        action="store_true")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="<service_name>:<port_name>:<target_port>")

    return parser


if __name__ == "__main__":
    exit(main())

