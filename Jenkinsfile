pipeline {
    agent any  // Use any available Jenkins agent

    environment {
        # ✅ editable: Change to your EC2 user if different
        EC2_USER = 'ec2-user'

        # ✅ editable: Update with your EC2 public IP
        EC2_HOST = '16.170.231.171'

        # ✅ editable: Path to your PEM key (only for Windows Jenkins master)
        PRIVATE_KEY_PATH = 'C:/Users/Success/Downloads/electric-key.pem'

        # ✅ editable: Local name of the Docker image (does not include DockerHub username)
        IMAGE_NAME = 'deploy-electricaa-aws'

        # Do not change: Tag includes Jenkins build number
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"

        # ✅ editable: Full DockerHub repo path (username/repo-name)
        DOCKERHUB_REPO = 'successwise1/deploy-electricaa-aws'

        # ✅ editable: GitHub repository to clone
        GIT_REPO = 'https://github.com/Success-C-Opara/electric-001.git'

        # ✅ editable: Git branch to build
        BRANCH_NAME = 'main'

        # Required to run shell/bash commands via Git Bash on Windows
        GIT_BASH = '"C:\\Program Files\\Git\\bin\\bash.exe" -c'
    }

    stages {
        stage('Clone Code') {
            steps {
                echo "Cloning '${BRANCH_NAME}' from ${GIT_REPO}"
                git branch: "${BRANCH_NAME}", url: "${GIT_REPO}"  // Checkout GitHub branch
            }
        }

        stage('Docker Login & Build') {
            steps {
                echo "Building and tagging Docker image..."
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',  // Must match the Jenkins credential ID
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    // ✅ Do not hardcode credentials — they are securely injected above
                    bat "${GIT_BASH} \"docker login -u $DOCKER_USER -p $DOCKER_PASS\""
                    bat "${GIT_BASH} \"docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .\""
                    bat "${GIT_BASH} \"docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${DOCKERHUB_REPO}:${IMAGE_TAG}\""
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                echo "Pushing image to DockerHub..."
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',  // Same as above
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat "${GIT_BASH} \"docker push ${DOCKERHUB_REPO}:${IMAGE_TAG}\""
                }
            }
        }

        stage('Deploy on EC2') {
            steps {
                echo "Pulling and deploying Docker image on EC2..."

                // Use SSH to login to EC2 and deploy Docker container
                bat """
                ${GIT_BASH} "ssh -o StrictHostKeyChecking=no -i '${PRIVATE_KEY_PATH}' ${EC2_USER}@${EC2_HOST} \\
                'docker login -u successwise1 -p ${env.DOCKER_PASS} && \\
                 docker stop ${IMAGE_NAME} || true && \\
                 docker rm ${IMAGE_NAME} || true && \\
                 docker pull ${DOCKERHUB_REPO}:${IMAGE_TAG} && \\
                 docker run -d --name ${IMAGE_NAME} -p 80:80 ${DOCKERHUB_REPO}:${IMAGE_TAG}'"
                """
            }
        }
    }
}
