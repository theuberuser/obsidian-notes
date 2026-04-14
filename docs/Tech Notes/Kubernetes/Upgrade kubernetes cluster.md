## Upgrade control plane node

```
# Add new minor version to kubernetes apt sources
sudo sed -i 's/v1.34/v1.35/g' /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt-cache madison kubeadm

# Copy the version from the apt-cache output and use for the command below:
K8S_VER='1.35.1-1.1'
sudo apt-mark unhold kubeadm && \
sudo apt-get update && sudo apt-get install -y kubeadm=$K8S_VER && \
sudo apt-mark hold kubeadm

# Verify version
kubeadm version

# Print the upgrade plan
sudo kubeadm upgrade plan

# Copy paste the apply command from output above, example:
sudo kubeadm upgrade apply v1.35.3

# Upgrade kubelet and kubectl
sudo apt-mark unhold kubelet kubectl && \
sudo apt-get update && sudo apt-get install -y kubelet=$K8S_VER kubectl=$K8S_VER && \
sudo apt-mark hold kubelet kubectl

sudo systemctl daemon-reload
sudo systemctl restart kubelet

# After upgrading all nodes, run command below to confirm versions:
kubectl get nodes
```
## Upgrade worker node

```
# Run on control plane
kubectl drain <node-to-drain> --ignore-daemonsets

# Run on worker
sudo sed -i 's/v1.34/v1.35/g' /etc/apt/sources.list.d/kubernetes.list
sudo apt update
sudo apt-mark unhold kubeadm kubelet kubectl && \ 
sudo apt-get install -y kubeadm=$K8S_VER kubelet=$K8S_VER kubectl=$K8S_VER && \ sudo apt-mark hold kubeadm kubelet kubectl
sudo kubeadm upgrade node
sudo systemctl daemon-reload && sudo systemctl restart kubelet

# Run on control plane
kubectl uncordon <node-to-uncordon>
```