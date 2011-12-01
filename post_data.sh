# Script for posting test data to server.
curl -d "test_ipn=1&payment_type=instant&payment_date=08%3A39%3A48+Dec+01%2C+2011+PST&payment_status=Completed&payer_status=verified&first_name=John&last_name=Smith&payer_email=buyer%40paypalsandbox.com&payer_id=TESTBUYERID01&business=seller%40paypalsandbox.com&receiver_email=seller%40paypalsandbox.com&receiver_id=TESTSELLERID1&residence_country=US&item_name1=something&item_number1=AK-1234&quantity1=1&tax=2.02&mc_currency=USD&mc_fee=0.44&mc_gross=15.34&mc_gross" http://localhost:8080/

