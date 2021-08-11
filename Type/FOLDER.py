class FOLDER:
    def __init__(self, root):
        self.root   = root if root.endswith('/') else f'{root}/'
        self.valid  = self.isValid()


    def isValid(self):
        import os
        return os.path.exists(self.root)


    def getFiles(self, endswith=''):
        #########################################################################################
        # import glob
        #
        # if endswith: endswith = f'.{endswith}'
        #
        # return [f for f in glob.glob(self.root + '**', recursive=True) if f.endswith(endswith)]
        #
        #########################################################################################

        # ![pathlib](docs.python.org/3/library/pathlib.html)
        from pathlib import Path

        if endswith: endswith = f'.{endswith}'

        return [str(f) for f in Path(self.root).glob(f'**/*{endswith}') if f.is_file()]

