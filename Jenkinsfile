pipeline {
    agent {node {label "${env.AGENT_LABEL}"}}
    environment{
        FLASK_APP='AWS_automation'
    }
    stages {
        stage('Code checkout'){
            steps{
                git branch: 'main', credentialsId: 'github', url: 'https://github.com/Akhamesra/create_image.git'
                echo 'Code Checkout Done'
            }
        }
        
        stage('set variables'){
            steps{
                script{
                    ec2_name = "${env.EC2_Name}"
                    ipv4 = "${env.IPv4}"
                    refid = "${env.REF_ID}"
                }
            }
        }
        
        stage('Creating Image'){
            steps{
                script{
                    if(ec2_name){
                        // sh "echo name : "+ec2_name
                        sh "flask ami_cli create_ami -r "+REF_ID+" -n "+ec2_name
                    }
                    else{
                        // sh "echo ipv4 : "+ipv4
                        sh "flask ami_cli create_ami -r "+REF_ID+" -i "+ipv4
                    }
                    
                }
            }
        }

    }
}
