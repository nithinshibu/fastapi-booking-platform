from datetime import timedelta

import pytest

from app.core.security import(create_access_token,decode_access_token,hash_password,verify_password)

# pytest does NOT use classes or attributes like xUnit's [Fact] / [Theory].
# Each function prefixed with test_ is automatically discovered and run.
# No [TestClass] , no inheritance - just plain functions.

# Run all tests:        pytest
# Run this file only:   pytest tests/test_auth.py
# Run one test:         pytest tests/test_auth.py::test_verify_password_correct
# Verbose output:       pytest -v 


# --- hash_password ---

def test_hash_password_differs_from_plain():
    """ Stored hash must never equal the original password. """
    plain = "supersecret123"
    assert hash_password(plain) != plain

def test_hash_password_is_not_deterministic():
    """ 
    Two hashes of the same password must be different strings.

    bcrypt generates a new random salt on every call and embeds it in the output.
    This means even if two users have the same password ,their stored hashes differ - 
    a leaked hash from one account cannot be used to attack another.
    verify_password handles comparison correctly by extracting the embedded salt. 
    
    """
    plain = "supersecret123"
    assert hash_password(plain) != hash_password(plain)


# --- verify_password ---

def test_verify_password_correct():
    """ Returns True when the plain password matches the stored hash. """ 
    plain = "supersecret123"
    hashed = hash_password(plain)
    assert verify_password(plain,hashed) is True

def test_verify_password_wrong_input():
    """ Returns False when the plain password doesn't match """
    hashed = hash_password("correct_password")
    assert verify_password("wrong password",hashed) is False 

# --- create_access_token ---

def test_create_access_token_returns_nonempty_string():
    """ Token must be a non-empty string (dot-separated JWT Format). """
    token = create_access_token({"sub":"user@example.com"})
    assert isinstance(token,str)
    assert len(token) > 0

def test_create_access_token_has_three_parts():
    """ 
    A valid JWT always has exactly three dot-separated parts:
    header.payload.signature

    """
    token = create_access_token({"sub":"user@example.com"})
    parts = token.split(".")
    assert len(parts) == 3

# --- decode_access_token ---

def test_decode_returns_correct_subject():
    """ Decoded payload must contain the same 'sub' claim we put in. """
    token = create_access_token({"sub":"user@example.com"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload["sub"] == "user@example.com"

def test_decode_invalid_token_returns_none():
    """ 
    A garbage string must return None , not raise an exception.
    
    In .NET this would throw - here we are deliberately swallow JWTError so 
    the caller gets a clean None to branch on. HTTP 401 handling is done one layer up
    in the dependency , not here.
    
    """
    result = decode_access_token("this.is.not.a.real.token")
    assert result is None

def test_decode_tampered_token_returns_none():
    """ A token with it's signature changed or removed must return None. """
    token = create_access_token({"sub":"user@example.com"})
    tampered = token[:-5] + "ABCDE"
    result = decode_access_token(tampered)
    assert result is None

def test_decode_expired_token_returns_none():
    """ 
    A token with a negative expiry (already in the past) must return None.

    python-jose checks the 'exp' claim automatically - we don't need to write expiry-check
    logic ourselves.
    """
    token = create_access_token({"sub":"user@example.com"},expires_delta=timedelta(seconds=-1)) # Go 1 second into the past.The token is instantly expired
    result = decode_access_token(token)
    assert result is None