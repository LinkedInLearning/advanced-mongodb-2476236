# Based on https://pymongo.readthedocs.io/en/stable/examples/encryption.html

import os
import pymongo

from pymongo.encryption import (Algorithm,
                                ClientEncryption)
from pymongo.encryption_options import AutoEncryptionOpts

local_master_key_file = open('master_local_keyfile', 'r')
local_master_key = local_master_key_file.read()
kms_providers = {"local": {"key": local_master_key}}

# The MongoDB namespace (db.collection) used to store
# the encryption data keys.
key_vault_namespace = "encryption.__CSFLEExampleKeyVault"
key_vault_db_name, key_vault_coll_name = key_vault_namespace.split(".", 1)

# bypass_auto_encryption=True disable automatic encryption but keeps
# the automatic _decryption_ behavior. bypass_auto_encryption will
# also disable spawning mongocryptd.
auto_encryption_opts = AutoEncryptionOpts(
    kms_providers, key_vault_namespace, bypass_auto_encryption=True)

client = pymongo.MongoClient(os.environ['DB'], auto_encryption_opts=auto_encryption_opts)
coll = client.test.orders_encrypted

# Set up the key vault (key_vault_namespace) for this example.
key_vault = client[key_vault_db_name][key_vault_coll_name]
# Ensure that two data keys cannot share the same keyAltName.
key_vault.create_index(
    "keyAltNames",
    unique=True,
    partialFilterExpression={"keyAltNames": {"$exists": True}})

client_encryption = ClientEncryption(
    kms_providers,
    key_vault_namespace,
    # The MongoClient to use for reading/writing to the key vault.
    # This can be the same MongoClient used by the main application.
    client,
    # The CodecOptions class used for encrypting and decrypting.
    # This should be the same CodecOptions instance you have configured
    # on MongoClient, Database, or Collection.
    coll.codec_options)

# Create a new data key for the encryptedField.
data_key_1 = client_encryption.create_data_key(
    'local', key_alt_names=['example_key_1'])

data_key_2 = client_encryption.create_data_key(
    'local', key_alt_names=['example_key_2'])


# Explicitly encrypt a field:
encrypted_credit_card_info = client_encryption.encrypt(
    "4111 1111 1111 1111",
    Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Random,
    key_alt_name='example_key_1')

encrypted_address = client_encryption.encrypt(
    "Address",
    Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
    key_alt_name='example_key_2')

coll.insert_one({
    "credit_card": encrypted_credit_card_info,
    "address": encrypted_address
})

# Automatically decrypts any encrypted fields.
doc = coll.find_one()
print('Decrypted document: %s' % (doc))

unencrypted_coll = pymongo.MongoClient(os.environ['DB']).test.orders_encrypted
print('Encrypted document: %s' % (unencrypted_coll.find_one()))

# Cleanup resources.
client_encryption.close()
client.close()
