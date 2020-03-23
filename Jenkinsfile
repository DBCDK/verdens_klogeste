#!groovy

def workerNode = "xp-build-i01"

pipeline {
	agent {label workerNode}
	environment {
		DOCKER_TAG = "${env.BRANCH_NAME}-${env.BUILD_NUMBER}"
		GITLAB_PRIVATE_TOKEN = credentials("ai-gitlab-api-token")
	}
	triggers {
		pollSCM("H/02 * * * *")
	}
	stages {
		stage("build info") {
			agent {
				docker {
					label workerNode
					image "docker.dbc.dk/build-env"
					alwaysPull true
				}
			}
			steps {
				sh """#!/usr/bin/env bash
					make-build-info
				"""
				stash includes: "src/verdens_klogeste/_build_info.py", name: "build-stash"
			}
		}
		stage("docker build") {
			steps {
				unstash "build-stash"
				script {
					image = docker.build(
						"docker-xp.dbc.dk/verdens-klogeste:${DOCKER_TAG}", "--pull --no-cache .")
					image.push()
					if(env.BRANCH_NAME == "master") {
						image.push("latest")
					}
				}
			}
		}
		stage("update staging version number") {
			agent {
				docker {
					label workerNode
					image "docker.dbc.dk/build-env"
					alwaysPull true
				}
			}
			when {
				branch "master"
			}
			steps {
				sh "set-new-version verdens-klogeste-1-0.yml ${env.GITLAB_PRIVATE_TOKEN} ai/verdens-klogeste-secrets ${env.DOCKER_TAG} -b staging"
				build job: "ai/verdens-klogeste-deploy/staging", wait: true
			}
		}
		stage("validate staging") {
			agent {
				docker {
					label workerNode
					image "docker.dbc.dk/build-env"
					alwaysPull true
				}
			}
			when {
				branch "master"
			}
			steps {
				sh "webservice_validation.py http://verdens-klogeste-1-0.mi-staging.svc.cloud.dbc.dk deploy/validation.yml"
			}
		}
		stage("update prod version number") {
			agent {
				docker {
					label workerNode
					image "docker.dbc.dk/build-env"
					alwaysPull true
				}
			}
			when {
				branch "master"
			}
			steps {
				sh "set-new-version verdens-klogeste-1-0.yml ${env.GITLAB_PRIVATE_TOKEN} ai/verdens-klogeste-secrets ${env.DOCKER_TAG} -b prod"
				build job: "ai/verdens-klogeste-deploy/prod", wait: true
			}
		}
		stage("validate prod") {
			agent {
				docker {
					label workerNode
					image "docker.dbc.dk/build-env"
					alwaysPull true
				}
			}
			when {
				branch "master"
			}
			steps {
				sh "webservice_validation.py http://verdens-klogeste-1-0.mi-prod.svc.cloud.dbc.dk deploy/validation.yml"
			}
		}
	}
}
