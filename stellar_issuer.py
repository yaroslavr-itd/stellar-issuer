import sys
import argparse

import stellar_base.address
import stellar_base.keypair
import stellar_base.utils
import stellar_base.builder

parser = argparse.ArgumentParser(description='Issue an asset and send issued amount to recipient.')
parser.add_argument('issuer', type=str, help='Secret key of issuer-account.')
parser.add_argument('asset', type=str, help='Code of asset, that need to be issued.')
parser.add_argument('amount', type=str, help='Amount of issued asset that will be sent to recipient.')
parser.add_argument('recipient', type=str, help='Recipient of issued amount of asset.')
parser.add_argument(
    '-d', '--debug', required=False, action='store_true', default=False,
    help='Transaction will be submitted to test network if debug mode specified and to main network otherwise.'
         ' (default: %(default)s)')


class StellarTransactionFailed(Exception):
    """A stellar transaction failed."""


def get_account_sequence(secret, network='TESTNET'):
    """Get account sequence number."""
    details = stellar_base.address.Address(secret=secret, network=network)
    details.get()
    return details.sequence


def gen_builder(secret_key, network, sequence=None):
    """Create a builder."""
    builder = stellar_base.builder.Builder(secret=secret_key, network=network, sequence=sequence)
    return builder


def prepare_send(builder, from_secret, to_pubkey, amount, asset_code):
    """Prepare asset transfer."""
    from_pubkey = stellar_base.keypair.Keypair.from_seed(from_secret).address()
    builder.append_payment_op(to_pubkey, amount, asset_code, from_pubkey)
    return builder.gen_te().xdr().decode()


def submit(builder):
    """Sign and submit a transaction"""
    builder.sign()
    response = builder.submit()
    if 'status' in response and response['status'] >= 300:
        raise StellarTransactionFailed(response)
    return response


def main():
    args = parser.parse_args()
    network = 'TESTNET' if args.debug else 'PUBLIC'
    try:
        sequence_number = get_account_sequence(secret=args.issuer, network=network)
        builder = gen_builder(args.issuer, network, sequence=sequence_number)
        prepare_send(builder, args.issuer, args.recipient, args.amount, args.asset)
        submit(builder)
    except StellarTransactionFailed as exc:
        print(exc)
        parser.print_help()
    except stellar_base.utils.DecodeError:
        print('Incorrect address.')
        parser.print_help()
    except stellar_base.address.AccountNotExistError:
        print('No account found for provided secret.')
        parser.print_help()
    else:
        print('{} of {} successfully issued and sent to {}'.format(args.amount, args.asset, args.recipient))


if __name__ == '__main__':
    main()

