# cryptofy

Simple encryption/decryption functions for Python

## Installation

```
pip install cryptofy
```

## Usage

**Generate** a secret:

```python
from cryptofy import encoding, generate_secret

key = generate_secret().decode(encoding)

print(key)  # Output randomized secret
```

**Encrypt** a string:

```python
from cryptofy import encoding, encrypt

string = 'my-password'
key = 'my-secret'

encrypted = encrypt(bytes(key, encoding=encoding), bytes(string, encoding))

print(encrypted)  # Output encrypted string
```

**Decrypt** a string:

```python
from cryptofy import encoding, decrypt

encrypted = 'my-encrypted-password'
key = 'my-secret'

string = decrypt(bytes(key, encoding=encoding), encrypted).decode(encoding)

print(string)  # Output decrypted string
```

## Command Line

### Usage:

```
cryptofy ((-d | -e) -k <key> -s <source>) | (-n [-l <length>])
```

**Example 1:** Generate a secret

```
cryptofy -n
```

**Example 2:** Encrypt a string:

```
cryptofy -e -k "my-secret" -s "my-password"
```

**Example 3:** Decrypt a string:

```
cryptofy -d -k "my-secret" -s "my-encrypted-password"
```

## License

Distributed under the [Apache, version 2.0 license](https://opensource.org/licenses/Apache-2.0).