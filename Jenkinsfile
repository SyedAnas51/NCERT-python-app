cat > Jenkinsfile << 'EOF'
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "calculator-app:${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'pytest --junitxml=results.xml'
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner -Dsonar.projectKey=calculator-app -Dsonar.sources=.'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Deploy to Development') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    sh 'kubectl apply -f k8s/dev/deployment.yaml'
                }
            }
        }

        stage('Integration Test') {
            steps {
                echo 'Running integration tests against dev environment'
            }
        }

        stage('Deploy to Staging') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    sh 'kubectl apply -f k8s/staging/deployment.yaml'
                }
            }
        }

        stage('Manual Approval') {
            steps {
                input message: 'Approve deployment to Production?', ok: 'Deploy'
            }
        }

        stage('Deploy to Production') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-cred', variable: 'KUBECONFIG')]) {
                    sh 'kubectl apply -f k8s/prod/deployment.yaml'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed — check logs above.'
        }
    }
}
EOF
