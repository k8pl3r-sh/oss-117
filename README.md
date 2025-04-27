# OpenSearch-Server
Repository for the infrastructure management of the OpenSearch server


# Run the stack
First git clone the project with `git clone --recurse-submodules` in order to get also the parser submodule

1) In order to run the stack, you need to have `docker` and `docker-compose` installed on your machine.

2) Disable memory paging and swapping performance on the host
`sudo swapoff -a`

3) Increase the number of memory maps available to OpenSearch :
`sudo sysctl -w vm.max_map_count=262144` is also required to run the stack.
`sudo sysctl -p` to apply the changes.
`cat /proc/sys/vm/max_map_count` to check the changes

To make it persistent, you can add `vm.max_map_count=262144` in your /etc/sysctl.conf and run

4) Create a `.env` file copied from `dotenv_example` with a strong password.

5) Create a `config.yml` file copied from `config_template.yml` according to your needs.

6) Then, you can run the stack with the following command:
```bash
docker-compose up -d
```

7) Add your test data in a created `data` directory


8) Use the web app to ingest easily files into opensearch :
```bash
docker build -t web_app .
docker run -v /sftp/sftpuser/files:/data -p 8100:8100 web_app
```

8bis) Create and enable venv to run the ingestor
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 ingestor.py
```

9) FIXME : [add index pattern in OpenSearch (must be automated so not explained here)](https://opensearch.org/docs/latest/dashboards/management/index-patterns/)
#### Possible errors on start

Password is not strong enough : error writen in the logs, you need to have a really strong password

# Usage of the ingestor

Once the stack is running, you can use the ingestor to send data to the OpenSearch server.

For this, you have to specify the parsers' directory and the logs directory to the `config_template.yml` file that you have to rename `config.yml`.

THen, simply run `ingestor.py` to test the ingestor.

To verify that the data has been ingested, you can go to the OpenSearch server and check the indices :
-> for each new index, you have to create a new index :
1) Go to Management > Dashboards Management
2) Click on "Create Index pattern" (you can see your ingested indexes already in Management > Index Management)
3) Add as Index pattern name the name of your index that you see below, you have to do it for all of your indexes
4) Click on "Next step", eventually change the time field name, and click on "Create index pattern"
5) You can eventually edit some fields
6) Go to Discover and select your index pattern to see the ingested data, don't forget to select "All time" in the time range !!!

## How to contribute ?