pipeline {
    agent any

    environment {
        // EC2 instance SSH username (default Amazon Linux user)
        EC2_USER = 'ec2-user' 
        
        // Public IP or DNS of your EC2 instance
        EC2_HOST = '16.170.231.171'
        
        // Absolute path to your private key file (.pem) on the Jenkins agent machine
        // Edit this if your key is stored elsewhere
        PRIVATE_KEY_PATH = 'C:/Users/Success/Downloads/electric-key.pem'
        
        // Docker image name
        IMAGE_NAME = 'my-app'
        
        // Tag the Docker image with the Jenkins build number for uniqueness
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
        
        // GitHub repository URL
        GIT_REPO = 'https://github.com/Success-C-Opara/electric-001.git'
        
        // Branch to build, edit this to run a different branch/job
        BRANCH_NAME = 'main'
    }

    stages {
        stage('Clone Code') {
            // Clone the code from GitHub repo
            steps {
                echo "Cloning branch '${BRANCH_NAME}' from ${GIT_REPO}"
                git branch: "${BRANCH_NAME}", url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            // Build Docker image from the Dockerfile in the repo
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}"
                sh """
                docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                """
            }
        }

        stage('Save Docker Image') {
            // Save Docker image to a tar file for transfer to EC2
            steps {
                echo "Saving Docker image to ${IMAGE_NAME}-${IMAGE_TAG}.tar"
                sh """
                docker save -o ${IMAGE_NAME}-${IMAGE_TAG}.tar ${IMAGE_NAME}:${IMAGE_TAG}
                """
                // Archive the tar file as Jenkins artifact (optional)
                archiveArtifacts artifacts: "${IMAGE_NAME}-${IMAGE_TAG}.tar"
            }
        }

        stage('Copy and Deploy to EC2') {
            /* 
             * Copy the Docker image tarball to EC2 via SCP,
             * then SSH into EC2 and load & run the Docker container.
             * Uses the .pem file from PRIVATE_KEY_PATH for authentication.
             * Edit PRIVATE_KEY_PATH, EC2_USER, EC2_HOST if needed.
             */
            steps {
                echo "Deploying Docker image to EC2 at ${EC2_HOST}"
                sh """
                scp -o StrictHostKeyChecking=no -i ${PRIVATE_KEY_PATH} ${IMAGE_NAME}-${IMAGE_TAG}.tar ${EC2_USER}@${EC2_HOST}:~/

                ssh -o StrictHostKeyChecking=no -i ${PRIVATE_KEY_PATH} ${EC2_USER}@${EC2_HOST} << EOF
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
