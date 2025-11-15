pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    echo "Python version:"
                    python3 --version

                    echo "Installing project dependencies..."
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh 'python3 -m pytest --alluredir=allure-results -v'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**/*', fingerprint: true

            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'allure-results',
                reportFiles: '**/*.html',
                reportName: 'Test Results'
            ])
        }

        success {
            echo '✅ All tests passed successfully!'
        }

        failure {
            echo '❌ Tests failed!'
        }
    }
}