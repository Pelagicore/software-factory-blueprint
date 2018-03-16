/*
 * This file is part of the Software Factory project
 * Copyright (C) Pelagicore AB
 * SPDX-License_identifier: LGPL-2.1
 * This file is subject to the terms of the LGPL-2.1 license.
 * Please see the LICENSE file for details.
 */

pipeline {
    agent {
        dockerfile true
    }

    parameters {
        string(name: "REMOTE_SWF_LINK", defaultValue: "https://github.com/Pelagicore/software-factory.git")
        string(name: "BRANCH_SWF", defaultValue: "master")
        string(name: "SWF_DIR", defaultValue: "SWF_SRC")
        string(name: "SWF_BP_DIR", defaultValue: "SWF_BP_SRC")
    }

    stages {
        stage('Download') {
            steps {

                // Delete old files
                sh 'rm -rf .[^.] .??* *'

                // Make separate directories for SWF and SWF-BP for testing if the changeset is compatible with both.
                sh "mkdir ${SWF_DIR}"
                sh "mkdir ${SWF_BP_DIR}"

                // Get The latest SWF src
                dir ("${SWF_DIR}") {
                    retry(2) {
                        sh "git init"
                    }

                    sh "git remote add jenkins ${REMOTE_SWF_LINK}"
                    sh "git fetch jenkins ${BRANCH_SWF}"
                    sh "git checkout jenkins/${BRANCH_SWF}"

                    // Initialize the submodules and fetch the new code change into it
                    sh "git submodule init && git submodule update"
                }

                // Checkout BP src along wth changes in pull request
                dir ("${SWF_BP_DIR}") {
                    checkout scm
                }

                // Copying SWF BP code to SWF build, faking a "bump"
                sh "cp -r ${SWF_BP_DIR}/* ${SWF_DIR}/docs/swf-blueprint/" // It's for testing (BP changes + SWF code).
            }
        }

        // Configure and build SWF BP
        stage('Configure SWF-BP') {
            steps {
                script {
                    String buildParams = "-DENABLE_PDF=OFF"
                    sh "cd ${SWF_BP_DIR} && cmake -H. -Bbuild ${buildParams}" // Configure for SWF BP
                }
            }
        }

        stage('Build SWF-BP') {
            steps {
                sh "cd ${SWF_BP_DIR}/build && make" // Build SWF-BP code.
            }
        }

        // Configure and build SWF
        stage('Configure SWF') {
            steps {
                script {
                    String buildParams = "-DENABLE_PDF=OFF"
                    sh "cd ${SWF_DIR} && cmake -H. -Bbuild ${buildParams}" // Configure for SWF baseline
                }
            }
        }

        stage('Build SWF') {
            steps {
                sh "cd ${SWF_DIR}/build && make"  // Now build SWF baseline along with BP changes.
            }
        }

        // Archive SWF-BP and SWF's build files
        stage('Archive SWF-BP') {
            steps {
                script {
                    archive "${SWF_BP_DIR}/build/**"
                }
            }
        }

        stage('Archive SWF') {
            steps {
                script {
                    archive "${SWF_DIR}/build/**"
                }
            }
        }
    }
}
