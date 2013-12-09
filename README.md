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

If you have previously installed cexbot you will need to run an upgrade:

 `pip install -U cexbot`

## Dev Install

If you would like to contribute to the code:

 `git clone --depth=0 https://github.com/nikcub/cexbot.git`

 `pip install -r requirements.txt`

## Config

cexbot needs to know your username, API key and secret.

Configuration options are specified with the `config` command line option.

```
$ cexbot-cli config --list
Namespace(command='config', debug=False, list=True, name=None, value=None, verbose=False, version=False)
cex.username = nikcub
cex.secret = secret
cex.apikey = api
```

Set each config option with:

 `cexbot-cli config cex.username nikcub`

and then set your api key and secret:

  `cexbot-cli config cex.apikey <your_key>`

  `cexbot-cli config cex.secret <your_secret>`

If you have a local editor installed, you can edit your config directly with:

  `cexbot-cli config --edit`

Once you have those values defined, you can test that they work with:

  `cexbot-cli config --testauth`

## Usage and Help

see

  `cexbot-cli -h`

new features being added all the time.

## Update

Update frequently, new features being added all the time.

 `./cexbot-cli update`
