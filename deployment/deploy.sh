#!/bin/bash
az extension add -n containerapp
#export .env variables from a file
set -o allexport
source deployment/.env

docker build . -t $REGISTRY_USERNAME/$IMAGE_NAME
docker push $REGISTRY_USERNAME/$IMAGE_NAME

az group create -l $LOCATION -g $RESOURCE_GROUP
az containerapp env create \
   -g $RESOURCE_GROUP \
   -n $CONTAINER_APP_ENV_NAME \
   --location $LOCATION \
   --logs-workspace-id $LOG_WORKSPACE_ID \
   --logs-workspace-key $LOG_WORKSPACE_KEY

#az containerapp up --environment $CONTAINER_APP_ENV_NAME \
#   -g $RESOURCE_GROUP \
#   -n $CONTAINER_APP_NAME \
#   --image $REGISTRY_USERNAME/$IMAGE_NAME \
#   --ingress external\
#   --target-port 80 \

az containerapp create \
   -g $RESOURCE_GROUP \
   -n $CONTAINER_APP_NAME \
   --environment $CONTAINER_APP_ENV_NAME \
   --image $REGISTRY_USERNAME/$IMAGE_NAME \
   --ingress external\
   --target-port 3500 \
   --revision-suffix "v1" \
   --cpu 0.25\
   --memory 0.5Gi \
   --min-replicas 1 \
   --max-replicas 1 

az containerapp revision restart -n $CONTAINER_APP_NAME -g $RESOURCE_GROUP --revision "image-resizer--v1"