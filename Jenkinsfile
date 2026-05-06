pipeline {
    agent any
    environment {
        DOCKER_USER = "imamaziz" 
        GIT_REPO_URL = "https://github.com/imam-aziz/kantin-app.git"
    }
    stages {
        stage('Checkout Code') {
            steps {
                // 'github-token' adalah NAMA ID yang kamu buat di Jenkins UI tadi
                git branch: 'main', credentialsId: 'github-token', url: "${GIT_REPO_URL}"
            }
        }
        stage('Build & Push Docker Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-login', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "docker build -t ${USER}/kantin-backend:latest ./backend"
                    sh "docker build -t ${USER}/kantin-frontend:latest ./frontend"
                    sh "docker login -u %USER% -p %PASS%"
                    sh "docker push ${USER}/kantin-backend:latest"
                    sh "docker push ${USER}/kantin-frontend:latest"
                }
            }
        }
        stage('Deploy ke Azure AKS') {
            steps {
                withKubeConfig([credentialsId: 'kube-config']) {
                    sh "kubectl apply -f kantin-k8s.yaml"
                    sh "kubectl rollout restart deployment backend-kantin"
                    sh "kubectl rollout restart deployment frontend-kantin"
                }
            }
        }
    }
}