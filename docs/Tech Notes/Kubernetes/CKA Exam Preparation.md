
```md
---
aliases:
  - CKA
  - CKA exam
---
```

https://www.reddit.com/r/CKAExam/


## CKA Exam, practice, scheduling. + learning resources

- [Kubernetes Fundamentals (LFS258)](https://trainingportal.linuxfoundation.org/learn/course/kubernetes-fundamentals-lfs258)
- [Certified Kubernetes Administrator Exam](https://trainingportal.linuxfoundation.org/learn/course/certified-kubernetes-administrator-cka/exam/exam)


kubectl commands:

```
kubectl scale <resource type> <name> --replicas=N
kubectl replace -f <file> --force
kubectl expose deployment <name>
kubectl expose deployment <name> --type=<svc_type> --port=<port>
kubectl expose deployment <name> --type=<svc_type> --name=<svc_name>
kubectl cordon <node>
kubectl uncordon <node>
kubectl drain worker
kubectl logs <pod>
kubectl logs <pod> -c <container>
kubectl proxy --api-prefix=/ &
kubectl autoscale deployment <pod> --cpu=<percent>% --min=X --max=Y --dry-run=client -o yaml >hpa.yaml
kubectl exec -it <pod> -- /bin/bash
kubectl exec <pod> --/bin/bash -c 'command'
kubectl cp <file> <pod>:<path>
kubectl label node <node> <label_key>=<label_value>
kubectl label node <node> <label_key>-
kubectl rollout history <resource> <name>
kubectl rollout history <resource> <name> --revision=N
kubectl rollout undo <resource type> <name>
kubectl rollout undo <resource type> <name> --to-revision=N
kubectl rollout status <resource> <name>
kubectl create deploy <name> --image=NAME:<VERSION> --replicas=N --dry-run=client -o yaml >FILE.yaml
kubectl create pod <name> --image=NAME:<VERSION> --dry-run=client -o yaml >FILE.yaml
kubectl <apply|create> -f FILE.yaml
kubectl set image deploy <name> nginx=nginx:<VERSION>
kubeadm join <control_plan_node>:6443 --token <token> --discovery-token-ca-cert-hash sha256:<hash> --node-name=worker
kubeadm upgrade <node>
```