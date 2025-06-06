pipeline {
    agent any

    environment {
        EC2_USER = 'ec2-user'                         // ✅ editable: Your EC2 username (default for Amazon Linux)
        EC2_HOST = '16.170.231.171'                   // ✅ editable: Your EC2 public IP
        PRIVATE_KEY_PATH = 'C:/Users/Success/Downloads/electric-key.pem' // ✅ editable: Path to your EC2 .pem key on Jenkins machine
        IMAGE_NAME = 'deploy-electricaa-aws'          // ✅ editable: Your DockerHub repo name (not the full URL)
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"       // Automatically includes build number
        GIT_REPO = 'https://github.com/Success-C-Opara/electric-001.git' // ✅ editable: Your GitHub repo
        BRANCH_NAME = 'main'                          // ✅ editable: Branch name
        GIT_BASH = '"C:\\Program Files\\Git\\bin\\bash.exe" -c'  // Windows Git Bash path
        DOCKERHUB_CREDENTIALS_ID = 'dockerhub-creds'  // ✅ editable: ID of DockerHub credentials saved in Jenkins
    }

    stages {

        stage('Clone Code') {
            steps {
                echo "✅ Cloning '${BRANCH_NAME}' from ${GIT_REPO}"
                git branch: "${BRANCH_NAME}", url: "${GIT_REPO}"
            }
        }

        stage('Docker Build, Push & Deploy') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKERHUB_CREDENTIALS_ID}",
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_PASS'
                )]) {
                    echo "🐳 Logging into DockerHub"
                    bat "${GIT_BASH} \"docker login -u $DOCKERHUB_USER -p $DOCKERHUB_PASS\""

                    echo "🐳 Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                    bat "${GIT_BASH} \"docker build -t $DOCKERHUB_USER/${IMAGE_NAME}:${IMAGE_TAG} .\""

                    echo "📤 Pushing Docker image to DockerHub"
                    bat "${GIT_BASH} \"docker push $DOCKERHUB_USER/${IMAGE_NAME}:${IMAGE_TAG}\""

                    echo "🚀 Deploying to EC2: ${EC2_HOST}"
                    bat """
                    ${GIT_BASH} "ssh -o StrictHostKeyChecking=no -i '${PRIVATE_KEY_PATH}' ${EC2_USER}@${EC2_HOST} \\
                    'docker login -u $DOCKERHUB_USER -p $DOCKERHUB_PASS && \\
                    docker pull $DOCKERHUB_USER/${IMAGE_NAME}:${IMAGE_TAG} && \\
                    docker stop ${IMAGE_NAME} || true && \\
                    docker rm ${IMAGE_NAME} || true && \\
                    docker run -d --name ${IMAGE_NAME} -p 80:80 $DOCKERHUB_USER/${IMAGE_NAME}:${IMAGE_TAG}'"
                    """
                }
            }
        }
    }
}
