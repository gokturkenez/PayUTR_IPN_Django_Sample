# Importing Required Libraries
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import collections
from datetime import datetime
import hmac
import hashlib

# Creating Date
date = datetime.utcnow().strftime('%Y%m%d%H%M%S')

# PayU Merchant's Secret Key
secretkey= 'SECRET_KEY'

@csrf_exempt
def handle_ipn(request):
    # Handle IPN Post
    ipnparams = request.POST

    # Create Array with Required Params
    array = collections.OrderedDict()
    array['IPN_PID'] = ipnparams["IPN_PID[]"]
    array['IPN_PNAME'] = ipnparams["IPN_PNAME[]"]
    array['IPN_DATE'] = ipnparams["IPN_DATE"]
    array['DATE'] = date

    # Initializing the hashstring @param
    hashstring = ''

    for k, v in array.items():
        # Adding the UTF-8 byte length of each field value at the beginning of field value
        hashstring += str(len(v.encode("utf8"))) + str(v)

        # Signature Calculation
    signature = hmac.new(secretkey.encode('utf-8'), hashstring.encode('utf-8'), hashlib.md5).hexdigest()

    # Printing response
    return HttpResponse("<EPAYMENT>{0}|{1}</EPAYMENT>".format(date, signature))

