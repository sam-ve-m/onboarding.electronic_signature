fission spec init
fission env create --spec --name onb-br-signature-env --image nexus.sigame.com.br/fission-onboarding-br-electronic-signature:0.1.1 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-br-signature-fn --env onb-br-signature-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-br-signature-rt --method PUT --url /onboarding/set_electronic_signature --function onb-br-signature-fn
