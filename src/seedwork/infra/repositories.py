from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession


class Removed:
    def __repr__(self):
        return "<Removed entity>"

    def __str__(self):
        return "<Removed entity>"


REMOVED = Removed()


class SqlAlchemyGenericRepository:
    mapper_class: type
    model_class: type

    def __init__(
        self,
        session: AsyncSession,
        identity_map: dict | None = None,
    ):
        self._session = session
        self._identity_map = identity_map or dict()

    def add(self, entity):
        self._identity_map[entity.id] = entity
        instance = self.map_entity_to_model(entity)
        self._session.add(instance)

    async def remove(self, entity):
        self._check_not_removed(entity.id)
        self._identity_map[entity.id] = REMOVED
        instance = await self._session.get(self.get_model_class(), entity.id)
        await self._session.delete(instance)

    async def remove_by_id(self, entity_id: UUID):
        self._check_not_removed(entity_id)
        self._identity_map[entity_id] = REMOVED
        instance = await self._session.get(self.get_model_class(), entity_id)
        if instance is None:
            return None
        await self._session.delete(instance)

    async def get_by_id(self, entity_id: UUID, for_update: bool = False):
        instance = await self._session.get(
            self.get_model_class(),
            entity_id,
            with_for_update=for_update,
        )
        if instance is None:
            return None
        return self._get_entity(instance)

    async def persist(self, entity):
        """
        Persists all the changes made to the entity.
        Basically, entity is mapped to a model instance using a data_mapper, and then added to sqlalchemy session.
        """
        self._check_not_removed(entity.id)
        assert (
            entity.id in self._identity_map
        ), "Cannon persist entity which is unknown to the repo. Did you forget to call repo.add() for this entity?"
        instance = self.map_entity_to_model(entity)
        merged = await self._session.merge(instance)
        self._session.add(merged)

    async def persist_all(self):
        """Persists all changes made to entities known to the repository (present in the identity map)."""
        for entity in self._identity_map.values():
            if entity is not REMOVED:
                await self.persist(entity)

    def collect_events(self):
        """Collects all events from entities known to the repository (present in the identity map)."""
        events = []
        for entity in self._identity_map.values():
            if entity is not REMOVED:
                events.extend(entity.collect_events())
        return events

    @property
    def data_mapper(self):
        return self.mapper_class()

    def map_entity_to_model(self, entity):
        assert self.mapper_class, (
            f"No data_mapper attribute in {self.__class__.__name__}. "
            "Make sure to include `mapper_class = MyDataMapper` in the Repository class."
        )

        return self.data_mapper.entity_to_model(entity)

    def map_model_to_entity(self, instance):
        assert self.data_mapper
        return self.data_mapper.model_to_entity(instance)

    def get_model_class(self):
        assert self.model_class is not None, (
            f"No model_class attribute in in {self.__class__.__name__}. "
            "Make sure to include `model_class = MyModel` in the class."
        )
        return self.model_class

    def _get_entity(self, instance):
        if instance is None:
            return None
        entity = self.map_model_to_entity(instance)
        self._check_not_removed(entity.id)

        if entity.id in self._identity_map:
            return self._identity_map[entity.id]

        self._identity_map[entity.id] = entity
        return entity

    def _check_not_removed(self, entity_id):
        assert (
            self._identity_map.get(entity_id, None) is not REMOVED
        ), f"Entity {entity_id} already removed"
