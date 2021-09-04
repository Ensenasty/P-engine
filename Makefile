
ANYSRC   != find . -type f | grep -v git | grep -v .rope
FIRSTDEPLOY  = cat .init
SRV_IMAGE = gcr.io/mezaops/$(SERVICE):latest
SERVICE   = p-engine
PROJECT   = $(PROJ)
REGION    = us-west1

define DEPLOY_CMD
gcloud run deploy $(NAME) \
  --image $(SRV_IMAGE) \
  --region $(REGION) \
  --allow-unauthenticated
endef

PHONY: build init deploy run clean

default:: build
default:: deploy

build: .build

init: NAME=$(SERVICE)
init: .build

deploy: NAME=$(SERVICE)
deploy: run

run: deploy

rebuild:: clean
rebuild:: default

clean:
	rm -rf .build .init __pycache__

.build: $(ANYSRC)
	gcloud builds submit --tag $(SRV_IMAGE)
	touch $@

.init:
	@$(DEPLOY_CMD) \
  --no-allow-unauthenticated \
  --memory=512Mi \
  --no-use-http2 \
  --platform=managed \
  --project=$(PROJECT)
	echo 1 > $@

run:
	$(DEPLOY_CMD)

%:
