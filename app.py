import sys
import argparse

import stellar_base.keypair
import stellar_base.utils
import stellar_base.builder

parser = argparse.ArgumentParser(description='Issue an asset and send issued amount to recipient.')
parser.add_argument('issuer', type=str, help='Secret key of issuer-account.')
parser.add_argument('asset', type=str, help='Code of asset, that need to be issued.')
parser.add_argument('recipient', type=str, help='Recipient')
parser.add_argument(
    '-d', '--debug', required=False, action='store_true', default=True,
    help='Transaction will be submitted to test network if debug mode specified and to main network otherwise.'
         ' (default: %(default)s)')


class StellarTransactionFailed(Exception):
    """A stellar transaction failed."""


def gen_builder(secret_key, network):
    """Create a builder."""
    builder = stellar_base.builder.Builder(secret=secret_key, network=network)
    return builder


def prepare_send(builder, from_secret, to_pubkey, amount, asset_code):
    """Prepare asset transfer."""
    from_pubkey = stellar_base.keypair.Keypair.from_seed(from_secret).address()
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
    args = parser.parse_args()
    secret_key = sys.argv[1]
    asset_code = sys.argv[2]
    recipient_pubkey = sys.argv[3]
    builder = gen_builder(secret_key, 'TESTNET')
    prepare_send(builder, secret_key, recipient_pubkey, '10.0', asset_code)
    try:
        submit(builder)
    except StellarTransactionFailed as exc:
        print(exc)
        exit()

main()
