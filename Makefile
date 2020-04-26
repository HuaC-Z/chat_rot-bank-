.PHONY: clean test lint

TEST_PATH=./

help:
	@echo "    train"
	@echo "        Train a Rasa model."
	@echo "    run-cmdline"
	@echo "        Starts the bot on the command line"
	@echo "    run-http"
	@echo "        Starts the bot on http"
	@echo "    run-socketio"
	@echo "        Starts the bot on web ui"
	@echo "    run-x"
	@echo "        Starts the bot on Rasa X"
	@echo "    visualize"
	@echo "        Saves the story graphs into a file"

run-actions:
	rasa run actions --actions actions

train:
	rasa train

train-memo:
	rasa train core --domain domain.yml --stories data/core --config augmentedmemo-only.yml --out models/dialogue --augmentation 0 --quiet

run-cmdline:
	make run-actions&
	rasa shell --debug --endpoints endpoints.yml

run-http:
	make run-actions&
	rasa run --debug --endpoints endpoints.yml  --enable-api --cors '*'

run-socketio:
	make run-actions&
	rasa run --debug --endpoints endpoints.yml  --credentials credentials.yml --enable-api --cors '*'

run-x:
    docker run -p 8000:8000 rasa/duckling
	make run-actions&
	rasa x --endpoints endpoints.yml
	--user
	pip --default-timeout=9999 install rasa-x --extra-index-url https://pypi.rasa.com/simple

visualize:
	rasa visualize --stories data/core/ --domain domain.yml --out story_graph.html

evaluate-core:
	rasa test core --model models/dialogue --stories data/core/ --fail-on-prediction-errors --quiet


pip install google-auth==1.10.1 prompt-toolkit==2.0.10 questionary==1.4.0 SQLAlchemy==1.3.12 urllib3==1.25.7 -i https://pypi.tuna.tsinghua.edu.cn/simple


