curl -iXPOST http://localhost:8080/user \
-H 'Content-Type: application/json' \
-d '
    {
        "name": "Ola",
        "last_name": "Nordmann",
        "email": "norge.no",
        "auth_method": "basic"
    }
'
