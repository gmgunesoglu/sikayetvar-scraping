from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entity import Brand, ComplainedItem, Complaint, Reply, Member

class BrandDao:

    @staticmethod
    def add(brand: Brand):
        session.add(brand)
        session.commit()
        return brand

    @staticmethod
    def get_by_id(id: int):
        brand = session.query(Brand).filter_by(id=id).first()
        if brand:
            return brand
        # @+ burada hata oluşturmalı...

    @staticmethod
    def get_by_href(href: str):
        brand = session.query(Brand).filter_by(href=href).first()
        if brand:
            return brand
        # @+ burada hata oluşturmalı...
    
    @staticmethod
    def __update(old_brand: Brand, brand: Brand):
        if not brand:
            # @+ burada hata oluşturmalı...
            return
        if brand.href:
            old_brand.href = brand.href
        if brand.name:
            old_brand.name = brand.name
        if brand.replied_complaint:
            old_brand.replied_complaint = brand.replied_complaint
        if brand.total_complaint:
            old_brand.total_complaint = brand.total_complaint
        if brand.average_reply_sec:
            old_brand.average_reply_sec = brand.average_reply_sec
        if brand.rating_count:
            old_brand.rating_count = brand.rating_count
        if brand.rating:
            old_brand.rating = brand.rating
        session.commit()
        return old_brand
    
    @staticmethod
    def update_by_id(id: int, brand: Brand):
        old_brand = BrandDao.get_by_id(id)
        return BrandDao.__update(old_brand, brand)

    @staticmethod
    def update_by_href(href: str, brand: Brand):
        old_brand = BrandDao.get_by_href(href)
        return BrandDao.__update(old_brand, brand)
    
    @staticmethod
    def __delete(brand: Brand):
        session.delete(brand)
        session.commit()
        return brand

    @staticmethod
    def delete_by_id(id: int):
        brand = BrandDao.get_by_id(id)
        return BrandDao.__delete(brand)

    @staticmethod
    def delete_by_href(href: str):
        brand = BrandDao.get_by_href(href)
        return BrandDao.__delete(brand)
    
    @staticmethod
    def add_or_update(brand: Brand):
        old_brand = BrandDao.get_by_href(brand.href)
        if old_brand:
            return BrandDao.__update(old_brand, brand)
        return BrandDao.add(brand)

class ComplainedItemDao:

    @staticmethod
    def add(complained_item: ComplainedItem):
        session.add(complained_item)
        session.commit()
        return complained_item

    @staticmethod
    def get_by_id(id: int):
        complained_item = session.query(ComplainedItem).filter_by(id=id).first()
        if complained_item:
            return complained_item
        # @+ burada hata oluşturmalı...

    @staticmethod
    def get_by_href(href: str):
        complained_item = session.query(Complaint).filter_by(href=href).first()
        if complained_item:
            return complained_item
        # @+ burada hata oluşturmalı...

    @staticmethod
    def __update(old_complained_item: ComplainedItem, complained_item: ComplainedItem):
        if not complained_item:
            # @+ burada hata oluşturmalı...
            return
        if complained_item.href:
            old_complained_item.href = complained_item.href
        if complained_item.name:
            old_complained_item.name = complained_item.name
        if complained_item.rating:
            old_complained_item.rating = complained_item.rating
        if complained_item.rating_count:
            old_complained_item.rating_count = complained_item.rating_count
        if complained_item.upper_item_id:
            old_complained_item.upper_item_id = complained_item.upper_item_id
        if complained_item.brand_id:
            old_complained_item.brand_id = complained_item.brand_id
        session.commit()
        return old_complained_item

    @staticmethod
    def update_by_id(id: int, complained_item: Complaint):
        old_complained_item = ComplainedItemDao.get_by_id(id)
        return ComplainedItemDao.__update(old_complained_item, complained_item)
    
    @staticmethod
    def update_by_href(href: str, complained_item: Complaint):
        old_complained_item = ComplainedItemDao.get_by_href(href)
        return ComplainedItemDao.__update(old_complained_item, complained_item)

    @staticmethod
    def __delete(complained_item: Complaint):
        session.delete(complained_item)
        session.commit()
        return complained_item

    @staticmethod
    def delete_by_id(id: int):
        complained_item = ComplainedItemDao.get_by_id(id)
        return ComplainedItemDao.__delete(complained_item)

    @staticmethod
    def delete_by_href(href: str):
        complained_item = ComplainedItemDao.get_by_href(href)
        return ComplainedItemDao.__delete(complained_item)
    
    @staticmethod
    def add_or_update(complained_item: ComplainedItem):
        old_complained_item = ComplainedItemDao.get_by_href(complained_item.href)
        if old_complained_item:
            return ComplainedItemDao.__update(old_complained_item, complained_item)
        return ComplainedItemDao.add(complained_item)

