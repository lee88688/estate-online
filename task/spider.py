import requests
import json
import time
import enum
from celery import group
from celery.utils.log import get_task_logger
from datetime import date
from model.db_model import Session, Project, Building, Room, Region
from .celery_app import app


MAX_RETRY = 5
PROJECT_QUERY_URL = 'http://www.cq315house.com/WebService/Service.asmx/getParamDatas'
ROOM_QUERY_URL = 'http://www.cq315house.com/WebService/Service.asmx/GetRoomJson'
ROOM_STATUS_QUERY_URL = 'http://www.cq315house.com/WebService/Service.asmx/GetJsonStatus'
headers = {'Content-type': 'application/json',
           'Accept': 'application/json, text/javascript'}
logger = get_task_logger(__name__)


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
            building.update_time = date.today()
    session.commit()


@app.task
def get_projects(region: str) -> None:
    max_retry = MAX_RETRY
    payload = {"siteid": region, "useType": "", "areaType": "", "projectname": "",
               "entName": "", "location": "", "minrow": "1", "maxrow": "11"}
    page_size = 10
    page_index = 0
    page_index_max = 0
    while page_index <= page_index_max:
        payload['minrow'] = str(page_index * page_size + 1)
        payload['maxrow'] = str((page_index + 1) * page_size + 1)
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


class RoomStatus(enum.Enum):
    selling = 1
    sold = 2
    invalid = 3

    @classmethod
    def get_status(cls):
        if hasattr(cls, 'status'):
            return
        res = requests.post(ROOM_STATUS_QUERY_URL, data=json.dumps({'para': ''}), headers=headers)
        status_arr = json.loads(res.json()['d'])
        cls.status = [(s['val'], s['name']) for s in status_arr if s['showType'] == 0]
        cls.status.reverse()

    @classmethod
    def room_status(cls, v: int):
        cls.get_status()
        for sv, name in cls.status:
            if (v & sv) == sv:
                if name == '未售':
                    return cls.selling
                elif name == '已售':
                    return cls.sold
                else:
                    return cls.invalid
        return cls.invalid


    def __repr__(self):
        if self == self.selling:
            return '未售'
        elif self == self.sold:
            return '已售'
        else:
            return '不可售'


def room_valid(room: dict) -> bool:
    """
    from buildingTable __getStatus function
    """
    # sync-project 44，1193480中存在keys全部为0但是并不是不可用的情况，"YZ01201409110000010100100210009"
    return RoomStatus.room_status(room['status']) != RoomStatus.invalid


@app.task
def get_rooms(building_id: str) -> None:
    session = Session()
    building = session.query(Building).filter(Building.building_id == building_id).one_or_none()
    if not building:
        return
    building_id = building.building_id
    res = requests.post(ROOM_QUERY_URL, data=json.dumps({'buildingid': building_id}), headers=headers)
    try:
        rooms = json.loads(res.json()['d'])
    except json.JSONDecodeError:
        logger.warning(res.text)
        raise
    session = Session()
    room_set = set()
    for unit in rooms:
        for room in filter(room_valid, unit['rooms']):
            if (room['F_HOUSE_NO'] in room_set):
                continue
            if session.query(Room).filter(Room.room_number == room['F_HOUSE_NO']).update(Room.from_dict2update(room)):
                session.commit()
                continue
            r = Room.from_dict(room, building_id)
            r.room_status = RoomStatus.room_status(room['status']) == RoomStatus.sold
            session.add(r)
            room_set.add(room['F_HOUSE_NO'])
        session.commit()


@app.task
def task_sync_online_data():
    # job = group(map(lambda r: get_projects.s(str(r)), Region.region_map.keys()))
    # result = job.apply_async()
    # result.join()
    # print('task end')

    session = Session()
    job = group(map(lambda r: get_rooms.s(r.building_id), session.query(Building)))
    result = job.apply_async()
    result.join()
    logger.info('room sync end!')
