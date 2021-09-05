
ANYSRC   != find . -type f | grep -v git | grep -v .rope
FIRSTDEPLOY  = cat .init
SRV_IMAGE = gcr.io/mezaops/$(SERVICE):latest
SERVICE   = p-engine
PROJECT   = $(PROJ)
REGION    = us-west1

define DEPLOY_CMD
@echo define BOT_TOKEN and SECRET_KEY in your environment
@echo or this build will fail..
test -n "$(BOT_TOKEN)"
test -n "$(SECRET_KEY)"
gcloud run deploy $(NAME) \
  --image $(SRV_IMAGE) \
  --region $(REGION) \
  --set-env-vars=BOT_TOKEN="$(BOT_TOKEN)",SECRET_KEY="$(SECRET_KEY)" \
  --allow-unauthenticated
endef

PHONY: build init deploy run rebuild clean localserve

default:: build
default:: deploy

build: .build

deploy: NAME=$(SERVICE)
deploy: run

init: NAME=$(SERVICE)
init: .build

run:
	$(DEPLOY_CMD)

rebuild:: clean
rebuild:: default

clean:
	rm -rf .build .init __pycache__

localserve:
	gunicorn --bind localhost:8888 --workers 1 --threads 8 --timeout 0 p-engine:app

.build: $(ANYSRC)
	gcloud builds submit --tag $(SRV_IMAGE)
	touch $@

.init:
	@$(DEPLOY_CMD) \
  --no-allow-unauthenticated \
  --memory=512M \
  --no-use-http2 \
  --platform=managed \
  --project=$(PROJECT)
	echo 1 > $@

%:
