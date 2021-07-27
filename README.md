# nvim runner

This plugin is nvim code runner using terminal emulator.
You can use this plugin ":Runner" command.

## requarement
You must install python3 and neovim and toml package.
so,

```
brew install python3
pip3 install toml neovim
```

If your filetype (or extention) is not available, you can add g:exectorMap (ex. when filetype is hoge, g:exectorMap[hoge] = code) or g:extentionMap (ex. hoge.fuge -> g:extentionMap[fuge] = code).
