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
                    apk add --no-cache nodejs npm
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    npm install -g allure-commandline
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
                    allure generate ${ALLURE_RESULTS} --clean -o allure-report
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-report/**/*', fingerprint: true

            publishHTML(target: [
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'allure-report',
                reportFiles: 'index.html',
                reportName: 'Allure Report'
            ])
        }

        success {
            echo '✅ All tests passed successfully!'
        }

        failure {
            echo '❌ Tests failed!'
        }

        unstable {
            echo '⚠️ Some tests are unstable (flaky)'
        }
    }
}