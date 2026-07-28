import unittest
from uuid import uuid4

from fastapi import HTTPException, status

from app.models.club import Clubes
from app.models.equipo import Equipos
from app.models.estadio import Estadios
from app.services.club_service import delete_club


class FakeQuery:
    def __init__(self, result_count=None, result=None):
        self.result_count = result_count
        self.result = result

    def filter(self, *args, **kwargs):
        return self

    def first(self):
        return self.result

    def count(self):
        return self.result_count


class FakeSession:
    def __init__(self, club=None, related_count=0, stadium_count=0):
        self.club = club
        self.related_count = related_count
        self.stadium_count = stadium_count
        self.deleted = []
        self.committed = 0

    def query(self, model):
        if model is Clubes:
            query = FakeQuery(result=self.club)
            return query
        if model is Equipos:
            query = FakeQuery(result=None if self.related_count == 0 else object())
            return query
        if model is Estadios:
            query = FakeQuery(result=None if self.stadium_count == 0 else object())
            return query
        raise AssertionError(f"Unexpected model: {model}")

    def delete(self, obj):
        self.deleted.append(obj)

    def commit(self):
        self.committed += 1


class ClubServiceDeleteTests(unittest.TestCase):
    def test_delete_club_raises_when_related_equipos_exist(self):
        club_id = uuid4()
        session = FakeSession(club=Clubes(id=club_id), related_count=1)

        with self.assertRaises(HTTPException) as ctx:
            delete_club(session, club_id)

        self.assertEqual(ctx.exception.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            ctx.exception.detail,
            "No se puede eliminar el club porque tiene equipos o estadios relacionados"
        )
        self.assertEqual(session.deleted, [])
        self.assertEqual(session.committed, 0)

    def test_delete_club_blocks_when_any_dependency_exists(self):
        club_id = uuid4()
        session = FakeSession(club=Clubes(id=club_id), stadium_count=1)

        with self.assertRaises(HTTPException) as ctx:
            delete_club(session, club_id)

        self.assertEqual(ctx.exception.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(
            ctx.exception.detail,
            "No se puede eliminar el club porque tiene equipos o estadios relacionados"
        )
        self.assertEqual(session.deleted, [])
        self.assertEqual(session.committed, 0)

    def test_delete_club_removes_when_no_related_dependencies(self):
        club_id = uuid4()
        session = FakeSession(club=Clubes(id=club_id), related_count=0, stadium_count=0)

        result = delete_club(session, club_id)

        self.assertIs(result, session.club)
        self.assertEqual(session.deleted, [session.club])
        self.assertEqual(session.committed, 1)


if __name__ == "__main__":
    unittest.main()
