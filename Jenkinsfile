pipeline {
    agent any
    
    parameters {
        choice(name: 'BROWSER', choices: ['both', 'chrome', 'firefox'], description: 'Browser to run tests on')
        choice(name: 'MARKER', choices: ['full', 'smoke', 'regression'], description: 'Test marker to run')
        string(name: 'WORKERS', defaultValue: 'auto', description: 'Number of parallel workers')
    }
    
    options {
        timeout(time: 30, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
        timestamps()
    }
    
    environment {
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
                        
        stage('Prepare Directories') {
            steps {
                sh '''
                    mkdir -p reports
                    mkdir -p tests_recordings tests_screenshots
                '''
            }
        }
        
        stage('Create .env File') {
            steps {
                withCredentials([
                    string(credentialsId: 'BASE_URL', variable: 'BASE_URL'),
                    string(credentialsId: 'TEST_USERNAME', variable: 'USERNAME'),
                    string(credentialsId: 'TEST_PASSWORD', variable: 'PASSWORD')
                ]) {
                    sh '''
                        cat > .env << EOF
BASE_URL=${BASE_URL}
SHORT_TIMEOUT=${SHORT_TIMEOUT}
LONG_TIMEOUT=${LONG_TIMEOUT}
VIDEO_RECORDING=${VIDEO_RECORDING}
HEADLESS=${HEADLESS}
MAXIMIZED=${MAXIMIZED}
USERNAME=${USERNAME}
PASSWORD=${PASSWORD}
EOF
                    '''
                }
            }
        }
        
        stage('Check Website Availability') {
            steps {
                withCredentials([string(credentialsId: 'BASE_URL', variable: 'BASE_URL')]) {
                    sh 'curl -s -f ${BASE_URL} > /dev/null || exit 1'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    def browsers = params.BROWSER == 'both' ? ['chrome', 'firefox'] : [params.BROWSER]
                    def stages = [:]
                    
                    browsers.each { browser ->
                        stages["Test ${browser}"] = {
                            sh """
                                export BROWSER=${browser}
                                xvfb-run --auto-servernum --server-args="-screen 0 1920x1080x24" \
                                    pytest tests/ \
                                    -v \
                                    -n ${params.WORKERS} \
                                    --dist=loadfile \
                                    --browser=${browser} \
                                    --alluredir=reports/allure-results-${browser} \
                                    --junitxml=reports/junit-${browser}.xml \
                                    --reruns 1 \
                                    --reruns-delay 2 \
                                    -m ${params.MARKER} || true
                            """
                        }
                    }
                    
                    parallel stages
                }
            }
        }
    }
    
    post {
        always {
            script {
                def browsers = params.BROWSER == 'both' ? ['chrome', 'firefox'] : [params.BROWSER]
                
                // Generate individual browser HTML reports
                browsers.each { browser ->
                    sh """
                        if [ -d "reports/allure-results-${browser}" ]; then
                            allure generate reports/allure-results-${browser} \
                            -o reports/allure-report-${browser} \
                            --clean
                        fi
                    """
                    
                    // Archive individual browser HTML reports
                    archiveArtifacts artifacts: "reports/allure-report-${browser}/**", allowEmptyArchive: true
                    
                    // Publish individual HTML reports
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: "reports/allure-report-${browser}",
                        reportFiles: 'index.html',
                        reportName: "Allure-Report-${browser}",
                        reportTitles: ''
                    ])
                    
                    // Archive JUnit XML
                    // junit allowEmptyResults: true, testResults: "reports/junit-${browser}.xml"
                }
                
                // Archive other artifacts
                archiveArtifacts artifacts: 'tests_recordings/**', allowEmptyArchive: true
                archiveArtifacts artifacts: 'tests_screenshots/**', allowEmptyArchive: true
            }
        }
        
        success {
            echo 'Pipeline completed successfully!'
        }
        
        failure {
            echo 'Pipeline failed!'
        }
        
        cleanup {
            cleanWs()
        }
    }
}