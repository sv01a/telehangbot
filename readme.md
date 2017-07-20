run:

`docker run -i -e TELEHANGBOT_TELEGRAM_TOKEN='<token>' -e TELEHANGBOT_GOOGLE_EMAIL='<google account email>' -e TELEHANGBOT_GOOGLE_PASSWD='<google account password>' telehangbot`

or

- cd ansible/
- rename deploy.yml.example to deploy.yml
- rename inventory.example to inventory
- edit deploy.yml:
  - replace `<token-goes-here>` to telegram bot api token
  - replace `<email>` to google account email
  - replace `<password>` to google account password
- edit inventtory file:
  - replace <host-goes-here> to host ip. On the host should be installed docker

TODO:
- save\load cookies
