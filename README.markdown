# 🐳 Dockerized Todo List Microservices App with Helm & ArgoCD (GitOps)

A complete DevOps pipeline for deploying a Todo List web application using Docker, Kubernetes, Helm, and ArgoCD. The app features a responsive UI for managing todos with customizable themes, backed by a Flask API and PostgreSQL database.

---

## 🚀 Features

- **Todo Management**: Add, mark as completed, and delete todos with animations.
- **Customizable Themes**: Three theme options (standard, light, darker) with smooth transitions.
- **Real-Time Datetime**: Displays current date and time in the top-left corner.
- **Responsive Design**: Works on both mobile and desktop devices.
- **Containerization**: Docker for all services (frontend, backend, database).
- **Orchestration**: Kubernetes for scalable deployments.
- **Packaging**: Helm charts for easy configuration.
- **Continuous Delivery**: GitOps workflow with ArgoCD.
- **Persistent Storage**: PostgreSQL for storing todos.

---

## 🛠️ Tech Stack

| Layer         | Technology         |
| ------------- | ------------------ |
| Frontend      | HTML, CSS, JavaScript, Nginx |
| Backend       | Flask (Python) API |
| Database      | PostgreSQL         |
| Container     | Docker             |
| Orchestration | Kubernetes         |
| GitOps        | Helm + ArgoCD      |

---

## 📁 Project Structure

```
realsahilthakur-dockerized-microservices-app/
├── README.md                         # This file
├── docker-compose.yml                # Docker Compose for local development
├── docker-stack.yml                  # Docker Stack for Docker Swarm deployment
├── BACKEND/                          # Backend service (Python Flask)
│   ├── app.py                        # Flask application code
│   ├── Dockerfile                    # Dockerfile for backend image
│   └── requirements.txt              # Python dependencies
├── FRONTEND/                         # Frontend service (Nginx serving static HTML/CSS/JS)
│   ├── default.conf                  # Nginx configuration
│   ├── Dockerfile                    # Dockerfile for frontend image
│   ├── index.html                    # Todo List HTML
│   ├── main.css                      # Todo List styles
│   ├── main.js                       # Todo List JavaScript logic
│   └── time.js                       # Real-time datetime display
└── helm-chart/                       # Helm chart for Kubernetes deployment
    ├── Chart.yaml                    # Helm chart metadata
    ├── values.yaml                   # Default values for Helm chart
    └── templates/                    # Kubernetes resource templates
        ├── argocd-app.yaml           # ArgoCD Application definition
        ├── backend-deployment.yaml   # Kubernetes Deployment for backend
        ├── backend-service.yaml      # Kubernetes Service for backend
        ├── db-deployment.yaml        # Kubernetes Deployment for database
        ├── db-service.yaml           # Kubernetes Service for database
        ├── frontend-deployment.yaml  # Kubernetes Deployment for frontend
        └── frontend-service.yaml     # Kubernetes Service for frontend
```

---

## ✅ Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)
- [Kubernetes](https://kubernetes.io/) (e.g., Minikube or a cloud provider)
- [Helm](https://helm.sh/) (v3 or higher)
- [ArgoCD](https://argo-cd.readthedocs.io/) for GitOps
- Git and a GitHub account
- Modern web browser (Chrome, Firefox, etc.)

---

## 🛠️ Local Development with Docker Compose

1. **Build and run all services:**

```bash
docker-compose up --build
```

2. **Access the Todo List app in browser:**

`http://localhost:8000`

3. **Stop services:**

```bash
docker-compose down
```

---

## ☸️ Kubernetes Deployment with Helm

1. **Create namespace (optional):**

```bash
kubectl create ns microservices
```

2. **Deploy with Helm:**

```bash
helm install microservices-app ./helm-chart -n microservices
```

3. **Access the app:**

`http://<node-ip>:30080`

4. **Upgrade deployment:**

```bash
helm upgrade microservices-app ./helm-chart -n microservices
```

---

## 🚀 Continuous Delivery with ArgoCD (GitOps)

1. **Install ArgoCD:**

```bash
kubectl create ns argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argocd/stable/manifests/install.yaml
```

2. **Port-forward ArgoCD server:**

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

3. **Login to ArgoCD CLI:**

```bash
argocd login localhost:8080 --insecure
```

4. **Add your private GitHub repo to ArgoCD:**

```bash
argocd repo add https://github.com/realsahilthakur/dockerized-microservices-app.git --username <your-username> --password <personal-access-token>
```

5. **Create and sync app:**

```bash
argocd app sync microservices-app
```

---

## 🧑‍💻 Usage

- **Add Todo**: Type in the input field and click "Hit it!"
- **Complete Todo**: Click ✅ to mark a todo as completed (strikethrough effect).
- **Delete Todo**: Click 🗑️ to remove a todo with an animation.
- **Change Theme**: Click on `standard`, `light`, or `darker` buttons in the top-right corner.

---

## 🔐 Security Notes

- **Environment Variables**: Do not hardcode sensitive data (e.g., `POSTGRES_PASSWORD`) in production. Use Kubernetes secrets or a secrets manager.
- **PostgreSQL**:
  - Use strong credentials in production.
  - Restrict network access to the database.
- **GitHub**:
  - Use a private repository for better security.
  - Secure your personal access token for ArgoCD.

---

## 🧪 Troubleshooting

| Issue | Solution |
|-------|----------|
| Database connection error | Check `DB_HOST` (`db`) and ensure PostgreSQL is running on port 5432 inside the container |
| Frontend not loading | Check browser console (F12 → Console) for errors |
| Backend not responding | Check logs: `docker logs <backend-container>` or `kubectl logs <backend-pod> -n microservices` |
| 404 for favicon.png | Add a `favicon.png` to `FRONTEND/` or remove the favicon link in `index.html` |
| Nginx upstream error | Ensure `backend` service is running and accessible; verify `default.conf` uses `backend:9000` |
| PostgreSQL connection error | Ensure `db` service is running and accessible; verify `app.py` uses `db` as `DB_HOST` |

---

## 🔮 Future Improvements

- Add user authentication (e.g., with Clerk, already a dependency).
- Implement todo categories and due dates.
- Add filtering and sorting of todos.
- Enhance error handling and user feedback.

---

## 🙌 Authors

**Sahil Thakur** & **Sneha Kaimal**

```DevOps | Kubernetes | CI/CD | GitOps | Python```

---

## 🏁 License

This project is licensed under the MIT License.