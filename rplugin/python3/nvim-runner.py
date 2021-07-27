import re
from string import Template
import os
import toml
import neovim

@neovim.plugin
class Runner(object):

    def __init__(self, nvim):
        self.nvim = nvim

        self._cmd_exector_map = self.nvim.request("nvim_get_var","exectorMap")
        self._cmd_extention_map = self.nvim.request("nvim_get_var", "extentionMap")

        toml_path = os.path.join(os.path.dirname(__file__),"setting.toml")
        self.toml_dict = toml.load(open(toml_path))

    @neovim.command("Runner", nargs='*')
    def runner(self, _):
        filetype = self.nvim.request("nvim_buf_get_option",0,"filetype")

        cmd = self._make_command(filetype)
        if cmd == None:
            return

        config_dict = self._make_replace_config_dict()
        replaced_cmd = self._change_string_according_to_dict(cmd,config_dict)

        self.nvim.request("nvim_command","split term://"+replaced_cmd)
        self.nvim.request("nvim_buf_set_option",0,"ma",True)
        self.nvim.current.line = "Please input here..."

    def _change_string_according_to_dict(self,str_,dict_):
        return Template(str_).substitute(dict_)

    def _make_command(self,filetype):
        """
        first, search user defined file.
        second, search default file.

        default file is setting.toml which locate same dir.
        """
        ext = self.nvim.request("nvim_call_function","expand",["%:e"])

        if filetype in self._cmd_exector_map:
            cmd = self._cmd_exector_map[filetype]

        elif ext in self._cmd_extention_map:
            cmd = self._cmd_extention_map[ext]

        elif filetype in self.toml_dict["exector"]:
            cmd = self.toml_dict["exector"][filetype]

        elif ext in self.toml_dict["extention"]:
            cmd = self.toml_dict["extention"][ext]

        else:
            self.nvim.request("nvim_command",'echo "Error: Cannot find filetype in g:exectorMap or toml file"')
            cmd = None
        return cmd


    def _make_replace_config_dict(self):
        """
        like vscode, we can use these var.

        ${file}
        ${fileExtname}
        ${fileNoExtention}
        ${fileBasename}
        ${fileDirname}
        ${cwd}
        ${relativeFile}
        ${relativeFileDir}
        """

        file = self.nvim.request("nvim_call_function","expand",["%:p"])
        fileExtname = re.search(r'\.[\.]*', file).group()
        fileNoExtention = file[:len(fileExtname)]
        fileBasename = self.nvim.request("nvim_call_function","expand",["%:t"])
        fileDirname = file[:len(fileBasename)]
        cwd = self.nvim.request("nvim_call_function","getcwd",[])
        relativeFile = file[len(cwd):]
        relativeFileDir = relativeFile[:len(fileBasename)]

        config_dict = {
            "${file}"                   : file           ,
            "${fileExtname}"            : fileExtname    ,
            "${fileNoExtention}"        : fileNoExtention,
            "${fileBasename}"           : fileBasename   ,
            "${fileDirname}"            : fileDirname    ,
            "${cwd}"                    : cwd            ,
            "${relativeFile}"           : relativeFile   ,
            "${relativeFileDir}"        : relativeFileDir
        }

        return config_dict
