from datetime import datetime
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime, Boolean, Text, Float, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import enum
from config import DB_URL


engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class RoomStatus(enum.Enum):
    selling = 1  # 在售
    sold = 2  # 已售
    unavailable = 3  # 不可售


class Region(Base):
    __tablename__ = 'region'

    id = Column(String(10), primary_key=True)
    name = Column(String(20), nullable=False)

    region_map = {
        '4': '渝北区',
        '9': '北碚区',
        '14': '南岸区',
        '19': '沙坪坝区',
        '24': '九龙坡区',
        '29': '大渡口区',
        '34': '巴南区',
        '39': '江北区',
        '44': '渝中区',
        '1149': '两江新区',
    }

    @classmethod
    def insert_regions(cls):
        session = Session()
        for code in cls.region_map:
            r = cls(id=code, name=cls.region_map[code])
            session.add(r)

        session.commit()

    def __repr__(self):
        return f'<({self.id} {self.name})>'


class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, primary_key=True)
    project_id = Column(String(10), unique=True)
    project_name = Column(String(100))
    enterprise_name = Column(String(100))
    location = Column(String(100))
    region = Column(String(10), ForeignKey('region.id'))
    extra = Column(Text)  # 原始数据
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'<({self.project_id}) {self.project_name})>'


class Building(Base):
    __tablename__ = 'building'

    id = Column(Integer, primary_key=True)
    building_id = Column(String(10), unique=True)
    building_name = Column(String(100))
    project_id = Column(Integer, ForeignKey('project.id'))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f'<({self.building_id} {self.building_name})>'


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    room_id = Column(String(10), nullable=False, unique=True)
    building_id = Column(Integer, ForeignKey('building.id'))
    room_number = Column(String(35), nullable=False)  # 房籍号
    room_type = Column(String(20), nullable=True)  # 户型
    use_type = Column(String(50))  # 用途
    building_area = Column(Float)  # 建筑面积
    inner_area = Column(Float)  # 套内面积
    room_status = Column(Enum(RoomStatus))  # 房屋状态，是否已售或不可售
    room_doorplate = Column(String(20))  # 门牌编号，1-1-1，代表1单元1层第1户
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now)
    extra = Column(Text)  # 原始json信息
