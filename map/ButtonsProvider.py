from flask import json


class ButtonsProvider:

    def exportToFile(self, walls):
        data = []
        for wall in walls:
            data.append({
                'position': wall.position,
                'scale': wall.scale,
                'type': wall.type,
            })

        with open('exportMap.json', 'w') as file_:
            file_.write(json.dumps(data))