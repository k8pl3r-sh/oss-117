# OSS-117
OpenSearch stack for forensic automation

##### Let's go

Mettre un password solide dans le `.env` sinon la stack ne fonctionne pas.
Penser à désactiver le pare feu pour le localhost également !

Lancer le docker compose : `docker-compose up -d`


### Utilisation des parseurs

- Parseur `parsers/text_key_values` : `key=value key2=val ue2 key3=3`
- Parseur logs Web apache : `parsers/apache_logs`