# Copyright (c) 2020, Frappe Technologies Pvt. Ltd. and Contributors

# imports - standard imports
import os
import shlex
import subprocess
import unittest
from glob import glob

# imports - module imports
import frappe
from frappe.utils.backups import fetch_latest_backups


def clean(value):
	if isinstance(value, (bytes, str)):
		value = value.decode().strip()
	return value


class BaseTestCommands(unittest.TestCase):
	def execute(self, command, kwargs=None):
		site = {"site": frappe.local.site}
		if kwargs:
			kwargs.update(site)
		else:
			kwargs = site
		command = command.replace("\n", " ").format(**kwargs)
		command = shlex.split(command)
		self._proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.stdout = clean(self._proc.stdout)
		self.stderr = clean(self._proc.stderr)
		self.returncode = clean(self._proc.returncode)


class TestCommands(BaseTestCommands):
	def test_execute(self):
		# test 1: execute a command expecting a numeric output
		self.execute("bench --site {site} execute frappe.db.get_database_size")
		self.assertEquals(self.returncode, 0)
		self.assertIsInstance(float(self.stdout), float)

		# test 2: execute a command expecting an errored output as local won't exist
		self.execute("bench --site {site} execute frappe.local.site")
		self.assertEquals(self.returncode, 1)
		self.assertIsNotNone(self.stderr)

		# test 3: execute a command with kwargs
		# Note:
		# terminal command has been escaped to avoid .format string replacement
		# The returned value has quotes which have been trimmed for the test
		self.execute("""bench --site {site} execute frappe.bold --kwargs '{{"text": "DocType"}}'""")
		self.assertEquals(self.returncode, 0)
		self.assertEquals(self.stdout[1:-1], frappe.bold(text='DocType'))

	def test_backup(self):
		home = os.path.expanduser("~")
		site_backup_path = frappe.utils.get_site_path("private", "backups")

		# test 1: take a backup
		before_backup = fetch_latest_backups()
		self.execute("bench --site {site} backup")
		after_backup = fetch_latest_backups()

		self.assertEquals(self.returncode, 0)
		self.assertIn("successfully completed", self.stdout)
		self.assertNotEqual(before_backup["database"], after_backup["database"])

		# test 2: take a backup with --with-files
		before_backup = after_backup.copy()
		self.execute("bench --site {site} backup --with-files")
		after_backup = fetch_latest_backups()

		self.assertEquals(self.returncode, 0)
		self.assertIn("successfully completed", self.stdout)
		self.assertIn("with files", self.stdout)
		self.assertNotEqual(before_backup, after_backup)
		self.assertIsNotNone(after_backup["public"])
		self.assertIsNotNone(after_backup["private"])

		# test 3: take a backup with --backup-path
		backup_path = os.path.join(home, "backups")
		self.execute("bench --site {site} backup --backup-path {backup_path}", {"backup_path": backup_path})

		self.assertEquals(self.returncode, 0)
		self.assertTrue(os.path.exists(backup_path))
		self.assertGreaterEqual(len(os.listdir(backup_path)), 2)

		# test 4: take a backup with --backup-path-db, --backup-path-files, --backup-path-private-files, --backup-path-conf
		kwargs = {
			key: os.path.join(home, key, value)
			for key, value in {
				"db_path": "database.sql.gz",
				"files_path": "public.tar",
				"private_path": "private.tar",
				"conf_path": "config.json"
			}.items()
		}

		self.execute("""bench
			--site {site} backup --with-files
			--backup-path-db {db_path}
			--backup-path-files {files_path}
			--backup-path-private-files {private_path}
			--backup-path-conf {conf_path}""", kwargs)

		self.assertEquals(self.returncode, 0)
		for path in kwargs.values():
			self.assertTrue(os.path.exists(path))

		# test 5: take a backup with --compress
		self.execute("bench --site {site} backup --with-files --compress")

		self.assertEquals(self.returncode, 0)

		compressed_files = glob(site_backup_path + "/*.tgz")
		self.assertGreater(len(compressed_files), 0)

		# test 6: take a backup with --verbose
		self.execute("bench --site {site} backup --verbose")
		self.assertEquals(self.returncode, 0)

	def test_remove_from_installed_apps(self):
		from frappe.installer import add_to_installed_apps
		app = "test_remove_app"
		add_to_installed_apps(app)

		# check: confirm that add_to_installed_apps added the app in the default
		self.execute("bench --site {site} list-apps")
		self.assertIn(app, self.stdout)

		# test 1: remove app from installed_apps global default
		self.execute("bench --site {site} remove-from-installed-apps {app}", {"app": app})
		self.execute("bench --site {site} list-apps")
		self.assertNotIn(app, self.stdout)
