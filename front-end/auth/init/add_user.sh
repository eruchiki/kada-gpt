#!/bin/bash

/opt/keycloak/bin/kcadm.sh config credentials --server http://localhost:8081 --realm master --user admin --password hogehoge
/opt/keycloak/bin/kcadm.sh create users -r KadaGPT -f - << EOF
{
  "username": "ganbon",
  "firstName" : "和真",
  "lastName" : "岩本",
  "email" : "s00t200@kagawa-u.ac.jp",
  "emailVerified" : true,
  "enabled": true,
  "totp" : false,
  "attributes" : {
    "locale" : [ "ja" ]
  },
  "access" : {
    "manageGroupMembership" : true,
    "view" : true,
    "mapRoles" : true,
    "impersonate" : true,
    "manage" : true
  },
  "credentials": [
    {
      "type": "password",
      "value": "password123",
      "temporary": false
    }
  ]
}
EOF
