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
        SHORT_TIMEOUT = '3'
        LONG_TIMEOUT = '10'
        VIDEO_RECORDING = 'True'
        HEADLESS = 'True'
        MAXIMIZED = 'False'
        PYTHONUNBUFFERED = '1'
    }
    
    stages {
        stage('Setup') {
            steps {
                ansiColor('xterm') {
                    script {
                        echo 'Creating directories for reports and artifacts'
                        sh 'mkdir -p reports tests_recordings tests_screenshots'
                        
                        withCredentials([
                            string(credentialsId: 'BASE_URL', variable: 'BASE_URL'),
                            string(credentialsId: 'TEST_USERNAME', variable: 'USERNAME'),
                            string(credentialsId: 'TEST_PASSWORD', variable: 'PASSWORD')
                        ]) {
                            writeFile file: '.env', text: """BASE_URL=${BASE_URL}
SHORT_TIMEOUT=${SHORT_TIMEOUT}
LONG_TIMEOUT=${LONG_TIMEOUT}
VIDEO_RECORDING=${VIDEO_RECORDING}
HEADLESS=${HEADLESS}
MAXIMIZED=${MAXIMIZED}
USERNAME=${USERNAME}
PASSWORD=${PASSWORD}"""
                            
                            echo 'Verifying BASE_URL is accessible'
                            sh 'curl -sf ${BASE_URL} > /dev/null || exit 1'
                        }
                    }
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                ansiColor('xterm') {
                    script {
                        def browsers = params.BROWSER == 'both' ? ['chrome', 'firefox'] : [params.BROWSER]
                        
                        parallel browsers.collectEntries { browser -> 
                            [(browser): {
                                sh """
                                    xvfb-run -a -s "-screen 0 1920x1080x24" \
                                        pytest tests/ -v -n ${params.WORKERS} --dist=loadfile \
                                        --browser=${browser} \
                                        --alluredir=reports/allure-results-${browser} \
                                        --junitxml=reports/junit-${browser}.xml \
                                        --reruns 1 --reruns-delay 2 -m ${params.MARKER} || true
                                """
                            }]
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            ansiColor('xterm') {
                script {
                    def browsers = params.BROWSER == 'both' ? ['chrome', 'firefox'] : [params.BROWSER]
                    
                    browsers.each { browser ->
                        sh """
                            [ -d "reports/allure-results-${browser}" ] && \
                            allure generate reports/allure-results-${browser} \
                            -o reports/allure-report-${browser} --clean || true
                        """
                        
                        publishHTML([
                            allowMissing: true,
                            alwaysLinkToLastBuild: true,
                            keepAll: true,
                            reportDir: "reports/allure-report-${browser}",
                            reportFiles: 'index.html',
                            reportName: "Allure - ${browser.capitalize()}"
                        ])
                    }
                    
                    archiveArtifacts artifacts: 'reports/**,tests_recordings/**,tests_screenshots/**', allowEmptyArchive: true
                }
            }
        }
        
        cleanup {
            cleanWs(deleteDirs: true, patterns: [[pattern: 'reports/**', type: 'INCLUDE']])
        }
    }
}