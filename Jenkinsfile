pipeline {
    agent any
    environment {
        // GANTI dengan username Docker Hub kamu
        DOCKER_USER = "imamaziz" 
        // GANTI dengan URL Repo GitHub kamu
        GIT_REPO_URL = "https://github.com/imamaziz/kantin-app.git"
    }
    stages {
        stage('Checkout Code') {
            steps {
                // Mengambil kode terbaru dari GitHub
                git branch: 'main', url: "${GIT_REPO_URL}"
            }
        }
        stage('Build & Push Docker Image') {
            steps {
                // 'dockerhub-login' adalah ID Credential yang harus kamu buat di Jenkins
                withCredentials([usernamePassword(credentialsId: 'dockerhub-login', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    
                    // Build image menggunakan Dockerfile di folder masing-masing
                    sh "docker build -t ${USER}/kantin-backend:latest ./backend"
                    sh "docker build -t ${USER}/kantin-frontend:latest ./frontend"
                    
                    // Login dan Push ke Docker Hub
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${USER}/kantin-backend:latest"
                    sh "docker push ${USER}/kantin-frontend:latest"
                }
            }
        }
        stage('Deploy ke Azure AKS') {
            steps {
                // 'aks-config' adalah ID Credential Kubeconfig yang harus kamu buat di Jenkins
                withKubeConfig([credentialsId: 'aks-config']) {
                    // Menerapkan perubahan manifest ke kluster AKS
                    sh "kubectl apply -f kantin-k8s.yaml"
                    
                    // Restart agar pod menggunakan image terbaru yang baru di-push
                    sh "kubectl rollout restart deployment backend-kantin"
                    sh "kubectl rollout restart deployment frontend-kantin"
                }
            }
        }
    }
}