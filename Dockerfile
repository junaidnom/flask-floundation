# NOTE: Caller is responsible for specifying the
#       environment file.
#       when calling docker, specify the environment
#       bindings as such:
#       > docker run --env-file <configuration-path> <...>
# TODO: Document the intended use-case for this file.

FROM gcr.io/google_appengine/python
COPY . /app
COPY . /dev-resources

RUN pip install pipenv
RUN pipenv install
RUN /bin/bash -c "source dev-resources/dev.env"

EXPOSE 5000

CMD pipenv run gunicorn -b :5000 'wsgi:application'