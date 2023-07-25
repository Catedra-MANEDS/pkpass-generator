FOLDER_PUNTO_PASS = ""
PKPASS_NAME=""
OPENSSL_APP = "openssl"
DIRECTORIO_CON_LOS_PUNTO_PASS = "./directorios_punto_pass"
DIRECTORIO_CON_LOS_PKPASS="./pkpass_files/"

SUPPORTED_ASSET_FILES = [
    "icon.png",
    "icon@2x.png",
    "background.png",
    "background@2x.png",
    "logo.png",
    "logo@2x.png",
    "footer.png",
    "footer@2x.png",
    "strip.png",
    "strip@2x.png",
    "thumbnail.png",
    "thumbnail@2x.png",
    "signature",
    "pass.json",
    "manifest.json",
]

#Contraseña de la clave y el certificado
key_password = "pepe"
pass_type_identifier=""
serial_number=""

"""Ruta certificados en la vm"""
#directorio_certificados="/home/samuel/pass_generator/certificados/"

"""----------PASE PEPE NORMAL----------"""
directorio_certificados="/home/samuel/Documents/pkpassApple/pkpassPepephone/scp_mandar/certificados/"
#Certificado del pase
pass_certificate=directorio_certificados+"passcertificate.pem"
#Clave del pase
passkey=directorio_certificados+"passkey.pem"

"""----------PASE PRUEBAS----------"""
# directorio_certificados="/home/samuel/Documents/pkpassApple/pkpassPepephone/scp_mandar/certificados/"
# #Certificado del pase
# pass_certificate=directorio_certificados+"passcertificate2.pem"
# #Clave del pase
# passkey=directorio_certificados+"passkey2.pem"

"""Ruta al certificado de apple, no cambia"""
#Certificado de apple
certificado_apple=directorio_certificados+"AppleWWDRCA.pem"

"""Comandos anteriormente usados para generar fichero --> signature"""
#Para clave privada sin contraseña
#os_code = os.system(f"{globals.OPENSSL_APP} smime -binary -sign -certfile {globals.certificado_apple} -signer {globals.pass_certificate} -inkey {globals.passkey} -in {ruta_manifest} -out {ruta_signature} -outform DER")
#Para clave privada con contraseña
#os_code = os.system(f"{globals.OPENSSL_APP} smime -binary -sign -certfile {globals.certificado_apple} -signer {globals.pass_certificate} -inkey {globals.passkey} -in {ruta_manifest} -out {ruta_signature} -outform DER -passin pass:{globals.key_password}")