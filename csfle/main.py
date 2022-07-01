# Based on https://pymongo.readthedocs.io/en/stable/examples/encryption.html

import os
import pymongo

from pymongo.encryption import (Algorithm,
                                ClientEncryption)
from pymongo.encryption_options import AutoEncryptionOpts

def encrypt_fields(client_encryption, document):
    if "credit_card" in document:
        encrypted_credit_card_info = client_encryption.encrypt(
            document["credit_card"],
            Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Random,
            key_alt_name='example_key_1')
        document["credit_card"] = encrypted_credit_card_info

    if "address" in document:
        encrypted_address = client_encryption.encrypt(
            document["address"],
            Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Random,
            key_alt_name='example_key_2')
        document["address"] = encrypted_address

    return document

def main():
    local_main_key_file = open('local_keyfile', 'r')
    local_main_key = local_main_key_file.read()
    kms_providers = {"local": {"key": local_main_key}}

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

    # Create new data keys
    client_encryption.create_data_key(
        'local', key_alt_names=['example_key_1'])

    client_encryption.create_data_key(
        'local', key_alt_names=['example_key_2'])

    document = {
        "name": "Naomi Pentrel",
        "email": "naomi@email.com",
        "address": {
            "street": "Sample Street 123",
            "zip": "1234AB",
            "country": "Netherlands"
        },
        "credit_card": { "type": "maestro", "number": "0604871496158803" },
        "region": "NAMER",
        "items": [ { "book_id": "183408230-7", "price": 25.99 } ]
    }

    document = encrypt_fields(client_encryption, document)
    coll.insert_one(document)

    # Automatically decrypts any encrypted fields.
    doc = coll.find_one()
    print('Decrypted document: %s' % (doc))

    unencrypted_coll = pymongo.MongoClient(os.environ['DB']).test.orders_encrypted
    print('Encrypted document: %s' % (unencrypted_coll.find_one()))

    # Cleanup resources.
    client_encryption.close()
    client.close()

main()
