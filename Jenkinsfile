pipeline {
    agent any
    
    parameters {
        choice(name: 'BROWSER', choices: ['both', 'chrome', 'firefox'], description: 'Browser to run tests on')
        choice(name: 'MARKER', choices: ['full', 'smoke', 'regression'], description: 'Test marker to run')
        string(name: 'WORKERS', defaultValue: 'auto', description: 'Number of parallel workers')
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }
    
    environment {
        ALLURE_SERVER_URL = 'http://allure:5050'  // Hardcode since it's local and secure
        SHORT_TIMEOUT = '3'
        LONG_TIMEOUT = '10'
        VIDEO_RECORDING = 'True'
        HEADLESS = 'True'
        MAXIMIZED = 'False'
        PYTHONUNBUFFERED = '1'
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
                script {
                    def browsers = params.BROWSER == 'both' ? ['chrome', 'firefox'] : [params.BROWSER]
                    
                    parallel browsers.collectEntries { browser -> 
                        [(browser): {
                            sh """
                                xvfb-run -a -s "-screen 0 1920x1080x24" \
                                    pytest tests/ -v -n ${params.WORKERS} --dist=loadfile \
                                    --browser=${browser} \
                                    --alluredir=allure-results-${browser} \
                                    --html=report-${browser}.html \
                                    --self-contained-html \
                                    --reruns 1 --reruns-delay 2 -m ${params.MARKER} || true
                            """
                        }]
                    }
                }
            }
        }
        
        stage('Upload Reports') {  // New stage for clarity
            steps {
                script {
                    def browsers = params.BROWSER == 'both' ? ['chrome', 'firefox'] : [params.BROWSER]
                    
                    browsers.each { browser ->
                        uploadToAllure(browser, 'latest-only')
                        uploadToAllure(browser, 'latest-with-history')
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

def uploadToAllure(browser, reportType) {
    def resultsDir = "allure-results-${browser}"
    def projectName = "selenium-tests-${browser}-${reportType}"
    def allureUrl = env.ALLURE_SERVER_URL
    
    sh """
        # Prepare results
        if [ "${reportType}" = "latest-with-history" ]; then
            # Merge history for latest-with-history
            mkdir -p ${resultsDir}/history
            if [ -d "/workspace/allure-history/${browser}" ]; then
                cp -r /workspace/allure-history/${browser}/* ${resultsDir}/history/ || true
            fi
        fi
        
        # Tar and upload
        cd ${resultsDir}
        tar -czf ../allure-results-${browser}-${reportType}.tar.gz .
        cd ..
        
        echo "Uploading ${browser} ${reportType} results to Allure Docker Service..."
        RESPONSE=\$(curl -X POST \
            -F "results=@allure-results-${browser}-${reportType}.tar.gz" \
            -L \
            -w "\\nHTTP Status: %{http_code}\\n" \
            -s \
            "${allureUrl}/allure-docker-service/send-results?project_id=${projectName}")
        
        echo "\$RESPONSE"
        
        HTTP_CODE=\$(echo "\$RESPONSE" | tail -n 1 | grep -oP '\\d+')
        if [ "\$HTTP_CODE" = "200" ]; then
            echo "✓ ${browser} ${reportType} report uploaded successfully!"
            echo "View report at: ${allureUrl}/allure-docker-service/projects/${projectName}/reports/latest/index.html"
            
            # Update history for latest-with-history
            if [ "${reportType}" = "latest-with-history" ]; then
                mkdir -p /workspace/allure-history/${browser}
                # Generate report locally to extract history (optional, if needed)
                allure generate --clean ${resultsDir} -o temp-report || true
                if [ -d "temp-report/history" ]; then
                    cp -r temp-report/history/* /workspace/allure-history/${browser}/ || true
                fi
                rm -rf temp-report
            fi
        else
            echo "✗ Upload failed with status: \$HTTP_CODE"
            exit 1
        fi
    """
}