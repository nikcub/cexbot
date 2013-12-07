## cexbot

A bot for the cex.io cryptocurrency mining marketplace

*this is a really early version, recommend you check updates frequently*

## Signup

1. Go to [cex.io](https://cex.io/r/0/nikcub/0/)
2. Click signup
3. Fill out form, confirm etc.
4. Once signed up go to https://www.cex.io/trade/profile
5. Scroll down to API Access
6. *Optional* enter your IP address
7. Check all API access permission boxes
8. Click 'generate'
9. Copy the key and secret (see Config section)
10. Click 'activate'
11. Click the link in the activation email to confirm API access

## Install

The easiest way to install is with `pip`, it will download the package, build it and place `cexbot-cli` in your path. If you don't have `pip` on your
machine see ["How do I install pip on OS X"](http://stackoverflow.com/questions/17271319/installing-pip-on-mac-os-x) (*tl;dr: `sudo easy_install pip` or `brew install python`*)

 `pip install cexbot`

## Dev Install

 `git clone --depth=0 https://github.com/nikcub/cexbot.git`

 `pip install -r requirements.txt`

## Config

cexbot needs to know your username, API key and secret.

 `./cexbot-cli genconfig`

 will generate a blank config file at `cex.cnf`. Edit the file and fill in `username`, `key` and `secret`

## Example Config

```ini
  [auth]
  username = user
  apikey = key
  secret = secret
```

## Usage

 see

  `./cexbot-cli -h`

  new features being added all the time.

  see

  `./cexbot-cli listtasks`


## Update

Update frequently, new features being added all the time.

 `./cexbot-cli update`