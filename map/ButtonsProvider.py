from flask import json


class ButtonsProvider:

    def exportToFile(self, walls):
        data = []
        for wall in walls:
            data.append({
                'position': wall.position,
                'scale': wall.scale,
                'type': wall.type,
                'src': wall.src,
            })

        with open('exportMap.json', 'w') as file_:
            file_.write(json.dumps(data))

    def getMap(self):
        with open('exportMap.json', 'r') as f:
             read_data = f.read()

        return json.loads(read_data)