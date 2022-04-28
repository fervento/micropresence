"""
Module with utility functions to update kubernetes services selector
"""
import logging

log = logging.getLogger(__name__)


def restore_services_at_before_micropresence(namespace, specs):
    """
    "public" method to restore target services at their status of before micropresence execution.
    Wrap with a try-except schema an invocation of "private" restore_service_at_before_micropresence(namespace, spec)
    :param namespace: services namespace
    :param specs: services specification
    :return: void
    """
    for spec in specs:
        try:
            _restore_service_at_before_micropresence(namespace, spec)
        except Exception as e:
            log.warning(e)
    return


def update_services_for_micropresence(namespace, specs, selector_key, selector_value):
    """
    "public" method to handle services update for each spec it update specified service under specified namespace to
    update it' s selector
    :param namespace: services' namespace
    :param specs: service's spec
    :param selector_key: new selector key
    :param selector_value: new selector value.
    :return:
    """
    for spec in specs:
        try:
            _update_service_for_micropresence(namespace, selector_key, selector_value, spec)
        except Exception as e:
            log.warning(e)
    return


def _restore_service_at_before_micropresence(namespace, spec):
    """
    "private" method to restore target service at it's status of before micropresence execution.
    Original status should have been annotated in metadata annotations 'service_before_micropresence'
    by _update_service_for_micropresence.
    If the configuration of a service has been changed it warns user without changing anything in order to avoid
    undermining distributed system's integrity.
    :param namespace: services' namespace
    :param specs: services' specification
    :return: void
    """
    service = V1.read_namespaced_service(namespace=namespace, name=spec.service_name)
    old_properties = json.loads(service.metadata.annotations[SERVICE_BEFORE_MICROPRESENCE])
    properties = json.loads(service.metadata.annotations[SERVICE_FOR_MICROPRESENCE])
    for port in service.spec.ports:
        if port.name == spec.port_name:
            if port.target_port == properties[MICROPRESENCE_PORT]:
                port.target_port = old_properties[OLD_PORT]
            else:
                # TODO: speaking warning
                log.warning("")
                pass
    if service.spec.selector == properties[MICROPRESENCE_SELECTOR]:
        old_selector = {}
        json_selector = json.loads(old_properties[OLD_SELECTOR])
        for k in service.spec.selector.keys():
            old_selector[k] = None
        for k, v in json_selector.items():
            if service.spec.selector[k] == old_selector[k]:
                old_selector[k] = v
        service.spec.selector = old_selector
    else:
        # TODO: speaking warning
        log.warning("")
        pass
    service.metadata.annotations[SERVICE_BEFORE_MICROPRESENCE] = None
    service.metadata.annotations[SERVICE_FOR_MICROPRESENCE] = None
    V1.patch_namespaced_service(name=spec.service_name, namespace=namespace, body=service)


def _update_service_for_micropresence(namespace, selector_key, selector_value, spec):
    """
    "private" method to update selector of every specified services in specified namespace.
    If 'service_before_micropresence' has been annotated in metadata it means a previous execution of micropresence
    failed to quit smoothly. Do not overwrite it!
    :param namespace: service's namespace
    :param selector_key:  new selector key
    :param selector_value: new selector value
    :param spec: service's specification
    :return: void
    """
    service = V1.read_namespaced_service(namespace=namespace, name=spec.service_name)
    annotations = service.metadata.annotations
    keys = annotations.keys()

    if SERVICE_BEFORE_MICROPRESENCE not in keys:
        _update_service(namespace, selector_key, selector_value, service, spec)
    else:
        _update_service_recovery(namespace, selector_key, selector_value, service, spec)


def _update_service(namespace, selector_key, selector_value, service, spec):
    """
    "private" method to update selector of a specified service in specified namespace.
    It annotate in metadata old selector under 'service_before_micropresence' key for further recovery.
    :param namespace: service's namespace
    :param selector_key:  new selector key
    :param selector_value: new selector value
    :param spec: service's specification
    :return: void
    :return:
    """
    old_port = None
    target_port = int(spec.target_port)
    for port in service.spec.ports:
        if port.name == spec.port_name:
            old_port = port.target_port
            port.target_port = target_port
    old_selector = service.spec.selector
    new_selector = {}
    for k in service.spec.selector.keys():
        new_selector[k] = None
    new_selector[selector_key] = selector_value
    service.spec.selector = new_selector
    service.metadata.annotations[SERVICE_BEFORE_MICROPRESENCE] = json.dumps(
        {OLD_PORT: old_port, OLD_SELECTOR: json.dumps(old_selector)})
    service.metadata.annotations[SERVICE_FOR_MICROPRESENCE] = json.dumps(
        {MICROPRESENCE_PORT: target_port, MICROPRESENCE_SELECTOR: json.dumps(new_selector)})
    V1.patch_namespaced_service(name=spec.service_name, namespace=namespace, body=service)

    return


def _update_service_recovery(namespace, selector_key, selector_value, service, spec):
    """
    "private" method to update selector of a specified service in specified namespace.
    It does not ovverride metadata annotation 'service_before_micropresence' since this method is triggered in case of
    an old execution of micropresence failed to quit smoothly and the annotation contains original data.
    :param namespace: service's namespace
    :param selector_key:  new selector key
    :param selector_value: new selector value
    :param spec: service's specification
    :return: void
    :return:
    """
    target_port = int(spec.target_port)
    for port in service.spec.ports:
        if port.name == spec.port_name:
            port.target_port = target_port
    new_selector = {}
    for k in service.spec.selector.keys():
        new_selector[k] = None
    new_selector[selector_key] = selector_value
    service.spec.selector = new_selector
    service.metadata.annotations[SERVICE_FOR_MICROPRESENCE] = json.dumps(
        {MICROPRESENCE_PORT: target_port, MICROPRESENCE_SELECTOR: json.dumps(new_selector)})
    V1.patch_namespaced_service(name=spec.service_name, namespace=namespace, body=service)

    return
