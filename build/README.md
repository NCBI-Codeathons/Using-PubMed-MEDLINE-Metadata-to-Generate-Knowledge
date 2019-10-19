# Pseudo deployment process

There was no pipeline or any deployment platform awailable.

So instead of doing this in a right way there is a replacement.

## Prerequisites

Linux VPS with installed docker.

2 files need to be created in build folder

1. Entrez api keys: `keys.env`
   ```sh
   export CFG_TOOL="pm2k"
   export CFG_MAIL=<email for entrez api access>
   export CFG_KEY=<entrez api key>
   ```

2. SSH access to vps `access.env`
   ```sh
   export USER=<user with permissions to execute docker commands>
   export IP=<vps ip>
   export KEY=<path to ssh private key file for user>
    ```
  
## Build and deploy

`./build.sh` will build frontend, backend, upload content to VPS build docker image on VPS and deploy it.