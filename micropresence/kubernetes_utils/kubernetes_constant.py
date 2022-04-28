"""
A module containig constants for kubernetes_utils namespace package
"""
import logging
from kubernetes import config, client

log = logging.getLogger(__name__)


config.load_kube_config()
V1 = client.api.core_v1_api.CoreV1Api()

SERVICE_BEFORE_MICROPRESENCE = 'service_before_micropresence'
SERVICE_FOR_MICROPRESENCE = 'service_for_micropresence'
MICROPRESENCE_PORT = 'micropresence_port'
MICROPRESENCE_SELECTOR = 'micropresence_selector'
OLD_PORT = 'old_port'
OLD_SELECTOR = 'old_selector'
