from typing import Tuple
from flask import Blueprint, request
from json import dumps
from cryptools.gammal import generate_keys, encrypt,decrypt

import json
import plotly
import plotly.express as px



bp = Blueprint("rabin", __name__, url_prefix="/rabin")

@bp.route("/getKeys", methods =["GET"])
def getKeyPair_r():
    """
    Generate of publicKey and privateKey
    """
    pub_key, priv_key = generate_keys()
    
    return dumps({
        "publicKey": {
            "P": pub_key[0],
            "G":pub_key[1],
            "H":pub_key[2]
        },
        "privateKey": {
            "P": priv_key[0],
            "G": priv_key[1],
            "X": priv_key[2],
        }
    })




@bp.route("/encrypt", methods=["POST"])
def encrypt_r():
    """
    Rabin cipher encryption route.
    Receives plain text and n= p*q as request arguments
    Returns JSON with cipher text and if needed error information.
    """
    request_data = request.get_json()
    plain_text: str = request_data["plainText"]
    p: int = request_data["p"]
    g: int = request_data["g"]
    h: int = request_data["h"]

    pub_key= (p,g,h)

    
    cipher_text = encrypt(pub_key, plain_text) 
    error = False
    typeError = ""
    # lo que vamos enviar: 
   
    response_dict = {"cipherText": cipher_text,  "error": error, "typeError": typeError}
    
    return dumps(response_dict)


@bp.route("/decrypt", methods=["POST"])
def decrypt_r():
    """
    Rabin cipher decryption route.
    Receives cipher text, p prime and q prime  as request arguments
    Returns JSON with clear text and, if needed, error information.
    """
    request_data = request.get_json()
    cipher_text: str = request_data["cipherText"]
    P: int = request_data["p"]
    G: int = request_data["g"]
    X: int = request_data["x"]

    priv_key = (P,G,X)


    plain_text = decrypt(priv_key, cipher_text)
    error = False
    typeError = ""

    response_dict = {"decipherText": plain_text, "error": error, "typeError": typeError}
    return dumps(response_dict)


