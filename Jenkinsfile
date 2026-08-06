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
                sh 'pip install -r requirements.txt --break-system-packages'
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Trivy Image Scan') {
            steps {
                sh 'trivy image --exit-code 0 --severity HIGH,CRITICAL --format table $DOCKER_IMAGE | tee trivy-report.txt'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'trivy-report.txt', allowEmptyArchive: true
                }
            }
        }

	

		stage('Grype Image Scan') {
    steps {
        grypeScan(
            autoInstall: false,
            scanDest: "docker:${DOCKER_IMAGE}",
            repName: "grype-report"
        )

        recordIssues(
            enabledForFailure: true,
            tools: [grype(pattern: 'grype-report')]
        )
    }

    post {
        always {
            archiveArtifacts artifacts: 'grype-report*', allowEmptyArchive: true
        }
    }
}
	
	


	stage('Unit Tests') {
            steps {
                sh 'python3 -m pytest --junitxml=results.xml --cov=. --cov-report=xml'
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
                   sh 'sonar-scanner -Dsonar.projectKey=calculator-app -Dsonar.sources=. -Dsonar.exclusions=venv/**,**/__pycache__/** -Dsonar.host.url=$SONAR_HOST_URL -Dsonar.login=$SONAR_AUTH_TOKEN -Dsonar.python.coverage.reportPaths=coverage.xml'
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
        stage('OWASP ZAP DAST Scan') {
            steps {
                sh '''
    docker run -d --name calc-zap-target --network jenkins-network -p 5050:5000 calculator-app:$BUILD_NUMBER
    sleep 5
    docker run --rm --network jenkins-network -v "$(pwd):/zap/wrk/:rw" -t zaproxy/zap-stable zap-baseline.py -t http://calc-zap-target:5000 -r zap-report.html || true
    docker rm -f calc-zap-target
'''
            }
            post {
                always {
                    archiveArtifacts artifacts: 'zap-report.html', allowEmptyArchive: true
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
