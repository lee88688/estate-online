import requests
import json
import time
import math
from model.db_model import Session, Project, Building
from .celery import app


MAX_RETRY = 5
PROJECT_QUERY_URL = 'http://www.cq315house.com/WebService/Service.asmx/getParamDatas'
ROOM_QUERY_URL = 'http://www.cq315house.com/WebService/Service.asmx/GetRoomJson'
headers = {'Content-type': 'application/json',
           'Accept': 'application/json, text/javascript'}


def add_buildings(building_ids: str, block_names: str, project_id: int, session: Session) -> None:
    for building_id, building_name in zip(building_ids.split(','), block_names.split(',')):
        building = session.query(Building).filter(Building.building_id == building_id).one_or_none()
        if not building:
            building = Building(
                building_id=building_id,
                building_name=building_name,
                project_id=project_id
            )
            session.add(building)
        else:
            building.building_name = building_name
    session.commit()


def get_projects(region: str) -> None:
    max_retry = MAX_RETRY
    payload = {"siteid": region, "useType": "", "areaType": "", "projectname": "",
               "entName": "", "location": "", "minrow": "1", "maxrow": "11"}
    page_size = 10
    page_index = 0
    page_index_max = 0
    while page_index <= page_index_max:
        payload['minrow'] = str(page_index * 10 + 1)
        payload['maxrow'] = str((page_index + 1) * 10 + 1)
        res = requests.post(PROJECT_QUERY_URL,
                            data=json.dumps(payload), headers=headers)
        try:
            projects = json.loads(res.json()['d'].replace('\\', ''))
        except json.JSONDecodeError:
            if max_retry <= 0:
                print('reach to max retry!')
                return
            time.sleep(10)
            max_retry -= 1
            continue
        if page_index == 0 and len(projects) > 0:
            p = projects[0]
            counts = p.get('counts', 0)
            page_index_max = int(counts) // page_size
        session = Session()
        for p in projects:
            project = session.query(Project).filter(Project.project_id == p['projectid']).one_or_none()
            if not project:
                project = Project(
                    project_id=p['projectid'],
                    project_name=p['projectname'],
                    enterprise_name=p['enterprisename'],
                    location=p['location'],
                    region=region,
                    extra=json.dumps(p)
                )
                session.add(project)
                session.commit()
            add_buildings(p['buildingid'], p['blockname'], project.id, session)
        page_index += 1


def get_rooms(building: str) -> None:
    pass
