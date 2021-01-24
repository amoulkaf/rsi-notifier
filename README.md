# RSI-notifier
RSI-notifier is a cryptocurrency trading software that sends email notifications of Relative Strength Index divergences on intraday, and daily timeframes 

## Table of Contents

- [Features](#features)
- [Prerequisite](#prerequisite)
- [Quick-start](#quick-start)
- [Usage](#usage)
- [Support](#support)
- [Contributing](#contributing)

## Features

- [x] **Based on Python 3.7+**: For botting on any operating system - Windows, macOS and Linux.
- [x] **Swing**: Get bullish and bearish signals on multiple timeframes.
- [x] **Email chart**: Achieved with aws, link to charts stored in S3 are sent with the mail.
- [x] **Multiple Indicator chart**: Get multiple indicators in the emailed chart, such as EMAs.
- [x] **Advanced chart**: Choice between OHLC or heikin ashi for better trend reading.
- [x] **Group Usage**: One setup, Multiple people receive the signals.
- [x] **Desktop Notification**: Useful only if the software is setup on main user computer.
- [x] **Multiple crypto-currencies**: Select which crypto-currency you want to get signals of.


## Prerequisite
- [Python 3.7.x](http://docs.python-guide.org/en/latest/starting/installation/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [TA-Lib](https://mrjbq7.github.io/ta-lib/install.html)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) (Recommended)



## Quick-start

 - Install requirements.txt
 ```bash
pip install -r requirements.txt
```
 - Setup an email account that can be used controlled by a program.
 - For charts stored in S3: 
    - Create an S3 bucket
    - Install aws-cli and configure access key and secret access key
 - Create a config.json like the example ./quant-crypto/quant/config.example.json with:
    - The S3 bucket informations
    - The email account you just setup
    - The emails of the subscribers

## Usage

run the software with:
 ```bash
python main.py
```

## Support

Please [open an issue](https://github.com/amoulkaf/rsi-notifier/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and [open a pull request](https://github.com/amoulkaf/rsi-notifier/compare/).
