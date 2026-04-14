```bash
sudo cp /etc/kubernetes/pki/apiserver.crt /etc/kubernetes/pki/apiserver.crt.bak
  sudo cp /etc/kubernetes/pki/apiserver.key /etc/kubernetes/pki/apiserver.key.bak
  sudo rm /etc/kubernetes/pki/apiserver.crt /etc/kubernetes/pki/apiserver.key
  sudo kubeadm init phase certs apiserver --apiserver-cert-extra-sans <hostname-or-ip>
  sudo crictl pods --name kube-apiserver -q | xargs sudo crictl stopp

  # Verify the new SANs:
  openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text -noout | grep -A1 "Subject Alternative Name"

  # Ensure the hostname resolves on the control plane node:
  echo "<ip> <hostname>" | sudo tee -a /etc/hosts

  # Update kubeconfig to point to the new hostname/IP:
  kubectl config set-cluster <cluster-name> --server=https://<hostname-or-ip>:6443

  Replace <hostname-or-ip> with your new hostname (e.g. cp1) or IP. If adding multiple SANs, comma-separate them: --apiserver-cert-extra-sans cp1,192.168.1.10.
```