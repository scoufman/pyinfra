"""
Manage BSD init services (``/etc/rc.d``, ``/usr/local/etc/rc.d``).
"""

from __future__ import annotations

from pyinfra import host
from pyinfra.api import operation
from pyinfra.facts.bsdinit import RcdStatus
from pyinfra.facts.server import Os

from . import files
from .util.service import handle_service_control


@operation()
def service(
    service: str,
    running=True,
    restarted=False,
    reloaded=False,
    command: str | None = None,
    enabled: bool | None = None,
):
    """
    Manage the state of BSD init services.

    + service: name of the service to manage
    + running: whether the service should be running
    + restarted: whether the service should be restarted
    + reloaded: whether the service should be reloaded
    + command: custom command to pass like: ``/etc/rc.d/<service> <command>``
    + enabled: whether this service should be enabled/disabled on boot
    """

    status_argument = "status"
    if host.get_fact(Os) == "OpenBSD":
        status_argument = "check"

    yield from handle_service_control(
        host,
        service,
        host.get_fact(RcdStatus),
        "test -e /etc/rc.d/{0} && /etc/rc.d/{0} {1} || /usr/local/etc/rc.d/{0} {1}",
        running,
        restarted,
        reloaded,
        command,
        status_argument=status_argument,
    )

    # BSD init is simple, just add/remove <service>_enabled="YES"
    if isinstance(enabled, bool):
        yield from files.line._inner(
            path="/etc/rc.conf.local",
            line="^{0}_enable=".format(service),
            replace='{0}_enable="YES"'.format(service),
            present=enabled,
        )
