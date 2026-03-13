pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'master', url: 'https://github.com/manjuabhinayavr/E-commerce-website.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t flask-ecommerce .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker rm -f flask-app || true'
            }
        }

        stage('Deploy Container') {
            steps {
                sh 'docker run -d --name flask-app -p 5000:5000 flask-ecommerce'
            }
        }
    }
}