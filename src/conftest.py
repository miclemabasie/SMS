import pytest
from pytest_factoryboy import register

from tests.factories import UserFactory

# register(ProfileFactory)
register(UserFactory)


# fixtures
@pytest.fixture
def base_user(db, user_factory):
    new_base_user = user_factory.create(email="electrno@TECHWITHMICLEM.COM")
    return new_base_user


@pytest.fixture
def email_base_user(db, user_factory):
    new_base_user = user_factory.create(email="electrno@TECHWITHMICLEM.COM")
    return new_base_user


@pytest.fixture
def super_user(db, user_factory):
    new_user = user_factory.create(is_superuser=True, is_staff=True)
    return new_user


# @pytest.fixture
# def user_profile(db, profile_factory):
#     new_profile = ProfileFactory.create()
#     return new_profile
