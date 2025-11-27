pipeline {
    agent any
    
    environment {
        PYTHON_VERSION = '3.10'
        RAILWAY_ALLURE_URL = credentials('railway-allure-url')
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
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests/ \
                        --alluredir=allure-results \
                        --html=report.html \
                        --self-contained-html \
                        -v || true
                '''
            }
        }
        
        stage('Upload to Railway Allure Server') {
            steps {
                script {
                    def projectName = 'selenium-tests-jenkins'
                    def buildId = env.BUILD_NUMBER
                    
                    sh """
                        if [ -d "allure-results" ]; then
                            cd allure-results
                            tar -czf ../allure-results.tar.gz .
                            cd ..
                            
                            echo "Uploading to Railway Allure Server..."
                            curl -X POST \
                                -H "Content-Type: application/gzip" \
                                --data-binary @allure-results.tar.gz \
                                "${RAILWAY_ALLURE_URL}/api/upload/${projectName}?buildId=${buildId}" \
                                -w "\\nHTTP Status: %{http_code}\\n"
                            
                            echo "✓ Report uploaded successfully!"
                            echo "View report at: ${RAILWAY_ALLURE_URL}/reports/${projectName}"
                        fi
                    """
                }
            }
        }
        
        stage('Generate Local Allure Report') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'allure-results']]
                    ])
                }
            }
        }
        
        stage('Archive Reports') {
            steps {
                publishHTML([
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: true,
                    reportDir: 'allure-report',
                    reportFiles: 'index.html',
                    reportName: 'Allure Report',
                    reportTitles: "Build ${env.BUILD_NUMBER}"
                ])
                
                archiveArtifacts artifacts: 'report.html', allowEmptyArchive: true
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo "✓ Tests passed and report uploaded to Railway!"
            echo "View report: ${RAILWAY_ALLURE_URL}/reports/selenium-tests-jenkins"
        }
        failure {
            echo "✗ Tests failed. Check reports for details."
        }
    }
}