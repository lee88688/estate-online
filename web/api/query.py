from flask import request
from model.db_model import Session, Project, Building, Region
from web.utils import ApiResult, parameter_error
from . import bp


DEFAULT_PAGE_SIZE = 10


@bp.route('/query', methods=['POST'])
def query():
    """
    query projects
    :param region: str object for region code
    :param project_name: str object
    :param enterprise_name: str object
    :param location: str object
    """
    session = Session()

    page_size = request.json['page_size'] if request.json.get('page_size') else DEFAULT_PAGE_SIZE
    page_index = request.json['page_index'] if request.json.get('page_index') else 1
    if type(page_index) != int or type(page_size) != int or page_index <= 0 or page_size < 0:
        return parameter_error.make_response()

    region_clause = Project.region == request.json['region'] if request.json.get('region') else True
    project_name_clause = Project.project_name.like(f'%{request.json["project_name"]}%') if request.json.get('project_name') else True
    enterprise_name_clause = Project.enterprise_name.like(f'{request.json["enterprise_name"]}') if request.json.get('enterprise_name') else True
    location_clause = Project.location.like(f'%{request.json["location"]}%') if request.json.get('location') else True
    q = session.query(Project).limit(page_size).offset((page_index - 1) * page_size).from_self().\
        join(Building).join(Region).\
        filter(region_clause, project_name_clause, enterprise_name_clause, location_clause).\
        with_entities(
            Project.project_id, Project.project_name, Region.name, Project.location,
            Project.enterprise_name, Building.building_id, Building.building_name
        )
    result = []
    d = {}
    for row in q:
        project_id = row[0]
        if project_id in d:
            d[project_id]['building'].append((row[5], row[6]))
        else:
            item = {
                'project_id': row[0],
                'project_name': row[1],
                'region_name': row[2],
                'location': row[3],
                'enterprise_name': row[4],
                'building': [(row[5], row[6])]
            }
            result.append(item)
            d[project_id] = item
    return ApiResult(result=result).make_response()
