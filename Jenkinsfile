pipeline {
    agent any
    stages {
        stage('Preparation') {
            steps {
                echo "Descargar el codigo desde el repositorio en GitHub"
                //git branch: 'main', url: 'https://github.com/whitejaguars/curso_devsecops_python.git'
                checkout scm
                echo "Directorio actual"
                sh "pwd"
            }
        }
        stage('Build') {
            steps {
                echo "Compilando los archivos"
                sh "python3 -m compileall . -q"
            }
        }
        stage('Unit Testing'){
            steps {
                echo 'Run pytest for generating a report from unit tests'
                sh 'python3 -m pytest --junitxml=pytest-report.xml'
            }
        }
        stage('SonarQube'){
            steps {
                echo 'Run scan with SonarQube'
                script {
                    def scannerHome = tool 'SonarQube';
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=CICD_Python_${env.BRANCH_NAME} -Dsonar.projectName=CICD_Python_${env.BRANCH_NAME} -Dsonar.sources=application -Dsonar.python.xunit.reportPath=pytest-report.xml"
                    }
                }
            }
        }
        stage("Quality Gate") {
            steps {
                sleep(10)
                // waitForQualityGate abortPipeline: true
            }
        }
        stage("Deploy"){
            steps {
                sh "bash deploy/deploy.sh 192.168.1.60"
            }
        }
    }
}
