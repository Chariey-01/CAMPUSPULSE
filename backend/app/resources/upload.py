from flask_jwt_extended import jwt_required
from flask_restful import Resource

from app.utils.uploads import generate_upload_signature


class UploadSignatureResource(Resource):
    # POST /api/uploads/signature - any logged-in user can request one; this is
    # what stops an anonymous stranger from burning our Cloudinary quota, since
    # nothing about a signature is specific to admins vs students.
    @jwt_required()
    def post(self):
        return generate_upload_signature(), 200
