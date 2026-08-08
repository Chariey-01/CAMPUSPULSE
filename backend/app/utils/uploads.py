import time

import cloudinary
import cloudinary.utils


# The frontend never talks to Cloudinary without one of these - it proves the
# upload was authorized by our backend (a real logged-in user), not just
# anyone with the cloud name. Cloudinary recomputes the signature from the
# same params using its own copy of the api_secret, and only accepts the
# upload if they match, so the secret itself never has to leave the server.
def generate_upload_signature(folder="campuspulse"):
    timestamp = int(time.time())
    params_to_sign = {"timestamp": timestamp, "folder": folder}

    signature = cloudinary.utils.api_sign_request(params_to_sign, cloudinary.config().api_secret)

    return {
        "signature": signature,
        "timestamp": timestamp,
        "api_key": cloudinary.config().api_key,
        "cloud_name": cloudinary.config().cloud_name,
        "folder": folder,
    }
