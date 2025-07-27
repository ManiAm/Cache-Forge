
import hashlib


def get_file_hash(file_path, algorithm="md5", chunk_byte=65536):
    """
        algorithm: md5,
                    sha1, sha224, sha256, sha384, sha512,
                    sha3_224, sha3_256, sha3_384, sha3_512,
                    blake2b, blake2s,
                    shake_128, shake_256
    """

    hash_object = hashlib.new(algorithm)

    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(chunk_byte), b''):
            hash_object.update(chunk)

    return hash_object.hexdigest()
