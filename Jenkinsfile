pipeline {
    agent any
    environment {
        DOCKER_USER = "imamaziz" 
        GIT_REPO_URL = "https://github.com/imam-aziz/kantin-app.git"
    }
    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', credentialsId: 'github-token', url: "${GIT_REPO_URL}"
            }
        }
        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-login', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    // Semua pakai sh sesuai poin 4d
                    sh "docker build -t ${USER}/kantin-backend:latest ./backend"
                    sh "docker build -t ${USER}/kantin-frontend:latest ./frontend"
                    sh "echo ${PASS} | docker login -u ${USER} --password-stdin"
                    sh "docker push ${USER}/kantin-backend:latest"
                    sh "docker push ${USER}/kantin-frontend:latest"
                }
            }
        }
        stage('Deploy ke Azure AKS') {
            steps {
                withKubeConfig([credentialsId: 'kube-config']) {
                    // Poin 4c: Deploy menggunakan kubeconfig
                    sh "kubectl apply -f kantin-k8s.yaml"
                    sh "kubectl rollout restart deployment backend-kantin"
                    sh "kubectl rollout restart deployment frontend-kantin"
                }
            }
        }
    }
}