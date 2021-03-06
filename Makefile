
FIRSTDEPLOY  = cat .init
SRV_IMAGE = gcr.io/$(PROJ)/$(SERVICE):latest
SERVICE   = p-engine
PROJECT   = $(PROJ)
REGION    = us-west1

define DEPLOY_CMD
gcloud run deploy $(NAME) \
  --image $(SRV_IMAGE) \
  --region $(REGION) \
  --allow-unauthenticated
endef

ifndef PORT
PORT=8888
endif

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
	gunicorn --bind localhost:$(PORT) --workers 1 --threads 8 --timeout 0 p-engine:app

.build:
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
