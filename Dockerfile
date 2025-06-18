FROM python:3.11 as dev

FROM python:3.11 as build

RUN python3 -m pip install --no-cache-dir pipx==1.7.1 && pipx install poetry==1.8.4

ENV PATH="/root/.local/bin:$PATH"

COPY . /workspace/dummy_project

WORKDIR /workspace/dummy_project

RUN poetry build

FROM python:3.11-alpine as prod

# Put your environment variables here
# ARG DOLIAPIKEY=$DOLIAPIKEY
# ENV DOLIAPIKEY $DOLIAPIKEY

COPY --from=build /workspace/dummy_project/dist /workspace/dummy_project/dist

WORKDIR /workspace/dummy_project

RUN pip install --no-cache-dir dist/*.whl

# Put your entrypoint here
ENTRYPOINT ["dummy_project"]
