import sys

import stellar_base.keypair
import stellar_base.utils
import stellar_base.builder


class StellarTransactionFailed(Exception):
    """A stellar transaction failed."""


def gen_builder(secret_key, network):
    """Create a builder."""
    builder = stellar_base.builder.Builder(secret=secret_key, network=network)
    return builder


def prepare_send(from_secret, to_pubkey, amount, asset_code, network='TESTNET', builder=None):
    """Prepare asset transfer."""
    from_pubkey = stellar_base.keypair.Keypair.from_seed(from_secret).address()
    builder = builder or gen_builder(from_secret, network)
    builder.append_payment_op(to_pubkey, amount, asset_code, from_pubkey)
    return builder.gen_te().xdr().decode()


def submit(builder):
    """Submit a transaction"""
    builder.sign()
    response = builder.submit()
    if 'status' in response and response['status'] >= 300:
        raise StellarTransactionFailed(response)
    return response


def main():
    secret_key = sys.argv[1]
    asset_code = sys.argv[2]
    recipient_pubkey = sys.argv[3]
    builder = gen_builder(secret_key, 'TESTNET')
    prepare_send(secret_key, recipient_pubkey, '10.0', asset_code, builder=builder)
    try:
        submit(builder)
    except StellarTransactionFailed as exc:
        print(exc)
        exit()

main()
