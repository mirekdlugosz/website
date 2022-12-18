Title: Podman Pod definition for WordPress development
Slug: podman-pod-definition-for-wordpress-development
Date: 2022-12-12 23:30:32
Category: Blog
Tags: Linux, planet MoT

Recently I took on a task to develop a WordPress plugin.
WordPress is old school web app that is usually executed in the context of HTTP server, and needs SQL server to store data.
This is a setup that lends itself very well to containers.

There are plenty of `docker-compose.yml` WordPress examples floating around, but I am using [Podman](https://podman.io/) here and I had trouble running them under [podman-compose](https://github.com/containers/podman-compose).
Instead of trying to fix these problems, I decided to create Pod definition file that Podman understands natively.
Including it below in case it is useful for others.

```
apiVersion: v1
kind: Pod
metadata:
  name: wordpress
  labels:
    app: wordpress
spec:
  containers:
  - name: wpdb
    image: docker.io/library/mariadb:10
    volumeMounts:
    - mountPath: /var/lib/mysql/
      name: mysql_data-pvc
    ports:
      - containerPort: 3306
        hostPort: 13306
    env:
      - name: MARIADB_ROOT_PASSWORD
        value: somewordpress
      - name: MARIADB_DATABASE
        value: wordpress_db
      - name: MARIADB_USER
        value: wordpress_user
      - name: MARIADB_PASSWORD
        value: wordpress_password
    tty: true
  - name: wp
    image: docker.io/library/wordpress:latest
    volumeMounts:
    - mountPath: /var/www/html/wp-content/plugins/my-wordpress-project:Z
      name: wp-plugin-hp
    env:
      - name: WORDPRESS_DB_HOST
        value: 127.0.0.1:3306
      - name: WORDPRESS_DB_NAME
        value: wordpress_db
      - name: WORDPRESS_DB_USER
        value: wordpress_user
      - name: WORDPRESS_DB_PASSWORD
        value: wordpress_password
      - name: WORDPRESS_DEBUG
        value: "1"
      - name: WORDPRESS_CONFIG_EXTRA
        value: |
          define( 'WP_ENVIRONMENT_TYPE', 'local' );
    ports:
      - containerPort: 80
        hostPort: 8080
    tty: true
  restartPolicy: OnFailure
  volumes:
  - name: mysql_data-pvc
    persistentVolumeClaim:
      claimName: mysql_data
  - name: wp-plugin-hp
    hostPath:
      path: "/home/USER/projects/my-wordpress-project/"
```

Pod name, container names and exposed ports must be globally unique.
While you can use the same file for multiple projects, you won't be able to start these projects at the same time.

This file will keep database data across container restarts and system reboots.
If you use the same file for multiple projects, you will end up using the same database for all of them.
Change `claimName` near the bottom to prevent this.

In `docker-compose.yml`, usually you map specific local path to specific container path.
In Podman Pod definition, this is broken into two steps.
First, you define container path and volume name.
Then, you configure volume with specific name.
Full documentation is available in [Kubernetes API page](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.26/#volume-v1-core).
Most of the time you want `persistentVolumeClaim` (keep data on host machine, but let Podman figure out the details) or `hostPath` (keep data on host machine, let me specify the host path).
In case of `hostPath`, if you use SELinux, you should add `:Z` at the end of **container** path.

You start both containers with `podman kube play ./wordpress_pod.yaml`, and stop them with `podman kube down ./wordpress_pod.yaml`.

If you want to remove MariaDB data, use `podman volume ls` and `podman volume rm`.
