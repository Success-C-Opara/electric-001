pipeline {
    agent any

    environment {
        // AWS region where your EC2 instance runs
        AWS_DEFAULT_REGION = 'us-east-1'

        // Docker image tag with build number for unique versioning
        IMAGE_TAG = "build-${env.BUILD_NUMBER}"

        // SSH user for EC2 instance, usually 'ec2-user' for Amazon Linux
        EC2_USER = 'ec2-user'

        // Public IP address of your EC2 instance - EDIT this for new EC2 server
        EC2_HOST = '16.170.231.171'

        // Full path to your PEM SSH key on Jenkins machine - EDIT this path if needed
        PEM_PATH = 'C:/Users/Success/Downloads/electric-key.pem'

        // Docker image name (change to your app’s name)
        DOCKER_IMAGE = 'my-app'
    }

    stages {
        stage('Clone Code') {
            steps {
                // Clone the GitHub repo - change URL here to use a different repo
                git 'https://github.com/Success-C-Opara/electric-001.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image with the defined tag
                sh """
                docker build -t $DOCKER_IMAGE:$IMAGE_TAG .
                """
            }
        }

        stage('Save Docker Image') {
            steps {
                // Save the Docker image to a tar file for transferring to EC2
                sh """
                docker save -o $DOCKER_IMAGE.tar $DOCKER_IMAGE:$IMAGE_TAG
                """
            }
        }

        stage('Deploy to EC2') {
            steps {
                // Copy Docker image tar file to EC2 and run container there
                sh """
                scp -i "$PEM_PATH" -o StrictHostKeyChecking=no $DOCKER_IMAGE.tar $EC2_USER@$EC2_HOST:/home/$EC2_USER/
                ssh -i "$PEM_PATH" -o StrictHostKeyChecking=no $EC2_USER@$EC2_HOST << EOF
                    docker load -i $DOCKER_IMAGE.tar
                    docker stop $DOCKER_IMAGE || true  # stop existing container if running
                    docker rm $DOCKER_IMAGE || true    # remove old container
                    docker run -d --name $DOCKER_IMAGE -p 80:80 $DOCKER_IMAGE:$IMAGE_TAG  # run new container
                EOF
                """
            }
        }
    }
}
