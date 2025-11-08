// Jenkinsfile for DMARC Parser
// This pipeline runs the DMARC parser on a schedule

pipeline {
    agent any
    
    // Schedule: Run daily at 2 AM
    triggers {
        cron('H 2 * * *')
    }
    
    environment {
        // Credentials stored in Jenkins Credentials
        GMAIL_CREDENTIALS = credentials('gmail-dmarc-credentials')
        REPORT_DIR = "${WORKSPACE}/reports"
    }
    
    stages {
        stage('Setup') {
            steps {
                echo 'Setting up environment...'
                sh 'mkdir -p ${REPORT_DIR}'
                sh 'python3 --version'
            }
        }
        
        stage('Run DMARC Parser') {
            steps {
                echo 'Running DMARC parser...'
                script {
                    def timestamp = sh(returnStdout: true, script: 'date +%Y%m%d_%H%M%S').trim()
                    def reportFile = "${REPORT_DIR}/dmarc_failures_${timestamp}.json"
                    
                    sh """
                        python3 dmarc_parser.py \
                            --email "${GMAIL_CREDENTIALS_USR}" \
                            --password "${GMAIL_CREDENTIALS_PSW}" \
                            --limit 100 \
                            --output "${reportFile}"
                    """
                    
                    // Store report file path for later stages
                    env.REPORT_FILE = reportFile
                }
            }
        }
        
        stage('Analyze Results') {
            steps {
                script {
                    // Parse JSON to check for failures
                    def failureCount = sh(
                        returnStdout: true,
                        script: "python3 -c 'import json; data=json.load(open(\"${env.REPORT_FILE}\")); print(data[\"total_failures\"])'"
                    ).trim().toInteger()
                    
                    echo "Total failures found: ${failureCount}"
                    
                    if (failureCount > 0) {
                        echo "WARNING: DMARC failures detected!"
                        // Mark build as unstable if failures found
                        currentBuild.result = 'UNSTABLE'
                        
                        // Optional: Send notification
                        // emailext (
                        //     subject: "DMARC Failures Detected: ${failureCount}",
                        //     body: "Please review the attached report.",
                        //     attachmentsPattern: "${env.REPORT_FILE}",
                        //     to: "admin@yourdomain.com"
                        // )
                    } else {
                        echo "All DMARC checks passed!"
                    }
                }
            }
        }
        
        stage('Archive Report') {
            steps {
                echo 'Archiving report...'
                archiveArtifacts artifacts: 'reports/*.json', fingerprint: true
            }
        }
        
        stage('Cleanup Old Reports') {
            steps {
                echo 'Cleaning up old reports (keeping last 30 days)...'
                sh 'find ${REPORT_DIR} -name "dmarc_failures_*.json" -mtime +30 -delete || true'
            }
        }
    }
    
    post {
        success {
            echo 'DMARC parser completed successfully'
        }
        failure {
            echo 'DMARC parser failed!'
            // Send failure notification
            // emailext (
            //     subject: "DMARC Parser Job Failed",
            //     body: "The DMARC parser job failed. Please check Jenkins logs.",
            //     to: "admin@yourdomain.com"
            // )
        }
        always {
            echo "Build completed with status: ${currentBuild.result}"
        }
    }
}
