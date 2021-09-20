#!/bin/bash
# 基于curl的openshift基础工具
# TOKEN: 请使用service account的token(oc serviceaccounts get-token robot)或者从kubeconfig.yaml中获取users中的token
# ENDPOINT: 即openshift的集群地址，请从kubeconfig.yaml中获取，如https://jqdev-l-00860.jqdev.shanghaigm.com:8443
# uri: 请求地址如/oapi/v1
# yaml: yaml内容


# TOKEN=`DecryptString ${TOKEN}`

function GET() {
    curl -k -XGET -H "Authorization: Bearer ${TOKEN}" "${ENDPOINT}${uri}"
}

function POST() {
    curl -k -XPOST -H 'Authorization: Bearer ${TOKEN}' -H 'Accept: application/json' -H 'Content-Type: application/json' \
    '${ENDPOINT}${uri}' -d '${yaml}'
}


case $operation in
    "GET")
        GET
        ;;
    "POST")
        POST
        ;;
    *)
        echo "only support: GET/POST"
        ;;
esac