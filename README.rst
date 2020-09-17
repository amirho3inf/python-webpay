Python package for `Webpay <https://webpay.bahamta.ir>`__ gateway API
=====================================================================

Installation
------------

Install from PyPI:

.. code:: bash

    pip install webpay-bahamta

For async support:

.. code:: bash

    pip install webpay-bahamta[async]

Usage
-----

Simple example:

.. code:: python

    from webpay import WebpayAPI

    API_KEY = "webpay:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz"
    webpay = WebpayAPI(API_KEY)

    # Make a payment
    payment_url = webpay.payment(
        reference='payment#1',
        amount_irr=100000,
        callback_url='https://example.com',
        payer_mobile='+989111111111',  # Optional
        trusted_pan=None  # Optional
    )

    # Verify payment
    payment_data = webpay.verify(
        reference='payment#1',
        amount_irr=100000
    )

Async example:

.. code:: python

    import asyncio
    from webpay import AsyncWebpayAPI

    API_KEY = "webpay:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx:zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz"
    webpay = AsyncWebpayAPI(API_KEY)


    async def main():
        # Make a payment
        payment_url = await webpay.payment(
            reference='payment#1',
            amount_irr=100000,
            callback_url='https://example.com',
            payer_mobile='+989111111111',  # Optional
            trusted_pan=None  # Optional
        )

        # Verify payment
        payment_data = await webpay.verify(
            reference='payment#1',
            amount_irr=100000
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

payment\_url will be like:

::

    https://webpay.bahamta.com/api/…

payment\_data will be like:

.. code:: json

    {
        "state": "paid",
        "total": 1000000,
        "wage": 5000,
        "gateway": "sep",
        "terminal": "11223344",
        "pay_ref": "GmshtyjwKSu5lKOLquYrzO9BqjUMb/TPUK0qak/iVs",
        "pay_trace": "935041",
        "pay_pan": "123456******1234",
        "pay_cid": "77CB1B455FB5F60415A7A02E4502134CFD72DBF6D1EC8FA2B48467DFB124AA75A",
        "pay_time": "2019-11-12T16:39:57.686436+03:30"
    }

API Documentation
-----------------

https://webpay.bahamta.com/doc/api
