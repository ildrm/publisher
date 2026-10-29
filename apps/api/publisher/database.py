"""SQLite adapter. WAL+FULL local durable commit; no multi-region guarantee."""
from contextlib import contextmanager
from pathlib import Path
import sqlite3
import os
from datetime import datetime, timezone


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ClosingConnection(sqlite3.Connection):
    def __exit__(self,*args):
        try:return super().__exit__(*args)
        finally:self.close()


class Database:
    schema_version=2

    def __init__(self, path: Path):
        self.path=path
        path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        # SQLite derives WAL/SHM permissions from the database. Set privacy before
        # opening it, including databases restored with permissive file modes.
        descriptor=os.open(path,os.O_WRONLY|os.O_CREAT,0o600)
        try:os.fchmod(descriptor,0o600)
        finally:os.close(descriptor)
        for suffix in ('-wal','-shm'):
            try:Path(str(path)+suffix).chmod(0o600)
            except FileNotFoundError:pass
        with self.connect() as connection:
            connection.execute('PRAGMA journal_mode=WAL')
            current=connection.execute('PRAGMA user_version').fetchone()[0]
            if current>self.schema_version:raise RuntimeError('Unsupported schema version; refusing to start')
            migrations={1:'001_authoring.sql',2:'002_interface_locales.sql'}
            for version,filename in migrations.items():
                connection.execute('BEGIN IMMEDIATE')
                try:
                    # Recheck inside the write transaction to serialize concurrent initializers.
                    actual=connection.execute('PRAGMA user_version').fetchone()[0]
                    if actual>self.schema_version:raise RuntimeError('Unsupported schema version; refusing to start')
                    if actual<version:
                        statement=''
                        for line in (Path(__file__).parent/'migrations'/filename).read_text().splitlines(True):
                            statement+=line
                            if sqlite3.complete_statement(statement):
                                connection.execute(statement);statement=''
                        if statement.strip():raise RuntimeError('Incomplete migration statement')
                        connection.execute('INSERT INTO schema_migrations VALUES(?,?)',(version,now()))
                        connection.execute(f'PRAGMA user_version={version}')
                    connection.commit()
                except BaseException:
                    connection.rollback();raise
        path.chmod(0o600)

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, isolation_level=None, timeout=10, factory=ClosingConnection)
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys=ON')
        connection.execute('PRAGMA synchronous=FULL')
        connection.execute('PRAGMA busy_timeout=10000')
        return connection

    @contextmanager
    def transaction(self):
        connection = self.connect()
        try:
            connection.execute('BEGIN IMMEDIATE')
            yield connection
            connection.commit()
        except BaseException:
            connection.rollback()
            raise
        finally:
            connection.close()

    def backup(self, destination: Path) -> None:
        if destination.resolve() == self.path.resolve() or destination.exists():
            raise ValueError('Backup destination must be a new, separate file')
        destination.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        # Reserve the target atomically: concurrent backups must not overwrite each other.
        descriptor=os.open(destination,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        identity=os.fstat(descriptor);os.close(descriptor)
        try:
            with self.connect() as source, sqlite3.connect(destination, factory=ClosingConnection) as target:
                source.backup(target)
                if target.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                    raise RuntimeError('Backup integrity check failed')
            destination.chmod(0o600)
        except BaseException:
            # Do not leave a partial file that can be mistaken for a valid backup,
            # and never remove a replacement another process owns.
            try:
                current=destination.stat()
                if (current.st_dev,current.st_ino)==(identity.st_dev,identity.st_ino):destination.unlink()
            except FileNotFoundError:pass
            raise
