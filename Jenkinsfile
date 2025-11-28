pipeline {
    agent any
    
    environment {
        ALLURE_SERVER_URL = credentials('allure-server-url')
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
                                uploadToAllure('chrome')
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
                                uploadToAllure('firefox')
                            }
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo "✓ Tests passed and report uploaded to Allure Docker Service!"
            echo "View combined reports: ${ALLURE_SERVER_URL}/allure-docker-service/projects"
        }
        failure {
            echo "✗ Tests failed. Check reports for details."
        }
    }
}

def uploadToAllure(browser) {
    def resultsDir = "allure-results-${browser}"
    def projectName = "selenium-tests-${browser}"
    def buildId = env.BUILD_NUMBER
    def allureUrl = env.ALLURE_SERVER_URL
    
    sh """
        cd ${resultsDir}
        tar -czf ../allure-results-${browser}.tar.gz .
        cd ..
        
        echo "Uploading ${browser} results to Allure Docker Service..."
        RESPONSE=\$(curl -X POST \
            -H "Content-Type: application/gzip" \
            --data-binary @allure-results-${browser}.tar.gz \
            -L \
            -w "\\nHTTP Status: %{http_code}\\n" \
            -s \
            "${allureUrl}/allure-docker-service/send-results?project_id=${projectName}")
        
        echo "\$RESPONSE"
        
        HTTP_CODE=\$(echo "\$RESPONSE" | tail -n 1 | grep -oP '\\d+')
        if [ "\$HTTP_CODE" = "200" ]; then
            echo "✓ ${browser} report uploaded successfully!"
            echo "View report at: ${allureUrl}/allure-docker-service/projects/${projectName}/reports/latest/index.html"
        else
            echo "✗ Upload failed with status: \$HTTP_CODE"
            exit 1
        fi
    """
}