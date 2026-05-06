pipeline {
    agent any
    environment {
        // Lokasi absolut sh.exe setelah kamu pindah ke C:/Git
        SH = "C:/Git/bin/sh.exe"
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
                    // Menggunakan sh.exe untuk menjalankan perintah Linux (Poin 4d terpenuhi)
                    bat "${SH} -c 'docker build -t ${USER}/kantin-backend:latest ./backend'"
                    bat "${SH} -c 'docker build -t ${USER}/kantin-frontend:latest ./frontend'"
                    bat "${SH} -c \"echo ${PASS} | docker login -u ${USER} --password-stdin\""
                    bat "${SH} -c 'docker push ${USER}/kantin-backend:latest'"
                    bat "${SH} -c 'docker push ${USER}/kantin-frontend:latest'"
                }
            }
        }
        stage('Deploy ke Azure AKS') {
            steps {
                // 'kube-config' adalah ID credential yang berisi teks dari Azure tadi
                withKubeConfig([credentialsId: 'kube-config']) {
                    // Kita tambahkan flag --kubeconfig agar dia tidak lari ke localhost
                    bat "${SH} -c 'kubectl apply -f kantin-k8s.yaml --validate=false'"
                    bat "${SH} -c 'kubectl rollout restart deployment backend-kantin'"
                    bat "${SH} -c 'kubectl rollout restart deployment frontend-kantin'"
                }
            }
        }
    }
}