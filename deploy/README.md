# Deploy Family Meals on Hetzner + Tailscale

Private access only: the app listens on `127.0.0.1:8001`. Tailscale Serve publishes it to your Tailnet with HTTPS (no paid domain, not on the public internet).

## Prerequisites

- Hetzner VPS (Ubuntu) with SSH
- Docker + Docker Compose plugin
- Tailscale account ([tailscale.com](https://tailscale.com))
- Render Postgres access for the one-time dump

## 1. Install Docker and Tailscale on the server

```bash
# Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker "$USER"   # then log out/in

# Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# approve the machine in the Tailscale admin console if needed
```

Optional: set a memorable hostname:

```bash
sudo tailscale set --hostname=meals
```

## 2. Clone and configure

```bash
sudo mkdir -p /opt/meals && sudo chown "$USER:$USER" /opt/meals
cd /opt/meals
git clone https://github.com/mysakli/family-meals.git .
git checkout hetzner-tailscale-deploy   # or main after merge

cp .env.example .env
nano .env   # set SECRET_KEY, DB_PASSWORD, ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, AWS_* if using S3
```

After Tailscale is up, get your MagicDNS name:

```bash
tailscale status
# e.g. meals.tailXXXX.ts.net  and  100.x.y.z
```

Put those in `.env`:

```env
ALLOWED_HOSTS=meals,meals.tailXXXX.ts.net,100.x.y.z
CSRF_TRUSTED_ORIGINS=https://meals.tailXXXX.ts.net
BEHIND_PROXY=True
```

## 3. Start the stack

```bash
cd /opt/meals
docker compose up -d --build
docker compose exec web python manage.py migrate --noinput
```

Create a superuser only if you are **not** restoring a Render dump yet:

```bash
docker compose exec web python manage.py createsuperuser
```

## 4. Publish via Tailscale Serve

```bash
# HTTPS on your Tailnet → local Gunicorn
sudo tailscale serve --bg 8001
tailscale serve status
```

Open on a device with Tailscale connected (laptop or iOS app):

`https://meals.tailXXXX.ts.net`

## 5. Migrate data from Render

Freeze writes on Render, then from your laptop:

```bash
pg_dump "$RENDER_DATABASE_URL" --no-owner --no-acl -F c -f meals_render.dump
scp meals_render.dump user@HETZNER_IP:/opt/meals/
```

On the server:

```bash
cd /opt/meals
# Copy dump into the db container and restore
docker compose cp meals_render.dump db:/tmp/meals_render.dump
docker compose exec -T db pg_restore -U meals -d meals --no-owner --no-acl --clean --if-exists /tmp/meals_render.dump
docker compose exec web python manage.py migrate --noinput
```

Verify login, meals, and images (S3 should keep working if `USE_S3=True`).

## 6. Devices

- **Laptop:** install Tailscale, sign in, open the `*.ts.net` URL
- **iOS:** App Store → Tailscale → same account → Safari → same URL

## 7. Decommission Render

After a few days of successful use:

1. Keep a local copy of `meals_render.dump`
2. Suspend/delete the Render web service and Postgres
3. Cancel the Render plan if nothing else remains

## Updates later

```bash
cd /opt/meals
git pull
docker compose up -d --build
docker compose exec web python manage.py migrate --noinput
```

## Firewall note

Do **not** open port 8001 publicly. Keep Hetzner firewall to SSH (and whatever your other project needs). The meals app is reached only through Tailscale.
