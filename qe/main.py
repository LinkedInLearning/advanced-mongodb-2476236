import os
import pymongo

from pymongo.encryption import (ClientEncryption)
from pymongo.encryption_options import AutoEncryptionOpts
from bson.codec_options import CodecOptions
from bson.binary import STANDARD


def main():
    local_main_key_file = open('local_keyfile', 'r')
    local_main_key = local_main_key_file.read()
    kms_providers = {"local": {"key": local_main_key}}

    # The MongoDB namespace (db.collection) used to store
    # the data encryption keys.
    key_vault_namespace = "encryption.__QEExampleKeyVault"

    auto_encryption_opts = AutoEncryptionOpts(
        kms_providers, key_vault_namespace)

    client = pymongo.MongoClient(os.environ['DB'], auto_encryption_opts=auto_encryption_opts)

    # Drops these collections if they exist so you can rerun this script:
    # - "encryption.__keyVault"
    # - "shop.orders_encrypted"
    client["encryption"]["__keyVault"].drop()
    client["shop"]["orders_encrypted"].drop()

    # Document to be inserted
    document = {
        "name": "Naomi Pentrel",
        "email": "naomi@email.com",
        "address": {
            "street": "Sample Street 123",
            "zip": "1234AB",
            "country": "Netherlands"
        },
        "credit_card": { "type": "maestro", "number": "0604871496158803" },
        "items": [ { "book_id": "183408230-7", "price": 25.99 } ]
    }

    encrypted_fields_map = {
        "fields": [
            {
                "path": "address",
                "bsonType": "object",
                # Cannot be queried on with this configuration
            },
            {
                "path": "credit_card.number",
                "bsonType": "string",
                # Can be queried on
                "queries": [{"queryType": "equality"}]
            }
        ]
    }

    # Create the client with the information for creating an encrypted collection

    try:
        client_encryption = ClientEncryption(
            kms_providers=kms_providers,
            key_vault_namespace=key_vault_namespace,
            key_vault_client=client,
            codec_options=CodecOptions(uuid_representation=STANDARD)
        )
    except Exception as e:
        raise Exception("Exception creating encrypted client: ", e)

    # Create the new collection that is capable of Queryable Encryption

    try:
        client_encryption.create_encrypted_collection(
            client.shop,
            "orders_encrypted",
            encrypted_fields_map,
            kms_provider="local",
        )
    except Exception as e:
        raise Exception("Exception creating encrypted collection: ", e)



    coll = client.shop.orders_encrypted
    coll.insert_one(document)

    # Automatically decrypts any encrypted fields.
    doc = coll.find_one()
    print('Decrypted document: %s' % (doc))

    # Show unencrypted document by queried from a MongoClient without auto_encryption_opts
    unencrypted_client = pymongo.MongoClient(os.environ['DB'])
    unencrypted_coll = unencrypted_client.shop.orders_encrypted
    print('Encrypted document: %s' % (unencrypted_coll.find_one()))

    # Cleanup resources.
    client_encryption.close()
    client.close()
    unencrypted_client.close()

main()
