Composed with ChatGPT

---

# 📄 Linux USE Method — 1-Page Incident Checklist

**USE = Utilization • Saturation • Errors**  
**Goal:** Identify the system bottleneck _before_ debugging the application.

---

## 🔰 Quick Triage (Run First)

```bash
uptime
```

- **What it does:** Shows load average (1/5/15 min)
    
- **Look for:** Load ≫ CPU count → CPU or I/O saturation
    

```bash
vmstat 1
```

- **What it does:** Snapshot of CPU, memory, and run queue
    
- **Look for:**
    
    - `r` > CPU cores → CPU saturation
        
    - `si` / `so` > 0 → memory pressure
        
    - High `wa` → I/O wait
        

```bash
free -h
```

- **What it does:** Memory usage summary
    
- **Look for:** Low **available** memory, swap usage
    

```bash
iostat -xz 1
```

- **What it does:** Per-disk utilization & latency
    
- **Look for:** `%util` ≈ 100%, high `await`
    

```bash
ip -s link
```

- **What it does:** Network interface counters
    
- **Look for:** Packet drops or errors
    

---

## 1️⃣ CPU

### Utilization

```bash
top
mpstat -P ALL 1
```

- **Does:** Shows CPU usage overall and per core
    
- **Look for:** Low `%idle`, high `%sys`, single hot core
    

### Saturation

```bash
vmstat 1
```

- **Does:** Shows run queue (`r`)
    
- **Look for:** `r` consistently > CPU count
    

### Errors

```bash
dmesg | grep -i cpu
```

- **Does:** Kernel CPU messages
    
- **Look for:** Throttling, machine check errors
    

---

## 2️⃣ Memory

### Utilization

```bash
free -h
```

- **Does:** RAM and swap usage
    
- **Look for:** Low available memory
    

### Saturation

```bash
vmstat 1
```

- **Does:** Paging activity
    
- **Look for:** `si` / `so` > 0 (active swapping)
    

### Errors

```bash
dmesg | grep -i oom
```

- **Does:** OOM killer events
    
- **Look for:** Processes being killed
    

---

## 3️⃣ Disk / Storage

### Utilization

```bash
iostat -xz 1
```

- **Does:** Disk busy time and latency
    
- **Look for:** `%util` near 100%
    

### Saturation

```bash
iostat -x 1
```

- **Does:** Disk queue depth
    
- **Look for:** High `avgqu-sz`, long `await`
    

### Errors

```bash
dmesg | grep -i -E "error|fail|reset"
```

- **Does:** Storage error logs
    
- **Look for:** I/O errors, controller resets
    

---

## 4️⃣ Network

### Utilization

```bash
sar -n DEV 1
```

- **Does:** Per-interface throughput
    
- **Look for:** RX/TX near NIC limits
    

### Saturation

```bash
ss -s
```

- **Does:** Socket summary
    
- **Look for:** Large connection counts, retries
    

### Errors

```bash
ip -s link
```

- **Does:** NIC error counters
    
- **Look for:** Dropped packets, overruns
    

---

## 5️⃣ Filesystems

### Utilization

```bash
df -h
df -i
```

- **Does:** Disk space & inode usage
    
- **Look for:** 100% full disks or inodes
    

### Saturation

```bash
cat /proc/sys/fs/file-nr
```

- **Does:** File descriptor usage
    
- **Look for:** Near system limits
    

### Errors

```bash
dmesg | grep -i ext4
dmesg | grep -i xfs
```

- **Does:** Filesystem error logs
    
- **Look for:** Corruption, remounts
    

---

## 🧠 Rule of Thumb

> **If Utilization is high → check Saturation.**  
> **If Saturation exists → look for Errors.**  
> **Only then debug the application.**

---

## 🚦 Common Patterns

|Symptom|Likely Bottleneck|
|---|---|
|High load, idle CPU|Disk I/O|
|CPU 100%, low I/O|CPU bound|
|Swap activity|Memory pressure|
|Packet drops|Network saturation|

---

If you want, I can:

- Turn this into a **PDF / printable version**
    
- Create a **night-shift ultra-minimal checklist**
    
- Add a **“what to alert on” section mapped to USE**
    
- Add **example incident scenarios** per resource
    

Just tell me which one you want next.