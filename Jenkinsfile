pipeline {
    agent any
    tools {
        maven "maven:3.6.3"
    }
    stages {
        
        stage('Checkout')
        {
            steps {
                echo "Starting fresh"
                deleteDir()
                checkout scm
            }
        }

        stage('Build, UT and pack') {
            when {
                anyOf {
                    branch pattern: 'feature/*'
                }
            }
            steps {
                echo 'Geting to work'
                sh 'mvn package'
            }
	    }
        
        stage('E2E Testing') {
            when {
                anyOf {
                    branch pattern: 'feature/*'
                    branch pattern: 'master'
                }
            }
            steps {
                echo "Testing"
                sh ( "curl -u jenkins:password http://artifactory:8081/artifactory/libs-snapshot-local/com/lidar/simulator/99-SNAPSHOT/simulator-99-20220502.212839-1.jar -o simulator.jar")
                sh ( "curl -u jenkins:password http://artifactory:8081/artifactory/libs-snapshot-local/com/lidar/telemetry/99-SNAPSHOT/telemetry-99-20220502.204618-1.jar -o telemetry.jar")
                sh ( "cp target/analytics-99-SNAPSHOT.jar . ")
                sh ( "cp ../tests.txt tests.txt")
                sh ( "ls -la")
                echo "Still testing..."
                sh ( "java -cp simulator.jar:telemetry.jar:analytics-99-SNAPSHOT.jar com.lidar.simulation.Simulator")
            }
        }
        
        stage('Publish') {
            when {
                anyOf {
                    branch pattern: 'master'
                }

            }
            steps {
                echo 'Publishing...'
                sh 'mvn deploy -DskipTests'
            }
        }
        
        stage('Deploy') {
            when {
                anyOf {
                    branch pattern: 'release/*'
                }
            }
            steps {
                echo 'Deploying'
                sh 'mvn deploy'
            }
        }
    }
}