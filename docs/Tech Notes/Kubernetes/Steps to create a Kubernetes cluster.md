### Setup control plane node
1. Disable swap
```bash
# Disable imediately until reboot
sudo swapoff -a
# Disable permanently if swap partition exists in /etc/fstab
sudo sed -i '/swap/ s/^\(.*\)$/#\1/g' /etc/fstab
```

2. Enable IPv4 forwarding
```bash
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.ipv4.ip_forward = 1
EOF
sudo sysctl --system
```

3. Install dependencies
```bash
K8S_VER='1.34'
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

# sudo mkdir -p -m 755 /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v${K8S_VER}/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo "deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v${K8S_VER}/deb/ /" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```
4. Install container runtime
```bash
# Install containerd v2.2.2 on linux amd64
CRI=containerd
VERSION='2.2.2'
RUNC_VER='1.4.2'
CNI_PLUGINS_VER='1.9.1'
ARCH=amd64
OS='linux'

# Install containerd and containerd systemd service
curl -L https://github.com/containerd/containerd/releases/download/v$VERSION/$CRI-$VERSION-$OS-$ARCH.tar.gz -o $CRI-$VERSION-$OS-$ARCH.tar.gz

sudo tar Cxzvf /usr/local $CRI-$VERSION-$OS-$ARCH.tar.gz
bin/
bin/containerd-shim-runc-v2
bin/containerd-shim
bin/ctr
bin/containerd-shim-runc-v1
bin/containerd
bin/containerd-stress

sudo curl -L https://raw.githubusercontent.com/containerd/containerd/main/containerd.service -o /usr/lib/systemd/system/containerd.service

sudo systemctl daemon-reload
sudo systemctl enable --now containerd

# Install runc
curl -L https://github.com/opencontainers/runc/releases/download/v$RUNC_VER/runc.$ARCH -o runc.$ARCH
sudo install -m 755 runc.$ARCH /usr/local/sbin/runc

# Install CNI plugins
curl -L https://github.com/containernetworking/plugins/releases/download/v$CNI_PLUGINS_VER/cni-plugins-$OS-$ARCH-v$CNI_PLUGINS_VER.tgz -o cni-plugins-$OS-$ARCH-v$CNI_PLUGINS_VER.tgz

sudo mkdir -p /opt/cni/bin
sudo tar Cxzvf /opt/cni/bin cni-plugins-$OS-$ARCH-v$CNI_PLUGINS_VER.tgz

# Configure systemd cgroup driver
sudo mkdir /etc/containerd
cat <<EOF |sudo tee /etc/containerd/config.toml
[plugins.'io.containerd.cri.v1.runtime'.containerd.runtimes.runc]
  [plugins.'io.containerd.cri.v1.runtime'.containerd.runtimes.runc.options]
    SystemdCgroup = true
EOF

sudo systemctl restart containerd

# Enable containerd service
sudo systemctl daemon-reload
sudo systemctl enable --now containerd
```
5. Install kubeadm, kubelet, kubectl
```bash
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo systemctl enable --now kubelet
```

6. Initialize cluster
```bash
sudo kubeadm init --pod-network-cidr=<CIDR>
```
7. Configure kubectl
```bash
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

8. Install Pod network add-on
```bash
# Install Calico
CALICO_VER=3.31.4
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v$CALICO_VER/manifests/tigera-operator.yaml

kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v$CALICO_VER/manifests/custom-resources.yaml
```

### Join worker to cluster
**Prerequisites:**
- Disable swap
- Enable IPv4 forwarding
- Install dependencies
- Install container runtime
- Install kubeadm, kubelet, and kubectl

Copy the join command from the [[control plan node initialization]]:
```bash
# Example
sudo kubeadm join 172.31.47.193:6443 --token 57xv25.lo4v2ecvdxs0de06 \
	--discovery-token-ca-cert-hash sha256:84637109308c0ef2e818154c819f378eefb5b12699a7885e61aecead3c690de3
```

To get a new token from the control plane node for joining workers:
```bash
kubeadm token create --print-join-command
```

Configure kubectl
```bash
scp -i <key> <user>@controlplanenode:~/.kube/config <user>@workernode:~/.kube
```
**NOTE:** Be sure to add host entry to /etc/hosts for kubectl to work.

Pod neworking add-on is deployed as a DaemonSet when deployed on control plane node, so, pods will be automatically created on workers when they join the cluster.