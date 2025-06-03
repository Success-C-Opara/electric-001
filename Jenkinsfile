pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'                             // AWS region (not used here, keep for future)
        EC2_USER = 'ec2-user'                                        // EC2 username
        EC2_HOST = '16.170.231.171'                                  // EC2 public IP
        PRIVATE_KEY = credentials('ec2-ssh-key')                     // SSH private key credential ID in Jenkins
        IMAGE_NAME = 'my-app'                                        // Docker image name
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"                      // Docker image tag using build number
        BRANCH_NAME = 'main'                                         // Git branch to build from
        GIT_REPO = 'https://github.com/Success-C-Opara/electric-001.git' // GitHub repo URL
    }

    stages {
        stage('Clone Code') {
            steps {
                // Clone the specific branch from GitHub repository
                git branch: "${BRANCH_NAME}", url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image locally tagged with build number
                sh """
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Save Docker Image') {
            steps {
                // Save the Docker image as a tarball to transfer to EC2 instance
                sh """
                docker save -o ${IMAGE_NAME}-${IMAGE_TAG}.tar ${IMAGE_NAME}:${IMAGE_TAG}
                """
                // Archive the tarball as a Jenkins artifact (optional)
                archiveArtifacts artifacts: "${IMAGE_NAME}-${IMAGE_TAG}.tar"
            }
        }

        stage('Copy and Deploy to EC2') {
            steps {
                // Copy the Docker image tarball to EC2 instance and deploy
                sh """
                scp -o StrictHostKeyChecking=no -i ${PRIVATE_KEY} ${IMAGE_NAME}-${IMAGE_TAG}.tar ${EC2_USER}@${EC2_HOST}:~/

                ssh -o StrictHostKeyChecking=no -i ${PRIVATE_KEY} ${EC2_USER}@${EC2_HOST} << EOF
                    docker stop ${IMAGE_NAME} || true
                    docker rm ${IMAGE_NAME} || true
                    docker load -i ${IMAGE_NAME}-${IMAGE_TAG}.tar
                    docker run -d --name ${IMAGE_NAME} -p 80:80 ${IMAGE_NAME}:${IMAGE_TAG}
                EOF
                """
            }
        }
    }
}
