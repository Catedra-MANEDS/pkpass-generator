#!/bin/bash

# Configuración de rutas y valores
CERTIFICATE_FILE_NAME="/home/samuel/Documents/pkpassApple/pkpassPepephone/scp_mandar/certificados/passcertificate2.pem"
CERTIFICATE_KEY_FILE_NAME="/home/samuel/Documents/pkpassApple/pkpassPepephone/scp_mandar/certificados/passkey2.pem"
TOPIC="pass.com.pruebas.notificar.eventTicket"
DEVICE_TOKEN="d379c1eb8ed9594be815995751d0ecd105ff3014242e713033ac287ea59910bd"
APNS_HOST_NAME="api.push.apple.com"
PUERTO_APPLE=2195

# Contraseña de la clave privada (si la tiene)
#passphrase = 'pepe'

# Comando 1 - openssl s_client para verificar la conexión
openssl s_client -connect "${APNS_HOST_NAME}":443 -cert "${CERTIFICATE_FILE_NAME}" -certform DER -key "${CERTIFICATE_KEY_FILE_NAME}" -keyform PEM
# Comando 2 - curl para enviar una notificación
curl -v --header "apns-topic: ${TOPIC}" --header "apns-push-type: alert" --cert "${CERTIFICATE_FILE_NAME}" --cert-type DER --key "${CERTIFICATE_KEY_FILE_NAME}" --key-type PEM --data '{"aps":""}}' --http2  "https://${APNS_HOST_NAME}/3/device/${DEVICE_TOKEN}"
