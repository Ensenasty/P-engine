
ANYSRC != find . -type f | grep -v git
SERVICE_ACCOUNT = 356720520556-compute@developer.gserviceaccount.com
PROJ    =  p-engine
SCOPES  = https://www.googleapis.com/auth/devstorage.read_only,
SCOPES += https://www.googleapis.com/auth/logging.write,
SCOPES += https://www.googleapis.com/auth/monitoring.write,
SCOPES += https://www.googleapis.com/auth/servicecontrol,
SCOPES += https://www.googleapis.com/auth/service.management.readonly,
SCOPES += https://www.googleapis.com/auth/trace.append

IMAGE = gcr.io/mezaops/$(PROJ):latest
REGION =  us-west2

PHONY: build default deltest stop test deploy del stop run

default:: build
default:: deploy

build: .build

.build: $(ANYSRC)
	gcloud builds submit --tag $(IMAGE)
	touch $@

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
	gcloud run deploy $(NAME) \
  --image $(IMAGE) \
  --region $(REGION) \
  --allow-unauthenticated
:wq





oldrun: .build
	gcloud beta compute --project=mezaops instances \
    create-with-container $(NAME) --zone=us-west2-a \
    --machine-type=e2-micro --subnet=default \
    --network-tier=STANDARD --metadata=google-logging-enabled=true \
    --maintenance-policy=MIGRATE \
    --service-account=$(SERVICE_ACCOUNT) \
    --tags=http-server,https-server --image=cos-stable-89-16108-470-16 \
    --image-project=cos-cloud --boot-disk-size=10GB --boot-disk-type=pd-balanced \
    --boot-disk-device-name=$(NAME) --no-shielded-secure-boot --shielded-vtpm  \
    --shielded-integrity-monitoring \
    --container-image=us-west2-docker.pkg.dev/mezaops/-$(PROJ)/$(PROJ)-image:tag1 \
    --container-restart-policy=always --container-tty \
    --labels=container-vm=cos-stable-89-16108-470-16
#

%:
