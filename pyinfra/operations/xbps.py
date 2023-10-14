"""
Manage XBPS packages and repositories. Note that XBPS package names are case-sensitive.
"""

from pyinfra import host
from pyinfra.api import operation
from pyinfra.facts.xbps import XbpsPackages

from .util.packaging import ensure_packages


@operation(is_idempotent=False)
def upgrade():
    """
    Upgrades all XBPS packages.
    """

    yield "xbps-install -y -u"


_upgrade = upgrade  # noqa: E305


@operation(is_idempotent=False)
def update():
    """
    Update XBPS repositories.
    """

    yield "xbps-install -S"


_update = update  # noqa: E305


@operation()
def packages(
    packages=None,
    present=True,
    update=False,
    upgrade=False,
):
    """
    Install/remove/update XBPS packages.

    + packages: list of packages to ensure
    + present: whether the packages should be installed
    + update: run ``xbps-install -S`` before installing packages
    + upgrade: run ``xbps-install -y -u`` before installing packages

    **Example:**

    .. code:: python

        xbps.packages(
            name="Install Vim and Vim Pager",
            packages=["vimpager", "vim"],
        )

    """

    if update:
        yield from _update()

    if upgrade:
        yield from _upgrade()

    yield from ensure_packages(
        host,
        packages,
        host.get_fact(XbpsPackages),
        present,
        install_command="xbps-install -y -u",
        uninstall_command="xbps-remove -y",
    )
