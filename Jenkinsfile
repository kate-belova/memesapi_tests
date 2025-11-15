pipeline {
    agent {
        docker {
            image 'python:3.13-alpine'
            args '--user root'
        }
    }

    environment {
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    apk add --no-cache git
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                    apk add --no-cache openjdk11
                    wget -O allure-2.15.0.tgz https://github.com/allure-framework/allure2/releases/download/2.15.0/allure-2.15.0.tgz
                    tar -zxvf allure-2.15.0.tgz -C /opt/
                    ln -s /opt/allure-2.15.0/bin/allure /usr/local/bin/allure

                    allure generate ${ALLURE_RESULTS} --clean -o allure-report
                '''
            }
        }
    }

    post {
        always {
            allure includeProperties: false,
                   jdk: '',
                   results: [[path: '${ALLURE_RESULTS}']]

            archiveArtifacts artifacts: 'allure-report/**/*', fingerprint: true
        }

        success {
            echo '✅ All tests passed successfully!'
        }

        failure {
            echo '❌ Tests failed!'
        }
    }
}