/*
 * This file is part of the Software Factory project
 * Copyright (C) Pelagicore AB
 * SPDX-License_identifier: LGPL-2.1
 * This file is subject to the terms of the LGPL-2.1 license.
 * Please see the LICENSE file for details.
 */

void configureAndBuild(String name, String dir) {
    stage("Configure ${name}") {
        String cmake_params = "-DENABLE_PDF=OFF"
        sh "cd ${dir} && cmake -H. -Bbuild ${cmake_params}"
    }

    stage("Build ${name}") {
        sh "cd ${dir}/build && make"
    }

    stage("Archive ${name}") {
        archiveArtifacts artifacts: "${dir}/build/**", fingerprint: true
    }
}

String SWF_DIR = "SWF_SRC"
String SWF_BP_DIR = "SWF_BP_SRC"

pipeline {
    agent {
        dockerfile true
    }

    parameters {
        string(name: "REMOTE_SWF_LINK", defaultValue: "https://github.com/Pelagicore/software-factory.git")
        string(name: "BRANCH_SWF", defaultValue: "master")
    }

    stages {
        stage('Download') {
            steps {
                // Delete old files
                sh 'rm -rf .[^.] .??* *'

                // Get the latest SWF src
                sh "git clone ${params.REMOTE_SWF_LINK} ${SWF_DIR}"
                sh "cd ${SWF_DIR} && git checkout origin/${params.BRANCH_SWF}"

                // Checkout BP src along wth changes in pull request
                sh "mkdir ${SWF_BP_DIR}"
                dir ("${SWF_BP_DIR}") {
                    checkout scm
                }

                // Copying SWF BP code to SWF build, faking a "bump"
                // It's for testing (BP changes + SWF code)
                sh "cp -r ${SWF_BP_DIR}/* ${SWF_DIR}/docs/swf-blueprint/"
            }
        }

        stage("Launch build") {
            parallel {
                stage("Blueprint") {
                    steps {
                        script {
                            // Configure, build, and archive the blueprint
                            configureAndBuild("Blueprint", SWF_BP_DIR)
                        }
                    }
                }

                stage("SWF + Blueprint") {
                    steps {
                        script {
                            // The same, but building it with the SWF Baseline
                            configureAndBuild("SWF + Blueprint", SWF_DIR)
                        }
                    }
                }
            }
        }
    }
}
