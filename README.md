[![btc-wallet-tracking](https://snapcraft.io/btc-wallet-tracking/badge.svg)](https://snapcraft.io/btc-wallet-tracking)

# Wallet Tracking App

This is a simple wallet tracking app built with Python and PyQt. It allows you to track Bitcoin wallets by saving their public addresses and viewing their transaction history and balance.

## Features

- Add, edit, and delete wallets
- View wallet details including balance, transaction history, and more
- Automatically updates wallet data from blockchain API
- Saves wallets to local JSON file
- Simple and easy to use UI

## Usage

The app uses the Blockchain.info API to fetch wallet details. An internet connection is required.

To get started:

1. Clone the repo
2. Install dependencies with `pip install -r requirements.txt` 
3. Run `python main.py`
4. Add wallets by clicking the '+Add' button
5. Wallet details will populate automatically 

The wallets are saved to `wallets.json` so your data will persist between sessions.

## To build SNAP:

1. Clone the repo
2. Open 'btc-wallet-tracking' directory in terminal
3. Run command 'snapcraft'

## Contributing

Contributions are welcome! Feel free to open an issue or PR.

Some ideas for improvements:

- Support more currencies (e.g. EUR, GBP, CAD, SEK...)
- Add charts and graphs
- Improve transaction history display
- Enhance UI/UX

## License

This project is open source and available under the [MIT License](LICENSE).

## Donate

<a href="https://nowpayments.io/donation?api_key=X1QFVQG-31Z4VTA-QNPGNHV-EMN5JHY&source=lk_donation&medium=referral" target="_blank"><img src="https://nowpayments.io/images/embeds/donation-button-white.svg" alt="Crypto donation button by NOWPayments"></a>

<details>
  <summary>Or direct transfer</summary>
<br>
BTC wallet:
<br>
bc1qtdz2fut4g2hzagjlh6fqnpuz5ghnj8dvjggcd3
<br>
<br>
Etherium wallet:
<br>
0xEb86bf93c6cd4A41cCd1a410Eb1E54d1eaD7D93D
<br>
</details>

