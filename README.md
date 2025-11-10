## VK Overflow

### How to start (Development&Testing)
#### Configuring
1. Install docker-compose. <br>
   for example, Arch:
   ```shell
   yay -S docker-compose
   ```
    [More here](https://docs.docker.com/compose/install/)

2. Set environment variables or configure .env (`.env.example` may help you)
3. Create centrifugo config with:
    ```shell
   docker run --rm -v$PWD:/centrifugo centrifugo/centrifugo:v6 centrifugo genconfig
    ```
4. Configure centrifugo, by editing ./centrifugo/config.json
5. Configure Django backend (I'll update this point later 🥸) 
6. Start up postgres and apply migrations
    ```shell
   docker compose up
    ```
    ```shell
    python ./manage.py migrate
    ```
7. Install requirements with
    ```shell
    pip install -r requirements_dev.txt
    ```

##### Linters and some additional features [Optional]
- To run flake8 just use
    ```shell
    flake8
    ```
- To run tests change directory to `VK_Overflow` and exec
    ```shell
    ./manage.py test
    ```
  
  -  To run all checks (<a style="color: green;">Preffered</a>)
  ```shell
  pre-commit run -a 
  ```
- Also you can install pre-commit hooks to automate routine (Run from root project dir)
    ```shell
    pre-commit install
    ```
####     Starting up
   1. **Start all requirements with executing**
       ```shell
       docker compose up
       ```
   2. **Run Django server**
      - Open new terminal and execute...
      - ```shell
        cd ./VK_Overflow
        ```
      - ```shell
        ./manage.py runserver
        ```
### Documentation for production could be here ^_^
