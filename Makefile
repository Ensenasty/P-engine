
SERVICE_ACCOUNT = 356720520556-compute@developer.gserviceaccount.com
PROJ  =  p_engin
SCOPES  = https://www.googleapis.com/auth/devstorage.read_only,
SCOPES += https://www.googleapis.com/auth/logging.write,
SCOPES += https://www.googleapis.com/auth/monitoring.write,
SCOPES += https://www.googleapis.com/auth/servicecontrol,
SCOPES += https://www.googleapis.com/auth/service.management.readonly,
SCOPES += https://www.googleapis.com/auth/trace.append

PHONY: build default deltest stoptest stest deploy

default:: build
default:: deploy

build:
	gcloud builds submit --config cloudbuild.yaml


deltest: NAME=$(PROJ)test
deltest: del

test: NAME=$(PROJ)test
test: run

stop: NAME=$(PROJ)
stop: stop

deploy: NAME=$(PROJ)
deploy: run

del:
	gcloud compute instances delete $(NAME) --zone=us-west2-a

stop:
	gcloud compute instances stop $(NAME) --zone=us-west2-a

run:
	gcloud beta compute --project=mezaops instances \
    create-with-container $(NAME) --zone=us-west2-a \
    --machine-type=e2-micro --subnet=default \
    --network-tier=STANDARD --metadata=google-logging-enabled=true \
    --maintenance-policy=MIGRATE \
    --service-account=$(SERVICE_ACCOUNT) \
    --scopes=$(SCOPES) \
    --tags=http-server,https-server --image=cos-stable-89-16108-470-16 \
    --image-project=cos-cloud --boot-disk-size=10GB --boot-disk-type=pd-balanced \
    --boot-disk-device-name=$(NAME) --no-shielded-secure-boot --shielded-vtpm  \
    --shielded-integrity-monitoring \
    --container-image=us-west2-docker.pkg.dev/mezaops/-$(PROJ)/$(PROJ)-image:tag1 \
    --container-restart-policy=always --container-tty \
    --labels=container-vm=cos-stable-89-16108-470-16
