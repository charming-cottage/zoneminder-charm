#!/usr/bin/env python3

"""Charm the application."""

import logging
import subprocess

import ops

logger = logging.getLogger(__name__)


class ZoneMinderCharm(ops.CharmBase):
    """Charm the application."""

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.stop, self._on_stop)

    def _on_start(self, event: ops.StartEvent):
        """Handle start event."""
        subprocess.run(["systemctl", "start", "zoneminder"])
        self.unit.status = ops.ActiveStatus("running")

    def _on_stop(self, event: ops.StopEvent):
        self.unit.status = ops.MaintenanceStatus("stopping")
        subprocess.run(["systemctl", "stop", "zoneminder"])

    def _on_install(self, event: ops.InstallEvent) -> None:
        self.unit.status = ops.MaintenanceStatus("installing")
        # apt setup
        subprocess.run(["apt", "update"])
        subprocess.run(["apt", "upgrade", "-y"])
        subprocess.run(["apt", "install", "-y", "software-properties-common"])
        version = self.config["version"]
        logger.debug("Adding PPA for zoneminder %s", version)
        subprocess.run(
            ["apt", "add-apt-repository", f"ppa:iconnor/zoneminder-{version}"]
        )
        subprocess.run(["apt", "update"])
        subprocess.run(["apt", "install", "-y", "zoneminder"])

        # apache2 setup
        subprocess.run(["a2enmod", "rewrite"])
        subprocess.run(["a2enconf", "zoneminder"])
        subprocess.run(["chgrp", "-c", "www-data", "/etc/zm/zm.conf"])
        subprocess.run(
            "mysql -u root < /usr/share/zoneminder/db/zm_create.sql", shell=True
        )
        subprocess.run(
            ["mysql", "-u", "root", "-e", "create user zmuser identified by 'zmpass';"]
        )
        subprocess.run(["mysql", "-u", "root", "-e", "grant all on zm.* to zmuser;"])
        subprocess.run(["systemctl", "restart", "apache2"])

        # start zoneminder
        subprocess.run(["systemctl", "enable", "zoneminder"])
        subprocess.run(["systemctl", "start", "zoneminder"])
        self.unit.open_port("tcp", 80)
        self.unit.status = ops.ActiveStatus("installed")


if __name__ == "__main__":  # pragma: nocover
    ops.main(ZoneMinderCharm)  # type: ignore
