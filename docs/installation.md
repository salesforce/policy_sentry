Installation
============

To get started, install Policy Sentry using Homebrew or `pip3`

* Homebrew

```bash
brew tap salesforce/policy_sentry https://github.com/salesforce/policy_sentry
brew install policy_sentry
```

* `pip3`

```bash
pip3 install --user policy_sentry
```


#### Shell completion

To enable Bash completion, put this in your `.bashrc`:

```bash
eval "$(_POLICY_SENTRY_COMPLETE=source policy_sentry)"
```

To enable ZSH completion, put this in your `.zshrc`:

```
eval "$(_POLICY_SENTRY_COMPLETE=source_zsh policy_sentry)"
```
