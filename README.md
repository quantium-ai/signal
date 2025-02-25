# Quantium Signal

TradingView is a great platform for charting, backtesting, etc., but for using one of the most powerful features,
alerts, you need to have a premium subscription. Quantium Signal is a free and open-source project that allows you to
use alerts completely free.

## Configuration

If you already have an EC2 instance or any other virtual private server, then you can follow the steps below to
self-host the Quantium Signal for handling TradingView alerts.

- Configure a DNS record for your server to access it with a domain name (mandatory).
- Install the package by `python3 -m pip install quantium-signal` command.
- Create a subclass for your crypto exchange and run the Signal handler ([step-by-step guide](https://github.com/quantium-ai/signal/discussions/1)).
- Once you run the Signal handler, you have created an SMTP server that handles emails sent to your domain.
- Open the Profile Settings of your TradingView account and set the "Alternative email for alerts" to
  `tradingview@yourdomain.com` - where username doesn't matter if you don't use username filtering.
- Create as many alerts as you need and tick the "Send plain text" checkbox from alert's "Notification" tab.

There you go! Once your strategy triggers an alert, the handler will receive the message through the SMTP server and
call the configured webhook URL with the alert message.

## Contribute

Any contribution is welcome. Always feel free to open an issue or a discussion if you have any questions not covered by
the documentation. If you have any ideas or suggestions, please, open a pull request.

## License

Copyright (C) 2025 Quantium. [MIT](https://github.com/quantium-ai/signal/blob/main/LICENSE)
