FROM alpine:latest
RUN apk add --no-cache bash
SHELL ["/bin/bash", "-c"]
RUN apk add --no-cache curl vim zip podman py3-pip openssl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && chmod +x kubectl && mv kubectl /usr/local/bin/
RUN curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 && chmod 700 get_helm.sh && ./get_helm.sh
RUN rm get_helm.sh
