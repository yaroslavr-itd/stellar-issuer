# stellar-issuer
Issue an asset and send issued amount to recipient.

### usage
``` app.py [-h] [-d] issuer asset amount recipient ```


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