# PubMeta backend

Distributed as a pip package with embeded data files and static.

## Project setup
```
. ./init
```

### Run in dev mode
```
./run_dev.sh
```
If frontend was not built first only /api calls will be available.

### Compiles and minifies for production
```
npm run build
```

Build process will copy static to backend package