
def lastEarthquakeData
def ceratiShouldBeWakeUp

pipeline {
    agent {
        docker {
            image 'andreypicado506/custom-python3:cerati'
        }
    }
    triggers {
        cron('H/30 * * * *')
    }
    parameters {
        string(
        name:'OVSICORI_URL',
        defaultValue:'http://www.ovsicori.una.ac.cr/sistemas/sentidos_map/index.php?tipo=center',
        description: 'URL de la tabla <Sismos Sentidos> del sitio web del OVSICORI.')
        string(
        name: 'S3_BUCKET_NAME',
        defaultValue: 'cerati-bucket',
        description: 'S3 bucket en donde está el archivo con los datos sísmicos.')
        string(
        name: 'S3_FILE_NAME',
        defaultValue: 'sismos',
        description: 'Nombre del archivo que contiene los datos sísmicos (se creará si no existe)')
    }
    environment {
        GITHUB_REPO_URL = 'git@github.com:andreypicado506/cuando-pase-el-temblor.git'
    }

    stages {
        stage('Obtener código fuente de Github') {
            steps {
                // Checkout the GitHub repository
                script {
                    git branch: 'main', credentialsId: 'github_wake_up', url: "${GITHUB_REPO_URL}"
                }
            }
        }

        stage('Obtener actividad sísmica más reciente') {
            steps {
                    script {
                        lastEarthquakeData = sh(
                            script: "python3 scripts/get_seismic_data.py -u '${OVSICORI_URL}'",
                            returnStdout: true).trim()
                        sh "echo '${lastEarthquakeData}' > ${S3_FILE_NAME}"
                    }
            }
        }
        stage('Validar si Cerati debe ser despertado') {
            steps {
                withAWS(
                    credentials:'aws_main',
                    region:     'us-west-2'
                ) {
                    script {
                        ceratiShouldBeWakeUp = sh(
                        script: 'python3 scripts/check_s3.py -b ${S3_BUCKET_NAME} \
                        -f ${S3_FILE_NAME} -l ${S3_FILE_NAME}',
                        returnStdout: true).trim()
                        if (ceratiShouldBeWakeUp == 'True') {
                            currentBuild.displayName = "${currentBuild.number}: Cerati fue despertado"
                        }
                        else {
                            currentBuild.displayName = "${currentBuild.number}: Cerati no fue despertado"
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            script{
                if (ceratiShouldBeWakeUp == 'True') {
                    mail(
                        subject: '¡Despierta!',
                        body:    'Ya pasó el temblor.',
                        to:      'andreypicado506@gmail.com'
                    )
                    echo '¡Cerati debe ser despertado!'
                }
                else {
                    echo 'Cerati no debe ser despertado.'
                }
            }
        }
        failure {
            // This block will be executed if the pipeline fails
            echo 'Algo salió mal.'
        }
    }
}
