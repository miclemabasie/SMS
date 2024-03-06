import pytest
from django.core.exceptions import ValidationError

from apps.users.managers import CustomUserManager


def test_user_str(base_user):
    assert base_user.__str__() == f"{base_user.username}"


def test_user_shortname(base_user):
    assert base_user.get_shortname() == f"{base_user.username.title()}"


def test_get_fullname(super_user):
    fname = super_user.first_name.title()
    lname = super_user.last_name.title()
    assert super_user.get_fullname == f"{fname} {lname}"


def test_user_can_not_create_account_without_firstname(user_factory):
    """Test that the system returns a proper error if a user tries to create an account with a first_name provided"""

    with pytest.raises(ValueError) as err:
        user_factory.create(first_name=None)
    assert str(err.value) == "User must provide First Name"


def test_user_account_has_username(user_factory):
    """Test that the user must provide a username to succesfuly create an account"""
    with pytest.raises(ValueError) as err:
        user_factory.create(username=None)
    assert str(err.value) == "User must provide username"


def test_user_accoutn_has_last_name(user_factory):
    """Test that the user must provide a lastname to create an account"""
    with pytest.raises(ValueError) as err:
        user_factory.create(last_name=None)
    assert str(err.value) == "User must provide a Last Name"


def test_base_user_must_provide_email_address(user_factory):
    """Test that an error is returned if user tries to create an account without an email address"""
    with pytest.raises(ValueError) as err:
        user_factory.create(email=None)
    assert str(err.value) == "BaseUser Account: An email address is required"


def test_superuser_must_have_is_superuser_as_true(user_factory):
    """Test that the superuser must have the property of is_superuser=True, else returns an error"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_staff=True, is_superuser=False)
    assert str(err.value) == "Superusers must have is_superuser = True"


def test_useruser_must_have_is_staff_as_true(user_factory):
    """Test that a superuser must have the property of is_staff set to true"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_staff=False, is_superuser=True)
    assert str(err.value) == "Superuser must have is_staff = True"


def test_user_account_has_password(user_factory):
    """Test that a superuser must have the property of is_staff set to true"""
    with pytest.raises(ValueError) as err:
        user_factory.create(is_staff=True, is_superuser=True, password=None)
    assert str(err.value) == "Superuser must provide a valid password"


# def test_user_email_is_normalized_properly(email_base_user):
#     """Test that a superuser must have the property of is_staff set to true"""
#     email = "electrno@TECHWITHMICLEM.COM"
#     assert email_base_user.email == email.lower()


def test_user_email_validators(email_base_user):
    """Test that the user email is properly validated"""
    with pytest.raises(ValueError) as err:
        CustomUserManager.email_validator(email_base_user, email="miclem@2222")
    assert str(err.value) == "You must provide a valide email address"
