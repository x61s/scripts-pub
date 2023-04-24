# https://github.com/kubernetes-client/python/blob/master/kubernetes/README.md

import os

import flask
import logging

from kubernetes import client, config

try:
    config.load_incluster_config() # in-cluster configuration load
except config.ConfigException:
    try:
        # for local environment KUBECONFIG value can be ~/.kube/kube-config.yml
        config.load_kube_config(os.environ.get("KUBECONFIG"))
    except config.ConfigException:
        raise Exception("Could not configure kubernetes python client")

v1 = client.AppsV1Api()

def get_api_response(json):
    servicesList = []
    response = {}
    gitlabUrl = ''
    for item in json.items:
        fullname = (
            item.metadata.namespace
            + "/"
            + item.metadata.name
            )

        try:
            version = item.metadata.labels['app.kubernetes.io/version']
        except:
            version = 'unknown'

        try:
            gitlabUrl = item.metadata.annotations['gitlabUrl']
        except:
            gitlabUrl = 'unknown'

        servicesList.append([fullname, version, gitlabUrl])
    return servicesList


env = os.environ.get("ENV")

app = flask.Flask(__name__)

# main routes
@app.route("/")
def index_page():
    deployments = get_api_response(v1.list_deployment_for_all_namespaces(watch=False))

    statefulsets = get_api_response(v1.list_stateful_set_for_all_namespaces(watch=False))

    daemonsets = get_api_response(v1.list_daemon_set_for_all_namespaces(watch=False))

    app.logger.info("/")

    return flask.render_template('index.html',
                                 environment=env,
                                 deployments=deployments,
                                 statefulsets=statefulsets,
                                 daemonsets=daemonsets)

# healthcheck
@app.route("/health")
def health_page():
    app.logger.info("/health")
    return flask.Response(status=200)
