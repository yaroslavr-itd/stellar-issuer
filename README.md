# stellar-issuer
Issue an asset and send issued amount to recipient.

### Requirements
This script require Python >3.5 and installed __stellar-base__ package.
For install: 

```pip3 install -r requirements.txt``` 

or 

```pip3 install stellar-base```

### Usage
``` 
python3 stellar_issuer.py [-h] [-d] issuer asset amount recipient
```

```
positional arguments:
  issuer       Secret key of issuer-account.
  asset        Code of asset, that need to be issued.
  amount       Amount of issued asset that will be sent to recipient.
  recipient    Recipient of issued amount of asset.

optional arguments:
  -h, --help   show this help message and exit
  -d, --debug  Transaction will be submitted to test network if debug mode
               specified and to main network otherwise. (default: False)
```

__Example__

Issue 2.5 ITDASSETXMPL and send it to GDCTX4THTQ6LF4ZNZIQ2KDTOA27FOQ6BF6D63VEKOFLGGDRU2AMLY6A5 in testnet:

```python3 stellar_issuer.py SD4KWOIZRGMTWNLYGTK7TOHC6E2ANDKY7BWFLF7SRJKXI7UOXY2NG6H4 ITDASSETXMPL 2.5 GDCTX4THTQ6LF4ZNZIQ2KDTOA27FOQ6BF6D63VEKOFLGGDRU2AMLY6A5 -d```