# k8s-ri

Kubernetes deployments/statefulsets/daemonsets release information Flask app.

`kube-config.yml` required.

## local development

```
$ podman build -f ./deploy/build/Dockerfile -t k8s-ri .
$ podman run -it -p 5000:5000 --name k8s-ri -v ~/.kube/kube-qshy-dev.yml:/tmp/kube-config.yml -e KUBECONFIG=/tmp/kube-config.yml -e ENV=dev localhost/k8s-ri
$ podman stop k8s-ri && podman rm k8s-ri
```
