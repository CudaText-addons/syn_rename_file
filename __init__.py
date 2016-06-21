'''
Plugin for Synwrite
Authors:
    Andrey Kvichansky    (kvichans on github.com)
    Alexey T (Synwrite)
'''

import os
from sw import *
from .sw_plug_lib import *
import sw_cmd as cmds

GAP = 4

class Command:
    def run(self):
        old_path = ed.get_filename()
        if not old_path:
            msg_status('File is not saved')
            return
            
        if ed.get_prop(PROP_MODIFIED):
            msg_box(MSG_WARN, 'Text is modified, save it first')
            return
            
        old_fn  = os.path.basename(old_path)
        old_stem= old_fn[: old_fn.rindex('.')]  if '.' in old_fn else old_fn
        old_ext = old_fn[1+old_fn.rindex('.'):] if '.' in old_fn else ''
        DLG_W,\
        DLG_H   = (300, 80)
        new_stem= old_stem
        new_ext = old_ext
        while True:
            btn,vals,chds   = dlg_wrapper('Rename file', GAP+300+GAP,GAP+80+GAP,     #NOTE: dlg-rename
                 [dict(           tp='lb'   ,t=GAP          ,l=GAP          ,w=200      ,cap='Enter new file name:'  ) # &e
                 ,dict(cid='stem',tp='ed'   ,t=GAP+18       ,l=GAP          ,w=200+10                                   ) # 
                 ,dict(           tp='lb'   ,tid='stem'     ,l=GAP+200+12   ,w=8        ,cap='.'                        ) # &.
                 ,dict(cid='sext',tp='ed'   ,tid='stem'     ,l=GAP+200+20   ,w=80                                       )
                 ,dict(cid='!'   ,tp='bt'   ,t=GAP+80-28    ,l=GAP+300-170  ,w=80       ,cap='OK',  props='1'        ) #     default
                 ,dict(cid='-'   ,tp='bt'   ,t=GAP+80-28    ,l=GAP+300-80   ,w=80       ,cap='Cancel'                )
                 ],    dict(stem=new_stem
                           ,sext=new_ext), focus_cid='stem')
            if btn is None or btn=='-': return None
            new_stem    = vals['stem']
            new_ext     = vals['sext']
            if new_stem==old_stem and new_ext==old_ext:
               return
               
            new_path    = os.path.dirname(old_path) + os.sep + new_stem + ('.'+new_ext if new_ext else '')
            
            if os.path.isdir(new_path):
                msg_box(MSG_WARN, 'There is directory with same name. Choose another name.')
                continue#while
            if os.path.isfile(new_path):
                if not msg_box(MSG_CONFIRM_Q, 'File already exists. Replace?'):
                    continue#while
            break#while
           #while

        crt = ed.get_caret_pos()
        ed.cmd(cmds.cmd_FileClose)
        msg_status('Renaming...')
        os.replace(old_path, new_path)
        file_open(new_path)
        ed.set_caret_pos(crt)
