app_name = test_kck
app_version = 0.2.0
app=$(app_name):$(app_version)


build:
	@docker build -t $(app) .

run:
	docker run -v ${PWD}/settings.json:/app/settings.json --rm --detach -p 9191:9191 $(app)

kill:
	@echo 'Killing container $(app)'
	@docker ps | grep $(app_name) | awk '{print $$1}' | xargs docker stop
