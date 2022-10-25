import subprocess
import os
import json
import configparser
config = configparser.ConfigParser()
from subprocess import call
from dotenv import load_dotenv
load_dotenv()

pwd = os.environ.get('pwd')



class Fan:

    default = {
        "light": "off",
        "fan": "off",
        "direction": "forward"
    }
    preamble = '10110010110010010010'
    frequency_mhz = '304128000'
    zero_length_ns = '333'
    one_wvl_ns = '333'
    repeat = '8'
    pause_ns = '10000'
    bit_bang = '/home/lilsqueaks/Documents/rpitx/sendook'
    ceiling = {
        "light_toggle": '0100100100100101100',
        "fan_off": '0100100100101100100',
        "fan_fwd_rev_toggle": "0100100101100100100",
        "fan_hi": "1100100100100100100",
        "fan_med": "0101100100100100100",
        "fan_low": "0100101100100100100",
    }

    def __init__(self):
        self.build_command()

    def run_cmd(self, cmd):
        call('echo {} | sudo -S {}'.format(pwd, cmd), shell=True)

    def get_status_fan(self):
        with open('settings.json', 'r') as r:
            cache = r.read()
            data = eval(cache)
            return data


    def set_status(self, req):
        old_status = self.get_status_fan()
        for param, new_status in req.items():
            # print(param)
            if param == 'fan_direction':
                self.set_fan_fwd_rev_toggle()
            if param == 'light':
                self.toggle_light()
            if param == 'fan':
                if new_status == 'hi':
                    self.set_fan_hi()
                if new_status == 'med':
                    self.set_fan_med()
                if new_status == 'lo':
                    self.set_fan_low()
                if new_status == 'off':
                    self.set_fan_off()
            old_status[param] = new_status

        newest_status = old_status
        with open('settings.json', 'w', encoding='utf-8') as w:
            json.dump(newest_status, w, ensure_ascii=False, indent=4, sort_keys=True)
        return newest_status

    def build_command(self):
        self.commands = {}
        for button, binary in self.ceiling.items():
            self.commands[button] = f'sudo {self.bit_bang} -f {self.frequency_mhz} -0 {self.zero_length_ns} -1 {self.one_wvl_ns} -r {self.repeat} -p {self.pause_ns} {self.preamble}{binary}'.split(
                ' ')
        return self.commands

    def toggle_light(self):
        print('self.toggle_light invoked')
        cmd = self.commands['light_toggle']
        return_code = subprocess.run(cmd).returncode
        # self.run_cmd(cmd)
        if return_code == 1:  # err
            return 'err'
        if return_code == 0:
            return 'success'
        return cmd

    def set_fan_off(self):
        print('self.set_fan_off invoked')
        cmd = self.commands['fan_off']
        print(cmd)
        subprocess.run(cmd)
        return cmd

    def set_fan_hi(self):
        print('self.set_fan_hi invoked')
        cmd = self.commands['fan_hi']
        print(cmd)
        subprocess.run(cmd)
        return cmd

    def set_fan_med(self):
        print('self.set_fan_med invoked')
        cmd = self.commands['fan_med']
        print(cmd)
        subprocess.run(cmd)
        return cmd

    def set_fan_low(self):
        print('self.set_fan_lo invoked')
        cmd = self.commands['fan_low']
        print(cmd)
        subprocess.run(cmd)
        return cmd

    def set_fan_fwd_rev_toggle(self):
        print('self.set_fan_fwd_rev')
        cmd = self.commands['fan_fwd_rev_toggle']
        print(cmd)
        subprocess.run(cmd)
        return cmd

