pipeline {
    agent any

    environment {
        EC2_USER = 'ec2-user'
        EC2_HOST = '16.170.231.171'
        PRIVATE_KEY_PATH = 'C:/Users/Success/Downloads/electric-key.pem'
        IMAGE_NAME = 'my-app'
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"
        GIT_REPO = 'https://github.com/Success-C-Opara/electric-001.git'
        BRANCH_NAME = 'main'
        GIT_BASH = '"C:\\Program Files\\Git\\bin\\bash.exe" -c'
    }

    stages {
        stage('Clone Code') {
            steps {
                echo "Cloning branch '${BRANCH_NAME}' from ${GIT_REPO}"
                git branch: "${BRANCH_NAME}", url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}"
                bat """
                ${GIT_BASH} "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                """
            }
        }

        stage('Save Docker Image') {
            steps {
                echo "Saving Docker image to ${IMAGE_NAME}-${IMAGE_TAG}.tar"
                bat """
                ${GIT_BASH} "docker save -o ${IMAGE_NAME}-${IMAGE_TAG}.tar ${IMAGE_NAME}:${IMAGE_TAG}"
                """
                archiveArtifacts artifacts: "${IMAGE_NAME}-${IMAGE_TAG}.tar"
            }
        }

        stage('Copy and Deploy to EC2') {
            steps {
                echo "Deploying Docker image to EC2 at ${EC2_HOST}"
                bat """
                ${GIT_BASH} "scp -o StrictHostKeyChecking=no -i ${PRIVATE_KEY_PATH} ${IMAGE_NAME}-${IMAGE_TAG}.tar ${EC2_USER}@${EC2_HOST}:~/"
                ${GIT_BASH} "ssh -o StrictHostKeyChecking=no -i ${PRIVATE_KEY_PATH} ${EC2_USER}@${EC2_HOST} \\
                'docker stop ${IMAGE_NAME} || true && \\
                 docker rm ${IMAGE_NAME} || true && \\
                 docker load -i ${IMAGE_NAME}-${IMAGE_TAG}.tar && \\
                 docker run -d --name ${IMAGE_NAME} -p 80:80 ${IMAGE_NAME}:${IMAGE_TAG}'"
                """
            }
        }
    }
}