class ComplaintDao:

    @staticmethod
    def add(complaint: Complaint):
        session.add(complaint)
        session.commit()
        return complaint

    @staticmethod
    def get_by_id(id: int):
        complaint = session.query(Complaint).filter_by(id=id).first()
        if complaint:
            return complaint
        # @+ burada hata oluşturmalı...

    @staticmethod
    def get_by_href(href: str):
        complaint = session.query(Complaint).filter_by(href=href).first()
        if complaint:
            return complaint
        # @+ burada hata oluşturmalı...
    
    @staticmethod
    def __update(old_complaint: Complaint, complaint: Complaint):
        if not complaint:
            # @+ burada hata oluşturmalı...
            return
        if complaint.href:
            old_complaint.href = complaint.href
        if complaint.complained_item_id:
            old_complaint.complained_item_id = complaint.complained_item_id
        if complaint.title:
            old_complaint.title = complaint.title
        if complaint.date:
            old_complaint.date = complaint.date
        if complaint.view_count:
            old_complaint.view_count = complaint.view_count
        if complaint.like_count:
            old_complaint.like_count = complaint.like_count
        if complaint.member_id:
            old_complaint.member_id = complaint.member_id
        if complaint.rating:
            old_complaint.rating = complaint.rating
        if complaint.solved:
            old_complaint.solved = complaint.solved
        session.commit()
        return old_complaint

    @staticmethod
    def update_by_id(id: int, complaint: Complaint):
        old_complaint = ComplaintDao.get_by_id(id)
        return ComplaintDao.__update(old_complaint, complaint)
    
    @staticmethod
    def update_by_href(href: str, complaint: Complaint):
        old_complaint = ComplaintDao.get_by_href(href)
        return ComplaintDao.__update(old_complaint, complaint)
    
    @staticmethod
    def __delete(complaint: Complaint):
        session.delete(complaint)
        session.commit()
        return complaint

    @staticmethod
    def delete_by_id(id: int):
        complaint = ComplaintDao.get_by_id(id)
        return ComplaintDao.__delete(complaint)
    
    @staticmethod
    def delete_by_href(href: str):
        complaint = ComplaintDao.get_by_href(href)
        return ComplaintDao.__delete(complaint)

class ReplyDao:

    @staticmethod
    def add(reply: Reply):
        session.add(reply)
        session.commit()
        return reply

    @staticmethod
    def get_by_id(id: int):
        reply = session.query(Reply).filter_by(id=id).first()
        if reply:
            return reply
        # @+ burada hata oluşturmalı...

    @staticmethod
    def get_by_href(href: str):
        reply = session.query(Reply).filter_by(href=href).first()
        if reply:
            return reply
        # @+ burada hata oluşturmalı...
    
    @staticmethod
    def __update(old_reply: Reply, reply: Reply):
        if not reply:
            # @+ burada hata oluşturmalı...
            return
        if reply.complaint_id:
            old_reply.complaint_id = reply.complaint_id
        if reply.message:
            old_reply.message = reply.message
        if reply.date:
            old_reply.date = reply.date
        if reply.is_from_brand:
            old_reply.is_from_brand = reply.is_from_brand
        session.commit()
        return old_reply

    @staticmethod
    def update_by_id(id: int, reply: Reply):
        old_reply = ReplyDao.get_by_id(id)
        return ReplyDao.__update(old_reply, reply)
    
    @staticmethod
    def update_by_href(href: str, reply: Reply):
        old_reply = ReplyDao.get_by_href(href)
        return ReplyDao.__update(old_reply, reply)
    
    @staticmethod
    def __delete(reply: Reply):
        session.delete(reply)
        session.commit()
        return reply

    @staticmethod
    def delete_by_id(id: int):
        reply = ReplyDao.get_by_id(id)
        return ReplyDao.__delete(reply)
    
    @staticmethod
    def delete_by_href(href: str):
        reply = ReplyDao.get_by_href(href)
        return ReplyDao.__delete(reply)

class MemberDao:

    @staticmethod
    def add(member: Member):
        session.add(member)
        session.commit()
        return member

    @staticmethod
    def get_by_id(id: int):
        member = session.query(Member).filter_by(id=id).first()
        if member:
            return member
        # @+ burada hata oluşturmalı...

    @staticmethod
    def get_by_href(href: str):
        member = session.query(Member).filter_by(href=href).first()
        if member:
            return member
        # @+ burada hata oluşturmalı...
    
    @staticmethod
    def __update(old_member: Member, member: Member):
        if not member:
            # @+ burada hata oluşturmalı...
            return
        if member.href:
            old_member.href = member.href
        session.commit()
        return old_member

    @staticmethod
    def update_by_id(id: int, member: Member):
        old_member = MemberDao.get_by_id(id)
        return MemberDao.__update(old_member, member)
    
    @staticmethod
    def update_by_href(href: str, member: Member):
        old_member = MemberDao.get_by_href(href)
        return MemberDao.__update(old_member, member)
    
    @staticmethod
    def __delete(member: Member):
        session.delete(member)
        session.commit()
        return member

    @staticmethod
    def delete_by_id(id: int):
        member = MemberDao.get_by_id(id)
        return MemberDao.__delete(member)
    
    @staticmethod
    def delete_by_href(href: str):
        member = MemberDao.get_by_href(href)
        return MemberDao.__delete(member)
    

# Veritabanı bağlantısını oluştur
engine = create_engine('postgresql://postgres:postgres@localhost:5432/sikayetvar')
Session = sessionmaker(bind=engine)
session = Session()


# brand = Brand("/turkcell", "Turkcell", 5000, 5200, 300, 600, 60)
# brand = BrandDao.add(brand)
# brand = BrandDao.get_by_href("/migros")
# print(brand.id)

# complained_item = ComplainedItem("/vodafone", "Vodafone", 53, 43262, None, 1)
# complained_item.is_leaf = True
# complained_item = ComplainedItemDao.add_or_update(complained_item)
# complained_item = ComplainedItemDao.get_by_href("/vodafone")
# print(complained_item.id)
