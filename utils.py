import os
import json

class FileIOUtils:
    """
        @author Rahul
        This Class handles all the `File IO` operations.
        =============================================

        Methods
        -------
        1. ReadJsonFile
        2. WriteJsonFile

    """
    def readJsonFile(self, filePath):
        out = {}
        if os.path.exists(filePath):
            with open(filePath) as file:
                try:
                    out['data'] = json.load(file)
                    out['status'] = 200
                except json.decoder.JSONDecodeError:
                    out['status'] = 500
                    out['data'] = 'JSON error'
                except:
                    out['status'] = 500
                    out['data'] = 'something went wrong!'
        else:
            out['status'] = 500
            out['data'] = 'No Data Available'

        return out


    def writeJsonFile(self, filePath, dataToWrite):
        out = {}
        try:
            with open(filePath, 'w') as file:
                json.dump(dataToWrite, file, indent=4)
                out['status'] = 200
        except:
            out['status'] = 500

        return out