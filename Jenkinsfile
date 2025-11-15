pipeline {
    agent any

    tools {
        python 'python3.13'
        nodejs 'nodejs'
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
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pytest'
                //
            }
        }

        stage('Generate Allure Report') {
            steps {
                sh """
                    allure generate ${ALLURE_RESULTS} --clean -o allure-report
                """
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

            sh '''
                rm -rf allure-results || true
            '''
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