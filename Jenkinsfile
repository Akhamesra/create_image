pipeline {
    agent any

    stages {
        stage('Code checkout'){
            steps{
                git branch: 'main', credentialsId: 'github', url: 'https://github.com/Akhamesra/create_image.git'
                echo 'Code Checkout Done'
            }
        }
        stage('Run Python Script') {
            steps {
                sh 'python3 AWS_automation.py'
            }
        }
    }
}