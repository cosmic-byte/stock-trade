import sys
from datetime import datetime
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError

from stock_trade.utils.constants import (
    ALLOWED_IMAGE_EXTENSIONS,
    BUCKET,
    ALLOWED_FILE_EXTENSIONS
)


def upload_file(file, folder, instance, attribute):
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)
    if hasattr(instance, attribute):
        previous_file = getattr(instance, attribute)
        if previous_file:
            xblob = bucket.blob(previous_file.split('eburu-bucket-v1/')[1])
            xblob.delete(client)
    else:
        raise ValidationError('{} does not have an attribute of {}'.format(instance.__class__.__name__, attribute))
    file_stream, filename, content_type = (file.read(), file.name, file.content_type)
    _check_extension(filename, ALLOWED_FILE_EXTENSIONS)
    filename = _safe_filename(filename, custom='Eburu-Document')
    blob = bucket.blob(folder + filename)
    return _upload(blob, file_stream, content_type)


def upload_profile_image(file, folder, user):
    """
    Uploads a file to a given Cloud Storage bucket and returns the public url
    to the new object.
    """
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)
    if user.profile_image_url:
        previous_image = user.profile_image_url.split('eburu-bucket-v1/')[1]
        if previous_image:
            xblob = bucket.blob(previous_image)
            xblob.delete(client)

    file = _compress_image(file)

    file_stream, filename, content_type = (file.read(), file.name, file.content_type)

    _check_extension(filename, ALLOWED_IMAGE_EXTENSIONS)
    filename = _safe_filename(filename, custom='Eburu-ProfileImage')

    blob = bucket.blob(folder + filename)

    return _upload(blob, file_stream, content_type)


def _upload(blob, file_stream, content_type):
    blob.upload_from_string(
        file_stream,
        content_type=content_type)

    url = blob.public_url

    return url


def _check_extension(filename, allowed_extensions):
    if ('.' not in filename or
            filename.split('.').pop().lower() not in allowed_extensions):
        raise ValidationError(
            "{0} has an invalid name or extension".format(filename))


def _safe_filename(filename, custom=None):
    """
    Generates a safe filename that is unlikely to collide with existing objects
    in Google Cloud Storage.
    ``filename.ext`` is transformed into ``filename-YYYY-MM-DD-HHMMSS.ext``
    """
    date = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
    name, extension = filename.rsplit('.', 1)
    name = custom if custom else name
    return "{0}-{1}.{2}".format(name, date, extension)


def _compress_image(image_file):
    temp = Image.open(image_file)
    output_io_stream = BytesIO()
    temp.resize((1020, 573))
    temp.save(output_io_stream, format='JPEG', quality=65)
    output_io_stream.seek(0)
    image_file = InMemoryUploadedFile(output_io_stream, 'ImageField', "%s.jpg" % image_file.name.split('.')[0],
                                      'image/jpeg', sys.getsizeof(output_io_stream), None)
    return image_file
