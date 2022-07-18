from typing import Any

from flask_batteries_included.sqldb import db
from flask_sqlalchemy import BaseQuery


class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "QueryWithSoftDelete":
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop("_with_deleted", False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted=None) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    def with_deleted(self) -> "QueryWithSoftDelete":
        return self.__class__(
            self._only_full_mapper_zero("get"), session=db.session(), _with_deleted=True
        )

    def _get(self, *args: Any, **kwargs: Any) -> Any:
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args: Any, **kwargs: Any) -> Any:
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.deleted else None
