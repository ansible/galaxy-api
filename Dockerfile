# Stage 1: Build galaxy-pulp from openapi spec
# --------------------------------------------
FROM openapitools/openapi-generator-cli AS galaxy-pulp

COPY bindings/openapi.yaml /local/openapi.yaml
RUN docker-entrypoint.sh generate \
    -i /local/openapi.yaml \
    -g python \
    -o /local/galaxy-pulp \
    --skip-validate-spec \
    --additional-properties=packageName=galaxy_pulp,projectName=galaxy-pulp

# Stage 2: Build galaxy image
# ---------------------------
FROM centos:7

ENV PATH="/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    LANG=en_US.UTF-8 \
    GALAXY_CODE=/code \
    GALAXY_VENV=/venv \
    GALAXY_STATIC_ROOT=/static \
    GALAXY_SETTINGS=/etc/galaxy/settings.py \
    DJANGO_SETTINGS_MODULE=galaxy_api.settings

RUN useradd \
    --uid 1000 \
    --user-group \
    --no-create-home \
    --home-dir /code/ \
    galaxy

RUN yum -y install epel-release \
    && yum -y install \
        gcc \
        git \
        python36 \
        python36-devel \
    && yum -y clean all

COPY . /code/galaxy-api
COPY --from=galaxy-pulp /local/galaxy-pulp /code/galaxy-pulp

RUN python3.6 -m venv "${GALAXY_VENV}" \
    && source "${GALAXY_VENV}/bin/activate" \
    && pip --no-cache-dir install -U \
        'pip<19.0' \
        wheel \
        pipenv \
        uwsgi \
    && pushd /code/galaxy-api \
    && PIPENV_VERBOSITY=-1 pipenv install --ignore-pipfile \
    && popd \
    && pip install -e /code/galaxy-api \
    && pip install -e /code/galaxy-pulp

RUN mkdir "$GALAXY_STATIC_ROOT" \
    && GALAXY_SECRET_KEY=x django-admin collectstatic --noinput

COPY --chown=galaxy:root \
    scripts/entrypoint \
    /entrypoint
RUN chmod +x /entrypoint

USER galaxy
WORKDIR /code/
ENTRYPOINT [ "/entrypoint" ]
CMD [ "start" ]
