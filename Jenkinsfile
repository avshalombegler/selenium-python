pipeline {
    agent any
    
    environment {
        RAILWAY_ALLURE_SERVER_URL = credentials('railway-allure-server-url')
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
            parallel {
                stage('Chrome Tests') {
                    steps {
                        sh """
                            pytest tests/ \
                                --alluredir=allure-results-chrome \
                                --browser=chrome \
                                --html=report-chrome.html \
                                --self-contained-html \
                                -v
                        """
                    }
                    post {
                        always {
                            script {
                                uploadToRailway('chrome')
                            }
                        }
                    }
                }
                stage('Firefox Tests') {
                    steps {
                        sh """
                            pytest tests/ \
                                --alluredir=allure-results-firefox \
                                --browser=firefox \
                                --html=report-firefox.html \
                                --self-contained-html \
                                -v
                        """
                    }
                    post {
                        always {
                            script {
                                uploadToRailway('firefox')
                            }
                        }
                    }
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

def uploadToRailway(browser) {
    def resultsDir = "allure-results-${browser}"
    def projectName = "selenium-tests-${browser}"
    def buildId = env.BUILD_NUMBER
    def railwayUrl = env.RAILWAY_ALLURE_SERVER_URL
    
    sh """
        cd ${resultsDir}
        tar -czf ../allure-results-${browser}.tar.gz .
        cd ..
        
        echo "Uploading ${browser} results to Railway Allure Server..."
        RESPONSE=\$(curl -X POST \
            -H "Content-Type: application/gzip" \
            --data-binary @allure-results-${browser}.tar.gz \
            -L \
            -w "\\nHTTP Status: %{http_code}\\n" \
            -s \
            "${railwayUrl}/api/upload/${projectName}?buildId=${buildId}")
        
        echo "\$RESPONSE"
        
        HTTP_CODE=\$(echo "\$RESPONSE" | tail -n 1 | grep -oP '\\d+')
        if [ "\$HTTP_CODE" = "200" ]; then
            echo "✓ ${browser} report uploaded successfully!"
            echo "View report at: ${railwayUrl}/reports/${projectName}/latest"
        else
            echo "✗ Upload failed with status: \$HTTP_CODE"
            exit 1
        fi
    """
}