import importlib
import logging
import pkgutil
import re
import uuid

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
)

from seedwork.config import MODULES_DIR, Config


class Base(DeclarativeBase):
    @declared_attr
    def __tablename__(cls) -> str:
        """Convert CamelCase to snake_case"""
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)


class DatabaseAdapter:
    def __init__(
        self,
        dsn: str,
        echo: bool,
        pool_size: int,
        pool_max_overflow: int,
    ) -> None:
        self.engine = create_async_engine(
            dsn,
            echo=echo,
            pool_size=pool_size,
            max_overflow=pool_max_overflow,
        )
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()


def get_db_adapter(config: Config) -> DatabaseAdapter:
    return DatabaseAdapter(
        dsn=config.db.get_db_dsn_for_environment(),
        echo=config.db.echo,
        pool_size=config.db.pool_size,
        pool_max_overflow=config.db.pool_max_overflow,
    )


def populate_base() -> None:
    """Populates Base by models imported from entire application."""
    lg = logging.getLogger(__name__)
    modules_dir_name = MODULES_DIR.name

    if not MODULES_DIR.exists():
        lg.error(f"{MODULES_DIR} does not exist")
        return

    for _, module_name, is_pkg in pkgutil.iter_modules([str(MODULES_DIR)]):
        if not is_pkg:
            continue

        module_path = f"{modules_dir_name}.{module_name}.infra.repositories"
        try:
            importlib.import_module(module_path)
            lg.debug(f"Successfully imported: {module_path}")

        except ModuleNotFoundError:
            lg.debug(f"No models.py found in {module_name}")

        except Exception as e:
            lg.error(f"Error importing {module_path}: {e}")


populate_base()
