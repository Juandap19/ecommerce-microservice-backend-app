pipeline {
    agent any

    tools {
        maven 'mvn'
        jdk 'JDK_11'
    }

    environment {
        DOCKERHUB_USER = 'minichocolate'
        DOCKER_CREDENTIALS_ID = 'password'
        SERVICES = 'api-gateway cloud-config favourite-service order-service payment-service product-service proxy-client service-discovery shipping-service user-service'
        K8S_NAMESPACE = 'ecommerce'
    }


    stages {
        stage('Init') {
            steps {
                script {
                    if (env.BRANCH_NAME == 'master') {
                        env.SPRING_PROFILE = 'prod'
                        env.IMAGE_TAG = 'prod'
                        env.DEPLOYMENT_SUFFIX = '-prod'

                    } else if (env.BRANCH_NAME == 'release') {
                        env.SPRING_PROFILE = 'stage'
                        env.IMAGE_TAG = 'stage'
                        env.DEPLOYMENT_SUFFIX = '-stage'

                    } else {
                        env.SPRING_PROFILE = 'dev'
                        env.IMAGE_TAG = 'dev'
                        env.DEPLOYMENT_SUFFIX = '-dev'
                    }

                    echo "Branch: ${env.BRANCH_NAME}"
                    echo "Namespace: ${env.K8S_NAMESPACE}"
                    echo "Spring profile: ${env.SPRING_PROFILE}"
                    echo "Image tag: ${env.IMAGE_TAG}"
                    echo "Deployment suffix: ${env.DEPLOYMENT_SUFFIX}"
                }
            }
        }

        stage('Verify Tools') {
                    steps {
                        bat 'java -version'
                        bat 'mvn -version'
                        bat 'docker --version'
                        bat 'kubectl config current-context'

                    }
                }

        stage('Ensure Namespace') {
            steps {
                script {
                    def ns = env.K8S_NAMESPACE
                    bat "kubectl get namespace ${ns} || kubectl create namespace ${ns}"
                }
            }
        }

        stage('Checkout') {
            steps {
                git branch: "${env.BRANCH_NAME}", url: 'https://github.com/Juandap19/ecommerce-microservice-backend-app.git'
            }
        }

        stage('Unit Tests') {
            parallel {
                stage('Unit Tests') {
                    when {
                        anyOf {
                            branch 'dev'
                            branch 'master'
                            branch 'release'
                            expression { env.BRANCH_NAME.startsWith('feature/') }
                        }
                    }
                    steps {
                        script {
                            echo "🔍 Running Unit Tests for ${env.BRANCH_NAME}"
                            bat "mvn test -pl product-service"
                        }
                    }
                }
            }
        }

        stage('Integration Tests') {
            parallel {
                stage('Integration Tests') {
                    when {
                        anyOf {
                            branch 'master'
                            expression { env.BRANCH_NAME.startsWith('feature/') }
                            allOf {
                                not { branch 'master' }
                                not { branch 'release' }
                            }
                        }
                    }
                    steps {
                        script {
                            echo "🧪 Running Integration Tests for ${env.BRANCH_NAME}"
                            bat "mvn verify -pl product-service"
                        }
                    }
                }
            }
        }

        stage('E2E Tests') {
                    parallel {
                        stage('E2E Tests') {
                            when {
                                anyOf {
                                    branch 'master'
                                    expression { env.BRANCH_NAME.startsWith('feature/') }
                                    allOf {
                                        not { branch 'master' }
                                        not { branch 'release' }
                                    }
                                }
                            }
                            steps {
                                script {
                                    echo "🧪 Running Integration Tests for ${env.BRANCH_NAME}"
                                    bat "mvn verify -pl e2e-tests"
                                }
                            }
                        }
                    }
                }

                

        stage('Build Services') {
            when {
                anyOf {
                    branch 'master'
                    branch 'release'
                }
            }
            steps {
                bat "mvn clean package -DskipTests"
            }
        }

        stage('Build Docker Images') {
            when { branch 'master' }
            steps {
                script {
                    SERVICES.split().each { service ->
                        bat "docker build -t ${DOCKERHUB_USER}/${service}:${IMAGE_TAG} .\\${service}"
                    }
                }
            }
        }

        stage('Push Docker Images') {
            when { branch 'master' }
            steps {
                withCredentials([string(credentialsId: "${DOCKER_CREDENTIALS_ID}", variable: 'password')]) {
                    bat "docker login -u ${DOCKERHUB_USER} -p ${password}"
                    script {
                        SERVICES.split().each { service ->
                            bat "docker push ${DOCKERHUB_USER}/${service}:${IMAGE_TAG}"
                        }
                    }
                }
            }
        }

        stage('Deploy Common Config') {
            when { branch 'master' }
            steps {
                bat "kubectl apply -f k8s\\common-config.yaml -n ${K8S_NAMESPACE}"
            }
        }

        stage('Deploy Core Services') {
            when { branch 'master' }
            steps {
                bat "kubectl apply -f k8s\\zipkin -n ${K8S_NAMESPACE}"
                bat "kubectl rollout status deployment/zipkin -n ${K8S_NAMESPACE} --timeout=200s"

                bat "kubectl apply -f k8s\\service-discovery -n ${K8S_NAMESPACE}"
                bat "kubectl set image deployment/service-discovery service-discovery=${DOCKERHUB_USER}/service-discovery:${IMAGE_TAG} -n ${K8S_NAMESPACE}"
                bat "kubectl rollout status deployment/service-discovery -n ${K8S_NAMESPACE} --timeout=300s"

                bat "kubectl apply -f k8s\\cloud-config -n ${K8S_NAMESPACE}"
                bat "kubectl set image deployment/cloud-config cloud-config=${DOCKERHUB_USER}/cloud-config:${IMAGE_TAG} -n ${K8S_NAMESPACE}"
                bat "kubectl rollout status deployment/cloud-config -n ${K8S_NAMESPACE} --timeout=350s"
            }
        }

        stage('Deploy Microservices') {
            when { branch 'master' }
            steps {
                script {
                    echo '👻👻👻👻👻👻'
                }
            }
        }
    }

    post {
        success {
            script {
                echo "✅ Pipeline completed successfully for ${env.BRANCH_NAME} branch."
                echo "📊 Environment: ${env.SPRING_PROFILE}"

                if (env.BRANCH_NAME == 'master') {
                    echo "🚀 Production deployment completed successfully!"
                } else if (env.BRANCH_NAME == 'release') {
                    echo "🎯 Staging deployment completed successfully!"
                } else {
                    echo "🔧 Development tests completed successfully!"
                }
            }
        }
        failure {
            script {
                echo "❌ Pipeline failed for ${env.BRANCH_NAME} branch."
                echo "🔍 Check the logs for details."
                echo "📧 Notify the development team about the failure."

            }
        }
        unstable {
            script {
                echo "⚠️ Pipeline completed with warnings for ${env.BRANCH_NAME} branch."
                echo "🔍 Some tests may have failed. Review test reports."
            }
        }
    }
}
