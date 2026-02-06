pipeline {
    agent any

    environment {
        // Docker image and container names
        DOCKER_IMAGE = "house-price-api"
        DOCKER_CONTAINER = "house-price-container"

        // DockerHub credential (ID in Jenkins: dockerhub-username)
        DOCKERHUB_CRED = credentials('dockerhub-username')

        // Ensure Jenkins can find docker and python
        PATH = "/usr/local/bin:${env.PATH}"
    }

    stages {

        // -------------------------
        stage('Checkout Code') {
            steps {
                echo "Checking out code from Git"
                checkout scm
            }
        }

        // -------------------------
        stage('Set Up Python Environment') {
            steps {
                echo "Creating Python virtual environment and installing dependencies"
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip setuptools wheel
                pip install -r requirements.txt
                '''
            }
        }

        // -------------------------
        stage('Run Tests') {
            steps {
                echo "Running unit tests"
                sh '''
                . venv/bin/activate
                pytest tests/ --maxfail=1 --disable-warnings -q
                '''
            }
        }

        // -------------------------
        stage('Build & Push Docker Image') {
    steps {
        echo "Building and pushing Docker image for linux/amd64"

        sh '''
        docker buildx create --use --name multiarch-builder || true

        docker buildx build \
          --platform linux/amd64 \
          -t $DOCKERHUB_CRED_USR/${DOCKER_IMAGE}:latest \
          --push .
        '''
    }
}

        // -------------------------
        stage('Optional: Push Docker Image to DockerHub') {
            when {
                expression { return env.DOCKERHUB_CRED_USR != null && env.DOCKERHUB_CRED_PSW != null }
            }
            steps {
                echo "Pushing Docker image to DockerHub"
                sh '''
                echo $DOCKERHUB_CRED_PSW | docker login -u $DOCKERHUB_CRED_USR --password-stdin
                docker tag ${DOCKER_IMAGE} $DOCKERHUB_CRED_USR/${DOCKER_IMAGE}:latest
                docker push $DOCKERHUB_CRED_USR/${DOCKER_IMAGE}:latest
                '''
            }
        }

        // -------------------------
        stage('Deploy Container') {
    steps {
        echo "Stopping old container and running new one"
        sh '''
        docker rm -f house-price-container || true
        docker run -d \
          -p 5001:5001 \
          --name house-price-container \
          keshavbh77/house-price-api:latest
        '''
    }
}

    }

    post {
        always {
            echo "Cleaning up temporary files"
            sh 'rm -rf venv'
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed. Check Jenkins logs."
        }
    }
}