pipeline{
    agent any

    stages {

        stage('Build Artifact - Maven') {
            steps {
                    sh "mvn clean package -DskipTests=true"
                    archive 'target/*.jar'
            }
        }

        stage('Unit Tests - JUnit and JaCoCo') {
            steps {
                    sh "mvn test"
            }
            post {
                always {
                    junit 'target/surefire-reports/*.xml'
                    jacoco execPattern: 'target/jacoco.exec'
                }
            }
        }

        stage('SonarQube - SAST') {
            steps {
                withSonarQubeEnv('SonarQube') {
                     sh "mvn sonar:sonar -Dsonar.projectKey=mssample -Dsonar.host.url=http://devsecops-demo-app.com:9000 -Dsonar.login=094858690495f456e6fr9c4b5a543g57c76f05"
                }
                timeout(time: 2, unit: 'MINUTES') {
                    script {
                        waitForQualityGate abortPipeline: true
                    }
                }
                   
            }
        }

        stage('Docker Build and Push') {
            steps {
                withDockerRegistry([credentialsId: "docker-hub", url: ""]) {
                    sh "printenv"
                    sh "docker build -t fadhiljr/ms-sample:${GIT_COMMIT} ."
                    sh "docker push fadhiljr/ms-sample:${GIT_COMMIT}"
                }
            }
        }

        stage('Kubernetes Deployment - DEV') {
            steps {
                withKubeConfig([credentialsId: "kubeconfig"]) {
                    sh "sed -i 's#replace#fadhiljr/ms-sample:${GIT_COMMIT}#g' k8s_deployment_service.yaml"
                    sh "kubectl apply -f k8s_deployment_service.yaml"
                }
            }
        }
    }
}