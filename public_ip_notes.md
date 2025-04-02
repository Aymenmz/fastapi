# ✅ Guide: Getting Real Client IP in FastAPI behind AKS + Ingress + Cloudflare

This guide explains how to get the real **public IP** of a user when your FastAPI app is deployed behind:
- Azure Kubernetes Service (AKS)
- NGINX Ingress Controller
- Cloudflare DNS (proxy enabled)

---

### 1. ✅ FastAPI Code Setup

Update your root route (or middleware) to extract the real IP:

```python
client_ip = (
    request.headers.get("cf-connecting-ip")  # Cloudflare header
    or request.headers.get("x-forwarded-for")  # Generic proxy header
    or request.client.host
)

if "," in client_ip:
    client_ip = client_ip.split(",")[0].strip()
```

---

### 2. ✅ Ingress Annotations

In your Ingress YAML:

```yaml
metadata:
  annotations:
    nginx.ingress.kubernetes.io/use-forwarded-headers: "true"
```

---

### 3. ✅ Ingress ConfigMap

Ensure the NGINX controller ConfigMap includes:

```yaml
use-forwarded-headers: "true"
```

Check with:
```bash
kubectl get configmap ingress-nginx-controller -n ingress-nginx -o yaml | grep use-forwarded-headers
```

---

### 4. ✅ Cloudflare Proxy

In Cloudflare DNS:
- Your `A` or `CNAME` record should have **proxy enabled** (orange cloud ☁️➡️🔶).
- This ensures `CF-Connecting-IP` header is sent.

---

### 5. ✅ (Optional) Enable HTTPS via Cert-Manager

If you're using HTTPS:
```yaml
annotations:
  nginx.ingress.kubernetes.io/ssl-redirect: "true"
  cert-manager.io/cluster-issuer: letsencrypt-prod

tls:
  - hosts:
    - fastapi.maiziz.org
    secretName: fastapi-tls
```

---

### 6. ✅ Test

Use `curl` to simulate the request:
```bash
curl -H "CF-Connecting-IP: 1.2.3.4" https://your-domain.com
```
Should return:
```json
{"message": "Welcome Anonymous!", "ip": "1.2.3.4"}
```

---

This setup ensures the user's real public IP is captured accurately, even behind multiple proxy layers.