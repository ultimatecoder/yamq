pipeline {
  agent any
  stages {
    stage('Test Stage') {
      parallel {
        stage('Test Stage') {
          steps {
            sh 'echo "hello world"'
          }
        }
        stage('Test substage 2') {
          steps {
            sh 'echo "hello world from substage2"'
          }
        }
      }
    }
  }
}