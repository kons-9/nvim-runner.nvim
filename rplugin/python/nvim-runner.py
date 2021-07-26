import neovim
import re

@neovim.plugin
class Runner(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.cmd_map = self.nvim.request("nvim_get_var","exectorMap")

    @neovim.command("Runner", nargs='*')
    def testcommand(self, args):
        filetype = self.nvim.request("nvim_buf_get_option",0,"filetype")
        path = self.nvim.request("nvim_call_function","expand",["%:p"]) 

        replaced_conf = {"$dirNoExtention":re.search(r'.*\.',path).group()[:-1],"$dir":path}
        cmd = self.cmd_map[filetype] 

        replaced_cmd = self._change_string_according_to_dict(cmd,replaced_conf)

        self.nvim.request("nvim_command","split term://"+replaced_cmd)
        self.nvim.request("nvim_buf_set_option",0,"ma",True)
        self.nvim.current.line = "Please input here..."

    def _change_string_according_to_dict(self,str, dic):
        for key , obj in dic.items():
            str = str.replace(key,obj)
        return str

