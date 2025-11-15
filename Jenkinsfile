pipeline {
    agent any

    environment {
        ALLURE_RESULTS = 'allure-results'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                    python3 --version || echo "Python3 not found, installing..."
                    python3 -m pip install --upgrade pip
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('Install Allure CLI') {
            steps {
                sh '''
                    # Установка Allure CLI
                    curl -o allure-2.15.0.tgz -Ls https://github.com/allure-framework/allure2/releases/download/2.15.0/allure-2.15.0.tgz
                    tar -zxvf allure-2.15.0.tgz
                    export PATH=$PATH:$(pwd)/allure-2.15.0/bin
                    allure --version
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    pytest
                '''
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh '''
                    # Используем локально установленный Allure
                    export PATH=$PATH:$(pwd)/allure-2.15.0/bin
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