"""a quick look at a build without the (slow) checks: python3 look.py build_<name>.py"""
import sys, os, runpy
import bcommon


def quick(name, D, place, pic, **k):
    bcommon.save(name, D, place); bcommon.save_white(name, pic.white)
    bcommon.preview(D, os.path.join(bcommon.HERE, 'out', name + '-look.png'))
    return True


bcommon.finish = quick
runpy.run_path(sys.argv[1], run_name='__main__')
