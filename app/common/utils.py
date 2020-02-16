from google.cloud import storage


def get_or_create(session, model, **kwargs):
    """
    This method fetches a db model if it exists. Otherwise
    it will create it and return the new object.

    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def insert_or_update(session, model, **kwargs):
    return


def represent(model, field):
    return "{0}:({1})".format(type(model).__name__, field)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))
