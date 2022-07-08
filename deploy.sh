#!/bin/bash
fission spec init
fission env create --spec --name electronic-signature-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name electronic-signature-fn --env electronic-signature-env --src "./func/*" --entrypoint main.set_electronic_signature
fission route create --spec --name electronic-signature-rt --method POST --url /set-electronic-signature --function electronic-signature-fn
