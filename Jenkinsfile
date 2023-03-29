pipeline {
    agent {node {label "${env.AGENT_LABEL}"}}
    stages {
        stage('Code checkout'){
            steps{
                git branch: 'main', credentialsId: 'github', url: 'https://github.com/Akhamesra/create_image.git'
                echo 'Code Checkout Done'
            }
        }

        stage('Run Python Script') {
            steps {
                sh 'flask ami_cli create_ami -n ${env.EC2_Name} -i ${env.Image_name} -r {$env.REF_ID}'
            }
        }
    }
}